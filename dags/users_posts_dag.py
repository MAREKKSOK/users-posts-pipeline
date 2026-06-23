from airflow import DAG
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

with DAG (
    dag_id = 'users_posts_dag',
    start_date = datetime(2026,1,1),
    schedule = None,
    catchup = False
) as dag:
    
    start_task = EmptyOperator(
        task_id = 'start_task')

    extract_posts_task = BashOperator(
        task_id = 'extract_posts_task',
        bash_command = 'python3 /home/marek/user_posts_pipeline/scripts/extract_posts.py',
        env={"BASE_URL": "{{ var.value.jsonplaceholder_base_url }}"})

    extract_users_task = BashOperator(
        task_id = 'extract_users_task',
        bash_command = 'python3 /home/marek/user_posts_pipeline/scripts/extract_users.py',
        env={"BASE_URL": "{{ var.value.jsonplaceholder_base_url }}"})
    
    transform_users_task = BashOperator(
        task_id = 'transform_users_task',
        bash_command = 'python3 /home/marek/user_posts_pipeline/scripts/transform_users.py')

    transform_posts_task = BashOperator(
        task_id = 'transform_posts_task',
        bash_command = 'python3 /home/marek/user_posts_pipeline/scripts/transform_posts.py')    
    
    load_posts_task = BashOperator(
        task_id = 'load_posts_task',
        bash_command = 'python3 /home/marek/user_posts_pipeline/scripts/load_posts.py')

    load_users_task = BashOperator(
        task_id = 'load_users_task',
        bash_command = 'python3 /home/marek/user_posts_pipeline/scripts/load_users.py')
    
    dbt_run_task = BashOperator(
        task_id = 'dbt_run_task',
        bash_command = 'cd /home/marek/user_posts_pipeline/users_posts_dbt_project && dbt run')

    dbt_test_task = BashOperator(
        task_id = 'dbt_test_task',
        bash_command = 'cd /home/marek/user_posts_pipeline/users_posts_dbt_project && dbt test')

    end_task = EmptyOperator(
        task_id = 'end_task')
    
    start_task >> [extract_posts_task, extract_users_task]
    
    extract_users_task >> transform_users_task >> load_users_task
    
    extract_posts_task >> transform_posts_task

    [load_users_task, transform_posts_task] >> load_posts_task

    load_posts_task >> dbt_run_task >> dbt_test_task >> end_task