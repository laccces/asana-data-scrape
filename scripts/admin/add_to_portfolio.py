import sys
import os
from pathlib import Path
import asana
from asana.rest import ApiException
import csv
from pprint import pprint

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import asana_utils

api_client = asana_utils.get_api_client()
portfolios_api_instance = asana.PortfoliosApi(api_client)

portfolio_gid = "1209422088955056"

project_export_csv = asana_utils.get_project_path('exports', 'project-export.csv')

if os.path.exists(project_export_csv):
    with open(project_export_csv, 'r', newline='', encoding='utf-8') as project_file:
        project_reader = csv.DictReader(project_file)
        
        for row in project_reader:
            project_gid = row.get('project_gid') or row.get('gid')
            if not project_gid:
                continue

            body = {
                "data": {
                    "item": project_gid
                }
            }  

            try:
                api_response = portfolios_api_instance.add_item_for_portfolio(body, portfolio_gid)
                pprint(api_response)
            except ApiException as e:
                print(f"Exception when calling PortfoliosApi->add_item_for_portfolio for project {project_gid}: {e.status}, {e}\n")
else:
    print(f"File not found: {project_export_csv}")

