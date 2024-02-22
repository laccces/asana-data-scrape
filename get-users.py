import csv
import json
import asana
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
users_api_instance = asana.UsersApi(api_client)
opts = {
    'workspace': WORKSPACE,
    'opt_fields': "name",
}

csv_file = 'asana_users.csv'

try:
    # Get multiple users
    api_response = users_api_instance.get_users(opts)
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'name']  # Define the fields you want to include in the CSV
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in api_response:
            writer.writerow({'id': user['gid'], 'name': user['name']})
    print(f'Data exported to {csv_file}')
except ApiException as e:
    print("Exception when calling UsersApi->get_users: %s\n" % e)
