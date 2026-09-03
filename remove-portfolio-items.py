import asana
from asana.rest import ApiException
from pprint import pprint
import asana_utils

api_client = asana_utils.get_api_client()
portfolios_api_instance = asana.PortfoliosApi(api_client)

project_gids = [
    "1210164269566314",
    "1207203291815834",
    "1210753060687727",
    "1210714874931856",
    "1210629734584654",
    "1208340084319202",
    "1205116269057268",
    "1209921392190669",
    "1209810361681265",
    "1209648759399430",
    "1209491564395894",
    "1208650177501624",
    "1206493939691332",
    "1207977496887437",
    "1207867169100418",
    "1208156882848362",
    "1208829262825323",
    "1206286183634715",
    "1207896922765502",
    "1208282585886427",
    "1206441532814394",
    "1209257625650591",
    "1208019555096740",
    "1207168798735210",
    "1206520964378478"
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