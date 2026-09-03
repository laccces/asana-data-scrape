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

api_client = asana_utils.get_api_client()
portfolios_api_instance = asana.PortfoliosApi(api_client)

portfolio_gid = "1209422088955056" 
opts = {
    'opt_fields': "due_date, name, modified_at"
}

try:
    api_response = portfolios_api_instance.get_items_for_portfolio(portfolio_gid, opts)
    output_csv = asana_utils.get_project_path('exports', 'portfolio-export.csv')

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'due_date', 'modified_at', 'gid']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for data in api_response:
            writer.writerow({
                'name': data.get('name', ''),
                'gid': data.get('gid', ''),
                'modified_at': data.get('modified_at', ''),
                'due_date': data.get('due_date', '')
            })
    print(f"Export to CSV successful: {output_csv}")
except ApiException as e:
    print("Exception when calling PortfoliosApi->get_items_for_portfolio: %s\n" % e)

