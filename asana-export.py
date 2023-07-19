import asana
import requests 
import csv
import json
import os

with open('config.json', 'r') as f:
    config = json.load(f)

PERSONAL_ACCESS_TOKEN = config['api_key']
WORKSPACE = config['workspace']

client = asana.Client.access_token(PERSONAL_ACCESS_TOKEN)

csv_filename = 'time_tracking_entries.csv'
csv_headers = ['gid', 'resource_type', 'duration_minutes', 'created_by', 'entered_on']

# Fetch all projects
result = client.projects.get_projects({'workspace': WORKSPACE, 'archived': 'false'}, opt_pretty=True)

# Create a list of project gids
project_gids = [project['gid'] for project in result]

with open(csv_filename, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=csv_headers)

    # Write the header
    writer.writeheader()

    # Loop through each project gid
    for project_gid in project_gids:
        # Fetch all tasks for the given project
        tasks = client.tasks.get_tasks({'project': project_gid}, opt_pretty=True)

        # Extract task gids
        task_gids = [task['gid'] for task in tasks]

        # For each task gid
        for task_gid in task_gids:
            url = "https://app.asana.com/api/1.0/tasks/" + task_gid + "/time_tracking_entries"

            headers = {
                "accept": "application/json",
                "authorization": "Bearer " + PERSONAL_ACCESS_TOKEN
            }

            # Get the response
            response = requests.get(url, headers=headers)

            # Parse the response text into a dictionary
            response_data = json.loads(response.text)

            # Extract the actual data from the response (which is a list)
            data_list = response_data.get('data', [])

            # Write each dictionary in the list to the CSV file
            for data in data_list:
                # Extract the 'name' from the 'created_by' dictionary
                created_by_name = data['created_by'].get('name')
                data['created_by'] = created_by_name
                writer.writerow(data)
