import asana
from asana.rest import ApiException
from pprint import pprint
import asana_utils

api_client = asana_utils.get_api_client()
tasks_api_instance = asana.TasksApi(api_client)

task_gid = "1208914039148860"
opts = {
    'opt_fields': "memberships.section,memberships.section.name"
}

try:
    api_response = tasks_api_instance.get_task(task_gid, opts=opts)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TasksApi->get_task: %s\n" % e)