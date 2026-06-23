{{config(materialized='table')}}

WITH CTE AS (
SELECT
    users.user_id,
    users.username,
    COUNT(posts.post_id) AS posts_count
FROM
    {{ ref('stg_users')}} AS users 
    JOIN {{ ref('stg_posts')}} AS posts ON users.user_id = posts.user_id
GROUP BY
    users.user_id,
    users.username)
, CTE1 AS (
SELECT 
    user_id, 
    username, 
    posts_count,
    RANK() OVER (ORDER BY posts_count DESC) AS rank
FROM CTE)
SELECT 
    user_id, 
    username, 
    posts_count,
    rank
FROM CTE1
WHERE rank <= 3