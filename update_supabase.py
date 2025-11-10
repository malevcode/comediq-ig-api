import os
import json
import sys
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import List


def get_active_mic_ids(processed_responses_file: str = "processed_responses.json") -> List[str]:
    """
    Extract mic IDs with verification_status: true from processed_responses.json supabase_updates field
    
    Args:
        processed_responses_file: Path to the processed responses JSON file
        
    Returns:
        List of mic identifiers that are active (verification_status: true)
    """
    try:
        with open(processed_responses_file, 'r') as f:
            data = json.load(f)
        
        active_ids = []
        
        # Use the supabase_updates field which contains database-ready format
        supabase_updates = data.get('supabase_updates', [])
        
        for update_entry in supabase_updates:
            # Only include mics with verification_status: true (active)
            if update_entry.get('verification_status') is True:
                active_ids.append(update_entry.get('mic_identifier'))
        
        print(f"Found {len(active_ids)} active mics")
        return active_ids
        
    except FileNotFoundError:
        print(f"❌ File {processed_responses_file} not found")
        return []
    except Exception as e:
        print(f"❌ Error reading processed responses: {e}")
        return []


def get_inactive_mic_ids(processed_responses_file: str = "processed_responses.json") -> List[str]:
    """
    Extract mic IDs with verification_status: false from processed_responses.json supabase_updates field
    
    Args:
        processed_responses_file: Path to the processed responses JSON file
        
    Returns:
        List of mic identifiers that are inactive (verification_status: false)
    """
    try:
        with open(processed_responses_file, 'r') as f:
            data = json.load(f)
        
        inactive_ids = []
        
        # Use the supabase_updates field which contains database-ready format
        supabase_updates = data.get('supabase_updates', [])
        
        for update_entry in supabase_updates:
            # Only include mics with verification_status: false (inactive)
            if update_entry.get('verification_status') is False:
                inactive_ids.append(update_entry.get('mic_identifier'))
        
        print(f"Found {len(inactive_ids)} inactive mics")
        return inactive_ids
        
    except FileNotFoundError:
        print(f"❌ File {processed_responses_file} not found")
        return []
    except Exception as e:
        print(f"❌ Error reading processed responses: {e}")
        return []


if __name__ == "__main__": 
    # Get filename from command line argument or use default
    filename = sys.argv[1] if len(sys.argv) > 1 else "processed_responses.json"
    
    load_dotenv()
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)

    active_ids = get_active_mic_ids(filename)
    if active_ids: 
        response = (
            supabase.table("open_mics_historical")
                .update({"active": True, "last_verified": "11/10"})
                .in_("unique_identifier", active_ids)
                .execute()
        )
        # print(response.data)
        # print(response.error)

    inactive_ids = get_inactive_mic_ids(filename)
    if inactive_ids: 
        response = (
            supabase.table("open_mics_historical")
                .update({"active": False, "last_verified": "11/10"})
                .in_("unique_identifier", inactive_ids)
                .execute()
        )
