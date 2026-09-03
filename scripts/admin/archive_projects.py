import sys
import os
from pathlib import Path
import asana
from asana.rest import ApiException
from pprint import pprint

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import asana_utils

api_client = asana_utils.get_api_client()
projects_api_instance = asana.ProjectsApi(api_client)

imported_gids_path = asana_utils.get_project_path('data', 'id_numbers.txt')
project_gids = []

if os.path.exists(imported_gids_path):
    with open(imported_gids_path, 'r', encoding='utf-8') as file:
        for line in file:
            gid = line.strip()
            if gid:
                project_gids.append(gid)

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

