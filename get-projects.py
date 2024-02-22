import asana
import csv
import json
from asana.rest import ApiException
from pprint import pprint

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
    'opt_fields': "name,owner,team.name,modified_at"
}

try:
    # Get multiple projects
    api_response = projects_api_instance.get_projects(opts)
    
    # Write data to CSV file
    with open('project-export.csv', 'w', newline='') as csvfile:
        fieldnames = ['name', 'owner', 'team', 'modified_at']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for data in api_response:
            owner_gid = data['owner']['gid'] if data.get('owner') else ''
            team_gid = data['team']['gid'] if data.get('team') else ''
            writer.writerow({'name': data['name'],
                             'owner': owner_gid,
                             'team': team_gid,
                             'modified_at': data['modified_at']})
    print("Export to CSV successful.")
except ApiException as e:
    print("Exception when calling ProjectsApi->get_projects: %s\n" % e)
