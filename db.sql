DELETE FROM authtoken_token WHERE user_id=1;


UPDATE auth_user
SET 
    is_staff = 1,
    is_active = 1
WHERE username = 'Carrie1945'
