-- Second-round Instagram response updates only
-- Extracted by comparing current dm_replies.json to response_runs/aug_2026_after_first_supabase_push/dm_replies.json.
-- Review before running in Supabase.
-- New handles: @johnbent.comedy, @losierty13, @paulzachcomedy, @rodneysopenmics, @sangerhallopenmic, @traumadumpthursdaymic, @tys.jokes, @wizman.comedy, @xhunterwrightx, @zebracakemack
BEGIN;
ALTER TABLE open_mics_historical
ADD COLUMN IF NOT EXISTS "aug_verification_status" text;

UPDATE open_mics_historical
SET active = TRUE, last_verified = '08/10/26', "aug_verification_status" = 'responded_confirmed'
WHERE unique_identifier = 'e5c52351-52ad-4df9-9009-4c615505d16f';
-- raw response for e5c52351-52ad-4df9-9009-4c615505d16f: Y

UPDATE open_mics_historical
SET active = FALSE, last_verified = '08/10/26', "aug_verification_status" = 'responded_changes'
WHERE unique_identifier = '6f772e76-eba9-447c-808a-d3079ab724f5';
-- raw response for 6f772e76-eba9-447c-808a-d3079ab724f5: N

UPDATE open_mics_historical
SET active = TRUE, last_verified = '08/10/26', "aug_verification_status" = 'responded_confirmed'
WHERE unique_identifier = '514094aa-c2da-4121-b71c-5ab7a76ea3ed';
-- raw response for 514094aa-c2da-4121-b71c-5ab7a76ea3ed: Y

UPDATE open_mics_historical
SET active = TRUE, last_verified = '08/10/26', "aug_verification_status" = 'responded_confirmed'
WHERE unique_identifier = '0d6e6906-18a8-4a7b-89e4-e5d1b70dccb1';
-- raw response for 0d6e6906-18a8-4a7b-89e4-e5d1b70dccb1: Y

UPDATE open_mics_historical
SET active = TRUE, last_verified = '08/10/26', "aug_verification_status" = 'responded_confirmed'
WHERE unique_identifier = 'ea37784d-b08f-45fa-8eea-ae9005d3f1d7';
-- raw response for ea37784d-b08f-45fa-8eea-ae9005d3f1d7: Y

UPDATE open_mics_historical
SET active = TRUE, last_verified = '08/10/26', "aug_verification_status" = 'responded_confirmed'
WHERE unique_identifier = '99028ebe-998f-43a8-a996-fda99067cb62';
-- raw response for 99028ebe-998f-43a8-a996-fda99067cb62: Y

UPDATE open_mics_historical
SET active = TRUE, last_verified = '08/10/26', "aug_verification_status" = 'responded_confirmed'
WHERE unique_identifier = '28ab9f17-e0d5-4d65-818b-5578e550f87b';
-- raw response for 28ab9f17-e0d5-4d65-818b-5578e550f87b: Y

UPDATE open_mics_historical
SET active = TRUE, last_verified = '08/10/26', "aug_verification_status" = 'responded_changes', "frequency_custom_text" = 'Active in August except off August 7 and August 14', "other_rules" = 'Active in August except off August 7 and August 14'
WHERE unique_identifier = '3cbcd790-258f-4a30-bc05-c932a0520d3f';
-- AI note for 3cbcd790-258f-4a30-bc05-c932a0520d3f: Host says they are off August 7 and August 14 but back the rest of August. Existing recurring fields may need date exception handling outside current schema.

UPDATE open_mics_historical
SET active = TRUE, last_verified = '08/10/26', "aug_verification_status" = 'responded_confirmed'
WHERE unique_identifier = '5444e091-b1bf-4ced-a337-a2b58e8f639a';
-- AI note for 5444e091-b1bf-4ced-a337-a2b58e8f639a: Host confirms current mic and says there is also a second Tuesday 5:45 PM mic at The Pear. Current SQL can update the existing row but adding the second mic requires a separate insert/manual add.

UPDATE open_mics_historical
SET active = TRUE, last_verified = '08/10/26', "aug_verification_status" = 'responded_confirmed'
WHERE unique_identifier = '0e3ab7f1-2448-4510-8d3f-a8475ef9eac9';
-- AI note for 0e3ab7f1-2448-4510-8d3f-a8475ef9eac9: Yes indeed confirms active; no changes mentioned.

COMMIT;
