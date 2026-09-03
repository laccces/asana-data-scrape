import sys
from pathlib import Path
import asana
from asana.rest import ApiException
from pprint import pprint

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import asana_utils

api_client = asana_utils.get_api_client()
portfolios_api_instance = asana.PortfoliosApi(api_client)

project_gids = [
    "1210164269566314",
    "1207203291815834",
    "1210753060687727"
]

portfolio_gid = "1209422088955056"

for gid in project_gids:
    body = {"data": {"item": gid}}

    try:
        api_response = portfolios_api_instance.remove_item_for_portfolio(body, portfolio_gid)
        pprint(api_response)
    except ApiException as e:
        print(f"Exception when calling PortfoliosApi->remove_item_for_portfolio for project {gid}: {e.status}, {e}\n")

print("Portfolio items removed successfully.")

