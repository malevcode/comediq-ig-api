#!/usr/bin/env python3
"""
Collect responses from Instagram DMs and save them for processing.

This script fetches DM replies from Instagram and saves them in a structured format.
"""

from ig_messaging import InstagramMessagingSystem
from process_responses import process_response_files
import argparse
import json
import os
import sys


def load_json(path: str):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)


def normalize_username(username: str) -> str:
    return str(username or "").strip().lstrip("@")


def missing_response_usernames(sent_messages_file: str, replies_file: str = "dm_replies.json"):
    sent_messages = load_json(sent_messages_file)
    replies = load_json(replies_file)
    replied_usernames = {normalize_username(username) for username in replies.keys()}
    return [
        normalize_username(username)
        for username in sent_messages.keys()
        if normalize_username(username) and normalize_username(username) not in replied_usernames
    ]


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Collect Instagram DM responses")
    parser.add_argument("--sent-messages-file", default="ig_sent_messages.json")
    parser.add_argument("--mic-mapping-file", default="ig_mic_mapping.json")
    parser.add_argument("--amount", type=int, default=250, help="Number of recent DM threads to fetch")
    parser.add_argument(
        "--username",
        action="append",
        help="Only collect for this Instagram username. Can be repeated.",
    )
    parser.add_argument(
        "--missing-only",
        action="store_true",
        help="Only collect for sent usernames that do not already have an entry in dm_replies.json.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List target usernames without logging into Instagram or collecting.",
    )
    args = parser.parse_args()

    sent_messages_file = args.sent_messages_file
    mic_mapping_file = args.mic_mapping_file
    target_usernames = [username.strip().lstrip("@") for username in args.username] if args.username else None
    if args.missing_only:
        missing_usernames = missing_response_usernames(sent_messages_file)
        target_usernames = [
            username for username in missing_usernames
            if target_usernames is None or username in set(target_usernames)
        ]
    
    print("=" * 70)
    print("📥 COLLECTING INSTAGRAM RESPONSES")
    print("=" * 70)
    print(f"📁 Using sent messages file: {sent_messages_file}")
    print(f"📁 Using mic mapping file: {mic_mapping_file}")
    print(f"📚 Fetching up to {args.amount} recent DM threads")
    if target_usernames:
        print(f"🎯 Target usernames: {', '.join('@' + username for username in target_usernames)}")
    elif args.missing_only:
        print("🎯 No missing-response usernames found.")

    if args.dry_run:
        print("\nDry run only. No Instagram login or collection performed.")
        print(f"Target count: {len(target_usernames or []) if args.missing_only or args.username else 'all sent handles'}")
        print("=" * 70)
        return

    if args.missing_only and not target_usernames:
        print("\n✅ Nothing to collect: every sent username already has a response entry.")
        print("=" * 70)
        return
    
    # Initialize messaging system
    try:
        print("\n🔐 Logging into Instagram...")
        messaging_system = InstagramMessagingSystem(sent_messages_file, mic_mapping_file)
    except Exception as e:
        print(f"❌ Error initializing Instagram: {e}")
        print("\nMake sure you have set the following environment variables:")
        print("- IG_USER")
        print("- IG_PASSWORD")
        sys.exit(1)
    
    # Collect responses
    print("\n📥 Collecting responses...")
    responses = messaging_system.collect_responses(amount=args.amount, usernames=target_usernames)
    
    # Print status report
    messaging_system.print_status_report()

    if messaging_system.last_collection_error:
        print("\n❌ Instagram collection failed, so cached replies were not reprocessed.")
        print("   Try logging into Instagram in a browser, then rerun this script.")
        print("=" * 70)
        sys.exit(1)
    
    if len(responses) > 0:
        print("\n✅ Responses collected and saved to: dm_replies.json")
    else:
        print("\n⚠️  No new responses found")

    print("\n🔄 Processing responses into direct updates, AI queue, and SQL...")
    try:
        result = process_response_files()
        print(f"✅ Direct Supabase updates: {result['direct_updates']}")
        print(f"🧠 AI parse queue items: {result['ai_queue_items']}")
        print(f"📄 Processed JSON: {result['output_file']}")
        print(f"🧠 AI queue: {result['ai_queue_file']}")
        print(f"🧾 Supabase SQL: {result['sql_output_file']}")
    except Exception as e:
        print(f"❌ Error processing responses after collection: {e}")
        print("   You can retry with: python process_responses.py")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
