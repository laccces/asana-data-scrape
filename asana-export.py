import asana
import requests 

client = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')

result = client.projects.get_projects({'param': 'value', 'param': 'value'}, opt_pretty=True)


# import multiple tasks
import asana

client = asana.Client.access_token('PERSONAL_ACCESS_TOKEN')

result = client.tasks.get_tasks({'param': 'value', 'param': 'value'}, opt_pretty=True)

# get a time entry ID
import requests

url = "https://app.asana.com/api/1.0/tasks/1204021827439397/time_tracking_entries"

headers = {
    "accept": "application/json",
    "authorization": "Bearer PERSONAL_ACCESS_TOKEN"
}

response = requests.get(url, headers=headers)

print(response.text)

# Get a time tracking entry
import requests

url = "https://app.asana.com/api/1.0/time_tracking_entries/1204021827439402"

headers = {
    "accept": "application/json",
    "authorization": "Bearer PERSONAL_ACCESS_TOKEN"
}

response = requests.get(url, headers=headers)

print(response.text)
