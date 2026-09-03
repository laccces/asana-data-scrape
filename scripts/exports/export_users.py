import sys
from pathlib import Path
import asana
from asana.rest import ApiException
import csv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import asana_utils

config = asana_utils.load_config()
WORKSPACE = config['workspace']
api_client = asana_utils.get_api_client()

users_api_instance = asana.UsersApi(api_client)
opts = {
    'workspace': WORKSPACE,
    'opt_fields': "role,name,email,department",
}

output_csv = asana_utils.get_project_path('exports', 'asana_users.csv')

try:
    api_response = users_api_instance.get_users(opts)
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'name', 'role', 'department']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in api_response:
            writer.writerow({
                'id': user.get('gid', ''),
                'name': user.get('name', ''),
                'role': user.get('role', ''),
                'department': user.get('department', '')
            })
    print(f'Data exported to {output_csv}')
except ApiException as e:
    print("Exception when calling UsersApi->get_users: %s\n" % e)

