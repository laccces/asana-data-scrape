import asana
import csv
import json
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def get_project_path(*path_segments):
    """Helper to get an absolute path relative to the project root."""
    return os.path.join(PROJECT_ROOT, *path_segments)

def load_config(config_path=None):
    """Load configuration from JSON file."""
    if config_path is None:
        config_path = get_project_path('config.json')
    elif not os.path.isabs(config_path):
        config_path = get_project_path(config_path)

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def get_api_client(config_path=None):
    """Initialize and return an Asana API client using v4 SDK."""
    config = load_config(config_path)
    personal_access_token = config.get('api_key')
    if not personal_access_token:
        raise ValueError("api_key not found in configuration file.")
    
    configuration = asana.Configuration()
    configuration.access_token = personal_access_token
    return asana.ApiClient(configuration)

def load_user_dict(csv_path=None):
    """Load user GID to name mapping from CSV file if present."""
    if csv_path is None:
        csv_path = get_project_path('exports', 'asana_users.csv')
        if not os.path.exists(csv_path):
            csv_path = get_project_path('asana_users.csv')
    elif not os.path.isabs(csv_path):
        csv_path = get_project_path(csv_path)

    user_dict = {}
    if os.path.exists(csv_path):
        with open(csv_path, 'r', newline='', encoding='utf-8') as user_file:
            user_reader = csv.DictReader(user_file)
            for row in user_reader:
                user_id = row.get('id') or row.get('gid')
                if user_id:
                    user_dict[user_id] = row.get('name', '')
    return user_dict
