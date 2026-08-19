# Comediq Open Mic Verification System

Automated monthly open mic verification through Instagram DMs and SMS, with multi-mic host grouping, timestamp-filtered response collection, AI-assisted parsing for unclear replies, and reviewable Supabase SQL output.

For the detailed current Instagram workflow, see [INSTAGRAM_RESPONSE_WORKFLOW.md](INSTAGRAM_RESPONSE_WORKFLOW.md).

## Overview

This system helps you:

- Send one grouped verification DM per Instagram host.
- Track which mic IDs were sent to each handle.
- Collect only replies that happened after your sent message.
- Map clear formatted replies directly to mics.
- Save change/unclear replies into an AI parsing queue.
- Map AI results back to original mic IDs.
- Generate SQL for Supabase updates.
- Classify full-list statuses such as `no_response` and `not_sent`.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `.env`:

```env
IG_USER=your_instagram_username
IG_PASSWORD=your_instagram_password

# Optional SMS/Twilio
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Optional link included in Instagram messages
CHANGES_FORM_LINK=https://your-form-link.com

# Optional public draft-post comment collection
IG_GRAPH_ACCESS_TOKEN=your_instagram_graph_api_token
IG_GRAPH_API_VERSION=v23.0
```

`dump.json` stores the Instagram session after login. Keep it unless Instagram login starts failing.

## Input CSV

Instagram sending expects:

| Column | Required | Purpose |
|---|---:|---|
| `unique_identifier` | Yes | Mic ID used to update Supabase |
| `open_mic` | Yes | Mic name shown in the DM |
| `changes_updates` | Yes | Instagram handle |
| `day` | Recommended | Day shown in the DM |
| `start_time` | Recommended | Start time shown in the DM |
| `venue_name` | Optional | Venue context |
| `location` | Optional | Address context |

SMS scripts use `sms_response` for phone numbers.

## Core Scripts

| Script | Purpose |
|---|---|
| `send_instagram_messages.py` | Send grouped Instagram DMs by valid handle |
| `collect_instagram_responses.py` | Collect Instagram replies and automatically process outputs |
| `prepare_instagram_comment_mapping.py` | Generate internal username-to-mic mapping for comment correction posts |
| `collect_instagram_comments.py` | Collect comments from an Instagram list post and automatically process outputs |
| `process_responses.py` | Build direct updates, AI queue, AI-result mapping, and SQL |
| `apply_response_updates.py` | Dry-run/apply processed direct and reviewed AI updates to Supabase |
| `prepare_monthly_verification_updates.py` | Build full-list monthly status CSVs |
| `update_monthly_verification_supabase.py` | Dry-run/apply full-list monthly CSV updates |
| `send_sms_messages.py` | Send grouped SMS messages |
| `collect_sms_responses.py` | Collect SMS replies |

## Sending Instagram DMs

```bash
source venv/bin/activate
python send_instagram_messages.py /path/to/current_mics.csv --dry-run
python send_instagram_messages.py /path/to/current_mics.csv --yes
```

The sender constructs all batches up front, writes `ig_batch_plan.json`, waits
5-15 seconds between individual DMs, and waits 30-60 minutes between batches by
default.

Tune the pacing when needed:

```bash
python send_instagram_messages.py /path/to/current_mics.csv --yes --batch-size 25 --message-delay-min 5 --message-delay-max 15 --batch-delay-min 30 --batch-delay-max 60
```

This creates or updates:

- `ig_sent_messages.json`
- `ig_mic_mapping.json`
- `ig_batch_plan.json`

The message format asks for:

- `Y` / `Yes` if active with no changes
- `N` / `No` if inactive
- `Changes` if updates are needed
- numbered responses for hosts with multiple mics, such as `1 Y`, `2 N`, `3 Changes`

## Collecting Instagram Responses

Collect all current-round replies:

```bash
python collect_instagram_responses.py --amount 300
```

Collect only sent handles that do not already have a `dm_replies.json` entry:

```bash
python collect_instagram_responses.py --missing-only --amount 300
```

Preview missing handles without logging into Instagram:

```bash
python collect_instagram_responses.py --missing-only --dry-run
```

Collect one handle:

```bash
python collect_instagram_responses.py --username paulzachcomedy --amount 300
```

Collection writes `dm_replies.json` and automatically runs `process_responses.py`.

## Collecting Public List Comments

To post the normal list graphic and let hosts comment corrections, first
generate the internal username mapping from the same CSV/export:

```bash
python prepare_instagram_comment_mapping.py /path/to/current_mics.csv
```

This creates `instagram_comment_mic_mapping.json` and
`instagram_comment_mic_mapping_review.csv`. The poster does not need public
codes; comments are matched by the Instagram username that left the comment.

After the post is live, collect comments by media ID:

```bash
python collect_instagram_comments.py --media-id YOUR_MEDIA_ID
```

Comments are written to `ig_comment_responses.json` and processed into the same
`ai_parse_queue.json` and `supabase_response_updates.sql` workflow as DMs/SMS.
The collector uses the Instagram Graph API token in `IG_GRAPH_ACCESS_TOKEN`.
Comment collection processes comments only by default; add
`--include-existing-response-files` to combine with current DM/SMS artifacts.

Single-mic usernames can produce direct updates. Clear confirmations update the
monthly verification status and `last_verified` the same way DM responses do.
Correction comments from usernames that map to multiple mics are queued with
candidate mic context for review instead of guessing.

## Processing Outputs

You can rerun processing anytime:

```bash
python process_responses.py
```

It writes:

- `processed_responses.json`: structured response summary
- `ai_parse_queue.json`: unclear/change replies that need AI or human parsing
- `ai_parse_results_template.json`: template for parsed queue results
- `ai_parse_results.json`: parsed queue results, if present
- `supabase_response_updates.sql`: reviewable SQL for Supabase

The processor re-parses raw message text on every run. It does not blindly trust stale `parsed_response` values stored in `dm_replies.json`.

## Direct Mapping Vs AI Queue

Directly mapped:

- `Y`, `Yes`, `Yup`
- `N`, `No`, `Inactive`
- clear numbered responses such as `1 Y`, `2 N`

Queued for AI/human parsing:

- "It now starts at 7:15"
- "Every other Wednesday"
- "Sign up required"
- "We added a Sunday 6pm mic"
- "This is the full schedule"
- non-text or unclear replies

AI queue items include `message_history` in newest-first order, so a later ambiguous message can be interpreted with earlier formatted replies.

## AI Parse Results

When `ai_parse_queue.json` has items, create or edit `ai_parse_results.json`.

Each result should keep `queue_id` and `mic_identifier` unchanged:

```json
{
  "queue_id": "original_queue_id",
  "mic_identifier": "original_mic_id",
  "verification_status": "responded_changes",
  "active": true,
  "updates": {
    "start_time": "7:15 PM"
  },
  "confidence": 0.98,
  "needs_human_review": false,
  "notes": "Host says it now starts at 7:15."
}
```

Supported `updates` fields:

- `active`
- `changes_updates`
- `cost`
- `day`
- `frequency`
- `frequency_custom_text`
- `hosts_organizers`
- `latest_end_time`
- `location`
- `open_mic`
- `other_rules`
- `sign_up_instructions`
- `signup_url`
- `sms_response`
- `stage_time`
- `start_time`
- `venue_name`

After editing AI results:

```bash
python process_responses.py
```

## Status Values

Monthly verification columns such as `aug_verification_status` use:

| Status | Meaning |
|---|---|
| `responded_confirmed` | Host confirmed; no update needed |
| `responded_changes` | Host responded and an update is needed |
| `responded_unclear` | Host responded but status/changes cannot be safely determined |
| `no_response` | Valid Instagram handle but no response collected |
| `not_sent` | No valid Instagram handle |

`last_verified` uses `MM/DD/YY`.

`last_verified` is only updated for:

- `responded_confirmed`
- `responded_changes`

It is not updated for:

- `responded_unclear`
- `no_response`
- `not_sent`

## Supabase SQL

Review generated SQL before running:

```bash
less supabase_response_updates.sql
grep -n "AI note" supabase_response_updates.sql
grep -n "responded_unclear" supabase_response_updates.sql
```

Then run `supabase_response_updates.sql` in the Supabase SQL editor.

Or dry-run/apply the same processed response payloads through the Supabase API:

```bash
python apply_response_updates.py
python apply_response_updates.py --apply
```

Notes:

- The SQL updates existing rows by text `unique_identifier`.
- It does not insert brand-new mics.
- New mics, true deletions, and complicated schedule exceptions require separate review.

## Full Monthly List

The response SQL only touches mics that have collected replies or AI results.

To classify every row in the current monthly export, including `no_response` and `not_sent`:

```bash
python prepare_monthly_verification_updates.py /path/to/current_export.csv
```

Dry-run the Supabase CSV updater:

```bash
python update_monthly_verification_supabase.py august_supabase_updates.csv
```

Apply after review:

```bash
python update_monthly_verification_supabase.py august_supabase_updates.csv --apply
```

## Same Round Vs New Round

For more replies from the same DM round, keep using:

- `ig_sent_messages.json`
- `ig_mic_mapping.json`
- `dm_replies.json`

Use missing-only collection for later passes:

```bash
python collect_instagram_responses.py --missing-only --amount 300
```

Before a new monthly round, archive current artifacts:

```bash
mkdir -p response_runs/aug_2026_after_push
cp dm_replies.json processed_responses.json ai_parse_queue.json ai_parse_results.json supabase_response_updates.sql ig_sent_messages.json ig_mic_mapping.json response_runs/aug_2026_after_push/
```

Then send the next batch.

## SMS Workflow

SMS still follows the older send/collect/process pattern:

```bash
python send_sms_messages.py /path/to/current_mics.csv
python collect_sms_responses.py
python process_responses.py
```

SMS responses are read from `twilio_responses.json` when present.

## Troubleshooting

### `No module named 'instagrapi'`

Activate the venv:

```bash
source venv/bin/activate
```

### Instagram `login_required`

Log into Instagram in a browser/app, clear any security challenge, then rerun collection.

### Missed Replies

Use:

```bash
python collect_instagram_responses.py --missing-only --dry-run
python collect_instagram_responses.py --missing-only --amount 300
```

Or target one handle:

```bash
python collect_instagram_responses.py --username handle --amount 300
```

### Supabase `text = uuid` Error

Regenerate SQL with the current processor:

```bash
python process_responses.py
```

The current SQL compares `unique_identifier` as text.

## Security

- Keep credentials in `.env`.
- Do not commit generated response artifacts.
- `dump.json`, `*.json`, `*.csv`, generated SQL, and response archives are ignored by `.gitignore`.
