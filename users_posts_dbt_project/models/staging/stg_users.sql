SELECT 
    user_id,
    name,
    username,
    email,
    phone,
    website,
    street,
    suite,
    city,
    company,
    updated_at,
    created_at
FROM 
    {{ source('raw','raw_users')}}