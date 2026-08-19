# Quick Start Guide

Get the Comediq monthly open mic verification flow running quickly.

For the full Instagram response workflow, see [INSTAGRAM_RESPONSE_WORKFLOW.md](INSTAGRAM_RESPONSE_WORKFLOW.md).

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
CHANGES_FORM_LINK=https://your-form-link.com

# Optional Instagram public-post comment collection
IG_GRAPH_ACCESS_TOKEN=your_instagram_graph_api_token
IG_GRAPH_API_VERSION=v23.0

# Optional SMS/Twilio
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

## Send Instagram DMs

Your CSV should include at least:

- `unique_identifier`
- `open_mic`
- `changes_updates`
- `day`
- `start_time`

Send grouped DMs:

```bash
source venv/bin/activate
python send_instagram_messages.py /path/to/current_mics.csv --dry-run
python send_instagram_messages.py /path/to/current_mics.csv --yes
```

By default, the sender builds all message batches, waits 5-15 seconds between
individual DMs, and waits 30-60 minutes between batches. It also writes
`ig_batch_plan.json` so you can inspect the constructed batches.

Common tuning options:

```bash
python send_instagram_messages.py /path/to/current_mics.csv --yes --batch-size 25 --message-delay-min 5 --message-delay-max 15 --batch-delay-min 30 --batch-delay-max 60
```

This writes:

- `ig_sent_messages.json`
- `ig_mic_mapping.json`
- `ig_batch_plan.json`

## Collect Responses

Collect replies for the current sent-message round:

```bash
python collect_instagram_responses.py --amount 300
```

Only collect handles that do not already have a response entry:

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

## Process And Review

You can rerun processing anytime:

```bash
python process_responses.py
```

Main outputs:

- `processed_responses.json`: structured summary
- `ai_parse_queue.json`: unclear/change replies needing AI or review
- `ai_parse_results_template.json`: fill-in format for AI results
- `ai_parse_results.json`: parsed AI results
- `supabase_response_updates.sql`: SQL to review and run in Supabase

If `ai_parse_queue.json` has items, parse/edit `ai_parse_results.json`, then rerun:

```bash
python process_responses.py
```

## Instagram List Comments

For public list posts, generate the internal username mapping:

```bash
python prepare_instagram_comment_mapping.py /path/to/current_mics.csv
```

This writes:

- `instagram_comment_mic_mapping.json`: Instagram username to mic ID mapping
- `instagram_comment_mic_mapping_review.csv`: handles to review, especially multi-mic accounts

After the post is live, collect comments from the Instagram Graph API media ID:

```bash
python collect_instagram_comments.py --media-id YOUR_MEDIA_ID
```

This writes `ig_comment_responses.json`, then reruns `process_responses.py`.
Clear `Y`/`N` comments can become direct SQL updates; corrections go into
`ai_parse_queue.json` for parsing/review. Updates stamp the monthly verification
status and `last_verified` the same way as DM responses.

## Supabase Update

Review generated SQL:

```bash
less supabase_response_updates.sql
grep -n "AI note" supabase_response_updates.sql
grep -n "responded_unclear" supabase_response_updates.sql
```

Then run `supabase_response_updates.sql` in the Supabase SQL editor.

The SQL updates existing rows only. Add brand-new mics separately.

Or use the Supabase API apply helper:

```bash
python apply_response_updates.py
python apply_response_updates.py --apply
```

## Status Values

- `responded_confirmed`: host confirmed; no update needed
- `responded_changes`: update needed
- `responded_unclear`: response received but not safely interpretable
- `no_response`: valid Instagram handle but no response collected
- `not_sent`: no valid Instagram handle

`last_verified` uses `MM/DD/YY` and is only stamped for `responded_confirmed` and `responded_changes`.

## Full Monthly List

To classify all mics, including `no_response` and `not_sent`:

```bash
python prepare_monthly_verification_updates.py /path/to/current_export.csv
python update_monthly_verification_supabase.py august_supabase_updates.csv
```

Apply after review:

```bash
python update_monthly_verification_supabase.py august_supabase_updates.csv --apply
```
