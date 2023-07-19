import asana
import requests
import json
from datetime import datetime, timedelta

with open('config.json', 'r') as f:
    config = json.load(f)

PERSONAL_ACCESS_TOKEN = config['api_key']
WORKSPACE = config['workspace']

client = asana.Client.access_token(PERSONAL_ACCESS_TOKEN)

one_month_ago = (datetime.now() - timedelta(days=30)).isoformat()

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {PERSONAL_ACCESS_TOKEN}"
}

# Get a list of all active projects in the workspace
result = client.projects.get_projects({'workspace': WORKSPACE, 'archived': 'false'}, opt_pretty=True)

project_gids = [project['gid'] for project in result]

all_tasks = []

# Loop through the projects and get all the tasks updated in the last month
for project_gid in project_gids:
    tasks = client.tasks.get_tasks({'project': project_gid, 'modified_since': one_month_ago, 'opt_fields': 'actual_time_minutes'}, opt_pretty=True)
    all_tasks.extend([task for task in tasks if 'actual_time_minutes' in task and task['actual_time_minutes'] is not None])

time_tracking_entries = []

for task in all_tasks:
    gid = task['gid']
    url = f"https://app.asana.com/api/1.0/tasks/{gid}/time_tracking_entries?opt_fields=duration_minutes,entered_on,created_by,created_by.name"
    response = requests.get(url, headers=headers)
    time_tracking_entries.extend(entry for entry in response.json()['data'] if entry['entered_on'] > one_month_ago)

print(time_tracking_entries)
