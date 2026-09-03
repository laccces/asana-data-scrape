import asana
from asana.rest import ApiException
import csv
from pprint import pprint
import asana_utils

api_client = asana_utils.get_api_client()
portfolios_api_instance = asana.PortfoliosApi(api_client)

portfolio_gid = "1209422088955056"  # Globally unique identifier for the portfolio.

# Read projects from CSV and add them to the portfolio
with open('project-export.csv', 'r', newline='', encoding='utf-8') as project_file:
    project_reader = csv.DictReader(project_file)
    
    for row in project_reader:
        project_gid = row['gid']

        body = {
            "data": {
                "item": project_gid
            }
        }  

        try:
            # Add a portfolio item
            api_response = portfolios_api_instance.add_item_for_portfolio(body, portfolio_gid)
            pprint(api_response)
        except ApiException as e:
            print(f"Exception when calling PortfoliosApi->add_item_for_portfolio for project {project_gid}: {e.status}, {e}\n")