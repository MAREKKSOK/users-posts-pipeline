import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import logging

logging.basicConfig(
    filename='posts_raw.log',
    level=logging.INFO,
    format=f'%(asctime)s - %(levelname)s - %(message)s')

logging.info('Start wczytywania danych z csv')

df_posts = pd.read_csv('/home/marek/user_posts_pipeline/data/processed/posts_processed.csv')

logging.info('Dane z csv zostaly wczytane')

conn = psycopg2.connect(
    host='localhost',
    database='users_posts_db',
    user='marek',
    password='marek',
    port='5434')

cur = conn.cursor()

columns = ', '.join(df_posts.columns)
rows = df_posts.values.tolist()

select_columns = [
    col for col in df_posts.columns
    if col not in ['post_id','updated_at','created_at']]

update_columns = ', '.join(
    f'{col} = EXCLUDED.{col}'
    for col in select_columns)

where_sql = ' OR '.join(
    f'raw_posts.{col} IS DISTINCT FROM EXCLUDED.{col}'
    for col in select_columns)

sql = f'''
    INSERT INTO raw_posts ({columns})
    VALUES %s
    ON CONFLICT (post_id) DO UPDATE SET
        {update_columns},
        updated_at = CURRENT_TIMESTAMP
    WHERE {where_sql}
    '''

try:
    execute_values(cur, sql, rows)
    conn.commit()
    logging.info('Dane poprawnie zaczytane do postgreSQL')
except Exception as e:
    conn.rollback()
    logging.error(f'Dane nie zostaly przeslane do postgreSQL, powod: {e}')
finally:
    cur.close()
    conn.close()