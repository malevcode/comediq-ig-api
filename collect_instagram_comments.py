#!/usr/bin/env python3
"""
Collect Instagram comments from a draft-list post and process them into SQL.

This uses the Instagram Graph API instead of password login. Set
IG_GRAPH_ACCESS_TOKEN in .env, then pass the media ID for the draft post.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

from dotenv import load_dotenv

from process_responses import (
    DEFAULT_COMMENT_MAPPING_FILE,
    DEFAULT_COMMENT_RESPONSES_FILE,
    process_response_files,
)


DEFAULT_GRAPH_VERSION = "v23.0"


def graph_get(url: str) -> Dict[str, Any]:
    try:
        with urlopen(url, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Instagram Graph API HTTP {e.code}: {body}") from e
    except URLError as e:
        raise RuntimeError(f"Instagram Graph API request failed: {e}") from e


def normalize_comment(comment: Dict[str, Any]) -> Dict[str, Any]:
    replies = comment.get("replies", {})
    if isinstance(replies, dict):
        replies = replies.get("data", [])
    if not isinstance(replies, list):
        replies = []

    return {
        "id": comment.get("id", ""),
        "text": comment.get("text", ""),
        "username": comment.get("username", ""),
        "timestamp": comment.get("timestamp", ""),
        "like_count": comment.get("like_count"),
        "replies": [
            {
                "id": reply.get("id", ""),
                "text": reply.get("text", ""),
                "username": reply.get("username", ""),
                "timestamp": reply.get("timestamp", ""),
                "like_count": reply.get("like_count"),
            }
            for reply in replies
            if isinstance(reply, dict)
        ],
    }


def fetch_comments(
    media_id: str,
    access_token: str,
    graph_version: str,
    limit: int,
    max_pages: int,
    include_replies: bool,
) -> List[Dict[str, Any]]:
    fields = "id,text,username,timestamp,like_count"
    if include_replies:
        fields += ",replies{id,text,username,timestamp,like_count}"

    params = {
        "fields": fields,
        "limit": str(limit),
        "access_token": access_token,
    }
    url = f"https://graph.facebook.com/{graph_version}/{media_id}/comments?{urlencode(params)}"
    comments: List[Dict[str, Any]] = []
    pages = 0

    while url and pages < max_pages:
        payload = graph_get(url)
        for item in payload.get("data", []):
            if isinstance(item, dict):
                comments.append(normalize_comment(item))

        pages += 1
        paging = payload.get("paging") or {}
        url = paging.get("next")

    return comments


def load_existing_comments(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {"comments": []}
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except Exception:
        return {"comments": []}
    return data if isinstance(data, dict) else {"comments": []}


def merge_comments(existing: Dict[str, Any], fresh_comments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_id = {}
    for comment in existing.get("comments", []):
        if isinstance(comment, dict) and comment.get("id"):
            by_id[str(comment["id"])] = comment
    for comment in fresh_comments:
        if comment.get("id"):
            by_id[str(comment["id"])] = comment
    return sorted(by_id.values(), key=lambda item: item.get("timestamp") or "", reverse=True)


def write_comments(path: str, media_id: str, comments: List[Dict[str, Any]]) -> None:
    payload = {
        "metadata": {
            "media_id": media_id,
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "comment_count": len(comments),
        },
        "comments": comments,
    }
    Path(path).write_text(json.dumps(payload, indent=2) + "\n")


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Collect Instagram draft-post comments")
    parser.add_argument("--media-id", required=True, help="Instagram Graph API media ID for the draft post")
    parser.add_argument("--output-file", default=DEFAULT_COMMENT_RESPONSES_FILE)
    parser.add_argument("--comment-mapping-file", default=DEFAULT_COMMENT_MAPPING_FILE)
    parser.add_argument("--graph-version", default=os.getenv("IG_GRAPH_API_VERSION", DEFAULT_GRAPH_VERSION))
    parser.add_argument("--limit", type=int, default=100, help="Comments per API page")
    parser.add_argument("--max-pages", type=int, default=25)
    parser.add_argument("--replace", action="store_true", help="Replace output instead of merging by comment ID")
    parser.add_argument("--no-replies", action="store_true", help="Do not request threaded replies")
    parser.add_argument("--no-process", action="store_true", help="Only collect comments; do not generate queue/SQL")
    parser.add_argument(
        "--include-existing-response-files",
        action="store_true",
        help="Also process existing dm_replies.json and twilio_responses.json. Default is comments only.",
    )
    args = parser.parse_args()

    access_token: Optional[str] = os.getenv("IG_GRAPH_ACCESS_TOKEN") or os.getenv("FACEBOOK_ACCESS_TOKEN")
    if not access_token:
        print("❌ Missing IG_GRAPH_ACCESS_TOKEN in .env")
        sys.exit(1)

    print("=" * 70)
    print("INSTAGRAM COMMENT COLLECTOR")
    print("=" * 70)
    print(f"Media ID: {args.media_id}")
    print(f"Output file: {args.output_file}")
    print(f"Comment mapping: {args.comment_mapping_file}")

    try:
        fresh_comments = fetch_comments(
            media_id=args.media_id,
            access_token=access_token,
            graph_version=args.graph_version,
            limit=args.limit,
            max_pages=args.max_pages,
            include_replies=not args.no_replies,
        )
    except RuntimeError as e:
        print(f"❌ {e}")
        sys.exit(1)

    existing = {"comments": []} if args.replace else load_existing_comments(args.output_file)
    comments = fresh_comments if args.replace else merge_comments(existing, fresh_comments)
    write_comments(args.output_file, args.media_id, comments)

    print(f"Fetched comments this run: {len(fresh_comments)}")
    print(f"Stored comments total: {len(comments)}")
    print(f"Saved: {args.output_file}")

    if args.no_process:
        print("=" * 70)
        return

    print("\nProcessing comments into AI queue and Supabase SQL...")
    result = process_response_files(
        instagram_file="dm_replies.json" if args.include_existing_response_files else "",
        sms_file="twilio_responses.json" if args.include_existing_response_files else "",
        comments_file=args.output_file,
        comment_mapping_file=args.comment_mapping_file,
    )
    print(f"Direct Supabase updates: {result['direct_updates']}")
    print(f"AI parse queue items: {result['ai_queue_items']}")
    print(f"Supabase SQL: {result['sql_output_file']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
