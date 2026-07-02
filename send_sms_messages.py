#!/usr/bin/env python3
"""
Send SMS messages to open mic hosts grouped by their phone numbers.

This script reads a CSV file and groups open mics by phone number, then sends
a personalized message listing all mics for each host via Twilio.

Usage:
    python send_sms_messages.py [csv_file]
    
Arguments:
    csv_file: Path to the CSV file containing mic data (default: active_to_confirm_NY.csv)
"""

import pandas as pd
from twilio_messaging import TwilioMessagingSystem
import sys
import os
import json
from dotenv import load_dotenv
from typing import Dict, List
from datetime import datetime
import re


DETAIL_COLUMNS = ["cost", "frequency", "location", "stage_time", "latest_end_time"]
MIC_DETAILS_MAPPING_FILE = "twilio_mic_details_mapping.json"


def clean_field_value(value) -> str:
    """Return a display-safe string for optional CSV fields."""
    if pd.isna(value):
        return ""

    text = str(value).strip()
    if text.lower() in ["nan", "none", "null", "#n/a", "n/a"]:
        return ""

    return text


def normalize_phone_to_e164(phone: str) -> str:
    """
    Normalize a phone number to E.164 format for Twilio.
    
    Handles various input formats:
    - Raw digits: 1234567890 → +11234567890
    - With formatting: (555) 123-4567 → +15551234567
    - With country code: +1 555-123-4567 → +15551234567
    - Already E.164: +11234567890 → +11234567890
    - International: +44 20 1234 5678 → +442012345678
    
    Args:
        phone: Raw phone number string from CSV
        
    Returns:
        E.164 formatted phone number (+[country][number])
    """
    phone_text = clean_field_value(phone)
    if not phone_text or phone_text.lower() == 'refuse to':
        return ''
    
    raw = phone_text
    
    # Extract all digits
    digits = re.sub(r'\D', '', raw)
    
    if not digits:
        return ''
    
    # If original started with '+', preserve the international format
    if raw.startswith('+'):
        return '+' + digits
    
    # Handle US numbers
    if len(digits) == 10:
        # Standard 10-digit US number
        return '+1' + digits
    elif len(digits) == 11 and digits.startswith('1'):
        # 11-digit with leading 1 (US format)
        return '+' + digits
    elif len(digits) >= 10:
        # Assume it's a US number and add +1
        return '+1' + digits

    return ''


def group_mics_by_phone_number(df: pd.DataFrame) -> Dict[str, List[Dict]]:
    """
    Group open mics by phone number, filtering for SMS preference only.
    
    Args:
        df: DataFrame with open mic data
        
    Returns:
        Dictionary mapping phone numbers to list of mic data
    """
    grouped = {}
    
    print("🔍 Filtering for SMS preference...")

    normalized_phones = df['sms_response'].apply(normalize_phone_to_e164)
    sms_preferred = df[normalized_phones != ''].copy()
    sms_preferred['_e164_phone'] = normalized_phones[sms_preferred.index]

    nonempty_sms = df['sms_response'].apply(clean_field_value) != ''
    invalid_phone_count = (nonempty_sms & (normalized_phones == '')).sum()

    print(f"   📱 {len(df)} total rows → {len(sms_preferred)} valid SMS rows")
    if invalid_phone_count:
        print(f"   ⚠️  Skipped {invalid_phone_count} row(s) with invalid SMS phone values")
    
    for _, row in sms_preferred.iterrows():
        phone = row['_e164_phone']
        
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
        
        if phone not in grouped:
            grouped[phone] = []
        grouped[phone].append(mic_info)
    
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


def create_message_for_host_phone(phone: str, mics: List[Dict], form_link: str = None) -> str:
    """
    Create a personalized message for a host listing their mics.
    
    Args:
        phone: Phone number of the host
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

        mic_line += "\n   " + " | ".join(details)
        
        mic_list.append(mic_line)
    
    mic_list_text = "\n".join(mic_list)
    
    # Base message
    if len(mics) > 1:
        base_message = f"""Hey! It's Adam from Comediq! I'm doing the monthly check in to update our {current_month} mic list. For each mic, reply with the number and status:

Reply format: [number] Y/N/Changes

Please include the correct cost, frequency, location, stage time, and latest end time for each mic.
Example: 1 Y, cost: $5, frequency: weekly, location: 123 Main St, stage time: 5 min, latest end time: 10pm

Here's what we have listed:"""
    else:
        base_message = f"""Hey! It's Adam from Comediq! I'm doing the monthly check in to update our {current_month} mic list. Please reply:

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
    print("📱 SMS MESSAGE SENDER")
    print("=" * 70)
    
    # Load environment variables for form link
    load_dotenv()
    form_link = os.getenv("CHANGES_FORM_LINK")
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = input("Enter the path to your CSV file (default: active_to_confirm_NY.csv): ").strip()
        if not csv_file:
            csv_file = "active_to_confirm_NY.csv"
    
    # Check if file exists
    try:
        # Ensure sms_response is always loaded as a string to preserve formatting
        df = pd.read_csv(csv_file, dtype={"sms_response": str})
        print(f"✅ Loaded CSV: {csv_file}")
        print(f"   Total rows: {len(df)}")
    except FileNotFoundError:
        print(f"❌ Error: File '{csv_file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        sys.exit(1)
    
    # Check for required columns
    required_columns = ['open_mic', 'sms_response', 'unique_identifier']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"❌ Error: Missing required columns: {missing_columns}")
        print(f"   Available columns: {list(df.columns)}")
        sys.exit(1)

    missing_detail_columns = [col for col in DETAIL_COLUMNS if col not in df.columns]
    if missing_detail_columns:
        print(f"⚠️  Optional detail columns missing: {missing_detail_columns}")
        print("   Messages will still send and placeholders will be shown for those details.")
    
    # Group mics by phone number (with SMS preference filtering)
    print("\n📋 Grouping mics by phone number...")
    grouped_mics = group_mics_by_phone_number(df)
    print(f"   Found {len(grouped_mics)} unique phone numbers (SMS preferred only)")
    
    # Show preview
    total_mics = sum(len(mics) for mics in grouped_mics.values())
    print(f"   Total mics to verify: {total_mics}")
    
    # Show hosts with multiple mics
    multi_mic_hosts = {p: mics for p, mics in grouped_mics.items() if len(mics) > 1}
    if multi_mic_hosts:
        print(f"\n📊 Hosts with multiple mics: {len(multi_mic_hosts)}")
        for phone, mics in sorted(multi_mic_hosts.items()):
            print(f"   {phone}: {len(mics)} mics")
    
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
        print("\n🔐 Initializing Twilio...")
        messaging_system = TwilioMessagingSystem()  # Uses default file paths
    except Exception as e:
        print(f"❌ Error initializing Twilio: {e}")
        sys.exit(1)
    
    # Send messages
    print("\n📤 Sending messages...")
    results = {}
    
    # Create phone to mic identifier mapping for all mics
    phone_to_mics = {}
    for phone, mics in grouped_mics.items():
        phone_to_mics[phone] = [mic['unique_id'] for mic in mics]
    
    # Store the mapping in the messaging system (phone -> list of mic IDs)
    messaging_system.mic_identifier_mapping = {}
    phone_to_e164 = {}  # Track E.164 formatted numbers for sending
    
    for phone, mic_ids in phone_to_mics.items():
        # Normalize phone number to E.164 format using our dedicated function
        formatted_phone = normalize_phone_to_e164(phone)
        
        if not formatted_phone:  # Skip if normalization failed
            print(f"⚠️  Skipping invalid phone number: {phone}")
            continue

        messaging_system.mic_identifier_mapping[formatted_phone] = mic_ids
        phone_to_e164[phone] = formatted_phone  # Map raw phone to E.164 for sending
    
    # Save the mapping
    messaging_system.save_mic_mapping()
    save_mic_details_mapping(grouped_mics)
    
    for phone, mics in sorted(grouped_mics.items()):
        message = create_message_for_host_phone(phone, mics, form_link)
        e164_phone = phone_to_e164.get(phone, phone)  # Use E.164 formatted number for sending
        
        try:
            result = messaging_system.send_message_to_numbers([e164_phone], message)
            results[phone] = result.get(e164_phone, "Error")
        except Exception as e:
            print(f"❌ Error sending to {phone}: {e}")
            results[phone] = f"Error: {str(e)}"
    
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
        failures = [(phone, result) for phone, result in results.items() 
                   if isinstance(result, str) and result.startswith("Error")]
        
        print("\n❌ Sample failures:")
        for phone, result in failures[:3]:
            print(f"   {phone}: {result}")
        if len(failures) > 3:
            print(f"   ... and {len(failures) - 3} more failures")
    
    # Print status report
    messaging_system.print_status_report()
    
    print("\n💡 To collect responses later, run: python collect_sms_responses.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
