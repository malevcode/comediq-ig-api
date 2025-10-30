from ig_messaging import InstagramMessagingSystem
import pandas as pd

# Initialize the messaging system
messaging_system = InstagramMessagingSystem()

# Collect responses from people you sent messages to
print("📥 Collecting responses from Instagram DMs...")
responses = messaging_system.collect_responses()

# Print status report
messaging_system.print_status_report()

# Optionally export to CSV
if len(responses) > 0:
    print("\n💡 Tip: You can export these responses to CSV for easier analysis.")
    print("The responses are saved in: dm_replies.json")
