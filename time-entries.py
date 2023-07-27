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

projects = list(client.projects.get_projects({
    'workspace': WORKSPACE,
    'archived': 'false',
    'opt_fields': 'name,gid,team.name,notes'
}, opt_pretty=True))

time_tracking_entries = []

for project in projects:
    tasks = client.tasks.get_tasks({
        'project': project['gid'],
        'modified_since': one_month_ago,
        'opt_fields': 'actual_time_minutes,notes,gid'
    }, opt_pretty=True)

    for task in tasks:
        actual_time = task.get('actual_time_minutes')
        if actual_time is not None:
            url = f"https://app.asana.com/api/1.0/tasks/{task['gid']}/time_tracking_entries?opt_fields=duration_minutes,entered_on,created_by,created_by.name"
            entries = requests.get(url, headers=headers).json()['data']

            for entry in entries:
                if entry['entered_on'] > one_month_ago:
                    entry.update({
                        'project_name': project['name'],
                        'project_gid': project['gid'],
                        'actual_time_minutes': actual_time,
                        'team.name': project.get('team', {}).get('name', 'nil'),
                        'project_notes': project.get('notes', '')
                    })
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
