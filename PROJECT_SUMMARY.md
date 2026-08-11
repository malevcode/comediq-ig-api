# Project Summary: Comediq Open Mic Verification System

## Overview

This project verifies open mic listings through Instagram DMs and SMS, maps formatted replies directly to mic records, queues ambiguous replies for AI/human parsing, and generates reviewable Supabase SQL.

The current Instagram workflow is documented in [INSTAGRAM_RESPONSE_WORKFLOW.md](INSTAGRAM_RESPONSE_WORKFLOW.md).

## Core Workflow

```text
CSV export
  -> send Instagram DMs grouped by host
  -> collect responses after sent timestamp
  -> map clear Y/N replies directly
  -> queue changes/unclear replies for AI parsing
  -> generate Supabase SQL
  -> review and run SQL
```

## Main Scripts

### `send_instagram_messages.py`

- Reads a CSV of mics.
- Validates Instagram handles in `changes_updates`.
- Groups multiple mics by host.
- Sends one DM per Instagram handle.
- Writes `ig_sent_messages.json` and `ig_mic_mapping.json`.

### `collect_instagram_responses.py`

- Logs into Instagram through `instagrapi`.
- Fetches recent DM threads.
- Keeps only replies after the original sent timestamp.
- Saves replies to `dm_replies.json`.
- Automatically runs `process_responses.py`.
- Supports targeted and missing-only collection:

```bash
python collect_instagram_responses.py --amount 300
python collect_instagram_responses.py --missing-only --dry-run
python collect_instagram_responses.py --missing-only --amount 300
python collect_instagram_responses.py --username paulzachcomedy --amount 300
```

### `process_responses.py`

- Re-parses raw reply text instead of trusting stale saved parser output.
- Maps clear `Y`, `N`, and numbered `1 Y` / `2 N` responses directly.
- Sends update-like or unclear replies to `ai_parse_queue.json`.
- Adds full `message_history` to AI queue items for context.
- Loads `ai_parse_results.json` when present.
- Generates `supabase_response_updates.sql`.

### `prepare_monthly_verification_updates.py`

- Builds full-list monthly outputs from a current export.
- Classifies `responded_confirmed`, `responded_changes`, `responded_unclear`, `no_response`, and `not_sent`.
- Useful when you need status values for every mic, not only respondents.

### `update_monthly_verification_supabase.py`

- Applies the narrow monthly CSV to Supabase.
- Dry-run by default.
- Stamps `last_verified` only when a row is `responded_confirmed` or `responded_changes`.

## Generated Files

### Sent/Mapping State

- `ig_sent_messages.json`: Instagram handles messaged and sent timestamps
- `ig_mic_mapping.json`: Instagram handle to mic identifiers
- `dump.json`: Instagram session state

### Response Processing

- `dm_replies.json`: collected Instagram replies
- `processed_responses.json`: structured summary of direct and queued responses
- `ai_parse_queue.json`: ambiguous/change replies for AI or human parsing
- `ai_parse_results_template.json`: template for AI parse output
- `ai_parse_results.json`: AI/human parsed queue results
- `supabase_response_updates.sql`: reviewable SQL updates

### Archives

- `response_runs/`: snapshots of response artifacts after important milestones

## Status Values

`aug_verification_status` and monthly equivalents use:

- `responded_confirmed`: host confirmed and no update is needed
- `responded_changes`: host responded and an update is needed
- `responded_unclear`: host responded but the update/status cannot be safely determined
- `no_response`: valid Instagram handle but no response collected
- `not_sent`: no valid Instagram handle

`last_verified` uses `MM/DD/YY`.

`last_verified` is only updated for:

- `responded_confirmed`
- `responded_changes`

It is not updated for:

- `responded_unclear`
- `no_response`
- `not_sent`

## AI Parse Result Shape

Each AI result keeps `queue_id` and `mic_identifier` unchanged:

```json
{
  "queue_id": "instagram_ig_example_micid_hash",
  "mic_identifier": "mic-id",
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

The SQL generator updates existing rows only. Brand-new mics and true deletions still need separate manual handling or insert SQL.

## File Structure

```text
.
├── send_instagram_messages.py
├── collect_instagram_responses.py
├── process_responses.py
├── prepare_monthly_verification_updates.py
├── update_monthly_verification_supabase.py
├── ig_messaging.py
├── twilio_messaging.py
├── INSTAGRAM_RESPONSE_WORKFLOW.md
├── QUICK_START.md
├── README.md
└── PROJECT_SUMMARY.md
```

## Current Best Practice

1. Send DMs with `send_instagram_messages.py`.
2. Collect broadly with `collect_instagram_responses.py --amount 300`.
3. Use `--missing-only` for later same-round collection.
4. Parse `ai_parse_queue.json` into `ai_parse_results.json`.
5. Rerun `process_responses.py`.
6. Review `supabase_response_updates.sql`.
7. Run SQL in Supabase.
8. Archive response artifacts in `response_runs/`.

## Support

- Start with [QUICK_START.md](QUICK_START.md).
- Use [INSTAGRAM_RESPONSE_WORKFLOW.md](INSTAGRAM_RESPONSE_WORKFLOW.md) for the full current Instagram process.
- Check console output and generated JSON/SQL files for debugging.
