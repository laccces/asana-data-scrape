import asana
import requests
from asana.rest import ApiException
from pprint import pprint
import json
import csv
from datetime import datetime, timedelta

with open('config.json', 'r') as f:
    config = json.load(f)

PERSONAL_ACCESS_TOKEN = config['api_key']
WORKSPACE = config['workspace']

configuration = asana.Configuration()
configuration.access_token = PERSONAL_ACCESS_TOKEN
api_client = asana.ApiClient(configuration)

# create an instance of the API class
projects_api_instance = asana.ProjectsApi(api_client)

project_gids = ["1205116338164165", "1205116338251102"]  # str | Globally unique identifier for the project.

# Get the project details before updating
for project_gid in project_gids:
    try:
        project_details_before = projects_api_instance.get_project(project_gid, opts={'opt_fields': 'name,archived'})
        print("Project Details Before Update:")
        pprint(project_details_before)
    except ApiException as e:
        print("Exception when calling ProjectsApi->get_project: %s\n" % e)

    # Update the project
    body = {"data": {"archived": True}}  # dict | The updated fields for the project.
    opts = {'opt_fields': 'name, archived'}
    try:
        # Update a project
        api_response = projects_api_instance.update_project(body, project_gid, opts)
        print("Project Details After Update:")
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ProjectsApi->update_project: %s\n" % e)