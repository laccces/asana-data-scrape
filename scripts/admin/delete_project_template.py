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

delete_gids = [
    '1203104124077434',
    '1203104406189741'
]

for gid in delete_gids:
    try:
        api_response = project_templates_api_instance.delete_project_template(gid)
        pprint(api_response)
    except ApiException as e:
        print(f"Exception when calling ProjectTemplatesApi->delete_project_template for {gid}: {e}\n")

