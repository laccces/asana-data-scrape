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

projects = list(client.projects.get_projects({
    'workspace': WORKSPACE,
    'archived': 'false',
    'opt_fields': 'name,gid,team.name,modified_at'
}, opt_pretty=True))

# Prepare the data for CSV export
project_data = []
for project in projects:
    project_data.append({
        'Name': project['name'],
        'GID': project['gid'],
        'Team': project['team']['name'],
        'Modified': project['modified_at']
    })

# Define the CSV file path
csv_file_path = 'projects-export.csv'

# Write the project data to the CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    fieldnames = ['Name', 'GID', 'Team', 'Modified']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    writer.writeheader()
    for project in project_data:
        writer.writerow(project)

print(f'Projects have been exported to {csv_file_path}')
