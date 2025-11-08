#!/usr/bin/env python3
"""
Collect responses from SMS messages and save them for processing.

This script fetches incoming SMS replies from Twilio and saves them in a structured format.
"""

from twilio_messaging import TwilioMessagingSystem
import sys


def main():
    """Main execution function."""
    print("=" * 70)
    print("📥 COLLECTING SMS RESPONSES")
    print("=" * 70)
    
    # Initialize messaging system
    try:
        print("\n🔐 Initializing Twilio...")
        messaging_system = TwilioMessagingSystem()
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

