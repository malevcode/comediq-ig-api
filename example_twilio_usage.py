"""
Example usage of the Twilio Messaging System
"""

from twilio_messaging import TwilioMessagingSystem


def example_send_messages():
    """Example of sending messages to phone numbers."""

    # Initialize the messaging system
    messaging_system = TwilioMessagingSystem()

    # List of phone numbers to send messages to
    phone_numbers = []

    # Your message
    message = """Hey, it's Adam from Comediq! I'm doing the monthly check in to update our monthly mic list, so please: 

Reply “Y” if your mic is active with no changes,
Reply “Changes” if there are any changes to your mic, or
Reply “N” if your mic is no longer happening

Thank you!"""

    # Send messages
    results = messaging_system.send_message_to_numbers(phone_numbers, message)

    # Print results
    print("Sending Results:")
    for phone, result in results.items():
        if result.startswith("SM"):
            print(f"✅ {phone}: Message sent successfully")
        else:
            print(f"❌ {phone}: {result}")

    # Print status report
    messaging_system.print_status_report()


def example_collect_responses():
    """Example of collecting responses from previously sent messages."""

    # Initialize the messaging system
    messaging_system = TwilioMessagingSystem()

    # Collect responses from incoming messages
    print("Collecting responses from incoming messages...")
    responses = messaging_system.collect_responses()

    # Print status report
    messaging_system.print_status_report()

    # Show detailed responses
    if responses:
        print("\n📱 Detailed Responses:")
        for phone, data in responses.items():
            response_type = data.get("parsed_response", "unrecognized")
            message = data.get("message", "")
            print(f"  {phone}: [{response_type}] {message}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "collect":
        example_collect_responses()
    else:
        example_send_messages()
