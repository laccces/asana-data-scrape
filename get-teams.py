import asana
import csv
import json
from asana.rest import ApiException
from pprint import pprint

with open('config.json', 'r') as f:
    config = json.load(f)

PERSONAL_ACCESS_TOKEN = config['api_key']
WORKSPACE = config['workspace']

configuration = asana.Configuration()
configuration.access_token = PERSONAL_ACCESS_TOKEN
api_client = asana.ApiClient(configuration)

# create an instance of the API class
teams_api_instance = asana.TeamsApi(api_client)
workspace_gid = "12345" # str | Globally unique identifier for the workspace or organization.
opts = {
    'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.
    'offset': "eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*
    'opt_fields': "description,edit_team_name_or_description_access_level,edit_team_visibility_or_trash_team_access_level,guest_invite_management_access_level,html_description,join_request_management_access_level,member_invite_management_access_level,name,offset,organization,organization.name,path,permalink_url,team_content_management_access_level,team_member_removal_access_level,uri,visibility", # list[str] | This endpoint returns a compact resource, which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.
}

try:
    # Get teams in a workspace
    api_response = teams_api_instance.get_teams_for_workspace(workspace_gid, opts)
    for data in api_response:
        pprint(data)
except ApiException as e:
    print("Exception when calling TeamsApi->get_teams_for_workspace: %s\n" % e)