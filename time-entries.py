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

# Fetch projects with required fields upfront
projects = list(client.projects.get_projects({
    'workspace': WORKSPACE,
    'archived': 'false',
    'opt_fields': 'name,gid,team.name'
}, opt_pretty=True))

all_tasks = []

# Loop through the projects and get all the tasks updated in the last month
for project in projects:
    project_name = project['name']
    project_gid = project['gid']
    company = project.get('team', {}).get('name', 'nil')

    project_data = client.projects.get_project(project_gid, opt_pretty=True)
    project_notes = project_data.get('notes', '')

    # print out project attribute of your choice
    # print(f"{project_name} ({project_gid}):")
    # print(project_data.get('notes'))

    tasks = client.tasks.get_tasks({
        'project': project_gid,
        'modified_since': one_month_ago,
        'opt_fields': 'actual_time_minutes,notes'
    }, opt_pretty=True)
    for task in tasks:
        if 'actual_time_minutes' in task and task['actual_time_minutes'] is not None:
            task['project_name'] = project_name
            task['project_gid'] = project_gid
            task['team.name'] = company
            task['project_notes'] = project_notes
            all_tasks.append(task)

time_tracking_entries = []

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {PERSONAL_ACCESS_TOKEN}"
}

for task in all_tasks:
    gid = task['gid']
    url = f"https://app.asana.com/api/1.0/tasks/{gid}/time_tracking_entries?opt_fields=duration_minutes,entered_on,created_by,created_by.name"
    response = requests.get(url, headers=headers)
    entries = response.json()['data']
    for entry in entries:
        if entry['entered_on'] > one_month_ago:
            entry['project_name'] = task['project_name']
            entry['project_gid'] = task['project_gid']
            entry['actual_time_minutes'] = task['actual_time_minutes']
            entry['team.name'] = task['team.name']
            entry['project_notes'] = task['project_notes']
            time_tracking_entries.append(entry)

# Save to CSV
with open('report.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['time_entry_id', 'employee_gid', 'employee_name', 'entered_on', 'project_name', 'project_gid', 'actual_time_minutes', 'company', 'NS Job ID'])
    for entry in time_tracking_entries:
        writer.writerow([
            entry['gid'],
            entry['created_by']['gid'],
            entry['created_by']['name'],
            entry['entered_on'],
            entry['project_name'],
            entry['project_gid'],
            entry['actual_time_minutes'],
            entry['team.name'],
            entry['project_notes']
        ])

print("CSV report created successfully!")
