{{config(materialized='table')}}

SELECT
    posts.post_id,
    users.name,
    users.email,
    posts.title,
    posts.text
FROM
    {{ ref('stg_users')}} AS users 
    JOIN {{ ref('stg_posts')}} AS posts ON users.user_id = posts.user_id