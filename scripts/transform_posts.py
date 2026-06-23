import json
import pandas as pd

with open('/home/marek/user_posts_pipeline/data/raw/posts.json','r') as file:
    data_posts = json.load(file)

df_posts = pd.DataFrame(data_posts)

df_posts = df_posts.rename(columns={'id':'post_id','userId':'user_id','body':'text'})

df_posts.to_csv('/home/marek/user_posts_pipeline/data/processed/posts_processed.csv', index = False)