import asana
from asana.rest import ApiException
import csv
import asana_utils

user_dict = asana_utils.load_user_dict('asana_users.csv')
config = asana_utils.load_config()
WORKSPACE = config['workspace']
api_client = asana_utils.get_api_client()

projects_api_instance = asana.ProjectsApi(api_client)
opts = {
    'workspace': WORKSPACE,
    'opt_fields': "name,owner,team.name,modified_at,completed"
}

try:
    api_response = projects_api_instance.get_projects(opts)
    
    with open('project-export.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'owner', 'owner_name', 'team', 'modified_at', 'gid', 'completed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for data in api_response:
            owner_gid = data['owner']['gid'] if data.get('owner') else ''
            owner_name = user_dict.get(owner_gid, '')
            team_name = data['team']['name'] if data.get('team') else ''
            gid = data.get('gid', '')
            completed = data.get('completed', False)
            writer.writerow({
                'name': data.get('name', ''),
                'owner': owner_gid,
                'owner_name': owner_name,
                'team': team_name,
                'gid': gid,
                'completed': completed,
                'modified_at': data.get('modified_at', '')
            })
    print("Export to CSV successful.")
except ApiException as e:
    print("Exception when calling ProjectsApi->get_projects: %s\n" % e)
