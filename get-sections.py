import asana
from asana.rest import ApiException
from pprint import pprint
import asana_utils

api_client = asana_utils.get_api_client()
sections_api_instance = asana.SectionsApi(api_client)

project_gid = "1213134639377600"  # Globally unique identifier for the project.
opts = {
    'limit': 50,
    'opt_fields': "created_at,name,path,project,project.name,projects,projects.name,uri",
}

try:
    # Get sections in a project
    api_response = sections_api_instance.get_sections_for_project(project_gid, opts)
    for data in api_response:
        pprint(data)
except ApiException as e:
    print("Exception when calling SectionsApi->get_sections_for_project: %s\n" % e)