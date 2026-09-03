import asana
from asana.rest import ApiException
from pprint import pprint
import asana_utils

api_client = asana_utils.get_api_client()
project_templates_api_instance = asana.ProjectTemplatesApi(api_client)

delete_gids = [
    '1203104124077434',
    '1203104406189741',
    '1203104255059400',
    '1203112478730894',
    '1203087991587177',
    '1203105881549015',
    '1203103735247941'
]

for gid in delete_gids:
    try:
        api_response = project_templates_api_instance.delete_project_template(gid)
        pprint(api_response)
    except ApiException as e:
        print(f"Exception when calling ProjectTemplatesApi->delete_project_template for {gid}: {e}\n")