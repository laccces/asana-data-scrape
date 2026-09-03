import asana
from asana.rest import ApiException
import csv
from pprint import pprint
import asana_utils

config = asana_utils.load_config()
WORKSPACE = config['workspace']
api_client = asana_utils.get_api_client()

teams_api_instance = asana.TeamsApi(api_client)

opts = {}

try:
    api_response = teams_api_instance.get_teams_for_workspace(WORKSPACE, opts=opts)
    teams_list = list(api_response)
    pprint(teams_list)

    with open('teams-export.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['gid', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for data in teams_list:
            writer.writerow({'gid': data.get('gid', ''), 'name': data.get('name', '')})

    print("Export to CSV successful.")

except ApiException as e:
    print("Exception when calling TeamsApi->get_teams_for_workspace: %s\n" % e)