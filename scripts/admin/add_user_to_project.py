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
projects_api_instance = asana.ProjectsApi(api_client)

body = {"data": {"members": ["1206231603739123"]}}
project_gid = "1208981846035227"

try:
    api_response = projects_api_instance.add_members_for_project(body, project_gid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProjectsApi->add_members_for_project: %s\n" % e)

