"""
Instagram Messaging System
Sends messages to a list of usernames and monitors responses for structured input using instagrapi.
"""

import pandas as pd
from instagrapi import Client
from instagrapi.exceptions import UserNotFound
from dotenv import load_dotenv
import os
import json
import time
import random
from typing import List, Dict, Optional
from datetime import datetime, timezone, timedelta


class InstagramMessagingSystem:
    def __init__(self, sent_messages_file: str = "ig_sent_messages.json", 
                 mic_mapping_file: str = "ig_mic_mapping.json"):
        """Initialize the Instagram messaging system."""
        load_dotenv()
        
        # Instagram credentials from environment variables
        self.username = os.getenv("IG_USER")
        self.password = os.getenv("IG_PASSWORD")
        
        if not all([self.username, self.password]):
            raise ValueError("Missing required Instagram environment variables. Please set IG_USER and IG_PASSWORD")
        
        # Initialize instagrapi client
        self.cl = Client()
        self.cl.challenge_code_handler = self.prompt_for_challenge_code
        self.cl.change_password_handler = self.prompt_for_new_password
        
        # Storage for tracking messages and responses
        self.sent_messages = {}
        self.received_responses = {}
        self.mic_identifier_mapping = {}  # Maps username to mic identifier
        self.response_log_file = "dm_replies.json"
        self.sent_messages_file = sent_messages_file
        self.mic_mapping_file = mic_mapping_file
        
        # Login to Instagram
        self.login()
        
        # Load existing data
        self.load_responses()
        self.load_sent_messages()
        self.load_mic_mapping()
    
    def login(self):
        """Login to Instagram with saved settings."""
        try:
            if os.path.exists("dump.json"):
                self.cl.load_settings("dump.json")

            self.cl.login(self.username, self.password)
            self.cl.dump_settings('dump.json')
        except Exception as e:
            message = str(e)
            if "legacy challenge flow" in message.lower():
                raise RuntimeError(
                    "Instagram is requiring a manual checkpoint. Open Instagram in a browser "
                    "or the mobile app, log into this account from the same network if possible, "
                    "complete the security check, then rerun this script. Keep dump.json so the "
                    "retry uses the same saved device settings."
                ) from e
            raise

    def prompt_for_challenge_code(self, username: str, choice=None):
        """Prompt for Instagram email/SMS security code during login."""
        destination = f" via {choice}" if choice else ""
        while True:
            code = input(f"Enter Instagram security code for {username}{destination}: ").strip()
            if code:
                return code

    def prompt_for_new_password(self, username: str):
        """Prompt for a new password if Instagram requires a password reset."""
        while True:
            password = input(f"Enter new Instagram password for {username}: ").strip()
            if password:
                return password
    
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
    
    def load_sent_messages(self):
        """Load previously sent messages from file."""
        try:
            if os.path.exists(self.sent_messages_file):
                with open(self.sent_messages_file, 'r') as f:
                    self.sent_messages = json.load(f)
        except Exception as e:
            print(f"Error loading sent messages: {e}")
            self.sent_messages = {}
    
    def save_sent_messages(self):
        """Save sent messages to file, merging with existing data."""
        try:
            # Load existing sent messages
            existing_messages = {}
            if os.path.exists(self.sent_messages_file):
                try:
                    with open(self.sent_messages_file, 'r') as f:
                        existing_messages = json.load(f)
                except Exception:
                    pass  # If file is corrupted, start fresh
            
            # Merge with current messages (current takes precedence)
            merged_messages = {**existing_messages, **self.sent_messages}
            
            # Save merged data
            with open(self.sent_messages_file, 'w') as f:
                json.dump(merged_messages, f, indent=2)
        except Exception as e:
            print(f"Error saving sent messages: {e}")
    
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
        """Save mic identifier mapping to file, merging with existing data."""
        try:
            # Load existing mic mapping
            existing_mapping = {}
            if os.path.exists(self.mic_mapping_file):
                try:
                    with open(self.mic_mapping_file, 'r') as f:
                        existing_mapping = json.load(f)
                except Exception:
                    pass  # If file is corrupted, start fresh
            
            # Merge with current mapping (current takes precedence)
            merged_mapping = {**existing_mapping, **self.mic_identifier_mapping}
            
            # Save merged data
            with open(self.mic_mapping_file, 'w') as f:
                json.dump(merged_mapping, f, indent=2)
        except Exception as e:
            print(f"Error saving mic mapping: {e}")
    
    def send_message_to_usernames(self, usernames: List[str], message: str) -> Dict[str, str]:
        """
        Send a message to a list of usernames.
        
        Args:
            usernames: List of Instagram usernames (with or without @)
            message: The message to send
            
        Returns:
            Dictionary mapping usernames to user IDs or error messages
        """
        results = {}
        
        # Removed verbose header prints
        
        for username in usernames:
            try:
                # Clean the username
                clean_username = username.strip("@").strip()
                
                # Send the message
                user_id = self.cl.user_id_from_username(clean_username)
                self.cl.direct_send(message, [user_id])
                
                # Store the message info
                self.sent_messages[clean_username] = {
                    'user_id': user_id,
                    'sent_at': datetime.now(timezone.utc).isoformat(),
                    'message': message
                }
                
                results[clean_username] = user_id
                # Removed individual success message
                
                # Random delay between messages to avoid rate limiting
                time.sleep(random.uniform(5, 15))
                
            except UserNotFound:
                error_msg = f"User @{username} not found"
                results[username] = error_msg
                # Removed individual error message
            except TypeError:
                pass  # Skip invalid usernames
            except Exception as e:
                error_msg = f"Error sending to @{username}: {str(e)}"
                results[username] = error_msg
                # Removed individual error message
        
        # Save sent messages
        self.save_sent_messages()
        
        return results
    
    def send_messages_from_csv(self, csv_file: str, username_column: str, message: str, 
                              identifier_column: str = "unique_identifier") -> Dict[str, str]:
        """
        Send messages to usernames from a CSV file and store mic identifier mapping.
        
        Args:
            csv_file: Path to the CSV file
            username_column: Column name containing the usernames
            message: The message to send
            identifier_column: Column name containing the mic identifiers
            
        Returns:
            Dictionary mapping usernames to results
        """
        try:
            df = pd.read_csv(csv_file)
            
            # Create mapping of usernames to ALL their mic identifiers (multiple mics per user)
            username_to_mics = {}
            for _, row in df.iterrows():
                username = str(row[username_column]).strip().lstrip('@')
                mic_id = row[identifier_column]
                
                if username not in username_to_mics:
                    username_to_mics[username] = []
                username_to_mics[username].append(mic_id)
            
            # Get unique usernames to send to
            usernames = list(username_to_mics.keys())
            
            # Store mic identifier mapping (username -> list of mic IDs)
            self.mic_identifier_mapping = getattr(self, 'mic_identifier_mapping', {})
            for username, mic_ids in username_to_mics.items():
                self.mic_identifier_mapping[username] = mic_ids
            
            # Save mapping
            self.save_mic_mapping()
            
            return self.send_message_to_usernames(usernames, message)
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
        # Check for exact 'Y' first, then other patterns
        if text == 'Y' or any(word in text for word in ['YES', 'Y ', ' Y ', 'CONFIRM', 'ACTIVE', 'Y!', ' Y.', ' Y\n', '\nY']):
            return 'Y'
        elif text == 'N' or any(word in text for word in ['NO', ' N ', ' N.', 'INACTIVE', 'NOT ACTIVE', 'N!', ' N\n', '\nN']):
            return 'N'
        elif text == 'C' or any(word in text for word in ['CHANGE', 'CHANGES', 'C ', ' C', 'UPDATED', 'MODIFIED', ' C\n', '\nC']):
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
    
    def collect_responses(self, amount: int = 100) -> Dict[str, List[str]]:
        """
        Collect responses from the usernames you sent messages to.
        Fetches DM threads and messages, matching them with sent messages.
        
        Args:
            amount: Number of threads to fetch
            
        Returns:
            Dictionary mapping usernames to list of their messages
        """
        # Removed verbose header prints
        
        # Fetch DM threads
        try:
            threads = self.cl.direct_threads(amount=amount)
            time.sleep(random.uniform(0.5, 1))
        except Exception as e:
            print(f"Error fetching threads: {e}")
            return {}
        
        responses_found = 0
        
        # Iterate through sent usernames and find their threads
        for username in self.sent_messages.keys():
            try:
                clean_username = username.strip("@").strip()
                
                # Get user ID
                user_id = self.cl.user_id_from_username(clean_username)
                time.sleep(random.uniform(0.5, 1))
                
                # Find a thread that includes this user
                thread = next(
                    (t for t in threads if user_id in [u.pk for u in t.users]),
                    None
                )
                
                if not thread:
                    # Removed individual error message
                    continue
                
                # Fetch messages in that thread
                try:
                    messages = self.cl.direct_messages(thread.id, amount=20)
                    time.sleep(random.uniform(0.5, 1))
                except Exception as e:
                    # Removed individual error message
                    continue
                
                # Get when we sent our message to this user
                sent_info = self.sent_messages.get(clean_username, {})
                sent_at_str = sent_info.get('sent_at')
                
                sent_at_time = None
                if sent_at_str:
                    try:
                        # Parse our sent_at timestamp (should be UTC)
                        sent_at_time = datetime.fromisoformat(sent_at_str)
                        if sent_at_time.tzinfo is None:
                            sent_at_time = sent_at_time.replace(tzinfo=timezone.utc)
                    except:
                        pass
                
                # Filter messages that are replies from the user (not from us) AND after our sent message
                user_msgs = []
                for m in messages:
                    if m.user_id == user_id and m.text:
                        # Check if message was sent after our outbound message
                        # instagrapi uses 'timestamp' attribute, not 'created_at'
                        message_time = getattr(m, 'timestamp', None)
                        
                        # Convert message timestamp to UTC for proper comparison
                        if message_time:
                            try:
                                # If message_time has no timezone info, it's local time - convert to UTC
                                if message_time.tzinfo is None:
                                    # Treat as local time and convert to UTC
                                    local_timezone = timezone(timedelta(seconds=-time.timezone))
                                    message_time = message_time.replace(tzinfo=local_timezone).astimezone(timezone.utc)
                                else:
                                    # Convert to UTC if it has timezone info
                                    message_time = message_time.astimezone(timezone.utc)
                            except:
                                # If conversion fails, skip timezone comparison
                                message_time = None
                        # Only collect messages sent AFTER our outbound message
                        if sent_at_time and message_time and message_time <= sent_at_time:
                            continue  # Skip messages from before our outbound message
                        
                        # Store with parsed response (both simple and numbered)
                        parsed_response = self.parse_response(m.text)
                        numbered_responses = self.parse_numbered_responses(m.text)
                        
                        msg_data = {
                            'message': m.text,
                            'parsed_response': parsed_response,
                            'numbered_responses': numbered_responses if numbered_responses else None,
                            'timestamp': message_time.isoformat() if message_time else datetime.now(timezone.utc).isoformat()
                        }
                        user_msgs.append(msg_data)
                
                if user_msgs:
                    # Instagram API should return messages in chronological order
                    # Trust the natural order rather than potentially incorrect timestamps
                    
                    # Get mic identifiers for this username (can be multiple)
                    mic_identifiers = self.mic_identifier_mapping.get(clean_username, [])
                    if not isinstance(mic_identifiers, list):
                        mic_identifiers = [mic_identifiers] if mic_identifiers else []
                    
                    self.received_responses[clean_username] = {
                        'messages': user_msgs,
                        'mic_identifiers': mic_identifiers  # List of mic IDs
                    }
                    responses_found += len(user_msgs)
                    
                    # Log the response - Instagram returns messages newest-to-oldest
                    latest = user_msgs[0]  # Most recent is first in array
                    status_emoji = "✅" if latest.get('parsed_response') else "📱"
                    mic_count = len(mic_identifiers) if mic_identifiers else 0
                    mic_info = f" ({mic_count} mics)" if mic_count > 0 else ""
                    print(f"{status_emoji} @{clean_username}{mic_info}: {latest['message'][:40]}...")
                    
                # Gentle extra delay between users
                time.sleep(random.uniform(0.5, 1))
                
            except UserNotFound:
                # Removed individual error message
                continue
            except Exception as e:
                # Removed individual error message
                continue
        
        # Save responses
        if responses_found > 0:
            self.save_responses()
            print(f"📥 Collected {responses_found} new response(s)")
        
        return self.received_responses
    
    def get_response_summary(self) -> Dict[str, int]:
        """Get a summary of received responses."""
        summary = {'Y': 0, 'N': 0, 'C': 0, 'unrecognized': 0}
        
        for username, response_data in self.received_responses.items():
            # Handle both old and new format
            messages = response_data.get('messages', response_data) if isinstance(response_data, dict) else response_data
            if not isinstance(messages, list):
                messages = [messages]
                
            for msg in messages:
                response = msg.get('parsed_response')
                if response in summary:
                    summary[response] += 1
                else:
                    summary['unrecognized'] += 1
        
        return summary
    
    def print_status_report(self):
        """Print a status report of sent messages and received responses."""
        print("\n" + "="*60)
        print("📊 INSTAGRAM MESSAGING STATUS REPORT")
        print("="*60)
        
        print(f"📤 Messages sent: {len(self.sent_messages)}")
        
        # Count unique users who responded
        unique_responses = len(self.received_responses)
        total_messages = sum(len(msgs) for msgs in self.received_responses.values())
        
        print(f"📥 Users who responded: {unique_responses}")
        print(f"📨 Total response messages: {total_messages}")
        
        if self.received_responses:
            summary = self.get_response_summary()
            print(f"\n📈 Response breakdown:")
            print(f"   ✅ Yes/Active (Y): {summary['Y']}")
            print(f"   ❌ No/Inactive (N): {summary['N']}")
            print(f"   📝 Changes (C): {summary['C']}")
            print(f"   🤔 Unrecognized: {summary['unrecognized']}")
        
        print("="*60)


def main():
    """Main function to demonstrate usage."""
    import sys
    
    try:
        # Initialize the messaging system
        messaging_system = InstagramMessagingSystem()
        
        # Check command line arguments
        if len(sys.argv) > 1 and sys.argv[1] == "collect":
            # If "collect" argument is passed, just collect responses
            print("📥 Collecting responses...")
            responses = messaging_system.collect_responses()
            messaging_system.print_status_report()
            
            # Optionally export to CSV
            if len(responses) > 0 and input("\n📄 Export responses to CSV? (y/n): ").lower() == 'y':
                data = []
                for username, messages in responses.items():
                    for msg in messages:
                        data.append({
                            'username': username,
                            'message': msg.get('message', ''),
                            'parsed': msg.get('parsed_response', ''),
                            'timestamp': msg.get('timestamp', '')
                        })
                df = pd.DataFrame(data)
                df.to_csv('ig_responses.csv', index=False)
                print("✅ Exported to ig_responses.csv")
            
            return
        
        # Example usage with CSV file
        csv_file = "active_to_confirm_NY.csv"
        username_column = "changes_updates"
        
        # Check if CSV file exists
        if not os.path.exists(csv_file):
            print(f"❌ CSV file '{csv_file}' not found.")
            print("\nExample usage:")
            print("  python ig_messaging.py  # Send messages from CSV")
            print("  python ig_messaging.py collect  # Collect responses")
            return
        
        # Example message
        message = """Yo I'm doing a monthly verification of every open mic on my platform! 
Can you confirm that your mic is active and lmk about any changes?"""
        
        # Send messages from CSV
        results = messaging_system.send_messages_from_csv(csv_file, username_column, message)
        
        # Print results
        print("\n📤 Sending Results:")
        for username, result in results.items():
            if result.startswith('0') or result.startswith('1'):  # User ID starts with number
                print(f"✅ @{username}: Message sent successfully")
            else:
                print(f"❌ @{username}: {result}")
        
        # Print status report
        messaging_system.print_status_report()
        
        print("\n" + "="*60)
        print("💡 HOW TO COLLECT RESPONSES LATER")
        print("="*60)
        print("To collect responses at any time, run:")
        print("   python ig_messaging.py collect")
        print("\nThis will fetch DM replies from the usernames you sent")
        print("messages to and parse Y/N/C responses.")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have set the following environment variables:")
        print("- IG_USER")
        print("- IG_PASSWORD")


if __name__ == "__main__":
    main()
