# How the Comediq AI Agent Works

This file explains the agent in plain words. If a 5th grader can follow it, it is written right.

## The big idea

Comediq should run like a lemonade stand where Adam is the only worker. That only works if a robot helper does the boring jobs first, and Adam just checks the robot's work.

The helper does five things:

1. It keeps the open mic list honest, so people only get sent to mics that are real.
2. It hands out points when people do real things at real mics.
3. It writes a report every Monday about what changed.
4. It writes drafts of messages and posts, and Adam approves them.
5. Over time, it earns the right to do some jobs without asking.

## Part 1: Keeping the mic list honest (`agent/stale_mics.py`)

Some websites list open mics that stopped years ago. Comediq wins by never doing that.

Every month the agent DMs each mic host on Instagram and asks, "Is your mic still running?" Then it uses two clocks:

- **Clock 1:** Did the host answer within 14 days?
- **Clock 2:** Has any real person checked into, confirmed, or recorded at that mic in the last 30 days?

A mic gets hidden only if BOTH clocks say "nobody is home." If either clock shows life, the mic stays. Hidden does not mean deleted. If the host answers later, or one person shows up, the mic comes back by itself.

Two safety rules keep the robot from making a big mistake:

- **Grace period.** If we only just started counting check-ins, nobody has had 30 days to act yet. So the robot waits instead of hiding everything.
- **Safety valve.** If one run wants to hide more than 15 out of every 100 mics, the robot stops and asks Adam instead. That usually means the data is wrong, not that lots of mics died.

Hiding a mic turns off its `active` switch. Our own export scripts already treat `active = false` as "off," so this should work without touching the website. But we have not checked how the public site and the phone app read the list, so confirm they also skip inactive mics. If the site uses a saved copy of the list (the static `mics.json` mode), a hidden mic only disappears after that copy is rebuilt. A second flag, `hidden_by_agent`, records that the robot did it, so the robot only ever brings back mics it hid. It never overrules a human.

## Part 2: Points (`agent/points.py`)

Points work like tickets at an arcade.

| What you do | Points |
| --- | --- |
| Check into a mic (stay 20 minutes) | 1 |
| Confirm a mic is still running | 1 |
| Sign up at a mic | 1 |
| Report a mic that is really dead | 5, paid after it is confirmed |

Rules that keep it fair:

- Your phone must be at the venue. A check-in from your couch earns nothing.
- You can check into up to 5 different mics per day, but only once per mic per day.
- The 5 point bonus only pays once someone else agrees the mic is dead, or the host stays silent. That stops people from spamming reports.
- Premium members earn 1.5 times as many points.

Points are saved in a ledger, which is a list where we only ever add lines, never erase them. A person's balance is the total of their lines. Because the ledger is tied to the person, the same points show up on the website and in the phone app.

## Part 3: The Monday report (`agent/weekly_report.py`)

Every Monday at 8am New York time, the agent writes a report: new accounts, mic changes, host replies, points handed out, unusual point earners, and where each job stands on its way to running alone.

If the agent cannot measure something yet, the report says "not connected yet." It never guesses.

Adam can also ask for a report any time. The command is `python -m agent.weekly_report --force`, or the "Run workflow" button on GitHub.

## Part 4: Earning independence (`agent/autonomy.py`)

The robot starts out asking permission for everything. Each kind of job is counted on its own: Instagram replies, email replies, Instagram posts, and host messages.

- Adam approves a draft with no edits: the counter goes up by 1.
- 3 in a row: that job now runs alone.
- Adam changes anything: the counter drops back to 0, and the robot writes down what he changed so it can learn.
- A pause button pulls any job back to asking permission right away.
- Some topics always go to Adam no matter what, like refunds, legal questions, safety problems, and reporters.

## Where everything lives

| File | What it does |
| --- | --- |
| `sql/001_agent_foundation.sql` | Adds the new tables and two new mic columns. Run it once in Supabase. |
| `agent/stale_mics.py` | The two clocks and the safety rules |
| `agent/run_stale_check.py` | Runs the check against the real database (dry run unless you add `--apply`) |
| `agent/points.py` | The points rules |
| `agent/autonomy.py` | The "3 in a row" counter |
| `agent/weekly_report.py` | Builds the Monday report |
| `tests/` | 43 checks that prove the rules behave |
| `.github/workflows/agent_weekly_report.yaml` | Runs the report every Monday |
| `.github/workflows/agent_stale_mic_check.yaml` | Runs the stale check when Adam clicks the button |

## What is NOT built yet

Being honest about this matters more than looking finished:

- **Nothing awards points yet.** The rules exist and are tested, but the website and phone app still need to call them when someone checks in. That work belongs in the web app and the mobile app repos.
- **The production points ledger question is open.** Notes from earlier work say a Confirm Active and Report Inactive feature with a points ledger may already exist in the live site, while other notes say no points system exists yet. This build uses new tables named `agent_points_ledger` and friends so nothing collides. Before wiring the apps, check whether an older ledger exists and pick one to keep.
- **The web app and mobile app repos are not touched.** This session only changed `comediq-ig-api`.
- **Check-ins are not recorded yet.** The stale check reads `agent_mic_activity`, which stays empty until the apps write to it. Until then, the grace period protects every mic.
- **The weekly report is not emailed yet.** It is saved as a file on GitHub. Sending it to Adam's inbox is the next step.
- **Instagram views and signups per post are not measured yet.** They need Instagram Graph API credentials.
- **Drafting messages and posts is not built yet.** The approval counter is built, but nothing feeds it drafts.
- **Streaks are not saved between runs in the cloud yet.** The counter works and is tested. Deciding where it lives permanently is still open.
- **Host DMs still use the unofficial Instagram login (`instagrapi`).** It works today, but Instagram can lock the account. The plan is a pause switch that stops sending if Instagram throws a login error, and email as a backup.

## Summarize

### Session 1 (2026-09-28): planning and the first build

**What we decided**

- Every job starts as draft-then-approve. Each job runs alone after 3 approved drafts in a row with no edits. Any edit resets the count, and Adam can change the process or pause a job at any time.
- Mics are hidden when the host is silent for 14 days AND nobody has used the mic for 30 days. Hidden mics are never deleted and come back automatically.
- The mic list is saved weekly (keep 8 weeks), monthly (keep forever), and every season (keep forever). Each mic also gets a life history so we can measure how long mics last.
- Points: 1 for real actions at the venue, 5 for a confirmed bad-mic report, 1.5 times for premium, up to 5 mics a day. Prizes are priced like an arcade: ad-free month 50, sign-up priority 50, premium month 100, notebook 150, merch 300, booked show spot 250 (max 2 a month).
- Points are saved on the user profile so they are the same on web and mobile. Web starts now, and the mobile app follows.
- Three Instagram posts a week: Monday "mics this week", Thursday "weekend mics", Saturday a rotating spotlight (most active mic, mic of the day, host takeover).
- A report arrives every Monday at 8am, and on demand any time.
- Host DMs go through the existing `comediq-ig-api` repo.

**What we built**

- The SQL migration, the stale-mic engine and its runner, the points rules, the autonomy counter, and the weekly report.
- 43 automated tests, all passing.
- Two GitHub workflows: the weekly report on a schedule, and the stale check on a manual button.

**What is next**

- Run the SQL migration in Supabase.
- Make the web app write check-ins to `agent_mic_activity` and award points using the rules in `agent/points.py`.
- Email the Monday report to Adam.

### Session 2 (2026-09-29): end of month blast and making it monthly

**What we decided**

- Every active New York mic host gets the monthly verification DM before October 1.
- The 23 mics that are inactive in our database but listed by Eye Candy are NOT switched back on by us. Their hosts get a DM, and a mic comes back only when the host replies Y. This is what keeps our list more trustworthy than other open mic sites.
- Mics on the Eye Candy list that we do not have are added as hidden (inactive) rows, and go live only when the host confirms.
- The two irreversible steps stay behind a typed word: `GO` (add the hidden mics and send the DMs) and `APPLY` (write the reply updates to the database). This is the same 3-approvals-in-a-row rule, applied to mass DMs.
- The long term goal is a monthly pipeline that prepares the blast, asks for one tap, collects and understands replies, updates the database, hides stale mics, and saves a snapshot, so nobody does this by hand again.

**What we learned about the code**

- A "Y" reply from a host already switches that mic to active, even if it was inactive before. So "reactivate only when the host confirms" needs no new code.
- The two GitHub workflows that send DMs and collect replies would push private DM replies and host handles into this public repository. They must not be run for real here. The monthly automation should live in a private copy of the repo.
- The export script has no city filter yet, and the audit notes use different table and column names (`mics_master`, `is_active`) than the scripts (`open_mics_historical`, `active`). The first step of the run is to check the real names.

**What we built**

- `prompts/monthly_run_2026-09.md`: one big prompt for Claude Code. Part A does this month's blast and audit with safety rules and two gates. Part B turns it into the monthly automatic pipeline.

**What is next**

- Run the prompt in a terminal inside the repo.
- Give Claude Code the CSV export and the seven Eye Candy screenshots.
- Add `ANTHROPIC_API_KEY` to the private repo so replies can be understood automatically.
