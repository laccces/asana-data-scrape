import asana
import requests 
import csv
import json
import os

with open('config.json', 'r') as f:
    config = json.load(f)

PERSONAL_ACCESS_TOKEN = config['api_key']

csv_filename = 'time_tracking_entries.csv'
csv_headers = ['gid', 'resource_type', 'duration_minutes', 'created_by', 'entered_on']

project_gid = "1203891839848794"

# get a project

client = asana.Client.access_token(PERSONAL_ACCESS_TOKEN)

result = client.tasks.get_tasks({'project':'1203891839848794'}, opt_pretty=True, headers={'asana-enable':'new_goal_memberships'})

gids = [task['gid'] for task in result]

with open(csv_filename, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=csv_headers)

    # Write the header
    writer.writeheader()

    # For each gid
    for gid in gids:
        url = "https://app.asana.com/api/1.0/tasks/" + gid + "/time_tracking_entries"

        headers = {
            "accept": "application/json",
            "authorization": "Bearer 1/1201719304365594:93eb946e8425cb45865ad7829a527f0c"
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
