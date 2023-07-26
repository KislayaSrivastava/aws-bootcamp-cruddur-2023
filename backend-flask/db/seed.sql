-- this file was manually created
INSERT INTO public.users (display_name, handle, cognito_user_id)
VALUES
  ('Andrew Brown', 'andrewbrown' ,'MOCK'),
  ('Andrew Bayko', 'bayko' ,'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'Kislaya' LIMIT 1),
    'This message was imported as seed data into Production DATABASE!',
    current_timestamp + interval '10 day'
  );

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'MksBlr' LIMIT 1),
    'This message was written to Production database and imported as seed data!',
    current_timestamp + interval '10 day'
  );