import requests
import asana_utils

def get_workspaces(token):
    url = "https://app.asana.com/api/1.0/workspaces"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print("Sending request to Asana API...")

    response = requests.get(url, headers=headers)

    print(f"Response Status Code: {response.status_code}")
    
    if response.status_code == 200:
        workspaces = response.json().get("data", [])
        for workspace in workspaces:
            print(f"Workspace Name: {workspace['name']}, GID: {workspace['gid']}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    config = asana_utils.load_config()
    personal_access_token = config.get('api_key')
    get_workspaces(personal_access_token)