# Instagram Response Workflow

This is the current monthly verification flow for Instagram DMs, AI parsing, and Supabase updates.

## 1. Setup

Activate the project environment before running scripts:

```bash
source venv/bin/activate
```

If dependencies are missing:

```bash
pip install -r requirements.txt
```

Your `.env` should include:

```env
IG_USER=your_instagram_username
IG_PASSWORD=your_instagram_password
CHANGES_FORM_LINK=https://your-form-link.com
```

`dump.json` stores the Instagram session. Keep it unless Instagram login starts failing.

For public draft-post comment collection, use the Instagram Graph API instead of
password login. Add:

```env
IG_GRAPH_ACCESS_TOKEN=your_instagram_graph_api_token
IG_GRAPH_API_VERSION=v23.0
```

The token must be able to read comments for the Instagram professional account
that owns the draft-list media.

## 2. Send DMs

Send a new verification batch from a CSV with `open_mic`, `changes_updates`, and `unique_identifier`:

```bash
python send_instagram_messages.py /path/to/current_mics.csv
```

This creates or updates:

- `ig_sent_messages.json`: sent message log by Instagram handle
- `ig_mic_mapping.json`: Instagram handle to one or more mic IDs

## 3. Collect Responses

Collect replies for the current sent-message round:

```bash
python collect_instagram_responses.py --amount 300
```

The collector fetches DM threads, keeps replies after the original sent timestamp, saves them to `dm_replies.json`, and then automatically runs `process_responses.py`.

Useful collection modes:

```bash
# Preview handles that have no collected response yet
python collect_instagram_responses.py --missing-only --dry-run

# Fetch only handles that do not already have dm_replies.json entries
python collect_instagram_responses.py --missing-only --amount 300

# Fetch one known handle
python collect_instagram_responses.py --username paulzachcomedy --amount 300
```

## 3b. Public Draft Comment Flow

If you want to post a draft open-mics list publicly and let hosts comment
corrections, first generate draft comment codes from the same CSV/export:

```bash
python prepare_instagram_draft_mapping.py /path/to/current_mics.csv
```

This creates:

- `instagram_draft_mic_mapping.json`: public code and username fallback mapping
- `instagram_draft_list.csv`: a posting source with `draft_code` next to each mic

Include the `draft_code` in the public draft list and ask hosts to comment with
it, for example:

```text
OMABC123 now starts at 8 PM
OMDEF456 N
```

After publishing, collect comments from the Instagram Graph API media ID:

```bash
python collect_instagram_comments.py --media-id YOUR_MEDIA_ID
```

The collector writes `ig_comment_responses.json` and automatically reruns
`process_responses.py`. Clear comments such as `OMDEF456 N` produce direct SQL
updates. Update-like or unclear comments go into `ai_parse_queue.json`, with the
matched mic context, before any SQL is generated from AI results.

By default, `collect_instagram_comments.py` processes comments only, so stale DM
or SMS artifacts are not mixed into the comment run. Add
`--include-existing-response-files` if you intentionally want one combined run.

## 4. Processing Outputs

After collection or after manually rerunning:

```bash
python process_responses.py
```

The processor writes:

- `processed_responses.json`: structured response summary
- `ai_parse_queue.json`: ambiguous/change replies that need AI or human parsing
- `ai_parse_results_template.json`: fill-in template for AI results
- `ai_parse_results.json`: parsed AI results, if you or Codex created it
- `supabase_response_updates.sql`: SQL updates for Supabase

The direct parser only maps clear responses directly:

- `Y`, `Yes`, numbered `1 Y` -> direct confirmed update
- `N`, numbered `1 N` -> direct confirmed inactive update
- comment-code variants such as `OMABC123 Y` or `OMABC123 N`
- update-like text such as "now starts at 7:15", "every other Wednesday", "sign up required" -> AI queue

AI queue items include `message_history`, newest first, so follow-up messages can be interpreted with earlier formatted replies.

## 5. Status Meanings

`aug_verification_status` values:

- `responded_confirmed`: host confirmed and no update is needed
- `responded_changes`: host responded and an update is needed
- `responded_unclear`: host responded, but status/changes cannot be safely determined
- `no_response`: valid Instagram handle but no response collected
- `not_sent`: no valid Instagram handle

`last_verified` is stamped as `MM/DD/YY` only for:

- `responded_confirmed`
- `responded_changes`

It is not updated for:

- `responded_unclear`
- `no_response`
- `not_sent`

## 6. AI Parse Review

When `ai_parse_queue.json` has items, parse them into `ai_parse_results.json`.

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

Supported `updates` fields include:

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

After editing or creating `ai_parse_results.json`, regenerate SQL:

```bash
python process_responses.py
```

## 7. Review And Run SQL

Always review the generated SQL before running it:

```bash
less supabase_response_updates.sql
```

Useful checks:

```bash
grep -n "AI note" supabase_response_updates.sql
grep -n "responded_unclear" supabase_response_updates.sql
grep -n "needs" ai_parse_results.json
```

Then run `supabase_response_updates.sql` in the Supabase SQL editor.

Or dry-run/apply through the Supabase API:

```bash
python apply_response_updates.py
python apply_response_updates.py --apply
```

The generated SQL updates existing rows by text `unique_identifier`; it does not insert brand-new mics. Handle new mic additions separately.

## 8. Full-List Statuses

The response SQL only updates mics that have collected replies or AI results.

To classify the full monthly list, including `no_response` and `not_sent`, run:

```bash
python prepare_monthly_verification_updates.py /path/to/current_export.csv
```

Preview the Supabase CSV updater:

```bash
python update_monthly_verification_supabase.py august_supabase_updates.csv
```

Apply only after review:

```bash
python update_monthly_verification_supabase.py august_supabase_updates.csv --apply
```

## 9. Same Round Vs New Round

For more responses from the same DM round, keep using the same:

- `ig_sent_messages.json`
- `ig_mic_mapping.json`
- `dm_replies.json`

For a new monthly round, archive the previous artifacts first:

```bash
mkdir -p response_runs/aug_2026_after_first_push
cp dm_replies.json processed_responses.json ai_parse_queue.json ai_parse_results.json supabase_response_updates.sql ig_sent_messages.json ig_mic_mapping.json response_runs/aug_2026_after_first_push/
```

Then send the next batch.

## 10. Common Problems

If you see `No module named 'instagrapi'`, activate the venv:

```bash
source venv/bin/activate
```

If Instagram returns `login_required`, log into Instagram in a browser/app, clear any security challenge, then rerun collection.

If Supabase says `operator does not exist: text = uuid`, regenerate SQL with the current `process_responses.py`; current SQL compares `unique_identifier` as text.
