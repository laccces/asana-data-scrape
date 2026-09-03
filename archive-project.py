import os
import asana
from asana.rest import ApiException
from pprint import pprint
import asana_utils

api_client = asana_utils.get_api_client()
projects_api_instance = asana.ProjectsApi(api_client)

imported_gids = 'id_numbers.txt'
project_gids = []

if os.path.exists(imported_gids):
    with open(imported_gids, 'r') as file:
        for line in file:
            gid = line.strip()
            if gid:
                project_gids.append(gid)
else:
    project_gids = []

for project_gid in project_gids:
    try:
        project_details_before = projects_api_instance.get_project(project_gid, opts={'opt_fields': 'name,archived'})
        print(f"Project Details Before Update ({project_gid}):")
        pprint(project_details_before)
    except ApiException as e:
        print(f"Exception when calling ProjectsApi->get_project for {project_gid}: {e}\n")

    body = {"data": {"archived": True}}
    opts = {'opt_fields': 'name,archived'}
    try:
        api_response = projects_api_instance.update_project(body, project_gid, opts=opts)
        print(f"Project Details After Update ({project_gid}):")
        pprint(api_response)
    except ApiException as e:
        print(f"Exception when calling ProjectsApi->update_project for {project_gid}: {e}\n")