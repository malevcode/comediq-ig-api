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
from datetime import datetime


class InstagramMessagingSystem:
    def __init__(self):
        """Initialize the Instagram messaging system."""
        load_dotenv()
        
        # Instagram credentials from environment variables
        self.username = os.getenv("IG_USER")
        self.password = os.getenv("IG_PASSWORD")
        
        if not all([self.username, self.password]):
            raise ValueError("Missing required Instagram environment variables. Please set IG_USER and IG_PASSWORD")
        
        # Initialize instagrapi client
        self.cl = Client()
        
        # Storage for tracking messages and responses
        self.sent_messages = {}
        self.received_responses = {}
        self.response_log_file = "dm_replies.json"
        self.sent_messages_file = "ig_sent_messages.json"
        
        # Login to Instagram
        self.login()
        
        # Load existing data
        self.load_responses()
        self.load_sent_messages()
    
    def login(self):
        """Login to Instagram with saved settings."""
        if os.path.exists("dump.json"):
            self.cl.load_settings("dump.json")
            self.cl.login(self.username, self.password)
        else:
            self.cl.login(self.username, self.password)
            self.cl.dump_settings('dump.json')
    
    def load_responses(self):
        """Load previously received responses from file."""
        try:
            if os.path.exists(self.response_log_file):
                with open(self.response_log_file, 'r') as f:
                    self.received_responses = json.load(f)
                print(f"Loaded {len(self.received_responses)} existing responses")
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
        """Save sent messages to file."""
        try:
            with open(self.sent_messages_file, 'w') as f:
                json.dump(self.sent_messages, f, indent=2)
        except Exception as e:
            print(f"Error saving sent messages: {e}")
    
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
        
        print(f"Sending message to {len(usernames)} usernames...")
        print(f"Message: {message}")
        print("-" * 50)
        
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
                    'sent_at': datetime.now().isoformat(),
                    'message': message
                }
                
                results[clean_username] = user_id
                print(f"✅ Sent to @{clean_username}: {user_id}")
                
                # Random delay between messages to avoid rate limiting
                time.sleep(random.uniform(5, 15))
                
            except UserNotFound:
                error_msg = f"User @{username} not found"
                results[username] = error_msg
                print(f"❌ {error_msg}")
            except TypeError:
                pass  # Skip invalid usernames
            except Exception as e:
                error_msg = f"Error sending to @{username}: {str(e)}"
                results[username] = error_msg
                print(f"❌ {error_msg}")
        
        # Save sent messages
        self.save_sent_messages()
        
        return results
    
    def send_messages_from_csv(self, csv_file: str, username_column: str, message: str) -> Dict[str, str]:
        """
        Send messages to usernames from a CSV file.
        
        Args:
            csv_file: Path to the CSV file
            username_column: Column name containing the usernames
            message: The message to send
            
        Returns:
            Dictionary mapping usernames to results
        """
        try:
            df = pd.read_csv(csv_file)[username_column].drop_duplicates()
            usernames = df.tolist()
            return self.send_message_to_usernames(usernames, message)
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return {}
    
    def parse_response(self, message_text: str) -> Optional[str]:
        """
        Parse structured Y/N/C responses from message text.
        
        Args:
            message_text: The text content of the received message
            
        Returns:
            Parsed response ('Y', 'N', 'C') or None if not recognized
        """
        text = message_text.strip().upper()
        
        # Look for Y/N/C patterns
        if any(word in text for word in ['YES', 'Y ', ' Y ', 'CONFIRM', 'ACTIVE', 'Y!', ' Y.']):
            return 'Y'
        elif any(word in text for word in ['NO', ' N ', ' N.', 'INACTIVE', 'NOT ACTIVE', 'N!']):
            return 'N'
        elif any(word in text for word in ['CHANGE', 'CHANGES', 'C ', ' C', 'UPDATED', 'MODIFIED']):
            return 'C'
        
        return None
    
    def collect_responses(self, amount: int = 100) -> Dict[str, List[str]]:
        """
        Collect responses from the usernames you sent messages to.
        Fetches DM threads and messages, matching them with sent messages.
        
        Args:
            amount: Number of threads to fetch
            
        Returns:
            Dictionary mapping usernames to list of their messages
        """
        print("🔍 Collecting responses...")
        print("-" * 50)
        
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
                    print(f"❌ No thread found for @{clean_username}")
                    continue
                
                # Fetch messages in that thread
                try:
                    messages = self.cl.direct_messages(thread.id, amount=20)
                    time.sleep(random.uniform(0.5, 1))
                except Exception as e:
                    print(f"Error fetching messages for @{clean_username}: {e}")
                    continue
                
                # Filter messages that are replies from the user (not from us)
                user_msgs = []
                for m in messages:
                    if m.user_id == user_id and m.text:
                        # Store with parsed response
                        parsed_response = self.parse_response(m.text)
                        msg_data = {
                            'message': m.text,
                            'parsed_response': parsed_response,
                            'timestamp': m.created_at.isoformat() if hasattr(m, 'created_at') else datetime.now().isoformat()
                        }
                        user_msgs.append(msg_data)
                
                if user_msgs:
                    self.received_responses[clean_username] = user_msgs
                    responses_found += len(user_msgs)
                    
                    # Log the response
                    latest = user_msgs[-1]
                    status_emoji = "✅" if latest.get('parsed_response') else "📱"
                    print(f"{status_emoji} @{clean_username}: {latest['message'][:60]}")
                
                # Gentle extra delay between users
                time.sleep(random.uniform(0.5, 1))
                
            except UserNotFound:
                print(f"User @{clean_username} not found")
                continue
            except Exception as e:
                print(f"Error processing @{clean_username}: {e}")
                continue
        
        # Save responses
        if responses_found > 0:
            self.save_responses()
            print(f"\n📥 Collected {responses_found} new response(s)")
        
        return self.received_responses
    
    def get_response_summary(self) -> Dict[str, int]:
        """Get a summary of received responses."""
        summary = {'Y': 0, 'N': 0, 'C': 0, 'unrecognized': 0}
        
        for username, messages in self.received_responses.items():
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

