import pandas as pd
import psycopg2
import logging
from psycopg2.extras import execute_values

logging.basicConfig(
    filename='users_raw.log',
    level=logging.INFO,
    format=f'%(asctime)s - %(levelname)s - %(message)s')

logging.info('Start wczytywania danych z csv')

df_users = pd.read_csv('/home/marek/user_posts_pipeline/data/processed/users_processed.csv')

logging.info('Dane z csv zostaly wczytane')

connect = psycopg2.connect(
    host = 'localhost',
    database = 'users_posts_db',
    user = 'marek',
    password = 'marek',
    port = '5434')

cur = connect.cursor()

columns = ', '.join(df_users.columns)
rows = df_users.values.tolist()

select_columns = [
    col for col in df_users.columns
    if col not in ['user_id','updated_at','created_at']]


update_columns = ', '.join(
    f'{col} = EXCLUDED.{col}'
    for col in select_columns)

where_columns = ' OR '.join(
    f'raw_users.{col} IS DISTINCT FROM EXCLUDED.{col}'
    for col in select_columns)

sql = f'''
    INSERT INTO raw_users ({columns})
    VALUES %s
    ON CONFLICT (user_id) DO UPDATE SET
        {update_columns},
        updated_at = CURRENT_TIMESTAMP
    WHERE
        {where_columns}
    '''

try:
    execute_values(cur, sql, rows)
    connect.commit()
    logging.info('Dane poprawnie zaczytane do postgreSQL')

except Exception as e:
    connect.rollback()
    logging.error(f'Dane nie zostaly przeslane do postgreSQL, powod: {e}')

finally:
    cur.close()
    connect.close()

