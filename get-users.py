import asana
from asana.rest import ApiException
import csv
import asana_utils

config = asana_utils.load_config()
WORKSPACE = config['workspace']
api_client = asana_utils.get_api_client()

users_api_instance = asana.UsersApi(api_client)
opts = {
    'workspace': WORKSPACE,
    'opt_fields': "role,name,email,department",
}

csv_file = 'asana_users.csv'

try:
    api_response = users_api_instance.get_users(opts)
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
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
    print(f'Data exported to {csv_file}')
except ApiException as e:
    print("Exception when calling UsersApi->get_users: %s\n" % e)
