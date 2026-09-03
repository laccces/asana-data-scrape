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
memberships_api_instance = asana.MembershipsApi(api_client)
membership_gid = "1208981846035227"

try:
    api_response = memberships_api_instance.get_membership(membership_gid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MembershipsApi->get_membership: %s\n" % e)

