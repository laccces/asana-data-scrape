import sys
from pathlib import Path
import asana
from asana.rest import ApiException
import csv
from pprint import pprint

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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

    output_csv = asana_utils.get_project_path('exports', 'teams-export.csv')
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['gid', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for data in teams_list:
            writer.writerow({'gid': data.get('gid', ''), 'name': data.get('name', '')})

    print(f"Export to CSV successful: {output_csv}")

except ApiException as e:
    print("Exception when calling TeamsApi->get_teams_for_workspace: %s\n" % e)

