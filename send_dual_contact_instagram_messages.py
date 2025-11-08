#!/usr/bin/env python3
"""
Send Instagram DM messages to hosts who have BOTH SMS phone numbers AND Instagram handles.

This script targets contacts who can be reached via both channels, sending Instagram DMs
to those who have valid phone numbers in sms_response AND Instagram handles in changes_updates.
"""

import pandas as pd
from ig_messaging import InstagramMessagingSystem
import sys
import os
from dotenv import load_dotenv
from typing import Dict, List
from datetime import datetime
import re


def normalize_phone_to_e164(phone: str) -> str:
    """
    Normalize a phone number to E.164 format.
    
    Args:
        phone: Raw phone number string from CSV
        
    Returns:
        E.164 formatted phone number (+[country][number]) or empty string if invalid
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


def group_mics_by_instagram_handle_sms_fallback(df: pd.DataFrame) -> Dict[str, List[Dict]]:
    """
    Group open mics by Instagram handle, targeting SMS-preferred contacts via Instagram fallback.
    
    This filters for contacts who were originally intended for SMS outreach but also have
    Instagram handles, allowing us to reach them via DM when SMS service is unavailable.
    
    Args:
        df: DataFrame with open mic data
        
    Returns:
        Dictionary mapping Instagram handles to list of mic data
    """
    grouped = {}
    
    print("🔍 Filtering for SMS-preferred contacts with Instagram fallback...")
    
    # Apply SMS-preferred + Instagram fallback filter: 
    # - Originally SMS preferred (has valid phone number)
    # - But also has Instagram handle for fallback communication
    sms_fallback = df[
        # Originally SMS preferred (has valid phone number)
        df['sms_response'].notna() &  # sms_response is NOT null
        (~df['sms_response'].isin(['refuse to', '#N/A', 'N/A'])) &  # NOT in refuse list
        (df['sms_response'].astype(str).str.strip() != '') &  # Not empty string
        (df['sms_response'].astype(str) != 'nan') &  # Not string 'nan'
        # Has Instagram handle for fallback
        df['changes_updates'].notna() &  # Must have Instagram handle
        (df['changes_updates'] != '') &  # Not empty
        (df['changes_updates'].astype(str) != 'nan') &  # Not string 'nan'
        (df['changes_updates'].astype(str) != '#N/A')  # Not #N/A
    ]
    
    print(f"   📱→📸 {len(df)} total rows → {len(sms_fallback)} SMS-preferred with Instagram fallback")
    
    for _, row in sms_fallback.iterrows():
        handle = str(row['changes_updates']).strip()
        phone = str(row['sms_response']).strip()
        
        # Skip invalid handles or phones
        if handle in ['nan', '#N/A', ''] or phone in ['nan', '#N/A', '', 'refuse to']:
            continue
        
        # Remove @ if present from handle
        if handle.startswith('@'):
            handle = handle[1:]
        
        # Validate phone number can be normalized
        normalized_phone = normalize_phone_to_e164(phone)
        if not normalized_phone:
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
            'phone_number': normalized_phone,  # Include normalized phone for reference
        }
        
        if handle not in grouped:
            grouped[handle] = []
        grouped[handle].append(mic_info)
    
    return grouped


def create_message_for_sms_fallback_host(handle: str, mics: List[Dict], form_link: str = None) -> str:
    """
    Create a personalized message for an SMS-preferred host reached via Instagram fallback.
    
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

    # Closing message - explain SMS fallback
    if form_link:
        closing = f"""

Please respond with updates for each mic. If you have changes, you can also fill out this form: {form_link}

Thanks!"""
    else:
        closing = """

Please respond with updates for each mic.

(Note: We're reaching out via Instagram since our SMS system is temporarily down)

Thanks!"""
    
    return base_message + "\n\n" + mic_list_text + closing


def main():
    """Main execution function."""
    print("=" * 70)
    print("📱→📸 SMS FALLBACK INSTAGRAM MESSAGE SENDER")
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
        # Ensure both sms_response and changes_updates are loaded as strings
        df = pd.read_csv(csv_file, dtype={"sms_response": str, "changes_updates": str})
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
    
    # Group mics by Instagram handle (SMS fallback filtering)
    print("\n📋 Grouping mics by Instagram handle (SMS fallback)...")
    grouped_mics = group_mics_by_instagram_handle_sms_fallback(df)
    print(f"   Found {len(grouped_mics)} unique Instagram handles (SMS fallback)")
    
    # Show preview
    total_mics = sum(len(mics) for mics in grouped_mics.values())
    print(f"   Total mics to verify: {total_mics}")
    
    # Show hosts with multiple mics
    multi_mic_hosts = {h: mics for h, mics in grouped_mics.items() if len(mics) > 1}
    if multi_mic_hosts:
        print(f"\n📊 Hosts with multiple mics: {len(multi_mic_hosts)}")
        for handle, mics in sorted(multi_mic_hosts.items()):
            phone_sample = mics[0]['phone_number']
            print(f"   @{handle} ({phone_sample}): {len(mics)} mics")
    
    # Show form link status
    if form_link:
        print(f"\n📝 Changes form link configured: {form_link[:50]}...")
    else:
        print("\n⚠️  No changes form link in .env (CHANGES_FORM_LINK)")
    
    # Confirm before sending
    print("\n" + "=" * 70)
    print("🎯 This will send Instagram DMs to SMS-preferred contacts as fallback")
    print("   (Reaching them via Instagram since SMS service is down)")
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
        print("\nMake sure you have set the following environment variables:")
        print("- IG_USER")
        print("- IG_PASSWORD")
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
    
    for handle, mics in sorted(grouped_mics.items()):
        message = create_message_for_sms_fallback_host(handle, mics, form_link)
        
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
    print("💡 These contacts were originally SMS-preferred but reached via Instagram fallback")
    print("=" * 70)


if __name__ == "__main__":
    main()