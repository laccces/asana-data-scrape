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
project_templates_api_instance = asana.ProjectTemplatesApi(api_client)

team_gid = "1201824767642281"
opts = {}

try:
    api_response = project_templates_api_instance.get_project_templates_for_team(team_gid, opts=opts)
    for data in api_response:
        pprint(data)
except ApiException as e:
    print("Exception when calling ProjectTemplatesApi->get_project_templates_for_team: %s\n" % e)

