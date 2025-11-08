#!/usr/bin/env python3
"""
Send SMS messages to open mic hosts grouped by their phone numbers.

This script reads a CSV file and groups open mics by phone number, then sends
a personalized message listing all mics for each host via Twilio.
"""

import pandas as pd
from twilio_messaging import TwilioMessagingSystem
import sys
import os
from dotenv import load_dotenv
from typing import Dict, List
from datetime import datetime
import re


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
    if not phone or phone.strip() in ['nan', '#N/A', '', 'refuse to']:
        return ''
    
    raw = str(phone).strip()
    
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
    else:
        # Assume it's a US number and add +1
        return '+1' + digits


def group_mics_by_phone_number(df: pd.DataFrame) -> Dict[str, List[Dict]]:
    """
    Group open mics by phone number, filtering for SMS preference only.
    
    Args:
        df: DataFrame with open mic data
        
    Returns:
        Dictionary mapping phone numbers to list of mic data
    """
    grouped = {}
    
    # Filter for SMS preference: sms_response NOT in ('refuse to', '#N/A', 'N/A') AND sms_response is NOT null
    print("🔍 Filtering for SMS preference...")
    
    # Apply SMS preference filter
    sms_preferred = df[
        df['sms_response'].notna() &  # sms_response is NOT null
        (~df['sms_response'].isin(['refuse to', '#N/A', 'N/A'])) &  # NOT in refuse list
        (df['sms_response'].astype(str).str.strip() != '') &  # Not empty string
        (df['sms_response'].astype(str) != 'nan')  # Not string 'nan'
    ]
    
    print(f"   📱 {len(df)} total rows → {len(sms_preferred)} SMS preferred")
    
    for _, row in sms_preferred.iterrows():
        phone = str(row['sms_response']).strip()
        
        # Skip invalid phone numbers (shouldn't happen after filtering but safety check)
        if phone in ['nan', '#N/A', '', 'refuse to']:
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
        }
        
        if phone not in grouped:
            grouped[phone] = []
        grouped[phone].append(mic_info)
    
    return grouped


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
        
        mic_list.append(mic_line)
    
    mic_list_text = "\n".join(mic_list)
    
    # Base message
    if len(mics) > 1:
        base_message = f"""Hey! It's Adam from Comediq! I'm doing the monthly check in to update our {current_month} mic list. For each mic, reply with the number and status:

Reply format: [number] Y/N/Changes

Here's what we have listed:"""
    else:
        base_message = f"""Hey! It's Adam from Comediq! I'm doing the monthly check in to update our {current_month} mic list. Please reply:

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
    print("📱 SMS MESSAGE SENDER")
    print("=" * 70)
    
    # Load environment variables for form link
    load_dotenv()
    form_link = os.getenv("CHANGES_FORM_LINK")
    
    # Get CSV file path
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
        messaging_system = TwilioMessagingSystem()
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
    
    for phone, mics in sorted(grouped_mics.items()):
        message = create_message_for_host_phone(phone, mics, form_link)
        e164_phone = phone_to_e164[phone]  # Use E.164 formatted number for sending
        
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

