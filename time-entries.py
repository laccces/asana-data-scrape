import asana
import requests 
import csv
import json
import os
from datetime import datetime, timedelta

with open('config.json', 'r') as f:
    config = json.load(f)

PERSONAL_ACCESS_TOKEN = config['api_key']
WORKSPACE = config['workspace']

client = asana.Client.access_token(PERSONAL_ACCESS_TOKEN)

# Get a list of all active projects in the workspace
result = client.projects.get_projects({'workspace': WORKSPACE, 'archived': 'false'}, opt_pretty=True)

project_gids = [project['gid'] for project in result]

# Loop through the projects and use the /tasks (get multiple tasks) endpoint to get all the tasks updated in the last month (this assumes adding time is considered updating a task, something I need to validate)

one_month_ago = (datetime.now() - timedelta(days=30)).isoformat()

all_tasks = []

for project_gid in project_gids:
    tasks = client.tasks.get_tasks({'project': project_gid, 'modified_since': one_month_ago, 'opt_fields': 'actual_time_minutes'}, opt_pretty=True)
    all_tasks.extend(list(tasks))

# filter those tasks to those which actually have time on them

tasks_with_time_entries = [task for task in all_tasks if 'actual_time_minutes' in task and task['actual_time_minutes'] is not None]

# Loop through the resulting list of tasks and query the time entries for those

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {PERSONAL_ACCESS_TOKEN}"
}

time_tracking_entries = []

for task in tasks_with_time_entries:
    gid = task['gid']
    url = f"https://app.asana.com/api/1.0/tasks/{gid}/time_tracking_entries?opt_fields=duration_minutes,entered_on"
    response = requests.get(url, headers=headers)
    time_tracking_entries.append(response.json())

# filter out the time entries that aren’t in the last month

one_month_ago = (datetime.now() - timedelta(days=30)).date().isoformat()

recent_time_tracking_entries = []

for entries in time_tracking_entries:
    for entry in entries['data']:
        # Check if the entry is from the last month
        if entry['entered_on'] > one_month_ago:
            recent_time_tracking_entries.append(entry)

print(recent_time_tracking_entries)