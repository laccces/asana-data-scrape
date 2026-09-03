import asana
from asana.rest import ApiException
from pprint import pprint
import asana_utils

api_client = asana_utils.get_api_client()
memberships_api_instance = asana.MembershipsApi(api_client)

body = {"data": {"members": [{"gid": "1208429896521653", "resource_type": "editor"}]}}
membership_gid = "1208981846035227"

try:
    api_response = memberships_api_instance.update_membership(body, membership_gid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MembershipsApi->update_membership: %s\n" % e)