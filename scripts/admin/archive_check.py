import sys
from pathlib import Path
import asana
from asana.rest import ApiException
from pprint import pprint

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import asana_utils

api_client = asana_utils.get_api_client()
projects_api = asana.ProjectsApi(api_client)

project_gid_list = ["xxxxx", "xxxxx"]

for project_gid in project_gid_list:
    try:
        result = projects_api.get_project(project_gid, opts={'opt_fields': 'name,team.name,archived'})
        pprint(result)
    except ApiException as e:
        print(f"Exception when calling ProjectsApi->get_project for {project_gid}: {e}\n")

