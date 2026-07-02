#!/usr/bin/env python3
"""
Send Instagram DM messages to open mic hosts grouped by their Instagram handles.

This script reads a CSV file and groups open mics by Instagram handle, then sends
a personalized message listing all mics for each host.
"""

import pandas as pd
from ig_messaging import InstagramMessagingSystem
import argparse
import sys
import os
import json
import re
from dotenv import load_dotenv
from typing import Dict, List
from datetime import datetime


DETAIL_COLUMNS = ["cost", "frequency", "location", "stage_time", "latest_end_time"]
MIC_DETAILS_MAPPING_FILE = "ig_mic_details_mapping.json"
INSTAGRAM_HANDLE_PATTERN = re.compile(r"^@?[A-Za-z0-9._]{1,30}$")


def clean_field_value(value) -> str:
    """Return a display-safe string for optional CSV fields."""
    if pd.isna(value):
        return ""

    text = str(value).strip()
    if text.lower() in ["nan", "none", "null", "#n/a", "n/a"]:
        return ""

    return text


def clean_instagram_handle(value) -> str:
    """Return a normalized Instagram handle, or an empty string when invalid."""
    handle = clean_field_value(value)
    if not handle or not INSTAGRAM_HANDLE_PATTERN.match(handle):
        return ""

    return handle.lstrip("@")


def group_mics_by_instagram_handle(df: pd.DataFrame, include_sms_contacts: bool = False) -> Dict[str, List[Dict]]:
    """
    Group open mics by Instagram handle, filtering for Instagram/DM preference only.
    
    Args:
        df: DataFrame with open mic data
        
    Returns:
        Dictionary mapping Instagram handles to list of mic data
    """
    grouped = {}
    
    print("🔍 Filtering for Instagram/DM preference...")

    valid_handles = df['changes_updates'].apply(clean_instagram_handle)
    no_sms_contact = (
        df['sms_response'].isin(['refuse to', '#N/A', 'N/A']) |
        df['sms_response'].isna() |
        (df['sms_response'].astype(str).str.strip() == '') |
        (df['sms_response'].astype(str).str.lower().str.strip() == 'nan')
    )
    if include_sms_contacts:
        instagram_preferred = df[valid_handles != ''].copy()
    else:
        instagram_preferred = df[(valid_handles != '') & no_sms_contact].copy()

    instagram_preferred['_clean_instagram_handle'] = valid_handles[instagram_preferred.index]

    invalid_handle_count = ((df['changes_updates'].apply(clean_field_value) != '') & (valid_handles == '')).sum()

    route_label = "valid Instagram rows" if include_sms_contacts else "valid Instagram-preferred rows"
    print(f"   📱 {len(df)} total rows → {len(instagram_preferred)} {route_label}")
    if invalid_handle_count:
        print(f"   ⚠️  Skipped {invalid_handle_count} row(s) with invalid Instagram handles/notes")
    
    for _, row in instagram_preferred.iterrows():
        handle = row['_clean_instagram_handle']
        
        # Create mic info dict
        mic_info = {
            'unique_id': row.get('unique_identifier', ''),
            'name': row.get('open_mic', ''),
            'day': row.get('day', ''),
            'time': row.get('start_time', ''),
            'venue': row.get('venue_name', ''),
            'location': clean_field_value(row.get('location', '')),
            'borough': row.get('borough', ''),
            'cost': clean_field_value(row.get('cost', '')),
            'frequency': clean_field_value(row.get('frequency', '')),
            'stage_time': clean_field_value(row.get('stage_time', '')),
            'latest_end_time': clean_field_value(row.get('latest_end_time', '')),
        }
        
        if handle not in grouped:
            grouped[handle] = []
        grouped[handle].append(mic_info)
    
    return grouped


def save_mic_details_mapping(grouped_mics: Dict[str, List[Dict]], file_path: str = MIC_DETAILS_MAPPING_FILE) -> None:
    """Save CSV-provided per-mic details for response/database processing."""
    mic_details = {}

    for mics in grouped_mics.values():
        for mic in mics:
            mic_id = clean_field_value(mic.get('unique_id', ''))
            if not mic_id:
                continue

            mic_details[mic_id] = {
                'location': clean_field_value(mic.get('location', '')),
                'cost': clean_field_value(mic.get('cost', '')),
                'frequency': clean_field_value(mic.get('frequency', '')),
                'stage_time': clean_field_value(mic.get('stage_time', '')),
                'latest_end_time': clean_field_value(mic.get('latest_end_time', '')),
            }

    try:
        existing_details = {}
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                existing_details = json.load(f)

        with open(file_path, 'w') as f:
            json.dump({**existing_details, **mic_details}, f, indent=2)

        print(f"💾 Saved mic details mapping to: {file_path}")
    except Exception as e:
        print(f"⚠️  Error saving mic details mapping: {e}")


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
        mic_name = mic['name']
        if mic['day'] and mic['time']:
            mic_line = f"{i}. {mic_name} ({mic['day']} at {mic['time']})"
        else:
            mic_line = f"{i}. {mic_name}"

        details = []
        details.append(f"cost: {mic.get('cost') or '[please confirm]'}")
        details.append(f"frequency: {mic.get('frequency') or '[please confirm]'}")
        details.append(f"location: {mic.get('location') or '[please confirm]'}")
        details.append(f"stage time: {mic.get('stage_time') or '[please confirm]'}")
        details.append(f"latest end time: {mic.get('latest_end_time') or '[please confirm]'}")

        if details:
            mic_line += "\n   " + " | ".join(details)
        
        mic_list.append(mic_line)
    
    mic_list_text = "\n".join(mic_list)
    
    # Base message
    if len(mics) > 1:
        base_message = f"""Hey @{handle}! It's Adam from Comediq! I'm doing the monthly check in to update our {current_month} mic list. For each mic, reply with the number and status:

Reply format: [number] Y/N/Changes

Please include the correct cost, frequency, location, stage time, and latest end time for each mic.
Example: 1 Y, cost: $5, frequency: weekly, location: 123 Main St, stage time: 5 min, latest end time: 10pm

Here's what we have listed:"""
    else:
        base_message = f"""Hey @{handle}! It's Adam from Comediq! I'm doing the monthly check in to update our {current_month} mic list. Please reply:

Reply: Y (active), N (not active), or Changes (has updates)

Please include the correct cost, frequency, location, stage time, and latest end time.
Example: Y, cost: $5, frequency: weekly, location: 123 Main St, stage time: 5 min, latest end time: 10pm

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
    
    # Load environment variables for form link
    load_dotenv()
    form_link = os.getenv("CHANGES_FORM_LINK")

    parser = argparse.ArgumentParser(description="Send or preview Instagram DM verification messages")
    parser.add_argument("csv_file", nargs="?", help="Path to CSV file containing mic data")
    parser.add_argument("--preview", action="store_true", help="Print sample messages without logging in or sending")
    parser.add_argument("--preview-count", type=int, default=3, help="Number of grouped host messages to print")
    parser.add_argument(
        "--include-sms-contacts",
        action="store_true",
        help="Send/preview Instagram messages even for rows that also have SMS phone numbers",
    )
    args = parser.parse_args()

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
    required_columns = ['open_mic', 'changes_updates', 'sms_response', 'unique_identifier']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"❌ Error: Missing required columns: {missing_columns}")
        print(f"   Available columns: {list(df.columns)}")
        sys.exit(1)

    missing_detail_columns = [col for col in DETAIL_COLUMNS if col not in df.columns]
    if missing_detail_columns:
        print(f"⚠️  Optional detail columns missing: {missing_detail_columns}")
        print("   Messages will still send and placeholders will be shown for those details.")
    
    # Group mics by Instagram handle (with Instagram preference filtering)
    print("\n📋 Grouping mics by Instagram handle...")
    grouped_mics = group_mics_by_instagram_handle(df, include_sms_contacts=args.include_sms_contacts)
    handle_scope = "all valid Instagram handles" if args.include_sms_contacts else "Instagram preferred only"
    print(f"   Found {len(grouped_mics)} unique Instagram handles ({handle_scope})")
    
    # Show preview
    total_mics = sum(len(mics) for mics in grouped_mics.values())
    print(f"   Total mics to verify: {total_mics}")
    
    # Show hosts with multiple mics
    multi_mic_hosts = {h: mics for h, mics in grouped_mics.items() if len(mics) > 1}
    if multi_mic_hosts:
        print(f"\n📊 Hosts with multiple mics: {len(multi_mic_hosts)}")
        for handle, mics in sorted(multi_mic_hosts.items()):
            print(f"   @{handle}: {len(mics)} mics")

    if args.preview:
        print("\n" + "=" * 70)
        print(f"👀 PREVIEW MODE - showing {min(args.preview_count, len(grouped_mics))} message(s)")
        print("=" * 70)

        for index, (handle, mics) in enumerate(sorted(grouped_mics.items()), 1):
            if index > args.preview_count:
                break

            print(f"\n--- Message {index}: @{handle} ({len(mics)} mic(s)) ---")
            print(create_message_for_host(handle, mics, form_link))

        print("\n✅ Preview complete. No messages were sent.")
        return
    
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
    
    # Create username to mic identifier mapping for all mics
    username_to_mics = {}
    for handle, mics in grouped_mics.items():
        username_to_mics[handle] = [mic['unique_id'] for mic in mics]
    
    # Store the mapping in the messaging system (username -> list of mic IDs)
    messaging_system.mic_identifier_mapping = username_to_mics
    
    # Save the mapping
    messaging_system.save_mic_mapping()
    save_mic_details_mapping(grouped_mics)
    
    for handle, mics in sorted(grouped_mics.items()):
        message = create_message_for_host(handle, mics, form_link)
        
        try:
            result = messaging_system.send_message_to_usernames([handle], message)
            results[handle] = result.get(handle, "Error")
        except Exception as e:
            print(f"❌ Error sending to @{handle}: {e}")
            results[handle] = f"Error: {str(e)}"
    
    # Print results summary
    print("\n" + "=" * 70)
    print("📊 SENDING COMPLETE")
    print("=" * 70)
    
    successful = sum(1 for r in results.values() if not isinstance(r, str) or not r.startswith("Error"))
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
