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


@dataclass
class OcrResult:
    text: str
    # For video, timestamp_seconds indicates when the frame was captured; for images, None
    timestamp_seconds: Optional[float] = None


def _import_easyocr_reader():
    # Fixed to English for now; avoid GPU for fast cold start on most systems
    return easyocr.Reader(["en"], gpu=False)


def _easyocr_image_list(reader, path_or_bgr_image) -> List[str]:
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

    results = reader.readtext(image_input, detail=0)
    return [r.strip() for r in results if r and str(r).strip()]


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


if __name__ == "__main__":  # Simple CLI for quick manual checks
    import argparse

    parser = argparse.ArgumentParser(description="Quick OCR extractor")
    parser.add_argument("path", help="Path to image or video")
    parser.add_argument("--video", action="store_true", help="Treat input as video")
    # EasyOCR only; fixed to English for now
    parser.add_argument("--interval", type=float, default=1.0, help="Seconds between frames (video)")
    parser.add_argument("--max_frames", type=int, default=None, help="Max frames to sample (video)")
    parser.add_argument("--width", type=int, default=None, help="Resize width (video) for speed")
    args = parser.parse_args()

    print(extract_text(args))

    # if args.video:
    #     out = extract_text_from_video(
    #         args.path,
    #         frame_interval=args.interval,
    #         max_frames=args.max_frames,
    #         resize_width=args.width,
    #     )
    #     for ts, words in out:
    #         if words:
    #             print(f"[{ts:.2f}s] " + ", ".join(words))
    # else:
    #     print("\n".join(extract_text_from_image(args.path)))


