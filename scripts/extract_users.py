import json
import requests
import os

base_url = os.getenv("BASE_URL")
url = f"{base_url}/users"

response = requests.get(url)
response.raise_for_status()

print(response.status_code)

data_users = response.json()

with open('/home/marek/user_posts_pipeline/data/raw/users.json','w') as file:
    json.dump(data_users, file, indent=4)