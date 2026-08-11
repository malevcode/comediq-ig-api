#!/usr/bin/env python3
"""
Send Instagram DM messages to open mic hosts grouped by their Instagram handles.

This script reads a CSV file and groups open mics by Instagram handle, then sends
a personalized message listing all mics for each host.
"""

import pandas as pd
from ig_messaging import InstagramMessagingSystem
import sys
import os
from dotenv import load_dotenv
from typing import Dict, List
from datetime import datetime
import re
import argparse


def normalize_instagram_handle(value) -> str:
    """Return a clean Instagram handle without @, or an empty string if invalid."""
    if value is None:
        return ""

    text = str(value).strip()
    if text.lower() in {"", "nan", "none", "null", "#n/a", "n/a", "no", "unknown"}:
        return ""
    if "http://" in text.lower() or "https://" in text.lower() or "instagram.com" in text.lower():
        return ""
    if re.fullmatch(r"[+()\d\s.-]{7,}", text):
        return ""

    if "@" in text:
        match = re.search(r"@([A-Za-z0-9._]{1,30})\b", text)
        if not match:
            return ""
        handle = match.group(1)
    else:
        handle = text

    if not re.fullmatch(r"[A-Za-z0-9._]{3,30}", handle):
        return ""
    if not re.search(r"[A-Za-z]", handle):
        return ""

    return handle


def group_mics_by_instagram_handle(df: pd.DataFrame) -> Dict[str, List[Dict]]:
    """
    Group open mics by Instagram handle, filtering for Instagram/DM preference only.
    
    Args:
        df: DataFrame with open mic data
        
    Returns:
        Dictionary mapping Instagram handles to list of mic data
    """
    grouped = {}
    
    print("🔍 Filtering for valid Instagram handles...")

    instagram_rows = df[df["changes_updates"].apply(lambda value: bool(normalize_instagram_handle(value)))]

    print(f"   📱 {len(df)} total rows → {len(instagram_rows)} rows with valid Instagram handles")
    
    for _, row in instagram_rows.iterrows():
        handle = normalize_instagram_handle(row["changes_updates"])
        if not handle:
            continue
        
        # Create mic info dict
        mic_info = {
            'unique_id': row.get('unique_identifier', ''),
            'name': row.get('open_mic', ''),
            'day': row.get('day', ''),
            'time': row.get('start_time', ''),
            'venue': row.get('venue_name', ''),
            'location': row.get('location', ''),
            'borough': row.get('borough', ''),
            'message_number': row.get('aug_message_number', row.get('message_number', '')),
        }
        
        if handle not in grouped:
            grouped[handle] = []
        grouped[handle].append(mic_info)
    
    return grouped


def create_message_for_host(handle: str, mics: List[Dict], form_link: str = None) -> str:
    """
    Create a personalized message for a host listing their mics.
    
    Args:
        handle: Instagram handle of the host
        mics: List of mic information dictionaries
        form_link: Link to changes form (optional)
        
    Returns:
        Formatted message string
    """
    # Get current month name
    current_month = datetime.now().strftime("%B")
    
    # Build mic list with simple format for parsing
    mic_list = []
    for i, mic in enumerate(mics, 1):
        display_number = mic.get('message_number') or i
        mic_name = mic['name']
        if mic['day'] and mic['time']:
            mic_line = f"{display_number}. {mic_name} ({mic['day']} at {mic['time']})"
        else:
            mic_line = f"{display_number}. {mic_name}"
        
        mic_list.append(mic_line)
    
    mic_list_text = "\n".join(mic_list)
    
    # Base message
    if len(mics) > 1:
        base_message = f"""Hey @{handle}! It's Adam from Comediq! I'm doing the monthly check in to update our {current_month} mic list. For each mic, reply with the number and status:

Reply format: [number] Y/N/Changes

Here's what we have listed:"""
    else:
        base_message = f"""Hey @{handle}! It's Adam from Comediq! I'm doing the monthly check in to update our {current_month} mic list. Please reply:

Reply: Y (active), N (not active), or Changes (has updates)

Here's what we have listed:"""

    # Closing message
    if form_link:
        closing = f"""

Please respond with updates for each mic. If you have changes, you can also fill out this form: {form_link}

Thanks!"""
    else:
        closing = """

Please respond with updates for each mic. Thanks!"""
    
    return base_message + "\n\n" + mic_list_text + closing


def main():
    """Main execution function."""
    print("=" * 70)
    print("📤 INSTAGRAM MESSAGE SENDER")
    print("=" * 70)
    
    parser = argparse.ArgumentParser(description="Send Instagram verification DMs")
    parser.add_argument("csv_file", nargs="?", help="CSV file containing mics to verify")
    parser.add_argument("--no-form-link", action="store_true", help="Do not include CHANGES_FORM_LINK in messages")
    args = parser.parse_args()

    # Load environment variables for form link
    load_dotenv()
    form_link = None if args.no_form_link else os.getenv("CHANGES_FORM_LINK")
    
    # Get CSV file path
    if args.csv_file:
        csv_file = args.csv_file
    else:
        csv_file = input("Enter the path to your CSV file (default: active_to_confirm_NY.csv): ").strip()
        if not csv_file:
            csv_file = "active_to_confirm_NY.csv"
    
    # Check if file exists
    try:
        df = pd.read_csv(csv_file)
        print(f"✅ Loaded CSV: {csv_file}")
        print(f"   Total rows: {len(df)}")
    except FileNotFoundError:
        print(f"❌ Error: File '{csv_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        sys.exit(1)
    
    # Check for required columns
    required_columns = ['open_mic', 'changes_updates', 'unique_identifier']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"❌ Error: Missing required columns: {missing_columns}")
        print(f"   Available columns: {list(df.columns)}")
        sys.exit(1)
    
    # Group mics by Instagram handle (with Instagram preference filtering)
    print("\n📋 Grouping mics by Instagram handle...")
    grouped_mics = group_mics_by_instagram_handle(df)
    print(f"   Found {len(grouped_mics)} unique Instagram handles")
    
    # Show preview
    total_mics = sum(len(mics) for mics in grouped_mics.values())
    print(f"   Total mics to verify: {total_mics}")
    
    # Show hosts with multiple mics
    multi_mic_hosts = {h: mics for h, mics in grouped_mics.items() if len(mics) > 1}
    if multi_mic_hosts:
        print(f"\n📊 Hosts with multiple mics: {len(multi_mic_hosts)}")
        for handle, mics in sorted(multi_mic_hosts.items()):
            print(f"   @{handle}: {len(mics)} mics")
    
    # Show form link status
    if form_link:
        print(f"\n📝 Changes form link configured: {form_link[:50]}...")
    else:
        print("\n⚠️  No changes form link in .env (CHANGES_FORM_LINK)")
    
    # Confirm before sending
    print("\n" + "=" * 70)
    confirm = input("Ready to send messages? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("Cancelled.")
        sys.exit(0)
    
    # Initialize messaging system
    try:
        print("\n🔐 Logging into Instagram...")
        messaging_system = InstagramMessagingSystem()
    except Exception as e:
        print(f"❌ Error initializing Instagram: {e}")
        sys.exit(1)
    
    # Send messages
    print("\n📤 Sending messages...")
    results = {}
    
    def send_succeeded(result_value) -> bool:
        if not result_value:
            return False
        if isinstance(result_value, str):
            return not (
                result_value.startswith("Error")
                or result_value.startswith("User")
                or result_value.startswith("Invalid")
            )
        return True
    
    for handle, mics in sorted(grouped_mics.items()):
        message = create_message_for_host(handle, mics, form_link)
        
        try:
            result = messaging_system.send_message_to_usernames([handle], message)
            result_value = result.get(handle, "Error")
            results[handle] = result_value
            if send_succeeded(result_value):
                existing_mic_ids = messaging_system.mic_identifier_mapping.get(handle, [])
                if not isinstance(existing_mic_ids, list):
                    existing_mic_ids = [existing_mic_ids] if existing_mic_ids else []
                for mic_id in [mic['unique_id'] for mic in mics]:
                    if mic_id and mic_id not in existing_mic_ids:
                        existing_mic_ids.append(mic_id)
                messaging_system.mic_identifier_mapping[handle] = existing_mic_ids
                messaging_system.save_mic_mapping()
        except Exception as e:
            print(f"❌ Error sending to @{handle}: {e}")
            results[handle] = f"Error: {str(e)}"
    
    # Print results summary
    print("\n" + "=" * 70)
    print("📊 SENDING COMPLETE")
    print("=" * 70)
    
    successful = sum(1 for r in results.values() if send_succeeded(r))
    failed = len(results) - successful
    
    print(f"✅ Successfully sent: {successful}/{len(results)}")
    if failed > 0:
        print(f"❌ Failed: {failed}/{len(results)}")
        
        # Show only first few failures
        failures = [(handle, result) for handle, result in results.items() 
                   if isinstance(result, str) and (result.startswith("Error") or result.startswith("User"))]
        
        print("\n❌ Sample failures:")
        for handle, result in failures[:3]:
            print(f"   @{handle}: {result}")
        if len(failures) > 3:
            print(f"   ... and {len(failures) - 3} more failures")
    
    # Print status report
    messaging_system.print_status_report()
    
    print("\n💡 To collect responses later, run: python collect_instagram_responses.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
