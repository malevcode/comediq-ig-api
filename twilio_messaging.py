"""
Twilio Messaging System
Sends messages to a list of phone numbers and monitors responses for Y/N/C structured input.
"""

import os
import json
import time
import random
from typing import List, Dict, Optional
from datetime import datetime
from dotenv import load_dotenv
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

# Load environment variables
load_dotenv()

class TwilioMessagingSystem:
    def __init__(self):
        """Initialize the Twilio messaging system."""
        # Twilio credentials from environment variables
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER')  # Your Twilio phone number
        
        if not all([self.account_sid, self.auth_token, self.from_number]):
            raise ValueError("Missing required Twilio environment variables. Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER")
        
        # Initialize Twilio client
        self.client = Client(self.account_sid, self.auth_token)
        
        # Storage for tracking messages and responses
        self.sent_messages = {}
        self.received_responses = {}
        self.mic_identifier_mapping = {}  # Maps phone number to mic identifier
        self.response_log_file = "twilio_responses.json"
        self.mic_mapping_file = "twilio_mic_mapping.json"
        
        # Load existing responses if file exists
        self.load_responses()
        self.load_mic_mapping()
    
    def load_responses(self):
        """Load previously received responses from file."""
        try:
            if os.path.exists(self.response_log_file):
                with open(self.response_log_file, 'r') as f:
                    self.received_responses = json.load(f)
                # Removed verbose loading message
        except Exception as e:
            print(f"Error loading responses: {e}")
            self.received_responses = {}
    
    def save_responses(self):
        """Save responses to file."""
        try:
            with open(self.response_log_file, 'w') as f:
                json.dump(self.received_responses, f, indent=2)
        except Exception as e:
            print(f"Error saving responses: {e}")
    
    def load_mic_mapping(self):
        """Load mic identifier mapping from file."""
        try:
            if os.path.exists(self.mic_mapping_file):
                with open(self.mic_mapping_file, 'r') as f:
                    self.mic_identifier_mapping = json.load(f)
        except Exception as e:
            print(f"Error loading mic mapping: {e}")
            self.mic_identifier_mapping = {}
    
    def save_mic_mapping(self):
        """Save mic identifier mapping to file."""
        try:
            with open(self.mic_mapping_file, 'w') as f:
                json.dump(self.mic_identifier_mapping, f, indent=2)
        except Exception as e:
            print(f"Error saving mic mapping: {e}")
    
    def send_message_to_numbers(self, phone_numbers: List[str], message: str) -> Dict[str, str]:
        """
        Send a message to a list of phone numbers.
        
        Args:
            phone_numbers: List of phone numbers in E.164 format (e.g., +1234567890)
            message: The message to send
            
        Returns:
            Dictionary mapping phone numbers to message SIDs or error messages
        """
        results = {}
        
        # Removed verbose header prints
        
        for phone_number in phone_numbers:
            try:
                # Format phone number if needed
                if not phone_number.startswith('+'):
                    phone_number = '+' + phone_number.lstrip('+')
                
                # Send the message
                message_obj = self.client.messages.create(
                    body=message,
                    from_=self.from_number,
                    to=phone_number
                )
                
                # Store the message info
                self.sent_messages[phone_number] = {
                    'sid': message_obj.sid,
                    'status': message_obj.status,
                    'sent_at': datetime.now().isoformat(),
                    'message': message
                }
                
                results[phone_number] = message_obj.sid
                # Removed individual success message
                
                # Random delay between messages to avoid rate limiting
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                error_msg = f"Error sending to {phone_number}: {str(e)}"
                results[phone_number] = error_msg
                # Removed individual error message
        
        # Save sent messages
        self.save_sent_messages()
        
        return results
    
    def save_sent_messages(self):
        """Save sent messages to file."""
        try:
            with open("twilio_sent_messages.json", 'w') as f:
                json.dump(self.sent_messages, f, indent=2)
        except Exception as e:
            print(f"Error saving sent messages: {e}")
    
    def send_messages_from_csv(self, csv_file: str, phone_column: str, message: str, 
                              identifier_column: str = "unique_identifier") -> Dict[str, str]:
        """
        Send messages to phone numbers from a CSV file and store mic identifier mapping.
        
        Args:
            csv_file: Path to the CSV file
            phone_column: Column name containing the phone numbers
            message: The message to send
            identifier_column: Column name containing the mic identifiers
            
        Returns:
            Dictionary mapping phone numbers to results
        """
        try:
            import pandas as pd
            df = pd.read_csv(csv_file)
            
            # Create mapping of phone numbers to ALL their mic identifiers (multiple mics per phone)
            phone_to_mics = {}
            for _, row in df.iterrows():
                phone = str(row[phone_column]).strip()
                mic_id = row[identifier_column]
                
                # Format phone number consistently
                formatted_phone = phone if phone.startswith('+') else '+' + phone.lstrip('+')
                
                if formatted_phone not in phone_to_mics:
                    phone_to_mics[formatted_phone] = []
                phone_to_mics[formatted_phone].append(mic_id)
            
            # Get unique phone numbers to send to
            phone_numbers = list(phone_to_mics.keys())
            
            # Store mic identifier mapping (phone -> list of mic IDs)
            for phone, mic_ids in phone_to_mics.items():
                self.mic_identifier_mapping[phone] = mic_ids
            
            # Save mapping
            self.save_mic_mapping()
            
            return self.send_message_to_numbers(phone_numbers, message)
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return {}
    
    def parse_response(self, message_text: str) -> Optional[str]:
        """
        Parse structured Y/N/C responses from message text.
        Handles both simple responses and numbered format (e.g., "1 Y", "2 N").
        
        Args:
            message_text: The text content of the received message
            
        Returns:
            Parsed response ('Y', 'N', 'C') or None if not recognized
        """
        text = message_text.strip().upper()
        
        # Look for Y/N/C patterns
        if any(word in text for word in ['YES', 'Y ', ' Y ', ' Y\n', '\nY', 'CONFIRM', 'ACTIVE', 'Y!', ' Y.']):
            return 'Y'
        elif any(word in text for word in ['NO', ' N ', ' N\n', '\nN', 'INACTIVE', 'NOT ACTIVE', 'N!', ' N.']):
            return 'N'
        elif any(word in text for word in ['CHANGE', 'CHANGES', 'C ', ' C', ' C\n', '\nC', 'UPDATED', 'MODIFIED']):
            return 'C'
        
        return None
    
    def parse_numbered_responses(self, message_text: str) -> Dict[int, str]:
        """
        Parse numbered responses from message text.
        Handles format like "1 Y" or "2 N" or "3 Changes".
        
        Args:
            message_text: The text content of the received message
            
        Returns:
            Dictionary mapping mic numbers to status ('Y', 'N', 'C')
        """
        results = {}
        lines = message_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for pattern: number followed by Y/N/C/Changes
            import re
            match = re.match(r'^(\d+)\s+(Y|N|C|YES|NO|CHANGES?|ACTIVE|INACTIVE)', line.upper())
            if match:
                mic_num = int(match.group(1))
                status = match.group(2)
                
                # Normalize status
                if status in ['Y', 'YES', 'ACTIVE']:
                    results[mic_num] = 'Y'
                elif status in ['N', 'NO', 'INACTIVE']:
                    results[mic_num] = 'N'
                elif status in ['C', 'CHANGES', 'CHANGE']:
                    results[mic_num] = 'C'
        
        return results
    
    def process_incoming_message(self, from_number: str, message_text: str) -> str:
        """
        Process an incoming message and return a response.
        
        Args:
            from_number: The phone number the message came from
            message_text: The text content of the message
            
        Returns:
            TwiML response string
        """
        # Parse the response
        parsed_response = self.parse_response(message_text)
        
        # Store the response
        timestamp = datetime.now().isoformat()
        self.received_responses[from_number] = {
            'message': message_text,
            'parsed_response': parsed_response,
            'timestamp': timestamp,
            'raw_response': message_text
        }
        
        # Save responses
        self.save_responses()
        
        # Log the response (only show parsed responses)
        if parsed_response:
            print(f"📱 {from_number}: {parsed_response}")
        
        # Create TwiML response
        response = MessagingResponse()
        
        if parsed_response == 'Y':
            response.message("✅ Confirmed! Your mic is marked as active.")
        elif parsed_response == 'N':
            response.message("❌ Noted. Your mic will be marked as inactive.")
        elif parsed_response == 'C':
            response.message("📝 Thanks for the update! Please provide details about the changes.")
        else:
            response.message("🤔 I didn't understand that. Please respond with Y (yes/active), N (no/inactive), or C (changes/updates).")
        
        return str(response)
    
    def get_response_summary(self) -> Dict[str, int]:
        """Get a summary of received responses."""
        summary = {'Y': 0, 'N': 0, 'C': 0, 'unrecognized': 0}
        
        for phone_number, data in self.received_responses.items():
            response = data.get('parsed_response')
            if response in summary:
                summary[response] += 1
            else:
                summary['unrecognized'] += 1
        
        return summary
    
    def fetch_incoming_messages(self, limit: int = 50) -> List:
        """
        Fetch incoming messages from Twilio.
        
        Args:
            limit: Maximum number of messages to fetch
            
        Returns:
            List of incoming message objects
        """
        try:
            messages = self.client.messages.list(
                to=self.from_number,  # Messages received by our Twilio number
                limit=limit
            )
            return messages
        except Exception as e:
            print(f"Error fetching messages: {e}")
            return []
    
    def collect_responses(self, check_since: Optional[datetime] = None) -> Dict[str, Dict]:
        """
        Collect responses from the phone numbers you sent messages to.
        Fetches incoming messages and matches them with sent messages.
        
        Args:
            check_since: Only check messages after this timestamp
            
        Returns:
            Dictionary mapping phone numbers to response data
        """
        # Removed verbose header prints
        
        # Fetch incoming messages
        incoming_messages = self.fetch_incoming_messages(limit=100)
        
        responses_found = 0
        
        for message in incoming_messages:
            try:
                # Get the sender's phone number
                from_number = message.from_
                
                # Check if this is from someone we sent a message to
                if from_number in self.sent_messages:
                    message_text = message.body
                    message_date = message.date_created
                    
                    # Skip if we already have a newer response from this number
                    if from_number in self.received_responses:
                        existing_time = self.received_responses[from_number].get('timestamp')
                        if existing_time and datetime.fromisoformat(existing_time) > message_date:
                            continue
                    
                    # Parse the response (both simple and numbered)
                    parsed_response = self.parse_response(message_text)
                    numbered_responses = self.parse_numbered_responses(message_text)
                    
                    # Get mic identifiers for this phone number (can be multiple)
                    mic_identifiers = self.mic_identifier_mapping.get(from_number, [])
                    if not isinstance(mic_identifiers, list):
                        mic_identifiers = [mic_identifiers] if mic_identifiers else []
                    
                    # Store the response
                    self.received_responses[from_number] = {
                        'message': message_text,
                        'parsed_response': parsed_response,
                        'numbered_responses': numbered_responses if numbered_responses else None,
                        'timestamp': message_date.isoformat(),
                        'raw_response': message_text,
                        'message_sid': message.sid,
                        'mic_identifiers': mic_identifiers  # List of mic IDs
                    }
                    
                    responses_found += 1
                    
                    # Log the response (only for successful responses with mic IDs)
                    mic_count = len(mic_identifiers) if mic_identifiers else 0
                    if mic_count > 0:
                        status_emoji = "✅" if parsed_response else "🤔"
                        print(f"{status_emoji} {from_number} ({mic_count} mics): {message_text[:30]}...")
                    
            except Exception as e:
                # Removed individual error message
                continue
        
        # Save responses
        if responses_found > 0:
            self.save_responses()
            print(f"📥 Collected {responses_found} new response(s)")
        
        return self.received_responses
    
    def print_status_report(self):
        """Print a status report of sent messages and received responses."""
        print("\n" + "="*60)
        print("📊 TWILIO MESSAGING STATUS REPORT")
        print("="*60)
        
        print(f"📤 Messages sent: {len(self.sent_messages)}")
        print(f"📥 Responses received: {len(self.received_responses)}")
        
        if self.received_responses:
            summary = self.get_response_summary()
            print(f"\n📈 Response breakdown:")
            print(f"   ✅ Yes/Active (Y): {summary['Y']}")
            print(f"   ❌ No/Inactive (N): {summary['N']}")
            print(f"   📝 Changes (C): {summary['C']}")
            print(f"   🤔 Unrecognized: {summary['unrecognized']}")
        
        print("="*60)


def create_webhook_handler():
    """
    Create a Flask webhook handler for receiving Twilio webhooks.
    This function should be used to create a webhook endpoint.
    """
    from flask import Flask, request
    
    app = Flask(__name__)
    messaging_system = TwilioMessagingSystem()
    
    @app.route('/webhook/sms', methods=['POST'])
    def handle_sms():
        """Handle incoming SMS webhook from Twilio."""
        from_number = request.form.get('From')
        message_text = request.form.get('Body', '')
        
        if from_number and message_text:
            response = messaging_system.process_incoming_message(from_number, message_text)
            return response
        
        return "OK"
    
    return app


def main():
    """Main function to demonstrate usage."""
    import sys
    
    try:
        # Initialize the messaging system
        messaging_system = TwilioMessagingSystem()
        
        # Check command line arguments
        if len(sys.argv) > 1 and sys.argv[1] == "collect":
            # If "collect" argument is passed, just collect responses
            print("📥 Collecting responses...")
            responses = messaging_system.collect_responses()
            messaging_system.print_status_report()
            
            # Optionally export to CSV
            if len(responses) > 0 and input("\n📄 Export responses to CSV? (y/n): ").lower() == 'y':
                import pandas as pd
                data = []
                for phone, response_data in responses.items():
                    data.append({
                        'phone_number': phone,
                        'response': response_data.get('message', ''),
                        'parsed': response_data.get('parsed_response', ''),
                        'timestamp': response_data.get('timestamp', '')
                    })
                df = pd.DataFrame(data)
                df.to_csv('twilio_responses.csv', index=False)
                print("✅ Exported to twilio_responses.csv")
            
            return
        
        # Example phone numbers (replace with your actual numbers)
        phone_numbers = [
            "+1234567890",  # Replace with actual phone numbers
            "+1987654321",
            "+1555123456"
        ]
        
        # Example message
        message = """Hi! This is a verification message for your open mic listing. 
        
Please respond with:
• Y - if your mic is still active
• N - if your mic is no longer active  
• C - if you have changes/updates to report

Thank you!"""
        
        # Send messages
        results = messaging_system.send_message_to_numbers(phone_numbers, message)
        
        # Print results
        print("\n📤 Sending Results:")
        for phone, result in results.items():
            if result.startswith('SM'):
                print(f"✅ {phone}: Message sent successfully")
            else:
                print(f"❌ {phone}: {result}")
        
        # Print status report
        messaging_system.print_status_report()
        
        print("\n" + "="*60)
        print("💡 HOW TO COLLECT RESPONSES LATER")
        print("="*60)
        print("To collect responses at any time, run:")
        print("   python twilio_messaging.py collect")
        print("\nThis will fetch all incoming messages from the numbers you")
        print("sent messages to and parse Y/N/C responses.")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have set the following environment variables:")
        print("- TWILIO_ACCOUNT_SID")
        print("- TWILIO_AUTH_TOKEN") 
        print("- TWILIO_PHONE_NUMBER")


if __name__ == "__main__":
    main()
