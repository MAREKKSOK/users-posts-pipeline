import json
import pandas as pd

with open('/home/marek/user_posts_pipeline/data/raw/users.json','r') as file:
    data_users = json.load(file)

df_users = pd.json_normalize(data_users)

df_users = df_users[['id','name','username','email','phone','website',
                     'address.street','address.suite','address.city','company.name']]

df_users = df_users.rename(columns={'id':'user_id','address.street':'street',
                                    'address.suite':'suite','address.city':'city','company.name':'company'})

df_users.to_csv('/home/marek/user_posts_pipeline/data/processed/users_processed.csv', index = False)