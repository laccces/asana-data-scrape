import asana
import csv
import json
from asana.rest import ApiException
from pprint import pprint

# Load user data from asana_users.csv into a dictionary
user_dict = {}
with open('asana_users.csv', 'r', newline='') as user_file:
    user_reader = csv.DictReader(user_file)
    for row in user_reader:
        user_dict[row['id']] = row['name']

with open('config.json', 'r') as f:
    config = json.load(f)

PERSONAL_ACCESS_TOKEN = config['api_key']
WORKSPACE = config['workspace']

configuration = asana.Configuration()
configuration.access_token = PERSONAL_ACCESS_TOKEN
api_client = asana.ApiClient(configuration)

# create an instance of the API class
projects_api_instance = asana.ProjectsApi(api_client)
opts = {
    'workspace': WORKSPACE,
    'archived': False,
    'opt_fields': "name,owner,team.name,modified_at,project_gid"
}

try:
    # Get multiple projects
    api_response = projects_api_instance.get_projects(opts)
    
    # Write data to CSV file
    with open('project-export.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'owner', 'owner_name', 'team', 'modified_at', 'project_gid']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for data in api_response:
            owner_gid = data['owner']['gid'] if data.get('owner') else ''
            owner_name = user_dict.get(owner_gid, '')  # Look up owner name from the dictionary
            team_name = data['team']['name'] if data.get('team') else ''
            project_gid = data['gid']
            writer.writerow({'name': data['name'],
                             'owner': owner_gid,
                             'owner_name': owner_name,
                             'team': team_name,
                             'modified_at': data['modified_at'],
                             'project_gid': project_gid})
    print("Export to CSV successful.")
except ApiException as e:
    print("Exception when calling ProjectsApi->get_projects: %s\n" % e)
