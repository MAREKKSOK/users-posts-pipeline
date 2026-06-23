# Users Posts Pipeline

End-to-end Data Engineering pipeline built with Python, PostgreSQL, dbt, Airflow and Docker.

## Pipeline flow

API → raw JSON → processed CSV → PostgreSQL → dbt staging → dbt marts → dbt tests → Airflow orchestration

## Tools

- Python
- PostgreSQL
- dbt
- Apache Airflow
- Docker
- Git/GitHub

## Project layers

- Extract: downloads users and posts from JSONPlaceholder API
- Transform: cleans and prepares users/posts data
- Load: loads data into PostgreSQL raw tables
- dbt staging: creates cleaned technical models
- dbt marts: creates analytical business models
- Airflow: orchestrates the full pipeline

## dbt models

- stg_users
- stg_posts
- mart_posts_with_users
- mart_top_users
- mart_users_post_stats
