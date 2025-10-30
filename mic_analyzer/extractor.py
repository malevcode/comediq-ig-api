"""
Minimal-setup OCR utilities using EasyOCR only.

Install deps:
  pip install easyocr opencv-python

Example:
  from extractor import extract_text_from_image, extract_text_from_video
  words = extract_text_from_image("/path/to/image.jpg")  # -> List[str]
  frames_words = extract_text_from_video("/path/to/video.mp4", frame_interval=1.0)  # -> List[(ts, List[str])]
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple
import cv2
import easyocr
import argparse
import json 
import ollama

SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "You are a data extraction and normalization model that processes noisy OCR text from event posters.\n"
        "Your goals:\n"
        "1. Correct OCR text errors.\n"
        "2. Identify and normalize event details.\n"
        "3. Match and repair any names or Instagram handles using known metadata.\n"
        "4. Always infer the most likely missing fields from context — never leave them blank if clues exist.\n\n"
        "### JSON Schema ###\n"
        "{\n"
        "  event_name: string (inferred if missing),\n"
        "  hosts: [list of full names],\n"
        "  date: string (if absent, infer day or mark as 'unknown'),\n"
        "  time: string (normalized ranges like '10am–12pm'),\n"
        "  location: string (infer from context or mark 'unknown'),\n"
        "  instagram_handles: [list, always starting with '@'],\n"
        "  other_details: {text_snippets: [corrected text lines], notes: string}\n"
        "}\n\n"
        "### Rules ###\n"
        "- Use metadata mapping of Instagram handles to correct host names.\n"
        "- If a handle or name approximately matches metadata, fix and map it.\n"
        "- Infer event names from visible titles like 'HOLLYWOOD COMEDY' or 'OPEN MIC'.\n"
        "- If times appear multiple times, merge them into one normalized string.\n"
        "- Always output **valid JSON only**, no markdown, commentary, or nulls."
    )
}

@dataclass
class OcrResult:
    text: str
    # For video, timestamp_seconds indicates when the frame was captured; for images, None
    timestamp_seconds: Optional[float] = None


def _import_easyocr_reader():
    # Fixed to English for now; avoid GPU for fast cold start on most systems
    return easyocr.Reader(["en"], gpu=False)


def _easyocr_image_list(reader: easyocr.Reader, path_or_bgr_image) -> List[str]:
    # easyocr supports file path or numpy array (RGB). If we have BGR (cv2), convert.
    image_input = path_or_bgr_image
    if "numpy" in str(type(path_or_bgr_image)):
        # Convert BGR (cv2) -> RGB for easyocr
        try:
            import cv2  # type: ignore
            image_input = cv2.cvtColor(path_or_bgr_image, cv2.COLOR_BGR2RGB)
        except Exception:
            # If cv2 missing, easyocr can still often read BGR fine
            image_input = path_or_bgr_image

    results = reader.readtext(image_input, detail=1)
    return results 


def extract_text_from_image(image_path: str) -> List[str]:
    """Extract list of strings from an image using EasyOCR (detail=0, lang=['en'])."""
    return _easyocr_image_list(_import_easyocr_reader(), image_path)


def extract_text_from_video(
    video_path: str,
    frame_interval: float = 1.0,
    max_frames: Optional[int] = None,
    resize_width: Optional[int] = None,
) -> List[Tuple[float, List[str]]]:
    """Extract list of strings per sampled frame of a video using EasyOCR.

    Returns a list of tuples: (timestamp_seconds, [words...])
    """
    cap = cv2.VideoCapture(video_path)
    reader = _import_easyocr_reader()

    if not cap.isOpened():
        print("Error: Could not open video.")
        return 

    fps = cap.get(cv2.CAP_PROP_FPS) or 0.0
    if fps <= 0:
        fps = 30.0  # sensible default if metadata missing

    results: List[Tuple[float, List[str]]] = []

    try:
        while True:  # Simplified loop condition
            ok, frame = cap.read()
            if not ok:
                break

            if frame is None or frame.size == 0:  # Ensure frame is valid
                continue

            words = _easyocr_image_list(reader, frame)  # Extract text only if frame is valid
            results.append(words) 
            if words != [] : 
              break
    finally:
        cap.release()
        cv2.destroyAllWindows()

    return results


def extract_text(
    args: argparse.Namespace
) -> List[str]:
    """One-call helper returning a list of strings.

    - Image: returns list of words.
    - Video: returns de-duplicated list of words across sampled frames.
    """
    if not args.video:
        return extract_text_from_image(args.path)

    frames = extract_text_from_video(
            args.path,
            frame_interval=args.interval,
            max_frames=args.max_frames,
            resize_width=args.width,
        )
        
    seen = set()
    flattened: List[str] = []
    for words in frames:
        for w in words:
            if w and w not in seen:
                seen.add(w)
                flattened.append(w)
    return flattened

def format_ocr_data(ocr_tuples):
    formatted = []
    for i, (coords, text, conf) in enumerate(ocr_tuples):
        coord_str = f"({coords[0]}, {coords[1]}, {coords[2]}, {coords[3]})"
        formatted.append(f"Box {i+1}: {coord_str} | Confidence: {conf:.2f} | Text: {text}")
    return "\n".join(formatted)

def format_metadata_text(metadata):
    return "\n".join(
        [f"@{handle}: {name}" if name else f"@{handle}" for handle, name in metadata.items()]
    )

def extract_event_info(ocr_tuples, metadata, model="phi3:mini"):
    """
    Takes OCR tuple list: [([[x1,y1],[x2,y2],[x3,y3],[x4,y4]], text, conf), ...]
    Returns structured JSON describing the event.
    """
    ocr_text = format_ocr_data(ocr_tuples)
    metadata_text = format_metadata_text(metadata) if metadata else "no metadata"

    user_prompt = {
        "role": "user",
        "content": (
            f"Here is the known metadata (Instagram handles and names):\n{metadata_text}\n\n"
            f"OCR Data:\n{ocr_text}\n\n"
            "Use the metadata to correct OCR text and extract structured event info. Return JSON only."
        )
    }


    # Send to Ollama
    response = ollama.chat(
        model=model,
        messages=[SYSTEM_PROMPT, user_prompt]
    )

    raw_output = response["message"]["content"].strip().strip("`json")

    # Try to parse JSON
    try:
        structured = json.loads(raw_output)
    except json.JSONDecodeError:
        print("⚠️ Could not parse model output as JSON. Raw output:")
        print(raw_output)
        structured = {"error": "Invalid JSON", "raw_output": raw_output}

    return structured

def get_reel_mentions(file_path):
    """
    Extract reel mentions from a metadata JSON file path and return a mapping.

    - `file_path` must be a string path to a JSON file (not a dict).
    - Returns a dict mapping username -> full_name, e.g.
        {"itslinagreen": "Lina Green", "paigeshanley": "paige"}
    - The function searches for common keys such as 'reel_mentions', 'tappable_objects',
      and any nested 'user' or 'username' fields, normalizes usernames (removes leading '@'),
      and deduplicates results by username while preserving the first seen full_name.
    """
    import os

    if not isinstance(file_path, str):
        raise TypeError("get_reel_mentions expects a file path string")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Metadata file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    mentions = {}

    def collect_from_obj(obj):
        # obj can be dict, list, or primitive
        if isinstance(obj, dict):
            # Check for 'user' object
            if "user" in obj and isinstance(obj["user"], dict):
                user = obj["user"]
                uname = user.get("username") or user.get("pk") or user.get("id")
                full = user.get("full_name") or user.get("fullName") or user.get("name") or ""
                if uname:
                    uname = str(uname).strip()
                    if uname.startswith("@"):
                        uname = uname[1:]
                    if uname and uname not in mentions:
                        mentions[uname] = full
            # Check for direct 'username' and optional 'full_name' in the same dict
            if "username" in obj:
                uname = obj.get("username")
                full = obj.get("full_name") or obj.get("fullName") or obj.get("name") or ""
                if uname:
                    uname = str(uname).strip()
                    if uname.startswith("@"):
                        uname = uname[1:]
                    if uname and uname not in mentions:
                        mentions[uname] = full
            # Check for arrays under common keys
            for key in ("reel_mentions", "tappable_objects", "story_mentions", "mentions"):
                if key in obj and isinstance(obj[key], list):
                    for item in obj[key]:
                        collect_from_obj(item)
            # Recurse into all values
            for v in obj.values():
                collect_from_obj(v)
        elif isinstance(obj, list):
            for item in obj:
                collect_from_obj(item)
        # primitives ignored

    collect_from_obj(data)

    return mentions

if __name__ == "__main__":  # Simple CLI for quick manual checks
    import argparse

    parser = argparse.ArgumentParser(description="Quick OCR extractor")
    parser.add_argument("path", help="Path to image or video")
    parser.add_argument("--path_metadata", help="Metadata to the post/story")
    parser.add_argument("--video", action="store_true", help="Treat input as video")
    parser.add_argument("--interval", type=float, default=1.0, help="Seconds between frames (video)")
    parser.add_argument("--max_frames", type=int, default=None, help="Max frames to sample (video)")
    parser.add_argument("--width", type=int, default=None, help="Resize width (video) for speed")
    args = parser.parse_args()

    ocr_data = extract_text(args)
    mentions = get_reel_mentions(args.path_metadata) if args.path_metadata else None
    result = extract_event_info(ocr_data, mentions)

    print(json.dumps(result, indent=2))


    # TODO: Binary classification if a mic is happening or not