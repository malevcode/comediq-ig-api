-- Monthly verification updates generated from CSV
-- Defensive guard: verification status rows only update when the status is still empty.
BEGIN;

ALTER TABLE open_mics_historical ADD COLUMN IF NOT EXISTS "aug_verification_status" text;

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '00de8153-b986-40f3-8080-16fab9905b77' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '00e667ff-46d7-4897-8800-6bcb4e1dc0fe' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '0132ffbb-8010-40f2-9543-0f6a985ffc3a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '01395627-4ac5-47ad-908a-699468629222' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '0244db94-ddbc-4254-9ff4-644ee32f3927' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '02d032b0-e230-4e10-9523-531dac0342f1' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '03202a02-88b4-4103-8a23-64b82b89b588' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '032ead3f-ef47-47ce-beef-df07896bd7bb' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '0336da7f-a548-4ac2-970c-a70814ae8e7d' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '03fdb3e8-9436-4421-8429-1a3b1f17221e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '046b9a55-cc32-4fbc-8393-5eff7c70fef8' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '0479e780-3a0f-434f-b17e-fa1ea39bc02e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '04f2ef0c-47c2-49fd-9c5c-8e32ec069a87' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '059afb5f-808a-4c87-8eeb-2a42088ed982' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '081397c0-c536-44f7-a9df-7671b1119dcb' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '083cf65e-a259-4911-b653-a571a2ad5158' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '087fe321-e1eb-4e1a-ae91-72d04b9ef2cb' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '0a1154b7-18e6-427b-a569-6c23849e406a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '0a347ec7-39a7-49e1-ae8f-250af1ef423b' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '0a80e2e1-ef05-4fc9-96b1-74ccf9a22e20' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '0ce8b294-5b5d-4a6b-8885-e1dcc9a594cd' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '0d96866f-f090-4e60-90f2-ee0f01e880d3' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '0dd26c3a-8310-4ebd-bc2c-931699196ee5' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '0f411037-d7b4-41b2-bbf8-9f736a60093a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '0f7cb01c-8879-4ea3-a97b-0de90802490a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '10461919-3db6-47d4-a225-5ff8949a1808' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1099c4a5-1f11-42df-bb90-2d3c1b71d112' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '11b6f83a-cd7f-4668-b4d1-5c5df5943fee' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '11cdf464-126f-4c1b-b409-dcc45a273075' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '123e2606-0132-4d49-83a1-64b1d16c31b3' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '128a6c60-195b-40ba-94ae-11bb0ab42765' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '12d7b490-1557-4f2b-a16e-68c1dff5f475' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '12d96cea-21b0-4147-94e3-ac97c1d6928c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '137d8edd-c4ef-4621-9899-c0a6e83763eb' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '137d9ced-be38-47af-a7b7-5f90456618cc' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '13e1ab66-a4f8-4dc8-9d2b-860e519dbf34' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '145d71d7-3476-4e86-964d-2f76f882fcd6' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '146319a4-5add-449a-bed0-377c1d000453' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '14ecea80-9e40-43c4-8dd1-ee0f8053c383' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '15213b26-a314-4506-92c0-4e3739815304' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '15403d35-4ea6-451f-a854-1ffd18913289' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '158166b2-b4ae-4317-9e1d-f286588ce7f3' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '16efc4c7-def8-43bf-af4d-c02012704db4' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '17a2c537-d8b7-46a3-89a2-76c14ee855cd' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '17f02914-a631-4103-a1a9-c2517e205c6f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '17f71e28-e602-4d36-a8ca-7e84637db401' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '1817438f-1263-448b-b69f-4e65eca8b24a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '181e6e4c-9c0e-4aa6-9663-53607de12f23' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '18838f99-fd80-46f5-a6f9-dc9def84e863' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '18fa5e91-09f4-4eba-9bc1-6c4ebd08f744' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '19aec36f-9dc0-4b52-9e3f-df1791d7abe6' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '19e2a5c6-035d-4510-b798-29f059686564' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '1a01e32a-0c80-421f-8fb5-d56f0d763abd' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1a29640d-e9cf-4dc0-a0a4-a1b6f61ef174' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '1a4a8e7c-46ce-4f29-99ec-70d342786a83' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1a52aa68-c544-4063-8b3a-c22ef54c7799' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1a779f44-477c-48f7-b145-080a63d980df' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '1a9f70ff-4781-4dab-a524-a5c2b6c739cc' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1b695b01-a77b-4438-aef9-86dcfb26df23' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1b774ee2-20e4-4db1-bef5-f0488202c880' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1bc73a47-af56-4a22-b452-890e1d30e97e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '1c145ee3-5380-481a-94a9-e9d13e878216' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1c86db6e-d40f-4314-874a-9291a1c477bc' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1c930dbc-a85d-4954-aee6-b074cd393a84' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '1d43e906-ec86-4880-91ae-f16343a228a4' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1d7b725d-2dd2-4fe6-9a0d-8a0f08208852' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1d8d58b4-2b12-4d92-9bb4-313c79e207cb' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1db8c4d9-8d99-48d4-a624-c0066f8a9a00' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1de3f6f7-51a7-419f-82fc-9d84582af408' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '1dee78bf-3596-498a-a822-c6be8f4ad38f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '1e536831-cc9b-40b4-8bae-b20177756ea3' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1e557ee2-7682-42ce-b3d8-d64c067dedf9' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1e8b3172-e842-4794-88af-512e9b9b1095' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1eb445bf-7244-49a9-9ea2-723908f06a17' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1ebb6bbe-6781-4fd6-ae8f-ba7593ec4b27' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1ec578cb-8b6e-4d88-8ac9-c7f9ac5dc8ca' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '1ecef174-a4b7-44f9-b50f-f73703e0c037' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1f115050-6f78-4f2b-be18-81807d13b548' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '1f2d7cf1-0b69-4284-9f34-a1ca4b811375' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1f39cafc-bbd8-4293-9693-f390d9f638f8' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1fc53062-69e7-4b6a-84d1-0df70149b7c3' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '1fd3b411-700a-4bcd-8ada-98216bc67919' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '1feac9e8-39a9-4910-a48e-f2922781935b' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '20c5899a-35fd-45cb-9479-ca24b30341c1' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '20e5cb3e-7568-4b70-a98c-62e846f4037d' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '20f2666b-12be-4384-8ae1-41b4aac64284' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '20ff5c59-6bb8-45c2-aea0-190fa6fd34a8' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '217104b3-dae2-46d9-902e-cd71aab5be48' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '217f3cf2-f818-4f26-bcb7-570e58b8dd16' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '22cb48b3-c572-4dd3-bc6c-7d65ee9e13a2' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '23626566-e9f6-45e3-b6c2-9a21828ea9ca' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '23bd3336-3bdf-4fcc-8764-9a3f355cdd3b' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '24396ba2-7422-404e-8887-76c6003e0f82' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '2476def2-7b21-4d4f-ab56-83b2a2f7384c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '24be9395-6fb3-414b-ae59-3585785bfff5' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '24d2e7b8-b38d-487c-a90a-a51d9c1b6e91' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '24d675ac-d906-43a5-870e-9cb8547e8bd9' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '251c539e-989f-442f-ac92-2a1b71e29f59' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '252f3b25-00f4-4896-8cdb-d74b73a93635' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '258b0913-a9dd-4a0d-bc25-634bb2595a9a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '25c014e1-7be0-4a26-aff2-2e7ec7935326' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '26e2e31f-bfc6-4029-8ac5-063c0d9223cc' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '26ea0619-42e2-426b-902e-295f7e28850e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '26ec8833-2811-4acc-8ffd-44e63d7f7bb3' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '26f07b40-e438-4d1c-aedf-0b9ecf2d9c93' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '26fdc583-e504-4c6b-9def-5a5f027bc851' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '29946515-c0b6-4013-b919-41ca2e51186d' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '2998d15b-4300-4d61-8d6d-b12b225108c7' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '2ae2ddfb-bb55-470e-b569-e5eb8bdae9e7' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '2b825b75-0480-4a4e-9232-437bdfacd637' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '2baad6c9-7b12-466e-b2ee-568fe52b9b23' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '2bc4061b-0dcb-44f1-9baa-369e865eb3d5' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '2d7757df-0ec2-4129-8750-e36cc3022121' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '2df014b3-227f-4e92-aee2-96644ce0b483' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '2e378c94-9c66-4677-8100-936d9e38ae82' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '2eb17703-6766-4002-8b37-f36e338f5ece' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '2f1fd122-8680-4bd3-b129-197977940488' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '2ff6c510-ca49-4f0f-bcdf-77c86b733dd5' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '315c524a-4674-4f7c-ad1e-c8beba0bd9e0' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '322b2eb4-71a4-4f11-a983-e9ea212c16af' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '33142031-39ec-400f-aca2-ea49c64eddb0' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '335f8421-a2f7-4757-8c4b-15ab60a5279d' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '33790fcd-e5f4-4a86-b063-fd4054fe9f4d' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '33b82543-d954-4de2-be6a-0a707d449900' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '33d70e62-4777-42a7-8d26-dec65d270f39' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '34254667-8a95-4cf4-9675-78ce900820b6' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '3478fc7e-a23d-4d42-bee7-939ccd43cb19' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '34e7498a-8643-4701-9190-355c9b7c2804' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '352a9809-4462-4915-b03f-f74a59535f4a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '3569288a-3e9e-4be9-905b-21af36a716a0' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '35f0ad79-fab1-4b34-8df0-ced4b7379eef' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '363db223-633f-4e16-8c23-4436de91c183' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '36a320cf-782d-4676-a1a0-8b65e730b9f7' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '3701d276-93c0-44a5-9741-57e8622bc781' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '370c9010-36e2-4392-aa67-2551382f7512' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '37608510-3cc7-40c7-9315-69945312649e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '37e0d199-b14a-41ae-9e09-dc5e5c709543' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '3947c118-fd7c-478a-b011-02ff6f19d9f4' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '3a3fbd37-f5f8-4e7a-ac14-c5a11b1bd1e5' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '3a438c58-2574-4da4-9c3e-8d2133d7b5a9' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '3ab7c412-8143-46b9-a69f-021a85d4865b' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '3b5e2ba5-99b2-47f9-a1c4-5c162eef9c95' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '3bc78f18-bb70-43a6-ab03-7176705d879c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '3bcc9937-9820-4395-a222-85fb565cf7e1' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '3bd61d40-6968-4aa7-85d4-900a278a0b67' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '3c07a147-d5df-47e1-ad1a-388cda47527c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '3c79a51d-e4b8-4984-b3d7-c4c83ab8c79d' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '3d404b0b-b74b-499e-a1d6-e33986cb3cb0' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '3e340117-a831-42a4-ab25-2602e7f2bb8c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '3e535bc8-8154-4d36-a8d1-5cfbfe62a6a2' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '3e741b14-e428-4dc0-823a-1c741d4c43e8' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '3eddffdf-baa0-44d7-9234-5281d340cc8a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '3f94f1c2-f9c0-4d16-9931-38a0238351a1' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '40c430bc-c68a-4f98-aa69-26fb7e4b7e2d' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '4100bb19-923f-4b44-a9f3-8e4a208ac116' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '41547971-0f3e-40ed-a409-ad34dc99b87f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '418ce4f4-94a1-4289-bec9-a55d176d4b99' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '41bc293d-015d-48d7-9083-c15a4e0cf5a1' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '41ee3ded-f6c8-4550-b774-3d6ca5a887af' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '42031289-ef53-46e4-8c58-39680208c673' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '428469ec-d4dc-4027-bc61-6c28aa5775dd' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '431a4ef2-4914-4b71-9d0f-d554fe478719' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '4356a68c-356f-4870-a098-c7498f4737d8' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '43b9cabc-e2fb-4da8-9119-64e5a1a6135f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '4420d710-dd44-4ada-b7bd-050abd8ead2a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '4449545a-6046-49f4-9810-edb2255b2de0' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '44ae6279-2a28-4e62-96bd-6da9c7885f19' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '44cbdff7-0bc8-43f0-9376-f925196b46b8' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '450dfc89-1997-4ce3-8397-cc1a8889548f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '454115c9-7dca-49d0-b664-0ca8b0b42403' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '45713a1b-7ba2-4b79-9314-a42f727885c5' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '45ce7806-cc11-43f8-950b-777436496a87' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '4683b63e-c2ec-4724-bb04-58ea61cfbb95' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '46ca27af-f419-4097-9380-0f67114d7fa0' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '46ee9807-0f32-4a5c-a22a-1b1b9ed80fa4' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '4769d8a1-7c92-4b63-bf83-50e6731f9782' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '4795ece3-a652-4931-b78c-4d1b60434e96' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '4798726f-8da5-4bd6-ab6b-a4a205e28109' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '47b66193-402d-4c7c-889a-015c80455e23' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '481222ae-69dc-43e9-8ce3-35640462f9ff' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '48216dc9-fb7e-4256-b048-d6940c829773' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '485bd039-7000-4b2e-9834-3c48bf51bd09' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '485d5df0-26ad-481b-84f1-b0e1ef8b50f9' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '48ab7d82-00af-4fbd-b70f-23fb40e6a16c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '48bbe8de-33ed-473d-b4b8-98f491293b0f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '48dc3e25-1f69-4817-a0da-deb29232e780' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '49124fef-a1ee-405d-b42c-e95e3e76004f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '497c92b7-67f3-4585-bcff-a9159bc8acd8' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '4a4a5f40-d0a4-4d2b-a236-e4e3589f635f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '4a6d0697-442d-44ca-9d33-608982388a82' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '4a762d15-fe05-44f3-872c-05abb78e4d76' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '4ab4b30b-4f6b-48e1-a795-5fbfb3bfb1b4' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '4b4c2546-e26a-49ca-b3d7-65dbd833f827' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '4c07341c-c141-4bd0-be8a-7b08986327c6' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '4c13473b-1836-4470-ac60-322b15ad79e9' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '4c262c00-8d13-4e8a-b348-a2c8eb84ddb7' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '4c3f02a1-26a5-4582-bee4-29c806ea2a26' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '4caab943-08a0-4d13-b115-d9172ee6c840' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '4cb00fb1-4a7e-4450-a93f-ec514147d53e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '4ce379b3-75e9-4b71-87f9-867e2849584f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '4d2f2a37-32e6-45fc-9fd4-4ff48961bd51' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '4e3f93c5-b0a2-4763-9ec0-17896f4b1d01' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '4e8231d8-cf2f-40eb-a85a-cf3766de4fc7' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '4e9c9391-dd7c-4089-af24-4f9584f31ea1' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '4eacc6a9-b113-4414-99f0-8dc50b4dbe90' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '4f5ddb07-b672-47dc-a9e2-98dbfc5400bd' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '5007dfb0-02e9-477c-aee7-52e55ed6ef8f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '5142ecff-a0f1-4f09-b714-b4299a20a8cd' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '51495931-553e-44b2-846d-a643502ee193' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '5185351c-0199-41d1-a976-92c7b6977d5e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '51fd7767-1871-4de0-9bbe-6d915e313c98' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '523d0101-ab2b-46df-8049-b9511542fae4' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '52b4195d-6399-4deb-a8e4-f41f5eb2944d' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '52e8ae11-4e97-4761-8248-90b77f8e91d9' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '531301d1-0ee2-4f9e-a4ef-f8aab11b5593' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '53425a33-e7b2-41cd-944e-c2163658ed29' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '534cd37a-c806-4db1-88dc-0420f346cad6' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '53628831-456d-40a8-b928-78bf97228712' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '53a27bd8-0261-4f3d-8848-2b9bd257fe9c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '53ded009-89c3-489c-ac44-db383bd7acfc' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '5513bf46-a9a1-4264-a49e-58ba992d31dd' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '559e6022-360c-4907-9ab8-7a1614db006f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '55d06b37-24b9-4813-93e2-5b7aa4d9afbd' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '5624ce77-2a4e-406f-b133-7a278c2fe261' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '56696571-72c3-4102-bd89-9e7ce6dd91f0' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '566c7f42-f346-43ed-8827-b64993fa00e4' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '5716308d-3662-4d40-84bc-6ff3b647746b' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '57edd6da-45e8-4e0e-9f24-8ccce3be95c8' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '580e050c-cf65-4685-ac4e-34601a0226ee' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '582b9d02-7455-472d-8c53-ae562f8acb70' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '584502a8-5e16-463e-9949-8cb61f92a9a5' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '5903510c-add6-43ec-9ce8-0c86a6729d56' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '5a2b2ad6-e2cb-4161-82f8-66bdfa48176b' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '5a6948bb-6b87-4f48-bdfc-a3c8f78f17d0' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '5b43d5b5-e4d0-4038-b02b-38ea43d7434c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '5c0ccee0-44bb-4a74-8080-863a021fd82f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '5cecc59a-f027-469d-a1a4-46d3c3c42c3a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '5e7b7729-91c7-4df7-8067-5af16e3643c7' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '5e88b796-f45b-44d5-a1c9-ef4ac56adb2c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '5eeb77a2-cbf3-4ca0-87fe-2781ad8f359f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '5f147e25-200f-4a47-b0e0-fc07468cd31b' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '5f200616-15b8-4f94-a24b-c3cd75276743' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '5ffc7bac-3bc1-4d19-b45f-381e71b506b0' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '60b43f3b-55a3-4bda-a014-859899b70e78' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '60ef4026-79d9-4d2e-a50c-1b49ebdfe926' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '6162720e-99ab-493f-9b2e-554ca7f0efe9' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '628d747a-0944-400b-a739-33619bf4d3b3' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '63013f40-9753-4630-b27d-66f5a48b854e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '634f42f8-7c47-48a2-882b-23cae51b8110' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '642c2cea-3224-40af-94fd-cc7caea825de' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '64416776-3461-4bac-ad50-dde9a16194a2' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '64d6f5f2-bffc-4ec5-ba72-76d4532a2a51' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '65886b8f-1140-43e4-a526-9c1222a5398c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '6602936a-9abf-4ade-9cba-41b7ff8a4824' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '6743137c-f451-41a6-ae84-f7e979660b3b' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '67e43f0b-ab0e-4f90-b5f8-eb20a4ca9f14' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '69b56f6e-3b84-4518-9d35-1e80f60c8831' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '69f0c91c-4997-43ff-8731-82394be15861' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '69fbad90-35ef-4563-a216-a3d2f46816f9' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '6a2a3632-ad32-4dc9-a2e6-62c028262dc5' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '6ad343d4-c84e-4a09-be21-5accc8123144' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '6ae989e4-1249-4728-aa94-97151cc9648d' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '6b28127f-1782-42d2-a06c-32e1414a65e1' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '6b93a0fa-f6d4-4e2d-8d2a-baf421efe704' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '6bd3d6dc-d83c-4764-8d92-3ff975fee046' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '6c84133b-d383-4844-85a5-7252a1a97876' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '6cbc96aa-f8b0-405f-82f9-5afec6759265' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '6cbdbd01-15be-4315-b535-891c95df0d98' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '6cfe5a87-3df3-4a4b-b3b4-c85abbce9958' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '6d4ee976-9238-4c1a-9021-6854458aea48' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '6dabc797-5897-4a0a-879b-54efde8092aa' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '6e48fa02-a9c0-4729-8ff8-1d1409df5fad' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '6e6d492d-8cac-471d-a570-3cdc5e83a98e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '6f47fc2b-4a03-46a8-b26b-7a683658f514' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '6f6faf9e-5176-43a5-bcc4-cc2ab4591065' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '6f74d61a-c76f-4722-a7c5-ab4b0ae0cbd7' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '701592e6-d2a0-47a5-9196-0585b43f30c2' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '71f9e70f-ef6b-451a-b9b5-c81cacba04c1' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '723dbc0a-cab7-4ddb-9919-404607df9b5e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '73494277-eaa9-4419-88f0-c44071f39952' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '735c9779-7701-4895-9bd8-a59ed48b9cb5' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '741c70b9-bb51-4789-865d-0c89a6272522' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '749a9ec3-a13b-4a6e-8738-0e874e48c35c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '7525a0dd-9b4d-4eab-a17c-feead83b3b1a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '76046782-1301-4309-b9b9-77a12884c199' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '7620eba5-c776-4ee7-b3aa-63aa496cc471' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '7678198e-8283-4b6b-b05f-a619e9583ed9' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '76db39dc-cacb-49b4-a0ae-743926235016' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '773f3b6b-d5c6-43b6-b52d-7ee547297244' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '77aa3d65-1c0e-4109-a4bc-142c1d5ebb99' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '77b1ed82-98fb-4810-9124-304453af6849' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '77b511c6-d77b-4e06-805c-cb56c53fa59e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '77ee111c-294a-43d1-8471-3e00a12f2d9f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '78269d2e-cf0b-4b46-9f93-055ee30a5d61' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '78e2e503-e4d6-481d-be9c-8c34e0be13e3' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '792f7e56-bb45-43de-b8d9-c10441eb9df3' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '798beffe-fc2a-4904-a7f3-86ff9c66c577' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '79a5c6e0-8d01-431f-bb0b-1e99f29e4d1b' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '79d61feb-e9c6-48da-b824-c730cda652d4' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '7a3fa744-b2a6-4d92-a344-ac4c6ce113e6' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '7b335b27-cd1f-4dff-8428-b99c0d88ef15' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '7cf3d9a5-7bf6-415f-8e35-88c6a06e7dbe' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '7d75afdc-c047-416b-8bec-cdda3be97ab9' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '7d772120-2e61-459b-93ca-6c9b6c912827' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '7d8dfd79-9682-4e2d-8123-cec0c39dce60' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '7db28e7d-8c8e-4c83-af5a-26796375e95a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '7e4d1dbc-8cb7-4482-ad17-46d46f6edf75' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '7f0faee1-6579-4410-a516-4ca039ca2bb5' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '7f3122c9-8ff5-4295-abb3-6864d92f9e2b' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '80039680-84db-4135-a855-37859f8857b9' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '8003aa08-1016-4f9f-b6b8-36f4221340e8' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '8048aba3-5bfc-495e-9a04-e1d152dd5d52' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '805960f4-ae7c-4c33-b5cf-5cca266f9609' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '810be17f-726b-4342-87ac-06192f16658c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '814be9e2-7e5e-4724-aa82-2ba2b768f11d' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '81d92ea5-8f01-419a-a47f-53fb50cc1cb1' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '8272fa66-0909-40fa-8a20-381566b82d64' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '828a6fd2-7d6c-4476-87e7-5fd0c2ef0178' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '82d2bbbf-d576-47cc-8219-e22ab59f73b9' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '835cdec2-8024-41bb-ba78-c7da968c4463' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '8455bbfb-160d-4580-9426-4b93d63dcd86' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '84574a68-d715-43ad-8ea9-1512df3148d1' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '845dc046-9e02-419a-960e-4924a3c5d87b' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '84dd5ab2-7b45-4dfa-ad46-023cdb661b6e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '84fa5b1b-8af3-4cf4-91b4-e418eec80254' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '8528f54c-7d26-4408-b400-1c42fe0f7ace' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '858aafe8-5f9b-4052-98df-51224b7e52b0' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '860740b2-0ba0-41fe-97e9-43ac848527e0' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '86ac4fb7-df21-4662-8df9-74267dc99b0f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '86ceecc9-bcf3-41cb-9604-a6aa6c4290b1' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '879bfcfe-3ec8-430b-ad4a-c8a77304cf66' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '8870eb08-4e52-4662-8d09-2d307aa63ddb' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '8914a362-fa72-461b-ae28-89cb2b1f2760' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '892f43cb-b965-412e-81f3-3f0fc3d6811b' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '8940b24e-1b1a-41ef-a5c5-4f0b615c4289' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '899b2f92-ac33-4288-ab4c-650b55270d1f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '8a4ec719-b1da-4b49-be72-f70b6a4f3957' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '8a5106a0-f886-4d97-80f0-b397c1fbcf00' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '8a7af4dc-eed9-49c6-8ce0-72b6ab40fa7e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '8c029eb4-ca1e-4754-bcaf-20930c6fd414' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '8c094164-1928-46f4-b487-57f4fb65d3a7' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '8c1d205c-1b5d-4614-9755-0aa871c5e0b4' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '8cda49aa-ef39-4031-8a3d-a0edf421f0b8' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '8d088f15-0ad1-4094-8331-69027761caed' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '8d9f739e-315a-404f-ba63-4f8060bdeac0' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '8e25cee4-ca30-4bdb-b6fc-9539f5626b53' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '8ea1a42c-56fa-4320-889f-8e67ce178b89' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '8ed77b76-6cab-4c5f-8724-df02b30de727' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '8f7b58b5-1348-4251-8e27-50f0cf5ac761' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '906fffee-4226-4dd8-b462-cd1db969ea2c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '909c470b-7c2d-4b0b-97e4-28f42c1861b7' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '90bbb569-be13-4216-82b8-2b316d87db23' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '90d79c01-c29b-4d79-911b-74997f3ce8a2' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '90f6dfec-f232-406b-9638-4457c3fe8623' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '91bb3838-2243-4deb-8204-0964f23b27c4' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '920ac28a-d1e0-45aa-b729-28d4ce8d6296' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '922aeca4-2e23-4db6-a33e-8bd45f1be9ac' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '924d0a37-6720-4726-b610-dc610bfee817' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '932defc5-0280-4449-9efc-50db7cd59687' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '948ba758-f7f3-483e-9d0d-4d21eb86dea5' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '94be5bb5-e46c-4d43-bb45-9d734c274d3e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '9539c948-44bf-4555-8c1a-9b6475ffde0c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '956ac3ea-14a9-4a41-905b-388d5700047d' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '957aee32-a8b3-47b0-80d1-cf38455a24fb' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '95e59658-7b2b-47a6-8fc1-61e72cb6693d' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '9614f594-073f-408a-9819-449f84a75748' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '96a76eca-dafc-49e5-b97d-65b1f3dbee1c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '971ad8fd-f610-4d0a-b2fc-d7b7091c5117' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '97226681-9dbe-4fe3-a13b-2ca0b97efb41' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '9722b67c-0bbf-4b2c-b3bf-16d0db40d1a8' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '97a91991-8763-4f76-8b9d-27078b0a5a7d' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '97ec746d-3328-4eee-958a-e4d9eee9a97d' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '9848ab29-b0a6-47e2-907b-c3cd5c92c170' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '985f2500-d5a7-4823-8278-9ec5ac4d4d1c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '98c99669-2a0c-4758-af64-c001299f2bc9' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '98f9d16f-b72e-4a5c-9bde-ad24baccfc3d' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '990e942f-d18a-408b-acbd-8e1f6e919c78' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '99cb03c9-b4bd-495f-ada6-1fc89adfdeb1' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '9b15deb4-b70f-449c-a8af-bb7ea2921811' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '9b92e250-84ab-43f7-b8d4-0aca75147084' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '9cc5cfde-2edf-42fe-8191-ed73057aefbd' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '9d126e6f-9934-4aab-8bda-8b2a46e25c4a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '9d19c23c-4ee7-4b8c-9113-35c122dee271' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '9d4e80b4-02db-4aed-97ff-ed0bb56bc913' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '9d726e6c-1987-4b63-bee8-5e2009cd7fc0' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '9db86dc4-36f6-4f46-a8fd-e6ba0b9add60' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '9e149baf-c7b1-4082-9785-575f752f2cdf' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '9e652aa7-82a9-4c5f-8040-84cad666f853' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '9e7c9741-7bc5-4ad8-a7d5-055c65ae9854' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '9ee2c031-f162-4026-b0e1-3e314c5727b6' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = '9fb9b3d5-adcc-4667-aa0a-8bef7fb07482' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = '9fe1c821-9689-4d3a-ae7a-ceffcbdae0d2' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'a078aff8-68cd-4a25-84ae-9117e2bfc06e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'a0fcf3c5-a41e-4efa-9e43-e5abdc6c8a16' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'a1535670-7205-46e5-8c8e-a905fa39beeb' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'a1b27b9b-fa5f-4d5f-9f18-1877829119f3' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'a1b5f3ca-f983-42b3-821b-81076049e483' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'a1e897f4-342a-4b6d-9a85-f33df5630b6e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'a1fa2241-365d-4c73-b1dd-e79ce6fb08af' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'a254f902-1b46-4965-a0b8-2e73162c7af8' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'a2c2e5c2-1709-4ba6-afa3-63abcea2616a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'a341d42c-d989-4b71-9cfc-7e3112f775bd' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'a38648e7-d451-4a8e-b818-520b103ce460' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'a3e83c9e-46cd-46db-9245-a3a9cb1d8ead' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'a4665fd4-1edd-43dc-9ed2-4993b459e59e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'a4b6c172-2f07-485d-ad37-c85608ff5f78' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'a5a61f4e-5762-4e54-b19b-b33801673c11' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'a5e8eaf5-b06f-473d-96dd-54a90d4be8e3' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'a644954b-1bc1-420e-8dbe-99ee08389f88' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'a66a61ca-88c6-4026-90f2-c06265b17cf0' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'a74f6cd7-a56f-4161-9c6b-d207337385b4' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'a76b31da-81ae-4c08-b19c-78119fd1ab54' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'a8b91d57-dcbf-45d9-95a0-e1b3730d2bb7' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'a9188177-d8a4-490a-aad6-1506ffdfa824' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'aa66e471-e173-4433-b95f-3e683c1babdc' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'ab040d4e-050c-4cfb-bdae-4f23f75b3ebe' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'ab460add-b9f3-4ace-bac6-6a52c69d60c9' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'abd640a2-8fa6-4471-b9fc-c22af4b26174' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'abf3b14d-c607-4818-aabc-fd7444942c60' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'acc2eae9-b950-4c21-b135-e6bc2164b20e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'acde7ecd-a11d-466c-aa2e-8cdb8bfac9f5' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'ad0721fe-6aef-4ce6-9833-3a5250fdeda4' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'ad095eb5-6fcc-4277-a190-2fa8631b67ec' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'ad5cffdd-0b65-486f-a5c2-ec910d27f73e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'ae8cf766-003b-4d4d-bb4a-8e274684874e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'af0267fa-1703-49bd-ba0c-82ea56529742' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'af5cad9b-5cc4-4292-9e71-d99074ade9bf' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'af6a6d01-0376-4b4f-8584-17ddb7f9bc24' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'af849a2b-3483-4605-98dc-85495f7135d8' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'b01b725b-3f73-4f70-bbb9-9ed0e26845b2' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'b0323ab0-311f-4ea4-bf96-1373dac96248' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'b037539a-8439-4173-a3b7-60a7a17710e2' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'b075ad57-c3c7-448c-a090-22246b70e421' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'b0bf6d9d-a253-4a0d-8371-a8f9a933f151' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'b1b0dfd1-3869-4131-8a82-c06490b42992' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'b295d769-c0ec-4dbb-a758-b5cb01aec896' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'b31ef4c6-0f40-4cc0-a26d-5373b6399c31' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'b33f945d-12f2-4f8a-baf5-533878af8ec9' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'b3751e54-4825-4a3b-8c9d-2ee65ea4b898' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'b4013567-f93c-4d01-962c-ee4e895fd5ab' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'b45905ec-29df-4e55-9735-c4a55dedf7b9' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'b484ae4f-53a2-4310-a821-97faf8f22f52' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'b48e43b1-4985-4a43-956b-c45261c4a5e8' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'b5a06e3b-bfd3-4718-9489-ba116e97fe01' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'b5b39dca-6d5b-41d9-84bd-dee2efcf1d07' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'b5fe2a10-76d1-4795-94c2-e4a640563a0d' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'b613dcb5-a79f-4743-9911-38db12856ebf' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'b61cee23-5ae3-423b-b598-095106fd5365' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'b6f7bf98-79f8-4e16-9c52-1a53fc5f4a5e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'b74952ac-4adf-4133-aadc-f1cd1df4235e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'b85a9359-cbb8-42d5-9fa0-7748c4a53137' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'b8dcccc7-ca09-4d13-b1e9-1a29ec2876f5' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'b90016c5-1738-4249-bc71-3943e0996f4b' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'b93ed6ce-c688-4c27-b07f-7543b9ae79e3' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'b98b840c-73cf-494c-99a5-9decd01c5fef' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'ba4a4dd8-ec6e-4515-9cee-f14b39646944' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'ba73cd4a-6fe1-4fb7-ad6d-7f9281983b48' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'ba886837-9aa9-4269-83f2-b84f766b5b4b' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'bab89661-e811-4339-9ca5-166d45783cee' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'bc196bfd-25fd-4d2c-b7f1-3e607a4e39f8' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'bc9c9987-c813-4582-86e7-1a966742b343' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'bcca0d69-fda8-4d09-b607-724f26eb5a7b' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'bcf3f27e-8ebb-4d25-9498-b6766d3d744f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'bd86817e-5374-4619-8cea-c67ac188253e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'bdbedd0c-d60a-49c4-8c1e-e3e21d47fb28' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'bdfa44ef-5039-4a95-ba50-171da916f352' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'be2f26b4-b628-4c59-9bfc-897441c4b360' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'be90f316-e4ba-4355-829b-5890ca8817c2' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'bea5b9cf-3ca7-469d-9671-c38043969ac2' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'bef0cd95-ea3e-4d5e-9b92-cc8850df457a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'bf13b5d2-064e-420b-a056-5b42c63b010c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'bf5ed7a4-658a-4cbf-835b-8b0f8da7cc96' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'bf6f9fce-60a6-42ae-98d6-8ab4550f3e01' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'bfec3020-7b82-44c4-913a-b63d61969260' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'bff4746a-f6d8-43fb-96a5-57545d12d914' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'c02c0125-201d-4e7f-be27-59893b486d04' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'c03e6a3e-cce3-4586-ba95-10b492e69987' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'c06215e2-6198-4cae-b109-05313ae44e16' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'c0c00e64-3550-4470-95ec-4c38dcf152a3' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'c0c6a530-d0f9-45ae-a53e-2a8b922963e4' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'c16ecce0-098c-4383-8385-6af6e977251a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'c1732502-63ef-43be-af63-9db5928c8ee4' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'c199fa9b-9601-495e-8a48-ba9432e50f07' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'c2a04a42-6ad1-4c17-b667-6cd3b6a5e310' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'c2c82353-e3f1-42ce-921a-a5c70f33da92' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'c2dd647d-5987-4e58-b48f-f13327fc9717' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'c320a2ba-cb08-4807-bba0-268bbc6b5e4a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'c3c2f0f0-a945-4f6c-a981-aaa68f99d2dc' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'c458dbbb-f2b4-4af8-bcd1-9fdf9a963633' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'c4ef4b5c-5937-4af5-a298-d22f26b5aae6' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'c4f50721-c4a7-425f-b9a5-d0dcfcaa291e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'c501698b-a54d-4826-8288-bafbb1c64f49' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'c5b4211a-a941-43f2-9ce2-6651b840d9a8' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'c60a6512-6a41-4451-81f8-3a6c493b5c7a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'c618d42c-a8fb-4c8f-ac9e-df9a9ba69a4c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'c7e33bcb-ff39-4ed7-97a5-84da9aaadaaf' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'c8374375-b706-49ac-bfb7-dca5205e55d0' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'c904454b-b103-4063-9910-644ccba54523' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'c91dfa8d-edad-4f3b-9410-b5cb5e2351f9' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'c93a96a9-0408-4bbe-ab75-a3aa2ab41cf6' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'c9af89a9-5744-4fbe-87a6-b89f3f109447' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'c9cc588a-57d7-494c-9625-f52c76afd4b0' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'c9f211f2-07fb-4bf7-b44e-6958bc09f561' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'ca4ac065-5bc5-4bfb-8ad3-d3ba630d756e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'ca61199d-9894-4325-aba2-5156e80840b6' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'ca81bcc0-f7cb-472e-8710-df18740a4d17' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'caa755e4-6a43-4271-a395-c2ee26eddc42' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'cbdb2393-068d-4060-842b-6f56f3efee97' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'cc2a253d-5273-491e-88ed-c09a303b450e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'cddd350c-0ead-46ac-82a3-c351166a8911' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'ce1fe866-698c-4504-bd52-396fcadb925a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'ce280de0-35f4-4252-9d6e-b1f620aaa2b5' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'ce2ba87f-35f9-4856-8f23-0b41be3b0ff8' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'ceb6fb59-bbbd-4655-8eaf-559e1c259d79' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'cecb9441-e087-4caa-a482-b06cee615f38' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'cfced183-b339-4e46-903e-ac656c914352' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'cff41a9e-605c-472f-9349-c76be5c82026' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd0962e65-4249-438f-aad0-66feeb249ca7' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd1369755-0c77-46cf-b160-e24792f6e6ba' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd17d18dd-7707-4794-98d6-cf0ca51ba9f3' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd184167a-3ceb-4b9b-a2b5-e8521e7d73ce' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'd19c89a4-e835-4650-b99d-008f5c771959' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd2420d40-d1cc-4f5e-9216-067f3a29fbc6' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'd27644b7-c3e3-4f4d-906b-9b7ab85494be' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd37a9ffb-41fd-47f0-9bfd-16d5a5f3a63b' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd3892e30-fb34-4863-9fa0-a7e06d43a76c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd44aba41-316b-4208-8ee3-64415d84d308' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd482f55f-df1f-453a-a77c-b94b51f43f36' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd531c7d7-1afc-4904-9f75-16d129372739' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd59c4302-4c48-439c-a085-0c006a16245c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'd5a70c63-563f-42e4-ba77-3dcffbacdee0' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd5a9b1a6-5515-45a0-927d-8e18b73020e8' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd62b14d8-6797-42ea-b424-45bcb2077288' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'd70271ea-db58-4a44-a721-6665386fabd5' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd7c5dde7-77f0-49d5-a4bd-c5dfc0c02523' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd8415ac9-0fd1-46c8-9e09-f56ee8a5fc3f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'd8974b6e-b577-4fb2-9930-5a4ecb32c874' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd89a477a-0cd8-4952-aeb3-12573c1343ea' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd97a8063-4b17-41b1-bcfc-84aced9f3437' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd97c797a-f8a7-4dc4-92a3-580b10893a82' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd9a9c0b5-7593-40a8-a748-c7ed80109ac6' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd9b8bd02-8d29-43c6-ab6f-4f8caef702f4' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'd9ca0086-fb18-42a8-a279-c8a0dddbfbcf' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'd9ee34bd-6c50-495a-b51c-425a88222be8' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'da4c34b8-d473-44c5-ae41-0eaf264f3777' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'da8cfc1b-3ae0-428e-85df-cc6eceb2b622' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'db93a94f-0dc3-43ff-a2a2-22c4749d873f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'dbedd99f-a036-4bbf-b409-668ffb0734f8' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'dc712c0d-70fa-464e-86fb-3c021b825d2f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'dcb28c2e-c8ba-4a1e-98e9-c05d7d702231' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'dd3bf4d6-8059-4d0b-82e9-273a14c42389' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'dd52f0d5-48d9-44ca-8158-73b9a57306c7' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'dda1af00-bb60-4bde-a1e8-a5083600b6a9' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'ddd595be-35df-4510-b679-7f41dc726842' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'de0d1f4b-d036-4748-998c-18a628bfc572' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'de7386d6-cd25-47b1-8511-4bf225af61a6' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'e117305b-e191-4f50-b629-73ddb0716adc' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'e12af4f5-fe5a-49e6-a196-82bb34b93824' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'e16cb817-aac2-42c8-93d6-9ad3a500a40e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'e1770be0-28b2-46cd-ad91-386011be2317' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'e1875e5c-9c73-44d6-bad5-683dc7d6a3cf' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'e18ee1b0-0164-4e75-9e97-9b242752542a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'e1f2cc9c-b42a-4594-8d25-0f61deb5e543' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'e276f4e6-655f-46a2-ae97-458b2961db90' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'e33bfece-02d2-43fc-a5ed-89450bfe60aa' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'e393766a-3667-41f2-ba23-dafc385b9559' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'e39faffe-6362-43df-9605-26fa9fd92043' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'e3b6e6a6-37bf-492a-bfb2-b34fe3faffed' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'e3f17608-ae1f-4756-8a41-686914709371' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'e583fed1-93c9-4ef2-bb71-9ea71af412c3' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'e65b0c09-71fb-481d-afae-1d48a6dddb63' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'e7105940-d07b-4f96-8240-f83e75419d58' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'e73080d4-944a-47e8-9fc0-9bb0faae8bbb' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'e7716990-548d-4666-a803-dccc2c23bdcd' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'e7ac20fa-dcbd-4219-a9fb-2720bb277707' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'e7cdc10e-e4d4-4d3a-9ec9-018c089426bf' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'e976556f-6c18-4731-920f-281282dfa178' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'e9e8c956-308d-4a13-8003-443f7738e0d2' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'e9f84726-4c29-41a4-b6ab-c4b6bc997929' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'e9fc2a6c-c846-407e-9ad4-82d0edf41af5' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'ea4f79a8-52c8-4108-b5bb-fad92969e9c6' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'eaf0ac36-0864-4a39-a8d4-b50d30e0ccc7' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'eb0a4e4d-5741-4d17-ad5b-ba69eaa89cf0' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'ec21f588-6286-4f93-94b8-0b686692503f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'eca0f78c-5a57-49a2-a23b-2c525ffb024f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'eca2a08e-0738-4702-984e-f98842470f80' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'ecf3921e-5669-49d1-974e-289c1faac691' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'ed011410-e26a-43c9-a654-65f7536181e6' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'eec0ff9c-d217-4909-b075-c1ff97c4953d' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'ef7c9d24-7c1f-476d-9524-462f5859bba9' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f04a0d1f-fabe-4995-82c1-2c2e64bdd65d' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f0521efb-b85c-4989-8457-a7d3edecbd16' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f060f3dc-6c14-4982-a183-6f8a8035ace3' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f203bbf4-02df-4766-81f7-bf5b91dc8cf2' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f23e7719-b5c7-479e-9c12-45bb1dbf717a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'f29afb15-c09b-466e-aedd-284f6b7ac433' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f31495d2-4763-4c69-83da-92c75169e11e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f31cd170-122b-4cc7-8b39-6556b948cd70' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f35240d3-93c4-41ec-b938-de0be0cf68e4' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'f39ddf4c-dd5f-47df-87db-6698b2ee7981' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f3e86ae8-201c-4f66-a80f-cdc08ec87d0c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f48269b5-0374-4b23-a130-a9fdae02f214' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f4f45882-3a6c-4b32-a3d4-5f46175ee3df' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f5023a3f-6581-466a-9abc-e8ba6a41ffe7' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f522faf2-30d8-4045-bb44-9dbea620c438' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f534b265-33b0-4af2-9287-1dc52c5c22eb' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f6547918-f56a-4e80-a670-6781910d9051' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'f6b4a30b-be4f-45b0-a1e5-029c7ee301bf' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'f6ece9cb-5473-43f1-b106-87254a50f0a3' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'f7427e7e-883b-43e1-942a-9bf6e4f4c197' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f7afd736-b916-4f04-90f0-dd5b73127d1f' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f7fceee0-ee96-4287-a3d2-f7cbee6debd3' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'f831f41f-09b0-4ac5-ae1c-b643b5380fee' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'f8d6c0a7-3647-4979-84f9-8184d2cb935e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f8d96ef8-3e49-4122-a466-4d8bcaf1313e' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f8e09bed-0b8e-4715-bc97-f0214b2cdd6d' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f9193667-6297-4f27-8245-0f75348673a2' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'f940ae95-a36d-499e-9de9-9f5850be1232' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'fa6fb4a0-0937-4404-9af6-575adbec8812' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'fab4a155-afdd-4339-a441-1f82a2f935d1' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'fab77b8f-2cba-45df-acab-a318f575d6df' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'faca8d7f-7870-41f1-92b3-e289cd13516c' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'fb2381a8-27e4-4c97-9d8c-86465a703c53' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'fb2c9bd5-51b5-4715-baf9-01470a18d2e4' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'fba803d2-b03e-400b-b544-11d8de8baa22' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'fbbcbddb-6217-4185-a793-57a77f27cee7' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'fbc09b69-d816-4f15-bd18-0351102df781' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'fcdd7197-04a4-4ebc-a3a6-a1a0db6fa809' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'fd4c0237-d37f-4710-a337-96df56a0b34a' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'fd6f8bd6-14de-491f-ab0d-2bd0f534fef4' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'fd828d9d-a57c-4f0f-9f7f-202cc022e6dd' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'not_sent'
WHERE unique_identifier = 'feaa17c1-0fca-459c-ae6a-a7662a1da7cc' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

UPDATE open_mics_historical
SET "aug_verification_status" = 'no_response'
WHERE unique_identifier = 'fec8594e-b3a6-4200-888d-0633477b838b' AND ("aug_verification_status" IS NULL OR "aug_verification_status" = '');

COMMIT;
