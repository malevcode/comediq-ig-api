#!/usr/bin/env python3
"""
Collect responses from Instagram DMs and save them for processing.

This script fetches DM replies from Instagram and saves them in a structured format.
"""

from ig_messaging import InstagramMessagingSystem
import sys


def main():
    """Main execution function."""
    # Get file paths from command line arguments or use defaults
    sent_messages_file = sys.argv[1] if len(sys.argv) > 1 else "ig_sent_messages.json"
    mic_mapping_file = sys.argv[2] if len(sys.argv) > 2 else "ig_mic_mapping.json"
    
    print("=" * 70)
    print("📥 COLLECTING INSTAGRAM RESPONSES")
    print("=" * 70)
    print(f"📁 Using sent messages file: {sent_messages_file}")
    print(f"📁 Using mic mapping file: {mic_mapping_file}")
    
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
    responses = messaging_system.collect_responses()
    
    # Print status report
    messaging_system.print_status_report()
    
    if len(responses) > 0:
        print("\n✅ Responses collected and saved to: dm_replies.json")
        print("\n💡 Next step: Run 'python process_responses.py' to organize the data")
    else:
        print("\n⚠️  No new responses found")
    
    print("=" * 70)


if __name__ == "__main__":
    main()

