import sys
from pathlib import Path
import asana
from asana.rest import ApiException
import csv
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import asana_utils

user_dict = asana_utils.load_user_dict()
config = asana_utils.load_config()
WORKSPACE = config['workspace']
api_client = asana_utils.get_api_client()

projects_api_instance = asana.ProjectsApi(api_client)
tasks_api_instance = asana.TasksApi(api_client)

def get_project_tasks_info(project_gid):
    """Get task counts and last activity date for a project"""
    try:
        opts = {
            'project': project_gid,
            'opt_fields': 'completed,modified_at',
            'limit': 100
        }
        tasks = tasks_api_instance.get_tasks(opts)

        total_tasks = 0
        completed_tasks = 0
        active_tasks = 0
        last_modified = None

        for task in tasks:
            total_tasks += 1
            if task.get('completed'):
                completed_tasks += 1
            else:
                active_tasks += 1

            task_modified = task.get('modified_at')
            if task_modified:
                task_modified_dt = datetime.fromisoformat(task_modified.replace('Z', '+00:00'))
                if last_modified is None or task_modified_dt > last_modified:
                    last_modified = task_modified_dt

        last_activity = last_modified.isoformat() if last_modified else ''
        return total_tasks, active_tasks, completed_tasks, last_activity
    except ApiException as e:
        print(f"Warning: Could not fetch tasks for project {project_gid}: {e}")
        return 0, 0, 0, ''


opts = {
    'workspace': WORKSPACE,
    'archived': False,
    'opt_fields': 'name,owner,team.name,modified_at,completed,due_on,start_on,created_at,is_template,current_status,color,public'
}

try:
    api_response = projects_api_instance.get_projects(opts)
    output_csv = asana_utils.get_project_path('exports', 'project-export.csv')

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'name', 'owner', 'owner_name', 'team', 'project_gid', 'completed',
            'created_at', 'start_on', 'due_on', 'modified_at', 'last_task_activity',
            'total_tasks', 'active_tasks', 'completed_tasks',
            'is_template', 'status', 'color', 'public'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        projects_list = list(api_response)
        for idx, data in enumerate(projects_list, 1):
            gid = data.get('gid', '')
            owner_gid = data['owner']['gid'] if data.get('owner') else ''
            owner_name = user_dict.get(owner_gid, '')
            team_name = data['team']['name'] if data.get('team') else ''

            print(f"Processing project {idx}/{len(projects_list)}: {data.get('name', 'Unknown')} ({gid})")

            total_tasks, active_tasks, completed_tasks, last_activity = get_project_tasks_info(gid)

            status = data.get('current_status', {})
            status_text = status.get('text') if isinstance(status, dict) else ''

            writer.writerow({
                'name': data.get('name', ''),
                'owner': owner_gid,
                'owner_name': owner_name,
                'team': team_name,
                'project_gid': gid,
                'completed': data.get('completed', False),
                'created_at': data.get('created_at', ''),
                'start_on': data.get('start_on', ''),
                'due_on': data.get('due_on', ''),
                'modified_at': data.get('modified_at', ''),
                'last_task_activity': last_activity,
                'total_tasks': total_tasks,
                'active_tasks': active_tasks,
                'completed_tasks': completed_tasks,
                'is_template': data.get('is_template', False),
                'status': status_text,
                'color': data.get('color', ''),
                'public': data.get('public', False)
            })
            csvfile.flush()

    print(f"\nExport to CSV successful: {output_csv}")
except ApiException as e:
    print("Exception when calling ProjectsApi->get_projects: %s\n" % e)

