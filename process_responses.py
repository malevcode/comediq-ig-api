#!/usr/bin/env python3
"""
Process and organize collected responses into a structured JSON format.

This script reads collected responses from Instagram and SMS, processes them,
and outputs an organized JSON file that can be used to update database tables.
"""

import json
import os
import sys
from typing import Dict, List, Any
from datetime import datetime
import pandas as pd


def load_instagram_responses(file_path: str = "dm_replies.json") -> Dict[str, Any]:
    """
    Load Instagram responses from JSON file.
    
    Args:
        file_path: Path to the responses file
        
    Returns:
        Dictionary of responses
    """
    if not os.path.exists(file_path):
        print(f"⚠️  Instagram responses file not found: {file_path}")
        return {}
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading Instagram responses: {e}")
        return {}


def load_sms_responses(file_path: str = "twilio_responses.json") -> Dict[str, Any]:
    """
    Load SMS responses from JSON file.
    
    Args:
        file_path: Path to the responses file
        
    Returns:
        Dictionary of responses
    """
    if not os.path.exists(file_path):
        print(f"⚠️  SMS responses file not found: {file_path}")
        return {}
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading SMS responses: {e}")
        return {}


def load_sent_messages(ig_file: str = "ig_sent_messages.json", 
                       sms_file: str = "twilio_sent_messages.json",
                       ig_mapping_file: str = "ig_mic_mapping.json",
                       sms_mapping_file: str = "twilio_mic_mapping.json") -> Dict[str, Dict]:
    """
    Load sent messages and mic mappings to map responses back to mic data.
    
    Args:
        ig_file: Instagram sent messages file
        sms_file: SMS sent messages file
        ig_mapping_file: Instagram mic mapping file
        sms_mapping_file: SMS mic mapping file
        
    Returns:
        Combined dictionary of sent messages with mic mappings
    """
    sent_messages = {}
    
    # Load Instagram sent messages
    if os.path.exists(ig_file):
        try:
            with open(ig_file, 'r') as f:
                ig_sent = json.load(f)
                sent_messages.update({f"ig_{k}": v for k, v in ig_sent.items()})
        except Exception as e:
            print(f"⚠️  Error loading Instagram sent messages: {e}")
    
    # Load SMS sent messages
    if os.path.exists(sms_file):
        try:
            with open(sms_file, 'r') as f:
                sms_sent = json.load(f)
                sent_messages.update({f"sms_{k}": v for k, v in sms_sent.items()})
        except Exception as e:
            print(f"⚠️  Error loading SMS sent messages: {e}")
    
    # Load Instagram mic mapping
    if os.path.exists(ig_mapping_file):
        try:
            with open(ig_mapping_file, 'r') as f:
                ig_mapping = json.load(f)
                # Add mic mappings to sent messages
                for username, mic_id in ig_mapping.items():
                    key = f"ig_{username}"
                    if key in sent_messages:
                        sent_messages[key]['mic_identifier'] = mic_id
        except Exception as e:
            print(f"⚠️  Error loading Instagram mic mapping: {e}")
    
    # Load SMS mic mapping
    if os.path.exists(sms_mapping_file):
        try:
            with open(sms_mapping_file, 'r') as f:
                sms_mapping = json.load(f)
                # Add mic mappings to sent messages
                for phone, mic_id in sms_mapping.items():
                    key = f"sms_{phone}"
                    if key in sent_messages:
                        sent_messages[key]['mic_identifier'] = mic_id
        except Exception as e:
            print(f"⚠️  Error loading SMS mic mapping: {e}")
    
    return sent_messages


def parse_response_content(response_data: Any, response_type: str) -> Dict[str, Any]:
    """
    Parse response content to extract key information and map numbered responses to specific mics.
    
    Args:
        response_data: Response data structure (varies by type)
        response_type: Type of response ('ig' or 'sms')
        
    Returns:
        Parsed response dictionary with individual mic statuses
    """
    parsed = {
        'mic_statuses': {},  # mic_position -> True/False/None
        'response_type': None,
        'raw_message': '',
        'timestamp': '',
        'mic_identifiers': [],
        'recognition_status': 'unrecognized'
    }
    
    try:
        if response_type == 'ig':
            # Instagram response format (new structure with mic_identifiers)
            if isinstance(response_data, dict) and 'messages' in response_data:
                # New format with mic identifiers list
                messages = response_data['messages']
                parsed['mic_identifiers'] = response_data.get('mic_identifiers', [])
                
                if messages:
                    # Instagram API returns messages in newest-to-oldest order
                    # So the first message [0] is the most recent
                    latest = messages[0] if isinstance(messages, list) else messages
                    
                    parsed['response_type'] = latest.get('parsed_response')
                    parsed['raw_message'] = latest.get('message', '')
                    parsed['timestamp'] = latest.get('timestamp', '')
                    
                    # Parse numbered responses if available
                    numbered_responses = latest.get('numbered_responses', {})
                    if numbered_responses:
                        parsed['mic_statuses'] = convert_numbered_responses_to_statuses(numbered_responses)
                        parsed['recognition_status'] = 'recognized'
                    elif parsed['response_type']:
                        # Single response for all mics
                        status = convert_yn_to_boolean(parsed['response_type'])
                        for i in range(len(parsed['mic_identifiers'])):
                            parsed['mic_statuses'][i + 1] = status
                        parsed['recognition_status'] = 'recognized'
                    
            elif isinstance(response_data, list):
                # Old format - list of messages
                latest = response_data[-1] if response_data else {}
                parsed['response_type'] = latest.get('parsed_response')
                parsed['raw_message'] = latest.get('message', '')
                parsed['timestamp'] = latest.get('timestamp', '')
                
            elif isinstance(response_data, dict):
                # Single message format
                parsed['response_type'] = response_data.get('parsed_response')
                parsed['raw_message'] = response_data.get('message', '')
                parsed['timestamp'] = response_data.get('timestamp', '')
        
        elif response_type == 'sms':
            # SMS response format
            parsed['response_type'] = response_data.get('parsed_response')
            parsed['raw_message'] = response_data.get('message', '')
            parsed['timestamp'] = response_data.get('timestamp', '')
            parsed['mic_identifiers'] = response_data.get('mic_identifiers', [])
            
            # Parse numbered responses if available
            numbered_responses = response_data.get('numbered_responses', {})
            if numbered_responses:
                parsed['mic_statuses'] = convert_numbered_responses_to_statuses(numbered_responses)
                parsed['recognition_status'] = 'recognized'
            elif parsed['response_type']:
                # Single response for all mics
                status = convert_yn_to_boolean(parsed['response_type'])
                for i in range(len(parsed['mic_identifiers'])):
                    parsed['mic_statuses'][i + 1] = status
                parsed['recognition_status'] = 'recognized'
    
    except Exception as e:
        print(f"⚠️  Error parsing response: {e}")
        parsed['recognition_status'] = 'error'
    
    return parsed


def convert_numbered_responses_to_statuses(numbered_responses: Dict[int, str]) -> Dict[int, Any]:
    """Convert numbered Y/N/C responses to True/False/None statuses."""
    statuses = {}
    for mic_position, response in numbered_responses.items():
        statuses[mic_position] = convert_yn_to_boolean(response)
    return statuses


def convert_yn_to_boolean(response: Any) -> Any:
    """Convert Y/N/C response to True/False/None."""
    if response == 'Y' or response is True:
        return True
    elif response == 'N' or response is False:
        return False
    elif response == 'C':
        return None
    else:
        return None


def organize_responses(ig_responses: Dict, sms_responses: Dict, 
                       ig_sent: Dict, sms_sent: Dict) -> Dict[str, Any]:
    """
    Organize all responses into individual mic status entries.
    
    Args:
        ig_responses: Instagram responses dictionary
        sms_responses: SMS responses dictionary
        ig_sent: Instagram sent messages
        sms_sent: SMS sent messages
        
    Returns:
        Dictionary with mic_responses (by identifier) and contact_responses (by contact)
    """
    mic_responses = {}  # Grouped by individual mic identifier
    contact_responses = []  # Individual contact responses
    
    # Process Instagram responses
    for username, response_data in ig_responses.items():
        contact_info = f"ig:{username}"
        parsed = parse_response_content(response_data, 'ig')
        
        contact_response = {
            'contact_method': 'instagram',
            'contact_info': contact_info,
            'username': username,
            'mic_identifiers': parsed['mic_identifiers'],
            'mic_statuses': parsed['mic_statuses'],  # Dict of position -> status
            'response_type': parsed['response_type'],
            'raw_message': parsed['raw_message'],
            'timestamp': parsed['timestamp'],
            'recognition_status': parsed['recognition_status'],
            'sent_message_info': ig_sent.get(f"ig_{username}")
        }
        
        contact_responses.append(contact_response)
        
        # Create individual mic responses
        if parsed['mic_identifiers'] and parsed['mic_statuses']:
            for position, status in parsed['mic_statuses'].items():
                # Get the actual mic ID for this position
                mic_index = int(position) - 1  # Convert 1-based to 0-based
                if 0 <= mic_index < len(parsed['mic_identifiers']):
                    mic_id = parsed['mic_identifiers'][mic_index]
                    
                    mic_responses[mic_id] = {
                        'mic_identifier': mic_id,
                        'status': status,
                        'contact_method': 'instagram',
                        'contact_info': contact_info,
                        'position_in_message': position,
                        'raw_message': parsed['raw_message'],
                        'timestamp': parsed['timestamp'],
                        'recognition_status': parsed['recognition_status']
                    }
    
    # Process SMS responses
    for phone, response_data in sms_responses.items():
        contact_info = f"sms:{phone}"
        parsed = parse_response_content(response_data, 'sms')
        
        contact_response = {
            'contact_method': 'sms',
            'contact_info': contact_info,
            'phone_number': phone,
            'mic_identifiers': parsed['mic_identifiers'],
            'mic_statuses': parsed['mic_statuses'],  # Dict of position -> status
            'response_type': parsed['response_type'],
            'raw_message': parsed['raw_message'],
            'timestamp': parsed['timestamp'],
            'recognition_status': parsed['recognition_status'],
            'sent_message_info': sms_sent.get(f"sms_{phone}")
        }
        
        contact_responses.append(contact_response)
        
        # Create individual mic responses
        if parsed['mic_identifiers'] and parsed['mic_statuses']:
            for position, status in parsed['mic_statuses'].items():
                # Get the actual mic ID for this position
                mic_index = position - 1  # Convert 1-based to 0-based
                if 0 <= mic_index < len(parsed['mic_identifiers']):
                    mic_id = parsed['mic_identifiers'][mic_index]
                    
                    mic_responses[mic_id] = {
                        'mic_identifier': mic_id,
                        'status': status,
                        'contact_method': 'sms',
                        'contact_info': contact_info,
                        'position_in_message': position,
                        'raw_message': parsed['raw_message'],
                        'timestamp': parsed['timestamp'],
                        'recognition_status': parsed['recognition_status']
                    }
    
    return {
        'mic_responses': mic_responses,
        'contact_responses': contact_responses
    }


def generate_summary(organized_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate summary statistics.
    
    Args:
        organized_data: Dictionary with mic_responses and contact_responses
        
    Returns:
        Summary dictionary
    """
    mic_responses = organized_data['mic_responses']
    contact_responses = organized_data['contact_responses']
    
    total_contacts = len(contact_responses)
    total_mics = len(mic_responses)
    
    # Count by status (True/False/None) for individual mics
    mic_status_counts = {'active': 0, 'inactive': 0, 'changes_needed': 0, 'unknown': 0}
    
    # Count mic responses
    for mic_id, mic_data in mic_responses.items():
        status = mic_data['status']
        if status is True:
            mic_status_counts['active'] += 1
        elif status is False:
            mic_status_counts['inactive'] += 1
        elif status is None:
            # Check if it's None due to changes or just unrecognized
            if mic_data.get('recognition_status') == 'changes_requested':
                mic_status_counts['changes_needed'] += 1
            else:
                mic_status_counts['unknown'] += 1
    
    # Count contact-level statistics
    by_method = {'instagram': 0, 'sms': 0}
    by_recognition = {'recognized': 0, 'unrecognized': 0, 'error': 0}
    
    for response in contact_responses:
        # Count by contact method
        method = response.get('contact_method', 'unknown')
        if method in by_method:
            by_method[method] += 1
        
        # Count by recognition status
        recognition = response.get('recognition_status', 'unknown')
        if recognition in by_recognition:
            by_recognition[recognition] += 1
    
    return {
        'total_contact_responses': total_contacts,
        'total_individual_mic_responses': total_mics,
        'mic_status_summary': mic_status_counts,
        'by_contact_method': by_method,
        'by_recognition_status': by_recognition,
        'processed_at': datetime.now().isoformat()
    }


def main():
    """Main execution function."""
    print("=" * 70)
    print("📊 PROCESSING RESPONSES")
    print("=" * 70)
    
    # Load responses
    print("\n📂 Loading collected responses...")
    ig_responses = load_instagram_responses()
    sms_responses = load_sms_responses()
    
    print(f"   Instagram responses: {len(ig_responses)}")
    print(f"   SMS responses: {len(sms_responses)}")
    
    if len(ig_responses) == 0 and len(sms_responses) == 0:
        print("\n⚠️  No responses found. Please run collection scripts first:")
        print("   - python collect_instagram_responses.py")
        print("   - python collect_sms_responses.py")
        sys.exit(0)
    
    # Load sent messages and mic mappings
    print("\n📂 Loading sent messages and mic mappings...")
    sent_messages = load_sent_messages()
    
    # Separate into IG and SMS for compatibility
    ig_sent = {k[3:]: v for k, v in sent_messages.items() if k.startswith('ig_')}
    sms_sent = {k[4:]: v for k, v in sent_messages.items() if k.startswith('sms_')}
    
    # Organize responses
    print("\n🔄 Organizing responses...")
    organized_data = organize_responses(ig_responses, sms_responses, ig_sent, sms_sent)
    
    # Generate summary
    summary = generate_summary(organized_data)
    
    # Create output structure optimized for Supabase updates
    output = {
        'metadata': {
            'processed_at': datetime.now().isoformat(),
            'summary': summary
        },
        'mic_responses': organized_data['mic_responses'],  # Individual mic responses by ID
        'contact_responses': organized_data['contact_responses'],  # Contact-level responses
        'supabase_updates': [  # Ready-to-use format for database updates
            {
                'mic_identifier': mic_id,
                'verification_status': mic_data['status'],  # True/False/None
                'last_verified': mic_data['timestamp'],
                'contact_method': mic_data['contact_method'],
                'position_in_response': mic_data['position_in_message'],
                'raw_response': mic_data['raw_message'][:100] + '...' if len(mic_data['raw_message']) > 100 else mic_data['raw_message']
            }
            for mic_id, mic_data in organized_data['mic_responses'].items()
        ]
    }
    
    # Save output
    output_file = "processed_responses.json"
    print(f"\n💾 Saving processed data to: {output_file}")
    
    try:
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        print(f"✅ Successfully saved to {output_file}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")
        sys.exit(1)
    
    # Print summary
    print("\n" + "=" * 70)
    print("📊 PROCESSING SUMMARY")
    print("=" * 70)
    print(f"Total contact responses: {summary['total_contact_responses']}")
    print(f"Total individual mic responses: {summary['total_individual_mic_responses']}")
    
    print("\nIndividual mic verification status:")
    print(f"   ✅ Active: {summary['mic_status_summary']['active']}")
    print(f"   ❌ Inactive: {summary['mic_status_summary']['inactive']}")
    print(f"   📝 Changes needed: {summary['mic_status_summary']['changes_needed']}")
    print(f"   🤔 Unknown/Unrecognized: {summary['mic_status_summary']['unknown']}")
    
    print("\nBy contact method:")
    print(f"   📱 Instagram: {summary['by_contact_method']['instagram']}")
    print(f"   💬 SMS: {summary['by_contact_method']['sms']}")
    print("=" * 70)
    
    print("\n💡 Next steps:")
    print("   1. Review processed_responses.json")
    print("   2. Use 'supabase_updates' array to update your database:")
    print("      - mic_identifier: unique ID for EACH mic")
    print("      - verification_status: true (active), false (inactive), null (changes/unknown)")
    print("      - last_verified: timestamp of verification")
    print("      - position_in_response: which number in the response (1, 2, 3, etc.)")
    print("   3. Each numbered response creates separate database updates")


if __name__ == "__main__":
    main()

