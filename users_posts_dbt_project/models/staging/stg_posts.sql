SELECT
    post_id,
    user_id,
    title,
    text,
    updated_at,
    created_at
FROM
    {{ source('raw','raw_posts')}}