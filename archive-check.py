import asana
import requests
import json
import csv
from datetime import datetime, timedelta

with open('config.json', 'r') as f:
    config = json.load(f)

PERSONAL_ACCESS_TOKEN = config['api_key']
WORKSPACE = config['workspace']

client = asana.Client.access_token(PERSONAL_ACCESS_TOKEN)

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {PERSONAL_ACCESS_TOKEN}"
}

project_gid_list = ["1205116582654603", "1205116338200473", "1205116582639456", "1205116582729758"]

for project_gid in project_gid_list:
    result = client.projects.get_project(project_gid, {'opt_fields': 'name,team.name,archived'}, opt_pretty=True)
    
    print(result)