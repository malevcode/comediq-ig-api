# Comediq Open Mic Verification System

Automated system for monthly open mic verification via Instagram DMs and SMS with multi-mic support and database integration.

## 🎯 Overview

Automates monthly verification by:
- **Smart Routing**: Instagram vs SMS based on contact preferences
- **Multi-Mic Support**: Groups mics by host, handles numbered responses ("1 Y, 2 N, 3 Changes") 
- **Timestamp Filtering**: Only collects new responses after sending messages
- **Database Ready**: Processes responses for Supabase integration
- **Configurable Files**: Custom file paths for different campaigns

## 📁 Core Files

**Messaging Systems:**
- `ig_messaging.py` - Instagram DM system with timezone-aware filtering
- `twilio_messaging.py` - SMS system with E.164 formatting

**Scripts:**
- `send_*.py` - Send messages (takes CSV file only)
- `collect_*_responses.py` - Collect responses (supports custom file paths)
- `process_responses.py` - Convert to database format
- `update_supabase.py` - Push active/inactive mics to database

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

**For Supabase (database updates):**
```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
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

All send scripts take only a CSV file - they create tracking files automatically.

```bash
# Instagram (Instagram-preferred contacts)
python send_instagram_messages.py [csv_file]

# SMS (SMS-preferred contacts) 
python send_sms_messages.py [csv_file]

# SMS Fallback via Instagram (when Twilio is down)
python send_dual_contact_instagram_messages.py [csv_file]
```

**Key Features:**
- **Multi-mic grouping** by contact (Instagram handle or phone)
- **E.164 phone formatting** for SMS (+15551234567)
- **Rate limiting** to avoid platform restrictions
- **Timezone-aware** message tracking for response filtering

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

Collect scripts support custom file paths for different campaigns:

```bash
# Use default files
python collect_instagram_responses.py
python collect_sms_responses.py

# Use custom files  
python collect_instagram_responses.py custom_sent_messages.json custom_mic_mapping.json
python collect_sms_responses.py custom_twilio_sent.json custom_twilio_mapping.json
```

**Smart Filtering:**
- **Timezone-aware**: Only collects responses after your sent messages (no old thread history)
- **Exact matching**: "Y" responses now parse correctly (was mapping to null)
- **UTC conversion**: Handles local time differences properly

## 🔄 Processing & Database Updates

```bash
# Process responses to database format
python process_responses.py

# Update Supabase with active/inactive mics
python update_supabase.py [processed_responses_file]
```

**Response Processing:**
- **Per-mic entries**: One database row per mic (not per contact)
- **Multi-mic parsing**: "1 Y, 2 N, 3 Changes" → 3 separate entries  
- **Status conversion**: Y→true, N→false, Changes→null
- **Supabase integration**: Extract active/inactive mic IDs for database updates

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

```bash
# 1. Send messages (choose platform)
python send_instagram_messages.py mics.csv
python send_sms_messages.py mics.csv

# 2. Wait for responses

# 3. Collect responses (timestamp-filtered)
python collect_instagram_responses.py
python collect_sms_responses.py

# 4. Process for database  
python process_responses.py

# 5. Update Supabase
python update_supabase.py processed_responses.json
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

## ⚠️ Key Features & Notes

**Recent Improvements:**
- ✅ **Fixed "Y" parsing**: Single-character responses now parse correctly
- ✅ **Timezone-aware filtering**: Only new responses collected (no old history)
- ✅ **Configurable file paths**: Custom files for different campaigns  
- ✅ **Supabase integration**: Direct database updates for active/inactive mics
- ✅ **Security audit**: Removed exposed credentials and phone numbers

**Data Safety:**
- **Timestamp filtering**: Only collects responses after sent messages
- **Merge operations**: Scripts don't overwrite existing data
- **Individual tracking**: One database entry per mic (not per contact)

## 🛠️ Troubleshooting

### Common Issues

**Instagram:**
- Rate limits: Wait 1+ hour between runs
- Login: May require 2FA on first use
- Handles: Verify in CSV `changes_updates` column

**SMS:**  
- Phone format: Auto-converts to E.164 (+15551234567)
- Twilio auth: Check credentials in `.env`
- Delivery fails: Use Instagram fallback script

**Responses:**
- "Y" not parsing: ✅ Fixed in latest version
- Old messages: ✅ Now filters by timestamp  
- Multi-mic: Use "1 Y, 2 N, 3 Changes" format

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

Check console output and generated JSON files for debugging.

## 🎓 Advanced Usage

**Custom File Paths:**
```bash
# Different campaigns
python collect_instagram_responses.py campaign_nov_sent.json campaign_nov_mapping.json
```

**Batch Processing:**
```bash
for file in *.csv; do
  python send_instagram_messages.py "$file"
  sleep 300  # Wait between batches
done
```

**Message Templates:**
- Edit `create_message_for_host()` in send scripts
- Customize `parse_response()` in messaging systems

---
*Internal Comediq tool - See console output for detailed logging*
