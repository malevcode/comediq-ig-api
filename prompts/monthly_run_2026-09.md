# Comediq monthly verification run: September 2026 (end of month)

You are Claude Code running on Adam Malev's Mac inside his local `comediq-ig-api` repo, with his `.env` and Instagram session available. Adam is a solo founder and NYC comedian. Talk to him warmly and directly, give ONE next action at a time, and never use em dashes anywhere (chat, code comments, docs, reports, or DM copy). Use commas, periods, colons, or hyphens instead.

There are two parts. Part A gets this month's host verification blast and the Eye Candy audit done before October 1. Part B turns all of it into a monthly pipeline so nobody ever does this by hand again. Finish Part A fully before starting Part B. If you run low on time or context in Part B, stop cleanly and write the remaining plan into `documentation.md` and `run_state/STATE.md`.

Move fast. Do not front-load questions. Stop ONLY for the two typed gates, a missing input you cannot find, or an Instagram safety tripwire. Everything else, just do it.

---

## 0. Hard rules (never break these)

1. **Two typed gates.** Nothing sends an Instagram DM and nothing writes to the production Supabase database until Adam types the gate word. GATE 1 is `GO` (covers inserting the new mics as inactive rows AND sending the DMs). GATE 2 is `APPLY` (covers writing reply-driven updates). This is Adam's own rule: AI drafts, Adam approves, and a category only runs alone after 3 approved runs in a row with no edits.
2. **KISS.** Smallest possible change. Reuse the existing scripts. Do not rewrite `process_responses.py`, `collect_instagram_responses.py`, or `ig_messaging.py`. Do not refactor. Every change should touch as little code as possible.
3. **This repo is PUBLIC** (and is a fork). Never commit or push: CSV exports, DB snapshots, `dm_replies.json`, `ig_sent_messages.json`, `ig_mic_mapping.json`, `ig_batch_plan.json`, `ai_parse_*.json`, `supabase_response_updates.sql`, host Instagram handles, DM text, `.env`, or `dump.json`. Keep all run data in a gitignored `run_state/` folder. Add `run_state/` to `.gitignore` first. Only code, tests, docs, and workflows get committed.
4. **Never delete rows.** New or unconfirmed mics are inserted as `active = false`. Nothing is ever removed.
5. **Grounded data only.** Never invent a mic, venue, time, day, or Instagram handle. If a value is not in the CSV or the screenshots, leave it null and list it for Adam. If text in a screenshot is illegible, mark `uncertain: true` and list it. Never force a count to match a target.
6. **Instagram safety.** If you see `login_required`, a challenge, `feedback_required`, a 429, or 3 consecutive send failures, STOP sending immediately, do not retry in a loop, and tell Adam. Also honor a kill switch: if the file `run_state/PAUSE` exists, stop after the current message.
7. **No duplicate DMs.** A host must never get the same monthly DM twice. Resuming after a crash must skip handles already sent this round.
8. **Never print secrets.** You may check that `.env` has the key NAMES (`IG_USER`, `IG_PASSWORD`, `SUPABASE_URL`, `SUPABASE_KEY`, `CHANGES_FORM_LINK`). Never echo the values.
9. **Branches and PRs.** Work on a branch, open a PR, never merge, never push to `main`.
10. **Tests.** Existing tests must keep passing (`python -m pytest -q`, 43 at last count). New logic gets tests.
11. **Docs.** Adam wants `documentation.md` (separate from any CLAUDE.md) that explains the architecture so a 5th grader can follow it, with a Summarize section covering what was decided and built. Update it before you finish.
12. **Resumability.** Keep `run_state/STATE.md` current after every step (what is done, what is running, what is next, exact commands). A brand new Claude Code session must be able to continue from it alone.

---

## 1. Verified facts about this repo (read the files anyway, do not just trust this)

- `send_instagram_messages.py` reads a CSV with columns `open_mic`, `changes_updates` (this column holds the host's Instagram handle), `unique_identifier`, plus `day`, `start_time`, `venue_name`, `location`, `borough`, `message_number`. It groups mics by handle, sends ONE DM per handle, paces with `--batch-size` (default 25), `--message-delay-min/max` (default 5-15 s) and `--batch-delay-min/max` (default 30-60 min), supports `--dry-run` and `--yes`, and writes `ig_sent_messages.json`, `ig_mic_mapping.json`, `ig_batch_plan.json`. It logs in through `instagrapi` using `IG_USER`/`IG_PASSWORD` and a saved session in `dump.json`.
- Its message template: "Hey @{handle}! It's Adam from Comediq! I'm doing the monthly check in to update our {Month} mic list..." followed by a numbered list of the host's mics and a reply format (Y / N / Changes). It uses the current month name.
- `collect_instagram_responses.py` fetches DM threads, keeps replies after each `sent_at`, writes `dm_replies.json`, then runs `process_responses.py`.
- `process_responses.py`: a clear `Y` sets `active = true`, `last_verified = today (MM/DD/YY)`, and `{mon}_verification_status = 'responded_confirmed'` on the row with that `unique_identifier`. A clear `N` sets `active = false`. The UPDATE has no filter on the current `active` value, so **a Y reply from the host of an inactive mic reactivates it**. That is exactly the rule Adam wants: reactivate only once the host confirms. Ambiguous or change-style replies go to `ai_parse_queue.json`; results go in `ai_parse_results.json` (shape documented in `PROJECT_SUMMARY.md`); the SQL is written to `supabase_response_updates.sql`. The SQL only UPDATES existing rows and never inserts.
- `apply_response_updates.py` applies that SQL through the Supabase API (dry run by default, `--apply` to write). Read it before using it.
- `export_monthly_verification_mics.py` exports `active = true` rows from `open_mics_historical` with NO city filter.
- The repo default table is `open_mics_historical` and the flag column is `active`. Adam's audit notes say `mics_master` and `is_active`. Resolve this from the real CSV header and a live `select ... limit 1`, and state which is correct.
- On `ai-native-agent-foundation` there is already an `agent/` package: `stale_mics.py` (hide when host silent 14 days AND no user activity 30 days, hide not delete, auto-revive, 15% safety valve), `points.py`, `autonomy.py` (3 approved in a row graduates a category; edits reset it; pause switch), `weekly_report.py`, `run_stale_check.py`, `sql/001_agent_foundation.sql`, 43 tests, and two workflows. Build on it, do not duplicate it.
- `collect_monthly_mic_verification.yaml` and `send_monthly_mic_verification.yaml` currently `git add -f` state files (`dm_replies.json`, `supabase_response_updates.sql`, `ig_sent_messages.json`, etc.) and push them to the public repo, and they upload the same files as Actions artifacts. `process_responses.py` also writes each host's raw reply text into SQL comments. **Do not run either workflow in real mode.**

---

## 2. Inputs

```
CSV_EXPORT      = <path to yesterday's Supabase CSV export>          # Adam fills in, or you find it
SCREENSHOTS_DIR = <folder with the 7 Eye Candy screenshots, Mon-Sun> # Adam fills in, or you find it
```

If either is still a placeholder, look in `~/Downloads`, `~/Desktop`, `~/Documents`, and this repo for a CSV modified in the last 3 days and for 7 recent image files. If you find exactly one plausible CSV and 7 images, use them and say so in one line. If it is ambiguous, ask Adam once, listing the candidates.

Known targets from Adam's earlier preliminary analysis of the 90-mic Eye Candy schedule (TREAT THESE AS TARGETS TO VERIFY, NOT AS TRUTH):

- 53 mics active and verified in the DB
- 23 mics in the DB but inactive (need reactivation review)
- 14 mics missing from the DB entirely

The 14 missing, by day: Monday (3): Cat Salad, Rant, Golden Hour. Tuesday (4): Breakfast of Champions, The Goated Mic, Clay Ones, Franzia. Wednesday (2): Ugh, I'm Already Crying, The Late Night Mic. Thursday (3): Some Good Comedy, Raw Charisma, Girls Night Mic. Friday (2): Summer Fridays, Get It Goin'.

Known inactive examples: Pillow Fight (Pinebox Rock Shop) and Phoenix Bar (Phoenix Bar). The full 23 must be derived from the data.

Matching keys from the earlier analysis: `venue_name`, `day_of_week`, `start_time`.

---

## PART A: THIS MONTH

### A0. Preflight (no writes to anything remote)

1. `git status`. `git fetch origin`. Check out `ai-native-agent-foundation` and pull it. Create branch `run/2026-09-monthly` from it.
2. Add `run_state/` to `.gitignore`. Create `run_state/` and `run_state/STATE.md`.
3. Check repo visibility with `gh repo view --json visibility,isFork` (if `gh` is missing, assume public). Record it in STATE.md.
4. Confirm `.env` has the required key names and that `dump.json` exists. `pip install -r requirements.txt` and `pip install pytest anthropic`. Run the tests.
5. **Snapshot first.** Export the ENTIRE mic table (no `active` filter, paged 1000 at a time) to `run_state/snapshot_pre_run_<YYYYMMDD_HHMM>.csv`. Record the row count. This is the restore point for everything that follows.

### A1. Learn the data (read-only)

1. Read the CSV header and 20 sample rows. Work out the real table name and the real column names for: id, mic name, venue, day, start time, active flag, city, borough, location, host Instagram handle (`changes_updates`), `last_verified`, and every `*_verification_status` column. Print a small mapping table.
2. Check what values the city column actually holds (for example "New York", "NYC", "Brooklyn", blanks). Print the distinct values with counts. **Do not silently drop variants.** Adam's rule is `active = true AND city = New York`; if other spellings clearly mean the same thing, include them and tell him exactly which ones. If it is unclear, list them and default to exact `New York`.
3. Count: active NYC mics, how many have a valid Instagram handle (use `normalize_instagram_handle` from `send_instagram_messages.py`), and how many do not. Save the no-handle list to `run_state/no_handle.csv`.
4. Look at how existing Brooklyn mics are stored (city, borough, location, id format) so new rows follow the same conventions. Note the `unique_identifier` format (uuid or text) and generate new ids in that same format.

### A2. Eye Candy audit

1. Read each of the 7 screenshots (you can view images). Transcribe EVERY listed mic into `run_state/eye_candy_extracted.json` as a list of objects: `{day, mic_name, venue, start_time, borough_or_neighborhood, host_handle_if_tagged, source_image, uncertain}`. The total should be 90. If your count differs, zoom into crops with PIL and re-read before continuing. Do not guess illegible text.
2. Write `agent/audit_schedule.py` with a pure function `match(extracted, db_rows)` that normalizes venue names (lowercase, strip punctuation and leading "the"), days, and times (parse "7pm", "7:00 PM", "19:00" to minutes), then classifies each extracted mic as `matched_active`, `matched_inactive`, `near_miss` (fuzzy score at or above 0.85 but not exact, needs a human look), or `missing`. Match on venue + day + start time, and also check mic name so two mics at one venue on one night do not collide. Write `tests/test_audit_schedule.py` covering time parsing, punctuation and "The" differences, near-miss handling, and same-venue-same-night collisions.
3. Run it. Compare with the 53 / 23 / 14 targets. Report every difference and why (for example a mic the earlier analysis called missing that is actually a near-miss). **Do not force the numbers.** Near-misses go to Adam, not into the insert list.
4. Produce, all inside `run_state/`:
   - `audit_diff.csv`: one row per Eye Candy mic with its classification, the matching DB id if any, and notes
   - `audit_report.md`: counts, deltas vs targets, near-miss list, uncertain items
   - `audit_insert_missing.sql`: INSERT statements for the missing mics, in a transaction, with `active = false`, following the conventions from A1. Use only columns that already exist. If a notes-style column exists, put "Added from Eye Candy list, Sept 2026, awaiting host confirmation". Set the `*_verification_status` value only if it follows an existing allowed label; do not invent new status values.
   - `audit_review_inactive.csv`: the inactive mics found on Eye Candy, with their current DB fields

**New-mic policy (Adam can flip this by editing one line here):** `NEW_MIC_DEFAULT_ACTIVE = false`. New mics enter the database hidden, and become active only when the host replies Y. Hosts with no known handle stay hidden and go on Adam's list.

### A3. Build the send list

1. Write `agent/build_send_list.py` (small, tested where practical) that creates `run_state/send_list.csv` from the snapshot and the audit:
   - every mic with `active = true` and the NYC city rule from A1 that has a valid Instagram handle
   - the inactive mics found on Eye Candy (their hosts get a DM too; reactivation happens only if the host replies Y)
   - the new missing mics that have a known host handle
   - an extra column `verify_note`: empty for normal rows; for inactive rows, `marked not running on my end, but it's on Eye Candy's list. Is it running?`; for new rows, `new to my list, saw it on Eye Candy's list. Is it running?`
   - the existing required columns unchanged, so the existing sender works
2. Rows without a valid handle go to `run_state/no_handle.csv`. Never guess a handle.
3. Make the smallest possible edits to `send_instagram_messages.py`:
   - if a `verify_note` column exists and is non-empty, append it to that mic's line in the message (for example `2. Cat Salad (Monday at 8:00 PM) - new to my list, saw it on Eye Candy's list. Is it running?`)
   - add `--skip-already-sent` plus `--round-start <ISO time>`: skip any handle already present in `ig_sent_messages.json` with a `sent_at` on or after the round start
   - check for `run_state/PAUSE` before each handle and stop cleanly if present
   - stop after 3 consecutive failures
   - add tests for the note formatting and the skip logic
4. Keep the existing message wording otherwise. A host who has both an active mic and an inactive one gets ONE DM listing both (the sender already groups by handle).

### A4. Dry run and the summary for Adam

1. Run `python send_instagram_messages.py run_state/send_list.csv --dry-run --batch-plan-output run_state/ig_batch_plan.json` with pacing: batch size 25, message delay 8-20 s, batch delay 15-30 min. Compute the total ETA. Target: every first DM sent before 11:59 pm ET on September 30, 2026. If the ETA is too long, shorten the batch delay but NEVER below 10 minutes or message delay below 5 seconds, and tell Adam you did.
2. Scan all generated message text and confirm it has no em dashes.
3. Print ONE compact summary:
   - total hosts to DM, split into active-NYC hosts, hosts of the inactive Eye Candy mics, and hosts of new mics
   - hosts with multiple mics
   - mics with no handle (count, file path)
   - Eye Candy audit numbers vs the 53 / 23 / 14 targets, and near-misses needing his eyes
   - the exact rows that will be inserted (count and names)
   - ETA and pacing
   - three sample messages: a normal one, one with an inactive note, one with a new-mic note
   - the snapshot path and row count (his restore point)
4. End with exactly: **"Type GO to insert the new mics as inactive rows and start sending. Type PAUSE-NOW at any time later to stop."** Then STOP and wait.

### A5. After Adam types GO

1. Apply `run_state/audit_insert_missing.sql` (transaction, inserts only, `active = false`). Verify the row count. New mics must exist before the send so that replies can map to their ids.
2. Start the send on this Mac so it uses his normal home connection and existing session, in the background and safe from sleep:
   `caffeinate -dimsu nohup python send_instagram_messages.py run_state/send_list.csv --yes --batch-size 25 --message-delay-min 8 --message-delay-max 20 --batch-delay-min 15 --batch-delay-max 30 --skip-already-sent --round-start <ISO now> > run_state/send.log 2>&1 &`
3. Watch `run_state/send.log` about every 10 minutes. Apply the tripwires from the hard rules. If the process dies, restart with the same command (the skip flag prevents duplicates). Update STATE.md at each batch.
4. When finished, report sent, failed (with reasons), and skipped counts.

### A6. Collect, parse, and apply (this can span several days)

1. Collect replies: `python collect_instagram_responses.py --amount 300`, then `--missing-only` on later passes. Suggested times: a few hours after the last batch, the next morning, and again after two days. Save the exact commands in STATE.md so a fresh session can continue.
2. Resolve `ai_parse_queue.json` yourself this month (you are the parser): write `ai_parse_results.json` in the exact shape in `PROJECT_SUMMARY.md`, keeping `queue_id` and `mic_identifier` unchanged. Use `needs_human_review: true` and low confidence for anything unclear. Never mark a mic inactive unless the host clearly says it ended. Rerun `python process_responses.py`.
3. Review `supabase_response_updates.sql`. Spot-check at least 10 statements against the raw replies. Confirm that every reactivation of an inactive or new mic comes from a host who clearly replied Y or gave a clear "still running" answer. Take another snapshot to `run_state/`.
4. Print a summary (confirmed, changes, inactive, unclear, no reply, reactivations, new mics activated) and end with exactly: **"Type APPLY to write these updates to Supabase."** Wait.
5. After APPLY, run `python apply_response_updates.py --apply`. Verify row counts against the summary. Note in STATE.md that the 14-day stale clock for silent hosts started at each host's `sent_at`.

### A7. Wrap up Part A

1. Update `documentation.md`: how this run works in plain language, what was decided (reactivate only on host Y, new mics enter hidden, the repo is public so no private data is committed), and what was built. Add a dated entry to its Summarize section.
2. Commit only code, tests, docs, workflows, and `.gitignore`. Push `run/2026-09-monthly`. Open a PR with `gh pr create` (or print the compare URL). Do not merge.
3. Send Adam a short status: what is done, what is waiting, and his single next action.

---

## PART B: MAKE IT MONTHLY AND AUTOMATIC

Goal: Adam never touches this again. Each month the pipeline prepares the blast, asks for one tap of approval until it has earned autonomy, collects and parses replies, updates the database, hides stale mics, snapshots the list, and reports. Build in this order, each step small, tested, and documented. Stop cleanly at any point and record state.

**B1. A private home for the automation.** This repo is a public fork, so cloud workflows here would leak host handles and DM text. Do this: `gh repo create malevcode/comediq-ops --private --source=. --push` (or the closest equivalent) so the automation runs from a private repo. Do not copy any `run_state/` content or secrets. Do NOT set any secrets yourself. Instead print the exact `gh secret set` commands Adam should run for: `IG_USER`, `IG_PASSWORD`, `SUPABASE_URL`, `SUPABASE_KEY`, `CHANGES_FORM_LINK`, `ANTHROPIC_API_KEY`. In the old public repo, disable or remove the two workflows that commit state to git.

**B2. Autonomy categories.** Add `verification_apply` and `stale_hide` to `DEFAULT_CATEGORIES` in `agent/autonomy.py` (`host_dm` already exists). Update the tests. Persist autonomy state where the private repo's workflows can read and write it (a committed `agent_state/autonomy.json` is fine in the private repo).

**B3. Monthly prepare workflow** `agent_monthly_verification.yaml`: on the 25th at 9 am New York time (use two UTC cron hours and an in-script guard, like `agent_weekly_report.yaml`). It takes a snapshot, exports active NYC mics plus any hidden-pending mics, builds the send list and the dry-run batch plan, and opens a GitHub Issue titled "September verification ready" (with the current month) containing the summary from A4. That issue is Adam's approval prompt.

**B4. Send workflow** (manual trigger). Input `edited` (boolean, default false). It records the outcome in `agent/autonomy.py` for `host_dm`: approved without edit counts toward the 3-in-a-row rule; an edit resets it. Once `host_dm` has graduated, the monthly prepare workflow triggers the send by itself, respecting the pause switch and the always-escalate topics. FIRST add a `login_check` mode that logs into Instagram from GitHub Actions, reads one thread, and sends nothing. Do not assume Actions can log in: Instagram often challenges datacenter IPs. If the check fails, keep the send and collect steps as local commands (`make monthly-send`, `make monthly-collect`, with a launchd plist Adam can install to run them on his Mac), automate everything else in the cloud, and document the limitation honestly.

**B5. Reply parsing with the Claude API.** Write `agent/parse_replies.py` that reads `ai_parse_queue.json` and writes `ai_parse_results.json` in the existing shape. Use the Anthropic API (model `claude-sonnet-5-5`), key from `ANTHROPIC_API_KEY`, strict JSON output, `updates` limited to the existing `AI_UPDATE_FIELDS`, `queue_id` and `mic_identifier` copied unchanged. Auto-accept only results with confidence at or above 0.9 and `needs_human_review` false; route the rest into a "needs you" list for the weekly report. Never set `active = false` unless the host clearly says it ended. Write tests using stubbed API responses so they run offline.

**B6. Apply step.** After parsing, build the SQL, snapshot, and either wait for Adam's approval (issue comment or manual trigger) or apply automatically once `verification_apply` has graduated. Always snapshot first.

**B7. Stale check.** 15 days after the send, run `agent/run_stale_check.py` in dry-run, post the result to the issue, and apply hides only after approval until `stale_hide` graduates. The 15% safety valve stays.

**B8. Snapshots.** Add `agent_mic_snapshots(id, taken_at, kind, row_count, data jsonb)` to a new `sql/002_snapshots.sql` (RLS on, service key only). Weekly on Sunday night (keep 8), monthly on the 1st (keep forever), seasonal on Mar 1, Jun 1, Sep 1, Dec 1 (keep forever). Note that the September 1 seasonal snapshot was never taken. Keep rows compact.

**B9. Monthly discovery.** Reuse `agent/audit_schedule.py` from Part A. Add `agent/extract_schedule.py` that reads images dropped into a private `inbox/` folder, extracts the schedule with the Claude API's vision input into the same JSON shape as `eye_candy_extracted.json`, then runs the same audit and produces proposals. Adam only drops screenshots; the diff, SQL, and DMs follow automatically. Look at the existing `mic_analyzer/` folder first and reuse anything useful.

**B10. Weekly report.** Extend `agent/weekly_report.py` with the monthly verification funnel: hosts DMed, replied, confirmed, changes, no reply, mics hidden, mics revived, new mics found, and the "needs you" list (unclear replies, near-misses, no-handle mics, Instagram tripwires). Keep the "not connected yet" behavior for anything unmeasurable.

**B11. Docs and PR.** Update `documentation.md` (plain language, Summarize section, an honest "what is not automated yet" list). Commit, push, and open a PR in the private repo.

---

## Definition of done

Part A is done when: the snapshot exists, the audit numbers are reported with any deltas explained, the 14 (or however many are truly missing) new mics exist as inactive rows, every DM has gone out or been listed with a reason, replies are being collected, and the PR is open.

Part B is done when: a monthly run needs one approval tap from Adam (or none once each category has graduated), reply parsing and DB updates run without him, the stale check and snapshots run on schedule, and `documentation.md` honestly lists anything still manual.

## Final report format (short)

1. What got done, in three lines.
2. The numbers (hosts DMed, replies, mics reactivated, mics added, mics hidden).
3. What is waiting on Adam.
4. His ONE next action.
