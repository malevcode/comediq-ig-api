#!/usr/bin/env python3
"""
Process and organize collected responses into a structured JSON format.

This script reads collected responses from Instagram and SMS, processes them,
and outputs an organized JSON file that can be used to update database tables.
"""

import json
import os
import sys
import argparse
import hashlib
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
import pandas as pd


DEFAULT_AI_QUEUE_FILE = "ai_parse_queue.json"
DEFAULT_AI_RESULTS_FILE = "ai_parse_results.json"
DEFAULT_AI_RESULTS_TEMPLATE_FILE = "ai_parse_results_template.json"
DEFAULT_SQL_OUTPUT_FILE = "supabase_response_updates.sql"
DEFAULT_COMMENT_RESPONSES_FILE = "ig_comment_responses.json"
DEFAULT_COMMENT_MAPPING_FILE = "instagram_comment_mic_mapping.json"

AI_UPDATE_FIELDS = {
    "active",
    "cost",
    "frequency",
    "frequency_custom_text",
    "location",
    "stage_time",
    "latest_end_time",
    "day",
    "start_time",
    "venue_name",
    "open_mic",
    "sign_up_instructions",
    "signup_url",
    "sms_response",
    "changes_updates",
    "hosts_organizers",
    "other_rules",
}

MONTH_STATUS_COLUMNS = {
    1: "jan_verification_status",
    2: "feb_verification_status",
    3: "mar_verification_status",
    4: "apr_verification_status",
    5: "may_verification_status",
    6: "jun_verification_status",
    7: "july_verification_status",
    8: "aug_verification_status",
    9: "sep_verification_status",
    10: "oct_verification_status",
    11: "nov_verification_status",
    12: "dec_verification_status",
}


def load_instagram_responses(file_path: str = "dm_replies.json") -> Dict[str, Any]:
    """
    Load Instagram responses from JSON file.
    
    Args:
        file_path: Path to the responses file
        
    Returns:
        Dictionary of responses
    """
    if not file_path:
        return {}
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
    if not file_path:
        return {}
    if not os.path.exists(file_path):
        print(f"⚠️  SMS responses file not found: {file_path}")
        return {}

    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading SMS responses: {e}")
        return {}


def load_comment_responses(file_path: str = DEFAULT_COMMENT_RESPONSES_FILE) -> Dict[str, Any]:
    """Load Instagram post comments collected through the Instagram Graph API."""
    if not file_path:
        return {}
    if not os.path.exists(file_path):
        return {}

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"⚠️  Error loading Instagram comments: {e}")
        return {}

    if isinstance(data, dict):
        return data
    if isinstance(data, list):
        return {"comments": data}
    return {}


def normalize_instagram_username(value: Any) -> str:
    """Normalize an Instagram username without @."""
    return str(value or "").strip().lstrip("@").lower()


def load_comment_mic_mapping(file_path: str = DEFAULT_COMMENT_MAPPING_FILE) -> Dict[str, Any]:
    """Load internal username-to-mic mapping generated for public comment collection."""
    if not os.path.exists(file_path):
        return {"usernames": {}, "mics": {}}

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"⚠️  Error loading comment mic mapping: {e}")
        return {"usernames": {}, "mics": {}}

    usernames = {}
    for username, mic_ids in (data.get("usernames") or {}).items():
        normalized = normalize_instagram_username(username)
        if not normalized:
            continue
        if not isinstance(mic_ids, list):
            mic_ids = [mic_ids]
        usernames[normalized] = [str(mic_id) for mic_id in mic_ids if mic_id]

    return {
        "usernames": usernames,
        "mics": data.get("mics") or {},
        "metadata": data.get("metadata") or {},
    }


def normalize_comment_items(comment_responses: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Flatten top-level comments and replies into newest-first comment records."""
    comments = comment_responses.get("comments", [])
    if isinstance(comments, dict):
        comments = comments.get("data", [])
    if not isinstance(comments, list):
        comments = []

    flattened = []
    for comment in comments:
        if not isinstance(comment, dict):
            continue
        base = {
            "id": comment.get("id", ""),
            "username": comment.get("username", ""),
            "text": comment.get("text") or comment.get("message") or "",
            "timestamp": comment.get("timestamp") or comment.get("created_time") or "",
            "parent_id": comment.get("parent_id") or None,
            "permalink": comment.get("permalink") or "",
        }
        flattened.append(base)

        replies = comment.get("replies", [])
        if isinstance(replies, dict):
            replies = replies.get("data", [])
        if isinstance(replies, list):
            for reply in replies:
                if not isinstance(reply, dict):
                    continue
                flattened.append({
                    "id": reply.get("id", ""),
                    "username": reply.get("username", ""),
                    "text": reply.get("text") or reply.get("message") or "",
                    "timestamp": reply.get("timestamp") or reply.get("created_time") or "",
                    "parent_id": comment.get("id", ""),
                    "permalink": reply.get("permalink") or comment.get("permalink") or "",
                })

    return sorted(flattened, key=lambda item: item.get("timestamp") or "", reverse=True)


def load_ai_results(file_path: str = DEFAULT_AI_RESULTS_FILE) -> List[Dict[str, Any]]:
    """Load AI parse results if the handoff file has been filled in."""
    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"⚠️  Error loading AI results: {e}")
        return []

    if isinstance(data, dict):
        results = data.get("results", [])
    elif isinstance(data, list):
        results = data
    else:
        return []

    return results if isinstance(results, list) else []


def default_last_verified() -> str:
    """Return the current date in MM/DD/YY last_verified format."""
    return datetime.now().strftime("%m/%d/%y")


def default_verification_column() -> str:
    """Return a month-specific verification status column, matching existing files."""
    return MONTH_STATUS_COLUMNS[datetime.now().month]


def make_queue_id(source: str, contact_info: str, timestamp: str, mic_identifier: str) -> str:
    """Create a stable, readable handoff ID for matching AI results back later."""
    safe_contact = contact_info.replace(":", "_").replace("@", "").replace("+", "")
    seed = f"{source}|{contact_info}|{timestamp}|{mic_identifier}"
    suffix = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:10]
    return f"{source}_{safe_contact}_{mic_identifier}_{suffix}"


def sql_literal(value: Any) -> str:
    """Safely format a primitive value for generated SQL."""
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"

    text = str(value)
    return "'" + text.replace("'", "''") + "'"


def sql_identifier(name: str) -> str:
    """Quote a SQL identifier that comes from our fixed allow-list."""
    return '"' + name.replace('"', '""') + '"'


def status_label_for_direct_status(status: Any) -> Optional[str]:
    if status is True:
        return "responded_confirmed"
    if status is False:
        return "responded_confirmed"
    return None


def parse_structured_response(message_text: str) -> Optional[str]:
    """Parse only clear Y/N/Changes replies; route update-like text to AI."""
    text = " ".join(str(message_text or "").strip().upper().split())
    if not text:
        return None

    change_markers = re.compile(
        r"\b(CHANGE|CHANGES|UPDATED?|MODIFIED|NOW|STARTS?|TIME|DAY|DATE|NEXT|EVERY OTHER|"
        r"VENUE|LOCATION|MOVED|COST|SIGN ?UP|REQUIRED|FOLLOW|MONTH|WEEK)\b"
    )
    if change_markers.search(text):
        return "C"

    if re.fullmatch(r"(Y|YES|YEP|YUP|ACTIVE|CONFIRMED?|STILL ACTIVE|SAME|NO CHANGES?)", text):
        return "Y"
    if re.fullmatch(r"(N|NO|NOPE|INACTIVE|NOT ACTIVE|CANCELLED|CANCELED|ENDED|DEAD)", text):
        return "N"
    if re.fullmatch(r"(C|CHANGE|CHANGES|UPDATES?)", text):
        return "C"

    return None


def parse_structured_numbered_responses(message_text: str) -> Dict[int, str]:
    """Parse clear numbered Y/N/Changes responses."""
    results = {}
    for raw_line in str(message_text or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue

        match = re.match(r"^(\d+)[\).:\-\s]+(.+)$", line)
        if not match:
            continue

        mic_num = int(match.group(1))
        status = parse_structured_response(match.group(2))
        if status:
            results[mic_num] = status

    return results


def should_stamp_last_verified(verification_status: Optional[str]) -> bool:
    """Only confirmed or changed responses count as a completed verification."""
    return verification_status in {"responded_confirmed", "responded_changes"}


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
        'recognition_status': 'unrecognized',
        'message_history': []
    }
    
    try:
        if response_type == 'ig':
            # Instagram response format (new structure with mic_identifiers)
            if isinstance(response_data, dict) and 'messages' in response_data:
                # New format with mic identifiers list
                messages = response_data['messages']
                parsed['mic_identifiers'] = response_data.get('mic_identifiers', [])
                parsed['message_history'] = normalize_message_history(messages)
                
                if messages:
                    # Instagram API returns messages in newest-to-oldest order
                    # So the first message [0] is the most recent
                    latest = messages[0] if isinstance(messages, list) else messages
                    
                    parsed['raw_message'] = latest.get('message', '')
                    parsed['timestamp'] = latest.get('timestamp', '')
                    parsed['response_type'] = parse_structured_response(parsed['raw_message'])
                    
                    # Parse numbered responses if available
                    numbered_responses = parse_structured_numbered_responses(parsed['raw_message'])
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
                parsed['raw_message'] = latest.get('message', '')
                parsed['timestamp'] = latest.get('timestamp', '')
                parsed['response_type'] = parse_structured_response(parsed['raw_message'])
                parsed['message_history'] = normalize_message_history(response_data)
                
            elif isinstance(response_data, dict):
                # Single message format
                parsed['raw_message'] = response_data.get('message', '')
                parsed['timestamp'] = response_data.get('timestamp', '')
                parsed['response_type'] = parse_structured_response(parsed['raw_message'])
                parsed['message_history'] = normalize_message_history([response_data])
        
        elif response_type == 'sms':
            # SMS response format
            parsed['raw_message'] = response_data.get('message', '')
            parsed['timestamp'] = response_data.get('timestamp', '')
            parsed['mic_identifiers'] = response_data.get('mic_identifiers', [])
            parsed['response_type'] = parse_structured_response(parsed['raw_message'])
            parsed['message_history'] = normalize_message_history([response_data])
            
            # Parse numbered responses if available
            numbered_responses = parse_structured_numbered_responses(parsed['raw_message'])
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


def normalize_message_history(messages: Any) -> List[Dict[str, Any]]:
    """Normalize collected messages into AI-friendly conversation context."""
    if not isinstance(messages, list):
        messages = [messages] if messages else []

    history = []
    for index, message in enumerate(messages):
        if not isinstance(message, dict):
            continue

        raw_message = message.get("message", "")
        structured_response = parse_structured_response(raw_message)
        numbered_responses = parse_structured_numbered_responses(raw_message)
        history.append({
            "index": index,
            "order": "newest_first",
            "message": raw_message,
            "timestamp": message.get("timestamp", ""),
            "deterministic_status": structured_response,
            "numbered_responses": numbered_responses or None,
        })

    return history


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


def organize_comment_responses(
    comment_responses: Dict[str, Any],
    comment_mapping: Dict[str, Any],
) -> Dict[str, Any]:
    """Turn draft-post comments into the same mic-level records used by DM/SMS replies."""
    mic_responses = {}
    contact_responses = []
    direct_supabase_updates = []
    ai_parse_queue = []

    username_mapping = comment_mapping.get("usernames") or {}
    mic_metadata = comment_mapping.get("mics") or {}

    for comment in normalize_comment_items(comment_responses):
        text = comment.get("text", "")
        username = normalize_instagram_username(comment.get("username"))
        timestamp = comment.get("timestamp", "")
        comment_id = str(comment.get("id") or "")

        mic_ids = []
        match_method = None
        if username and username in username_mapping:
            mic_ids = username_mapping[username]
            match_method = "instagram_username"

        # Preserve order while removing duplicates.
        mic_ids = list(dict.fromkeys(str(mic_id) for mic_id in mic_ids if mic_id))
        parsed_status = parse_structured_response(text)
        numbered_responses = parse_structured_numbered_responses(text)
        message_history = normalize_message_history([{
            "message": text,
            "timestamp": timestamp,
            "comment_id": comment_id,
            "username": username,
        }])

        contact_info = f"ig_comment:{comment_id or username or 'unknown'}"
        contact_response = {
            "contact_method": "instagram_comment",
            "contact_info": contact_info,
            "username": username,
            "comment_id": comment_id,
            "parent_id": comment.get("parent_id"),
            "permalink": comment.get("permalink"),
            "match_method": match_method,
            "mic_identifiers": mic_ids,
            "response_type": parsed_status,
            "raw_message": text,
            "timestamp": timestamp,
            "recognition_status": "recognized" if parsed_status and mic_ids else "unrecognized",
            "message_history": message_history,
        }
        contact_responses.append(contact_response)

        if not mic_ids:
            queue_id = make_queue_id("instagram_comment", contact_info, timestamp, "unmatched")
            ai_parse_queue.append({
                "queue_id": queue_id,
                "source": "instagram_comment",
                "contact_info": contact_info,
                "username": username,
                "comment_id": comment_id,
                "mic_identifier": None,
                "all_mic_identifiers_for_contact": [],
                "raw_message": text,
                "timestamp": timestamp,
                "message_history": message_history,
                "deterministic_status": parsed_status,
                "reason": "commenter_username_not_found_in_mapping",
                "expected_ai_result_shape": {
                    "queue_id": queue_id,
                    "mic_identifier": "fill_with_existing_unique_identifier",
                    "active": True,
                    "verification_status": "responded_changes",
                    "updates": {},
                    "confidence": 0.0,
                    "needs_human_review": True,
                    "notes": "Commenter username was not found in instagram_comment_mic_mapping.json."
                }
            })
            continue

        if len(mic_ids) > 1 and parsed_status == "C":
            queue_id = make_queue_id("instagram_comment", contact_info, timestamp, "multi_mic")
            ai_parse_queue.append({
                "queue_id": queue_id,
                "source": "instagram_comment",
                "contact_info": contact_info,
                "username": username,
                "comment_id": comment_id,
                "parent_id": comment.get("parent_id"),
                "permalink": comment.get("permalink"),
                "mic_identifier": None,
                "candidate_mic_identifiers": mic_ids,
                "candidate_mics": [
                    mic_metadata.get(str(mic_id), {"unique_identifier": str(mic_id)})
                    for mic_id in mic_ids
                ],
                "raw_message": text,
                "timestamp": timestamp,
                "message_history": message_history,
                "deterministic_status": parsed_status,
                "reason": "commenter_username_maps_to_multiple_mics",
                "expected_ai_result_shape": {
                    "queue_id": queue_id,
                    "mic_updates": [
                        {
                            "mic_identifier": "choose_candidate_unique_identifier",
                            "active": True,
                            "verification_status": "responded_changes",
                            "updates": {
                                "start_time": "8:00 PM"
                            },
                            "confidence": 0.0,
                            "needs_human_review": True,
                            "notes": ""
                        }
                    ]
                }
            })
            continue

        for position, mic_id in enumerate(mic_ids, 1):
            status = None
            if numbered_responses:
                numbered_status = numbered_responses.get(position) or numbered_responses.get(str(position))
                status = convert_yn_to_boolean(numbered_status)
            elif parsed_status:
                status = convert_yn_to_boolean(parsed_status)

            mic_record = {
                "mic_identifier": mic_id,
                "status": status,
                "contact_method": "instagram_comment",
                "contact_info": contact_info,
                "position_in_message": position,
                "raw_message": text,
                "timestamp": timestamp,
                "recognition_status": "recognized" if status in (True, False) else "unrecognized",
                "message_history": message_history,
            }

            if status in (True, False):
                mic_responses[mic_id] = mic_record
                direct_supabase_updates.append(mic_record)
            elif text:
                queue_id = make_queue_id("instagram_comment", contact_info, timestamp, str(mic_id))
                ai_parse_queue.append({
                    "queue_id": queue_id,
                    "source": "instagram_comment",
                    "contact_info": contact_info,
                    "username": username,
                    "comment_id": comment_id,
                    "parent_id": comment.get("parent_id"),
                    "permalink": comment.get("permalink"),
                    "mic_identifier": mic_id,
                    "position_in_message": position,
                    "match_method": match_method,
                    "all_mic_identifiers_for_contact": mic_ids,
                    "mic_context": mic_metadata.get(str(mic_id), {}),
                    "raw_message": text,
                    "timestamp": timestamp,
                    "message_history": message_history,
                    "deterministic_status": parsed_status,
                    "reason": "comment_changes_or_unclear_response",
                    "expected_ai_result_shape": {
                        "queue_id": queue_id,
                        "mic_identifier": mic_id,
                        "active": True,
                        "verification_status": "responded_changes",
                        "updates": {
                            "start_time": "8:00 PM"
                        },
                        "confidence": 0.0,
                        "needs_human_review": True,
                        "notes": ""
                    }
                })

    return {
        "mic_responses": mic_responses,
        "contact_responses": contact_responses,
        "direct_supabase_updates": direct_supabase_updates,
        "ai_parse_queue": ai_parse_queue,
    }


def merge_organized_responses(*organized_sources: Dict[str, Any]) -> Dict[str, Any]:
    """Merge organized response source dictionaries."""
    merged = {
        "mic_responses": {},
        "contact_responses": [],
        "direct_supabase_updates": [],
        "ai_parse_queue": [],
    }
    for source in organized_sources:
        if not source:
            continue
        merged["mic_responses"].update(source.get("mic_responses") or {})
        merged["contact_responses"].extend(source.get("contact_responses") or [])
        merged["direct_supabase_updates"].extend(source.get("direct_supabase_updates") or [])
        merged["ai_parse_queue"].extend(source.get("ai_parse_queue") or [])
    return merged


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
    direct_supabase_updates = []
    ai_parse_queue = []
    
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
            'message_history': parsed['message_history'],
            'sent_message_info': ig_sent.get(f"ig_{username}")
        }
        
        contact_responses.append(contact_response)
        
        # Create individual mic responses
        for position, mic_id in enumerate(parsed['mic_identifiers'], 1):
            status = parsed['mic_statuses'].get(position)
            if status is None:
                status = parsed['mic_statuses'].get(str(position))

            mic_record = {
                'mic_identifier': mic_id,
                'status': status,
                'contact_method': 'instagram',
                'contact_info': contact_info,
                'position_in_message': position,
                'raw_message': parsed['raw_message'],
                'timestamp': parsed['timestamp'],
                'recognition_status': parsed['recognition_status'],
                'message_history': parsed['message_history']
            }

            if status in (True, False):
                mic_responses[mic_id] = mic_record
                direct_supabase_updates.append(mic_record)
            elif parsed['raw_message']:
                queue_id = make_queue_id("instagram", contact_info, parsed['timestamp'], str(mic_id))
                ai_parse_queue.append({
                    "queue_id": queue_id,
                    "source": "instagram",
                    "contact_info": contact_info,
                    "username": username,
                    "mic_identifier": mic_id,
                    "position_in_message": position,
                    "all_mic_identifiers_for_contact": parsed['mic_identifiers'],
                    "raw_message": parsed['raw_message'],
                    "timestamp": parsed['timestamp'],
                    "message_history": parsed['message_history'],
                    "deterministic_status": parsed['response_type'],
                    "reason": "changes_or_unclear_response",
                    "sent_message_info": ig_sent.get(username),
                    "expected_ai_result_shape": {
                        "queue_id": queue_id,
                        "mic_identifier": mic_id,
                        "active": True,
                        "verification_status": "responded_changes",
                        "updates": {
                            "start_time": "8:00 PM"
                        },
                        "confidence": 0.0,
                        "needs_human_review": True,
                        "notes": ""
                    }
                })
    
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
            'message_history': parsed['message_history'],
            'sent_message_info': sms_sent.get(f"sms_{phone}")
        }
        
        contact_responses.append(contact_response)
        
        # Create individual mic responses
        for position, mic_id in enumerate(parsed['mic_identifiers'], 1):
            status = parsed['mic_statuses'].get(position)
            if status is None:
                status = parsed['mic_statuses'].get(str(position))

            mic_record = {
                'mic_identifier': mic_id,
                'status': status,
                'contact_method': 'sms',
                'contact_info': contact_info,
                'position_in_message': position,
                'raw_message': parsed['raw_message'],
                'timestamp': parsed['timestamp'],
                'recognition_status': parsed['recognition_status'],
                'message_history': parsed['message_history']
            }

            if status in (True, False):
                mic_responses[mic_id] = mic_record
                direct_supabase_updates.append(mic_record)
            elif parsed['raw_message']:
                queue_id = make_queue_id("sms", contact_info, parsed['timestamp'], str(mic_id))
                ai_parse_queue.append({
                    "queue_id": queue_id,
                    "source": "sms",
                    "contact_info": contact_info,
                    "phone_number": phone,
                    "mic_identifier": mic_id,
                    "position_in_message": position,
                    "all_mic_identifiers_for_contact": parsed['mic_identifiers'],
                    "raw_message": parsed['raw_message'],
                    "timestamp": parsed['timestamp'],
                    "message_history": parsed['message_history'],
                    "deterministic_status": parsed['response_type'],
                    "reason": "changes_or_unclear_response",
                    "sent_message_info": sms_sent.get(phone),
                    "expected_ai_result_shape": {
                        "queue_id": queue_id,
                        "mic_identifier": mic_id,
                        "active": True,
                        "verification_status": "responded_changes",
                        "updates": {
                            "start_time": "8:00 PM"
                        },
                        "confidence": 0.0,
                        "needs_human_review": True,
                        "notes": ""
                    }
                })
    
    return {
        'mic_responses': mic_responses,
        'contact_responses': contact_responses,
        'direct_supabase_updates': direct_supabase_updates,
        'ai_parse_queue': ai_parse_queue
    }


def normalize_ai_result_entries(ai_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Flatten supported AI result shapes into mic-level update records."""
    normalized = []

    for result in ai_results:
        if not isinstance(result, dict):
            continue

        if isinstance(result.get("mic_updates"), list):
            for update in result["mic_updates"]:
                if isinstance(update, dict):
                    normalized.append({**result, **update})
        else:
            normalized.append(result)

    return normalized


def generate_supabase_sql(
    direct_updates: List[Dict[str, Any]],
    ai_results: List[Dict[str, Any]],
    ai_parse_queue: Optional[List[Dict[str, Any]]] = None,
    output_file: str = DEFAULT_SQL_OUTPUT_FILE,
    table_name: str = "open_mics_historical",
    verification_column: Optional[str] = None,
    last_verified: Optional[str] = None,
) -> Dict[str, int]:
    """Write SQL updates for deterministic Y/N replies plus reviewed AI results."""
    verification_column = verification_column or default_verification_column()
    last_verified = last_verified or default_last_verified()
    ai_update_entries = normalize_ai_result_entries(ai_results)
    queue_by_id = {
        item.get("queue_id"): item
        for item in (ai_parse_queue or [])
        if isinstance(item, dict) and item.get("queue_id")
    }

    lines = [
        "-- Generated by process_responses.py",
        "-- Review before running in Supabase.",
        "BEGIN;",
        f"ALTER TABLE {table_name}",
        f"ADD COLUMN IF NOT EXISTS {sql_identifier(verification_column)} text;",
        "",
    ]

    direct_count = 0
    for update in direct_updates:
        mic_id = update.get("mic_identifier")
        status = update.get("status")
        if not mic_id or status not in (True, False):
            continue

        assignments = [
            f"active = {sql_literal(status)}",
            f"last_verified = {sql_literal(last_verified)}",
            f"{sql_identifier(verification_column)} = {sql_literal(status_label_for_direct_status(status))}",
        ]

        raw_response = update.get("raw_message", "")
        if raw_response and len(raw_response) <= 500:
            assignments.append(f"-- raw response: {sql_literal(raw_response)}")

        lines.append(
            f"UPDATE {table_name}\n"
            f"SET {', '.join(a for a in assignments if not a.startswith('--'))}\n"
            f"WHERE unique_identifier = {sql_literal(mic_id)};"
        )
        if raw_response:
            lines.append(f"-- raw response for {mic_id}: {raw_response.replace(chr(10), ' ')[:500]}")
        lines.append("")
        direct_count += 1

    ai_count = 0
    for result in ai_update_entries:
        if not isinstance(result, dict):
            continue

        queue_item = queue_by_id.get(result.get("queue_id"))
        mic_id = result.get("mic_identifier")
        if not mic_id and queue_item:
            mic_id = queue_item.get("mic_identifier")
        if not mic_id:
            continue

        assignments = []
        if "active" in result and result.get("active") is not None:
            assignments.append(f"active = {sql_literal(result.get('active'))}")

        updates = result.get("updates") or result.get("proposed_updates") or {}
        has_updates = isinstance(updates, dict) and any(value not in (None, "") for value in updates.values())
        verification_status = result.get("verification_status")
        if not verification_status:
            verification_status = "responded_changes" if has_updates or result.get("active") is not None else "responded_unclear"

        if should_stamp_last_verified(verification_status):
            assignments.append(f"last_verified = {sql_literal(result.get('last_verified') or last_verified)}")
        assignments.append(f"{sql_identifier(verification_column)} = {sql_literal(verification_status)}")

        if isinstance(updates, dict):
            for field, value in updates.items():
                if field in AI_UPDATE_FIELDS and value not in (None, ""):
                    assignments.append(f"{sql_identifier(field)} = {sql_literal(value)}")

        if not assignments:
            continue

        lines.append(
            f"UPDATE {table_name}\n"
            f"SET {', '.join(assignments)}\n"
            f"WHERE unique_identifier = {sql_literal(mic_id)};"
        )
        note = result.get("notes") or result.get("raw_message")
        if not note and queue_item:
            note = queue_item.get("raw_message")
        if note:
            lines.append(f"-- AI note for {mic_id}: {str(note).replace(chr(10), ' ')[:500]}")
        lines.append("")
        ai_count += 1

    lines.append("COMMIT;")
    lines.append("")

    with open(output_file, "w") as f:
        f.write("\n".join(lines))

    return {"direct_sql_updates": direct_count, "ai_sql_updates": ai_count}


def save_ai_results_template(ai_parse_queue: List[Dict[str, Any]], output_file: str) -> None:
    """Write a fill-in template that can be given to an AI parser."""
    template = {
        "instructions": (
            "Fill results with one object per queue item. Keep queue_id and mic_identifier unchanged. "
            "Use message_history for context; Instagram history is newest_first, so earlier formatted replies may appear after the latest message. "
            "Put changed Supabase columns inside updates. Use verification_status=responded_changes when updates are needed, "
            "responded_confirmed when no updates are needed, and responded_unclear when the reply still cannot be interpreted."
        ),
        "verification_status_values": [
            "responded_confirmed",
            "responded_changes",
            "responded_unclear",
        ],
        "allowed_update_fields": sorted(AI_UPDATE_FIELDS),
        "results": [
            item.get("expected_ai_result_shape", {})
            for item in ai_parse_queue
        ]
    }

    with open(output_file, "w") as f:
        json.dump(template, f, indent=2)


def process_response_files(
    instagram_file: str = "dm_replies.json",
    sms_file: str = "twilio_responses.json",
    comments_file: str = DEFAULT_COMMENT_RESPONSES_FILE,
    comment_mapping_file: str = DEFAULT_COMMENT_MAPPING_FILE,
    output_file: str = "processed_responses.json",
    ai_queue_file: str = DEFAULT_AI_QUEUE_FILE,
    ai_results_file: str = DEFAULT_AI_RESULTS_FILE,
    ai_results_template_file: str = DEFAULT_AI_RESULTS_TEMPLATE_FILE,
    sql_output_file: str = DEFAULT_SQL_OUTPUT_FILE,
    verification_column: Optional[str] = None,
    last_verified: Optional[str] = None,
    table_name: str = "open_mics_historical",
) -> Dict[str, Any]:
    """Run the full response processing pipeline and write JSON/SQL outputs."""
    ig_responses = load_instagram_responses(instagram_file)
    sms_responses = load_sms_responses(sms_file)
    comment_responses = load_comment_responses(comments_file)
    comment_mapping = load_comment_mic_mapping(comment_mapping_file)
    sent_messages = load_sent_messages()
    ig_sent = {k[3:]: v for k, v in sent_messages.items() if k.startswith('ig_')}
    sms_sent = {k[4:]: v for k, v in sent_messages.items() if k.startswith('sms_')}
    dm_sms_data = organize_responses(ig_responses, sms_responses, ig_sent, sms_sent)
    comment_data = organize_comment_responses(comment_responses, comment_mapping)
    organized_data = merge_organized_responses(dm_sms_data, comment_data)
    summary = generate_summary(organized_data)
    ai_results = load_ai_results(ai_results_file)

    output = {
        'metadata': {
            'processed_at': datetime.now().isoformat(),
            'summary': summary,
            'ai_queue_file': ai_queue_file,
            'ai_results_file': ai_results_file,
            'sql_output_file': sql_output_file,
            'comments_file': comments_file,
            'comment_mapping_file': comment_mapping_file,
        },
        'mic_responses': organized_data['mic_responses'],
        'contact_responses': organized_data['contact_responses'],
        'direct_supabase_updates': [
            {
                'mic_identifier': mic_data['mic_identifier'],
                'active': mic_data['status'],
                'verification_status': status_label_for_direct_status(mic_data['status']),
                'last_verified': last_verified or default_last_verified(),
                'contact_method': mic_data['contact_method'],
                'position_in_response': mic_data['position_in_message'],
                'raw_response': mic_data['raw_message'][:100] + '...' if len(mic_data['raw_message']) > 100 else mic_data['raw_message']
            }
            for mic_data in organized_data['direct_supabase_updates']
        ],
        # Backward-compatible alias. This now contains only direct Y/N updates.
        'supabase_updates': [
            {
                'mic_identifier': mic_data['mic_identifier'],
                'verification_status': mic_data['status'],
                'last_verified': mic_data['timestamp'],
                'contact_method': mic_data['contact_method'],
                'position_in_response': mic_data['position_in_message'],
                'raw_response': mic_data['raw_message'][:100] + '...' if len(mic_data['raw_message']) > 100 else mic_data['raw_message']
            }
            for mic_data in organized_data['direct_supabase_updates']
        ],
        'ai_parse_queue': organized_data['ai_parse_queue'],
        'ai_results_loaded': ai_results,
    }

    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    with open(ai_queue_file, 'w') as f:
        json.dump(organized_data['ai_parse_queue'], f, indent=2)

    save_ai_results_template(organized_data['ai_parse_queue'], ai_results_template_file)
    sql_counts = generate_supabase_sql(
        organized_data['direct_supabase_updates'],
        ai_results,
        ai_parse_queue=organized_data['ai_parse_queue'],
        output_file=sql_output_file,
        table_name=table_name,
        verification_column=verification_column,
        last_verified=last_verified,
    )

    return {
        "ig_responses": len(ig_responses),
        "sms_responses": len(sms_responses),
        "comment_responses": len(normalize_comment_items(comment_responses)),
        "summary": summary,
        "direct_updates": len(organized_data['direct_supabase_updates']),
        "ai_queue_items": len(organized_data['ai_parse_queue']),
        "ai_results_loaded": len(ai_results),
        "sql_counts": sql_counts,
        "output_file": output_file,
        "ai_queue_file": ai_queue_file,
        "ai_results_template_file": ai_results_template_file,
        "sql_output_file": sql_output_file,
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
    by_method = {'instagram': 0, 'sms': 0, 'instagram_comment': 0}
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
    parser = argparse.ArgumentParser(description="Process collected Instagram/SMS replies")
    parser.add_argument("--instagram-file", default="dm_replies.json")
    parser.add_argument("--sms-file", default="twilio_responses.json")
    parser.add_argument("--comments-file", default=DEFAULT_COMMENT_RESPONSES_FILE)
    parser.add_argument("--comment-mapping-file", default=DEFAULT_COMMENT_MAPPING_FILE)
    parser.add_argument("--output-file", default="processed_responses.json")
    parser.add_argument("--ai-queue-file", default=DEFAULT_AI_QUEUE_FILE)
    parser.add_argument("--ai-results-file", default=DEFAULT_AI_RESULTS_FILE)
    parser.add_argument("--ai-results-template-file", default=DEFAULT_AI_RESULTS_TEMPLATE_FILE)
    parser.add_argument("--sql-output-file", default=DEFAULT_SQL_OUTPUT_FILE)
    parser.add_argument("--table-name", default="open_mics_historical")
    parser.add_argument("--verification-column", default=default_verification_column())
    parser.add_argument("--last-verified", default=default_last_verified())
    args = parser.parse_args()

    print("=" * 70)
    print("📊 PROCESSING RESPONSES")
    print("=" * 70)
    
    print("\n📂 Loading collected responses...")
    result = process_response_files(
        instagram_file=args.instagram_file,
        sms_file=args.sms_file,
        comments_file=args.comments_file,
        comment_mapping_file=args.comment_mapping_file,
        output_file=args.output_file,
        ai_queue_file=args.ai_queue_file,
        ai_results_file=args.ai_results_file,
        ai_results_template_file=args.ai_results_template_file,
        sql_output_file=args.sql_output_file,
        verification_column=args.verification_column,
        last_verified=args.last_verified,
        table_name=args.table_name,
    )
    summary = result["summary"]

    print(f"   Instagram responses: {result['ig_responses']}")
    print(f"   SMS responses: {result['sms_responses']}")
    print(f"   Instagram comment responses: {result['comment_responses']}")

    if result["ig_responses"] == 0 and result["sms_responses"] == 0 and result["comment_responses"] == 0:
        print("\n⚠️  No responses found. Please run collection scripts first:")
        print("   - python collect_instagram_responses.py")
        print("   - python collect_sms_responses.py")
        print("   - python collect_instagram_comments.py --media-id YOUR_MEDIA_ID")
        return
    
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
    print(f"   💬 Instagram comments: {summary['by_contact_method'].get('instagram_comment', 0)}")
    print("\nOutputs:")
    print(f"   Direct Supabase updates: {result['direct_updates']}")
    print(f"   AI parse queue items: {result['ai_queue_items']}")
    print(f"   AI results loaded: {result['ai_results_loaded']}")
    print(f"   Processed JSON: {result['output_file']}")
    print(f"   AI queue: {result['ai_queue_file']}")
    print(f"   AI results template: {result['ai_results_template_file']}")
    print(f"   Supabase SQL: {result['sql_output_file']}")
    print("=" * 70)
    
    print("\n💡 Next steps:")
    print("   1. Review supabase_response_updates.sql for direct Y/N updates.")
    print("   2. Send ai_parse_queue.json to AI for unclear/change replies, including comments.")
    print("   3. Save AI output as ai_parse_results.json, then rerun this script.")
    print("   4. Review the regenerated SQL before running it in Supabase.")


if __name__ == "__main__":
    main()
