# Quick Start Guide

Get up and running with the Comediq Open Mic Verification System in 5 minutes.

## Prerequisites

- Python 3.8 or higher
- Instagram account credentials
- Twilio account (for SMS functionality)

## Setup (One-time)

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file in the project root:

```env
# Instagram Credentials
IG_USER=your_instagram_username
IG_PASSWORD=your_instagram_password

# Twilio Credentials (for SMS only)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Optional: Changes form link
CHANGES_FORM_LINK=https://your-form-link.com
```

## Basic Workflow

### Option A: Instagram Messages

```bash
# 1. Send messages
python send_instagram_messages.py active_to_confirm_NY.csv

# 2. Collect responses (later)
python collect_instagram_responses.py

# 3. Process responses
python process_responses.py
```

### Option B: SMS Messages

```bash
# 1. Send messages
python send_sms_messages.py active_to_confirm_NY.csv

# 2. Collect responses (later)
python collect_sms_responses.py

# 3. Process responses
python process_responses.py
```

## What Each Script Does

| Script | Purpose | When to Use |
|--------|---------|-------------|
| `send_instagram_messages.py` | Send DMs to Instagram handles | Initial outreach |
| `send_sms_messages.py` | Send SMS to phone numbers | Initial outreach |
| `collect_instagram_responses.py` | Fetch DM replies | After waiting for responses |
| `collect_sms_responses.py` | Fetch SMS replies | After waiting for responses |
| `process_responses.py` | Organize responses | After collection |

## Output Files

- `ig_sent_messages.json` - Log of sent Instagram DMs
- `twilio_sent_messages.json` - Log of sent SMS messages
- `dm_replies.json` - Collected Instagram responses
- `twilio_responses.json` - Collected SMS responses
- `processed_responses.json` - **Final organized output** ⭐

## Next Steps

After running `process_responses.py`, you'll have `processed_responses.json` with all your verification data ready to update your Supabase table.

## Need Help?

See the full [README.md](README.md) for detailed documentation and troubleshooting.

