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
    'opt_fields': "name,owner,team,modified_at"
}

try:
    # Get multiple projects
    api_response = projects_api_instance.get_projects(opts)
    for data in api_response:
        pprint(data)
except ApiException as e:
    print("Exception when calling ProjectsApi->get_projects: %s\n" % e)