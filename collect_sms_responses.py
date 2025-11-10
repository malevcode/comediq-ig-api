#!/usr/bin/env python3
"""
Collect responses from SMS messages and save them for processing.

This script fetches incoming SMS replies from Twilio and saves them in a structured format.

Usage:
    python collect_sms_responses.py [sent_messages_file] [mic_mapping_file]
    
Arguments:
    sent_messages_file: Path to the sent messages JSON file (default: twilio_sent_messages.json)
    mic_mapping_file: Path to the mic mapping JSON file (default: twilio_mic_mapping.json)
"""

from twilio_messaging import TwilioMessagingSystem
import sys


def main():
    """Main execution function."""
    print("=" * 70)
    print("📥 COLLECTING SMS RESPONSES")
    print("=" * 70)
    
    # Parse command line arguments
    sent_messages_file = sys.argv[1] if len(sys.argv) > 1 else "twilio_sent_messages.json"
    mic_mapping_file = sys.argv[2] if len(sys.argv) > 2 else "twilio_mic_mapping.json"
    
    print(f"📄 Using sent messages file: {sent_messages_file}")
    print(f"🎤 Using mic mapping file: {mic_mapping_file}")
    
    # Initialize messaging system
    try:
        print("\n🔐 Initializing Twilio...")
        messaging_system = TwilioMessagingSystem(
            sent_messages_file=sent_messages_file,
            mic_mapping_file=mic_mapping_file
        )
    except Exception as e:
        print(f"❌ Error initializing Twilio: {e}")
        print("\nMake sure you have set the following environment variables:")
        print("- TWILIO_ACCOUNT_SID")
        print("- TWILIO_AUTH_TOKEN")
        print("- TWILIO_PHONE_NUMBER")
        sys.exit(1)
    
    # Collect responses
    print("\n📥 Collecting responses...")
    responses = messaging_system.collect_responses()
    
    # Print status report
    messaging_system.print_status_report()
    
    if len(responses) > 0:
        print("\n✅ Responses collected and saved to: twilio_responses.json")
        print("\n💡 Next step: Run 'python process_responses.py' to organize the data")
    else:
        print("\n⚠️  No new responses found")
    
    print("=" * 70)


if __name__ == "__main__":
    main()

