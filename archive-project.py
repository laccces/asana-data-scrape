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

# create an instance of the API class
projects_api_instance = asana.ProjectsApi(api_client)
body = {"data": {"archived": True}} # dict | The updated fields for the project.
project_gid = "1205116582693549" # str | Globally unique identifier for the project.
opts = {}

try:
    # Update a project
    api_response = projects_api_instance.update_project(body, project_gid, opts)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsApi->update_project: %s\n" % e)