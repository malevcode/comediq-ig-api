# Comediq Open Mic Verification System

A streamlined system for sending verification messages to open mic hosts via Instagram DMs and SMS, collecting responses, and processing them into database-ready format with support for multiple mics per contact.

## 🎯 Overview

This system automates monthly open mic verification by:
1. **Contact Preference Filtering**: Automatically routes contacts to SMS or Instagram based on preferences
2. **Multi-Mic Support**: Groups multiple mics per host and handles numbered responses (e.g., "1 Y, 2 N, 3 Changes")
3. **SMS Fallback**: Reaches SMS-preferred contacts via Instagram when Twilio is unavailable
4. **Response Processing**: Converts Y/N/Changes responses to True/False/None for database updates
5. **Merge-Safe Operations**: Multiple scripts can run without overwriting each other's data

## 📁 Project Structure

```
.
├── ig_messaging.py                        # Core Instagram messaging system
├── twilio_messaging.py                    # Core SMS messaging system  
├── send_instagram_messages.py             # Send to Instagram-preferred contacts
├── send_sms_messages.py                   # Send to SMS-preferred contacts
├── send_dual_contact_instagram_messages.py # SMS fallback via Instagram
├── collect_instagram_responses.py         # Collect Instagram DM replies
├── collect_sms_responses.py              # Collect SMS replies
├── process_responses.py                  # Process into database format
├── requirements.txt                      # Python dependencies
├── test.csv                             # Sample test data
└── README.md                            # This file
```

## 🚀 Quick Start

### 1. Environment Setup

Create a `.env` file in the project root with the following variables:

**For Instagram:**
```
IG_USER=your_instagram_username
IG_PASSWORD=your_instagram_password
```

**For SMS (Twilio):**
```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

**Optional (for changes form):**
```
CHANGES_FORM_LINK=https://your-form-link.com
```

### 2. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Prepare Your Data

Ensure your CSV file has the following columns:
- `open_mic`: Name of the open mic
- `changes_updates`: Instagram handle (for Instagram messaging)
- `sms_response`: Phone number (for SMS messaging)
- `day`: Day of the week
- `start_time`: Start time
- `venue_name`: Venue name
- `location`: Full address
- `unique_identifier`: Unique ID for each mic

## 📤 Sending Messages

### Instagram Messages (Instagram-Preferred Contacts)

```bash
python send_instagram_messages.py [path/to/your/file.csv]
```

**Contact Filter**: Targets contacts where `sms_response` is missing/refused AND `changes_updates` has Instagram handle.

**Features:**
- Groups multiple mics by Instagram handle
- Sends one message per host listing all their mics
- Personalizes message with mic names, times, and venues
- Rate limiting to avoid Instagram restrictions
- **Merges** with existing mic mappings (doesn't overwrite)

### SMS Messages (SMS-Preferred Contacts)

```bash
python send_sms_messages.py [path/to/your/file.csv]  
```

**Contact Filter**: Targets contacts where `sms_response` has valid phone number (not refused/N/A).

**Features:**
- Groups multiple mics by phone number  
- E.164 phone formatting (+1 for US numbers)
- Handles various phone formats: (555) 123-4567, 555-123-4567, etc.
- Uses Twilio for reliable SMS delivery
- Rate limiting and error handling
- **Merges** with existing mic mappings (doesn't overwrite)

### SMS Fallback via Instagram

```bash
python send_dual_contact_instagram_messages.py [path/to/your/file.csv]
```

**Use Case**: When Twilio SMS service is down or unavailable.

**Contact Filter**: Targets contacts with BOTH valid `sms_response` AND `changes_updates` (dual contact capability).

**Features:**
- Reaches SMS-preferred contacts via Instagram fallback
- Explains in message that SMS system is temporarily down  
- Same multi-mic grouping and response handling
- **Merges** with existing mappings from other scripts

## 💬 Message Format

Messages are automatically personalized with:
- **Current month name** (e.g., "September mic list")
- **All mics listed by the host** with day, time, and venue
- **Clear instructions** for response
- **Optional changes form link** (if configured in `.env`)

### Example Message

**For hosts with multiple mics:**
```
Hey @username! It's Adam from Comediq! I'm doing the monthly check in to update our November mic list. For each mic, reply with the number and status:

Reply format: [number] Y/N/Changes

Here's what we have listed:

1. Bushwick Comedy Club (Tuesday at 7:00 PM)
2. Another Mic (Wednesday at 8:00 PM)

Please respond with updates for each mic. Thanks!
```

**For hosts with a single mic:**
```
Hey @username! It's Adam from Comediq! I'm doing the monthly check in to update our November mic list. Please reply:

Reply: Y (active), N (not active), or Changes (has updates)

Here's what we have listed:

1. My Mic Name (Monday at 8:00 PM)

Please respond with updates for each mic. Thanks!
```

### Response Format & Multi-Mic Support

**Single Mic Response:**
- Reply: `Y`, `N`, or `Changes`
- Applied to their one mic

**Multiple Mic Response:**  
- Numbered format: `1 Y`, `2 N`, `3 Changes` (one per line)
- Simple format: `Y` (applied to ALL their mics)

**Status Conversion:**
- `Y`/`Yes`/`Active` → `True` (active)  
- `N`/`No`/`Inactive` → `False` (inactive)
- `C`/`Changes` → `None` (needs updates)

**Example Multi-Mic Response:**
```
1 Y
2 N  
3 Changes
```

This creates individual database entries for each mic with their respective statuses.

See [RESPONSE_FORMAT.md](RESPONSE_FORMAT.md) for detailed parsing documentation.

## 📥 Collecting Responses

After hosts respond to your messages:

### Collect Instagram Responses

```bash
python collect_instagram_responses.py
```

This fetches DM replies from Instagram and saves them to `dm_replies.json`.

### Collect SMS Responses

```bash
python collect_sms_responses.py
```

This fetches incoming SMS messages and saves them to `twilio_responses.json`.

## 🔄 Processing Responses

Once you've collected responses, process them into database-ready format:

```bash
python process_responses.py
```

**Output:** `processed_responses.json`

**Individual Mic Processing:**
- Creates **one database entry per mic** (not per contact)
- Handles multi-mic responses: "1 Y, 2 N, 3 Changes" → 3 separate entries
- Uses **newest message** from Instagram API (messages[0])

**Status Conversion:**
- `Y`/`Yes`/`Active` → `true` (boolean)
- `N`/`No`/`Inactive` → `false` (boolean)  
- `C`/`Changes` → `null` (needs updates)

**Database Schema:**
```json
{
  "comediq_id": "mic_identifier_string",
  "status": "true|false|null",
  "response_timestamp": "ISO_timestamp"
}
```

## 📊 Response Processing Features

**Multi-Platform Support:**
- Instagram DM responses via Meta Basic Display API
- SMS responses via Twilio API
- **Message Ordering**: Uses newest-first Instagram API ordering (messages[0])

**Response Parsing:**
- **Y/Yes/Active** → Database: `true` (mic is active)
- **N/No/Inactive** → Database: `false` (mic inactive)  
- **C/Changes** → Database: `null` (needs updates)

**Multi-Mic Intelligence:**
- Numbered responses: "1 Y, 2 N, 3 Changes" creates 3 database entries
- Simple responses: "Y" applied to ALL mics for that contact
- **Individual tracking**: Each mic gets separate database row

## 🔄 Complete Workflow

```
1. Prepare CSV with open mic data
   ↓
2. Choose sending method:
   ├─ send_instagram_messages.py (Instagram-preferred contacts)
   ├─ send_sms_messages.py (SMS-preferred contacts)  
   └─ send_dual_contact_instagram_messages.py (SMS fallback via IG)
   ↓
3. Wait for host responses
   ↓
4. Collect responses:
   ├─ collect_instagram_responses.py (from Instagram DMs)
   └─ collect_sms_responses.py (from Twilio SMS)
   ↓
5. Process to database format:
   └─ process_responses.py → processed_responses.json
   ↓
6. Upload processed_responses.json to Supabase
```

## 📋 Database Output Format

### processed_responses.json Structure

**Individual Mic Entries:**
```json
[
  {
    "comediq_id": "amazing_mic_comedy_club_monday",
    "status": true,
    "response_timestamp": "2024-01-15T08:00:00Z"
  },
  {
    "comediq_id": "another_mic_tuesday", 
    "status": false,
    "response_timestamp": "2024-01-15T08:00:00Z"
  },
  {
    "comediq_id": "third_mic_changes_needed",
    "status": null,
    "response_timestamp": "2024-01-15T08:00:00Z" 
  }
]
```

**Multi-Mic Response Example:**
- Host response: "1 Y, 2 N, 3 Changes" 
- Creates 3 separate database entries as shown above
- Each mic gets individual `comediq_id` and `status`
```

## ⚠️ Important Notes

### Data Safety
- **Merge Operations**: All scripts merge with existing data (no overwrites)
- **Message Ordering**: Uses Instagram's newest-first API ordering (messages[0])
- **Phone Formatting**: E.164 standard (+1 for US numbers)
- **Individual Tracking**: One database entry per mic, not per contact

### Rate Limiting & Reliability  
- **Instagram**: Automatic delays to avoid rate limits, session persistence
- **SMS**: Twilio rate limiting, E.164 phone validation
- **Fallback**: SMS contacts reachable via Instagram when Twilio is down
- **Error Handling**: Scripts continue on errors and report failures

### Security & Privacy
- **Never commit**: `.env`, `dump.json`, response files, or session data
- **Instagram 2FA**: First login may require verification; saves session
- **Phone Privacy**: E.164 normalization for consistent formatting

## 🛠️ Troubleshooting

### Instagram Issues

**"User not found"**
- Verify Instagram handle exists and is public
- Check for typos in CSV `changes_updates` column

**"Login failed"** 
- Verify `INSTAGRAM_USERNAME`/`INSTAGRAM_PASSWORD` in `.env`
- Instagram may require 2FA verification on first login
- Check if account has restrictions

**"Rate limited"**
- Instagram has strict rate limits on DMs
- Scripts include automatic delays - don't reduce them
- Wait 1+ hour before running again

**"Message ordering wrong"**
- Fixed: System now uses newest-first Instagram API ordering
- Uses `messages[0]` for most recent response

### SMS/Twilio Issues

**"Invalid phone number"**
- System auto-formats to E.164: `normalize_phone_to_e164()`
- Handles: (555) 123-4567 → +15551234567
- Check for international numbers (non-US)

**"Twilio authentication failed"**
- Verify `TWILIO_ACCOUNT_SID`/`TWILIO_AUTH_TOKEN` in `.env`
- Check Twilio account is active and funded

**"SMS delivery failed"**
- Use SMS fallback: `send_dual_contact_instagram_messages.py`
- Reaches SMS contacts via Instagram when Twilio is down

### CSV & Data Issues

**"CSV file not found"**
- Provide absolute path: `/full/path/to/file.csv`
- Check current directory with `pwd`
- Verify file extension is `.csv`

**"Missing columns"**
- Required: `unique_identifier`, `changes_updates`, `sms_response`
- Force string loading: `dtype=str` prevents phone number corruption
- Check column names match exactly (case-sensitive)

**"Phone numbers not loading correctly"**
- CSV loads phone numbers as strings to preserve leading zeros
- Format (555) 123-4567 handled by `normalize_phone_to_e164()`
- Check for international numbers requiring country codes

### Multi-Mic Processing Issues

**"Response not parsing correctly"**
- Numbered format: "1 Y", "2 N", "3 Changes" (one per line)
- Simple format: "Y" applies to ALL mics for that contact
- System creates individual database entries per mic

**"Data overwriting problems"** 
- Fixed: All save operations now merge existing data
- Scripts can run in any order without data loss
- Each script adds to existing `ig_sent_messages.json`

## 🔐 Security

- Store credentials in `.env` file only
- Never commit `.env` to version control
- Review `.gitignore` to ensure sensitive files are excluded
- Rotate credentials periodically

## 📝 CSV Column Reference

| Column Name | Required | Description |
|------------|----------|-------------|
| `unique_identifier` | Yes | Unique ID for each mic |
| `open_mic` | Yes | Name of the open mic |
| `day` | Recommended | Day of the week |
| `start_time` | Recommended | Start time |
| `venue_name` | Recommended | Venue name |
| `location` | Recommended | Full address |
| `changes_updates` | Yes (IG) | Instagram handle (for Instagram messaging) |
| `sms_response` | Yes (SMS) | Phone number (for SMS messaging) |
| `borough` | Optional | Borough/area |

**Multi-Contact Support:**
- Contacts can have both Instagram AND phone number
- System chooses primary contact method based on data availability  
- SMS fallback script reaches SMS contacts via Instagram

## 📞 Support

For issues or questions, please check:
1. This README
2. Error messages in console output
3. Generated JSON files for debugging

## 🎓 Advanced Usage

### Custom Message Templates

**Instagram Messages:**
- Edit `create_message_for_host()` in `send_instagram_messages.py`
- Customize multi-mic vs single-mic message formats
- Update month name, signature, or instructions

**SMS Messages:**
- Modify message template in `send_sms_messages.py`
- Adjust for SMS character limits and formatting

### Response Parsing Customization

**Instagram Parsing:**
- Edit `parse_response_content()` in `process_responses.py`
- Add new response patterns beyond Y/N/Changes
- Handle special cases or alternative formats

**Multi-Mic Logic:**
- Modify numbered response parsing in `process_responses.py`
- Customize how simple responses ("Y") apply to multiple mics

### Script Customization

**Contact Filtering:**
- Adjust SQL-like filtering in each sender script
- Modify dual-contact logic for SMS fallback
- Change priority between SMS vs Instagram preferences

### Batch Processing Multiple Files

```bash
# Process multiple CSV files
for file in *.csv; do
  python send_instagram_messages.py "$file"
done
for file in *.csv; do
  python send_instagram_messages.py "$file"
  sleep 300  # Wait 5 minutes between batches
done
```

## 📜 License

This project is for internal use by Comediq.
