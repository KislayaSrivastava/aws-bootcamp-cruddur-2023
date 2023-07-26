-- this file was manually created
INSERT INTO public.users (display_name, email, handle, cognito_user_id)
VALUES
  ('Kislaya Srivastava','kislaya.srivastava@gmail.com','Kislaya','8143cd9a-70f1-70fc-9531-4ee18e32a4c8');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'Kislaya' LIMIT 1),
    'This message was imported as seed data into Production DATABASE!',
    current_timestamp + interval '10 day'
  );
