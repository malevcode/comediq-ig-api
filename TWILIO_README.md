# Twilio Messaging System

A Python script for sending SMS messages to multiple phone numbers using Twilio and monitoring structured responses (Y/N/C).

## Features

- Send messages to multiple phone numbers
- Monitor responses with structured Y/N/C parsing
- Webhook support for real-time response handling
- Response logging and status reporting
- Rate limiting and error handling

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file with your Twilio credentials:

```env
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

### 3. Twilio Setup

1. Sign up for a Twilio account
2. Get a phone number from Twilio
3. Note your Account SID and Auth Token from the Twilio Console

## Usage

### Basic Message Sending

```python
from twilio_messaging import TwilioMessagingSystem

# Initialize the system
messaging_system = TwilioMessagingSystem()

# List of phone numbers (in E.164 format)
phone_numbers = [
    "+1234567890",
    "+1987654321",
    "+1555123456"
]

# Your message
message = """Hi! This is a verification message for your open mic listing. 

Please respond with:
• Y - if your mic is still active
• N - if your mic is no longer active  
• C - if you have changes/updates to report

Thank you!"""

# Send messages
results = messaging_system.send_message_to_numbers(phone_numbers, message)

# Print status report
messaging_system.print_status_report()
```

### Running the Example

```bash
python example_twilio_usage.py
```

### Collecting Responses

After sending messages, you can collect responses at any time using Twilio's API:

```python
from twilio_messaging import TwilioMessagingSystem

messaging_system = TwilioMessagingSystem()
responses = messaging_system.collect_responses()
messaging_system.print_status_report()
```

Or run from command line:
```bash
python twilio_messaging.py collect
```

This will:
1. Fetch all incoming messages from your Twilio phone number
2. Match them with the numbers you sent messages to
3. Parse structured Y/N/C responses
4. Save responses to `twilio_responses.json`
5. Display a status report

## Response Parsing

The system automatically parses responses for structured input:

- **Y/Yes/Confirm/Active** → Parsed as 'Y'
- **N/No/Inactive/Not Active** → Parsed as 'N'  
- **C/Change/Updated/Modified** → Parsed as 'C'
- **Other responses** → Marked as unrecognized

## File Outputs

- `twilio_sent_messages.json` - Log of all sent messages
- `twilio_responses.json` - Log of all received responses
- Console output with real-time status updates

## Error Handling

- Rate limiting with random delays between messages
- Phone number validation and formatting
- Comprehensive error logging
- Graceful handling of Twilio API errors

## Security Notes

- Never commit your `.env` file to version control
- Use environment variables for all sensitive credentials
- Consider using Twilio's webhook signature validation for production

## Troubleshooting

### Common Issues

1. **"Missing required Twilio environment variables"**
   - Make sure your `.env` file is properly configured
   - Check that all three required variables are set

2. **"Error sending to +1234567890: [HTTP 400]"**
   - Verify the phone number is in E.164 format (+1234567890)
   - Check that the phone number is valid
   - Ensure your Twilio account has sufficient credits

3. **No responses collected**
   - Make sure enough time has passed for people to respond
   - Run `python twilio_messaging.py collect` to fetch responses
   - Check that your Twilio phone number is properly configured

### Rate Limits

Twilio has rate limits for SMS sending. The script includes random delays between messages to help avoid hitting these limits. For high-volume sending, consider:

- Using Twilio's Messaging Services
- Implementing exponential backoff
- Monitoring your Twilio account usage
