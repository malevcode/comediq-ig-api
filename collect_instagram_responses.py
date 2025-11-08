#!/usr/bin/env python3
"""
Collect responses from Instagram DMs and save them for processing.

This script fetches DM replies from Instagram and saves them in a structured format.
"""

from ig_messaging import InstagramMessagingSystem
import sys


def main():
    """Main execution function."""
    print("=" * 70)
    print("📥 COLLECTING INSTAGRAM RESPONSES")
    print("=" * 70)
    
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

