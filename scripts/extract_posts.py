import json
import requests
import os

base_url = os.getenv("BASE_URL")
url = f"{base_url}/posts"

response = requests.get(url)
response.raise_for_status()

print(response.status_code)

data_posts = response.json()

with open('/home/marek/user_posts_pipeline/data/raw/posts.json','w') as file:
    json.dump(data_posts, file, indent=4)