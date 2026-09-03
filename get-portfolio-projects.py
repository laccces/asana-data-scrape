import asana
from asana.rest import ApiException
import csv
from pprint import pprint
import asana_utils

api_client = asana_utils.get_api_client()
portfolios_api_instance = asana.PortfoliosApi(api_client)

portfolio_gid = "1209422088955056" 
opts = {
    'opt_fields': "due_date, name, modified_at"
}

try:
    # Get portfolio items
    api_response = portfolios_api_instance.get_items_for_portfolio(portfolio_gid, opts)

    # Write data to CSV file
    with open('portfolio-export.csv', 'w', newline='', encoding='utf-8') as csvfile:
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
    print("Export to CSV successful.")
except ApiException as e:
    print("Exception when calling PortfoliosApi->get_items_for_portfolio: %s\n" % e)