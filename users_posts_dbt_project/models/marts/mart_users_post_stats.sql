{{config(materialized='table')}}

SELECT
    users.user_id,
    users.username,
    COUNT(posts.post_id) AS posts_count 
FROM
    {{ ref('stg_users')}} AS users 
    JOIN {{ ref('stg_posts')}} AS posts ON users.user_id = posts.user_id
GROUP BY
    users.user_id,
    users.username
ORDER BY
    users.user_id,
    users.username