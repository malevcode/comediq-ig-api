-- Comediq AI-native agent foundation (slice 1)
-- Review first, then run in the Supabase SQL editor. Nothing here deletes data.
-- All new tables use an agent_ prefix so they cannot collide with existing tables.
-- Assumes user ids are uuids (Supabase auth). Change the type if yours differ.

BEGIN;

-- 1. Two new columns on the mic table so the agent can hide a mic and later revive it.
--    Hiding also sets active = false, so the public app needs no code change.
--    hidden_by_agent = true is how we know it is safe to revive (never revive a mic a human turned off).
ALTER TABLE open_mics_historical ADD COLUMN IF NOT EXISTS hidden_by_agent boolean NOT NULL DEFAULT false;
ALTER TABLE open_mics_historical ADD COLUMN IF NOT EXISTS hidden_at timestamptz;

-- 2. Every real action a user takes at a mic. This is the "is anyone using this mic" signal.
CREATE TABLE IF NOT EXISTS agent_mic_activity (
  id bigserial PRIMARY KEY,
  mic_id text NOT NULL,
  user_id uuid,
  kind text NOT NULL CHECK (kind IN ('checkin', 'confirm', 'signup', 'recorded_set', 'bad_mic_report')),
  verified_at_venue boolean NOT NULL DEFAULT false,
  at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS agent_mic_activity_mic_at_idx ON agent_mic_activity (mic_id, at DESC);
CREATE INDEX IF NOT EXISTS agent_mic_activity_user_at_idx ON agent_mic_activity (user_id, at DESC);

-- 3. The life story of each mic: lets you ask "how long does the average NYC mic last?"
CREATE TABLE IF NOT EXISTS agent_mic_history (
  id bigserial PRIMARY KEY,
  mic_id text NOT NULL,
  event text NOT NULL CHECK (event IN ('first_seen', 'confirmed', 'hidden', 'revived', 'deactivated')),
  reason text,
  at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS agent_mic_history_mic_at_idx ON agent_mic_history (mic_id, at DESC);

-- 4. Points ledger. Append only: a balance is the sum of a user's rows, never an edited number.
--    Because it is keyed by user, points are the same on web and mobile.
CREATE TABLE IF NOT EXISTS agent_points_ledger (
  id bigserial PRIMARY KEY,
  user_id uuid NOT NULL,
  action text NOT NULL,
  mic_id text,
  points numeric(6, 1) NOT NULL,
  reason text,
  at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS agent_points_ledger_user_idx ON agent_points_ledger (user_id, at DESC);

CREATE OR REPLACE VIEW agent_points_balance AS
  SELECT user_id, SUM(points) AS balance, MAX(at) AS last_earned_at
  FROM agent_points_ledger
  GROUP BY user_id;

-- 5. Lock the new tables. With RLS on and no policies, only the service key (the agent)
--    can write. Users cannot award themselves points from the browser.
ALTER TABLE agent_mic_activity ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_mic_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_points_ledger ENABLE ROW LEVEL SECURITY;

COMMIT;
