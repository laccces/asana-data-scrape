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

one_month_ago = (datetime.now() - timedelta(days=30)).isoformat()

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {PERSONAL_ACCESS_TOKEN}"
}

# Get a list of all active projects in the workspace
projects = list(client.projects.get_projects({'workspace': WORKSPACE, 'archived': 'false'}, opt_pretty=True))

all_tasks = []

# Loop through the projects and get all the tasks updated in the last month
for project in projects:
    project_name = project['name']
    project_gid = project['gid']
    tasks = client.tasks.get_tasks({'project': project['gid'], 'modified_since': one_month_ago, 'opt_fields': 'actual_time_minutes'}, opt_pretty=True)
    for task in tasks:
        if 'actual_time_minutes' in task and task['actual_time_minutes'] is not None:
            task['project_name'] = project_name
            task['project_gid'] = project_gid
            all_tasks.append(task)

time_tracking_entries = []

for task in all_tasks:
    gid = task['gid']
    url = f"https://app.asana.com/api/1.0/tasks/{gid}/time_tracking_entries?opt_fields=duration_minutes,entered_on,created_by,created_by.name"
    response = requests.get(url, headers=headers)
    entries = response.json()['data']
    for entry in entries:
        if entry['entered_on'] > one_month_ago:
            entry['project_name'] = task['project_name']
            entry['project_gid'] = task['project_gid']
            time_tracking_entries.append(entry)

# Save to CSV
with open('report.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(['time_entry_id', 'employee_gid', 'employee_name', 'entered_on', 'project_name', 'project_gid'])
    
    # Write the data rows
    for entry in time_tracking_entries:
        writer.writerow([
            entry['gid'],
            entry['created_by']['gid'],
            entry['created_by']['name'],
            entry['entered_on'],
            entry['project_name'],
            entry['project_gid'],
        ])

print("CSV report created successfully!")
