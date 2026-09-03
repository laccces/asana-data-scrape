import sys
from pathlib import Path
import asana
from asana.rest import ApiException
import csv
from datetime import datetime, timedelta

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import asana_utils

config = asana_utils.load_config()
WORKSPACE = config['workspace']
api_client = asana_utils.get_api_client()

projects_api = asana.ProjectsApi(api_client)
tasks_api = asana.TasksApi(api_client)
time_entries_api = asana.TimeTrackingEntriesApi(api_client)

thirty_days_ago = datetime.now() - timedelta(days=30)
one_month_ago_date = thirty_days_ago.strftime('%Y-%m-%d')
one_month_ago_iso = thirty_days_ago.strftime('%Y-%m-%dT%H:%M:%SZ')

time_tracking_entries = []

try:
    projects = list(projects_api.get_projects({
        'workspace': WORKSPACE,
        'archived': False,
        'opt_fields': 'name,gid,team.name,notes'
    }))

    for project in projects:
        project_gid = project.get('gid')
        project_name = project.get('name', '')
        team_name = project.get('team', {}).get('name', 'nil') if project.get('team') else 'nil'
        project_notes = project.get('notes', '')

        tasks = list(tasks_api.get_tasks_for_project(project_gid, {
            'modified_since': one_month_ago_iso,
            'opt_fields': 'actual_time_minutes,notes,gid'
        }))

        for task in tasks:
            actual_time = task.get('actual_time_minutes')
            if actual_time is not None:
                entries = list(time_entries_api.get_time_tracking_entries_for_task(
                    task['gid'],
                    {'opt_fields': 'duration_minutes,entered_on,created_by,created_by.name'}
                ))

                for entry in entries:
                    entered_on = entry.get('entered_on', '')
                    if entered_on and entered_on >= one_month_ago_date:
                        created_by = entry.get('created_by') or {}
                        entry_record = {
                            'gid': entry.get('gid', ''),
                            'created_by_gid': created_by.get('gid', ''),
                            'created_by_name': created_by.get('name', ''),
                            'entered_on': entered_on,
                            'project_name': project_name,
                            'project_gid': project_gid,
                            'actual_time_minutes': actual_time,
                            'team_name': team_name,
                            'project_notes': project_notes
                        }
                        time_tracking_entries.append(entry_record)

    output_csv = asana_utils.get_project_path('exports', 'report.csv')
    with open(output_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['time_entry_id', 'employee_gid', 'employee_name', 'entered_on', 'project_name', 'project_gid', 'actual_time_minutes', 'company', 'NS Job ID'])
        
        for entry in time_tracking_entries:
            writer.writerow([
                entry['gid'],
                entry['created_by_gid'],
                entry['created_by_name'],
                entry['entered_on'],
                entry['project_name'],
                entry['project_gid'],
                entry['actual_time_minutes'],
                entry['team_name'],
                entry['project_notes']
            ])

    print(f"CSV report created successfully! Saved {len(time_tracking_entries)} entries to {output_csv}.")

except ApiException as e:
    print(f"Exception when calling Asana API: {e}\n")

