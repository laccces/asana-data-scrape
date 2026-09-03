import asana
import csv
import json
import os

def load_config(config_path='config.json'):
    """Load configuration from JSON file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config

def get_api_client(config_path='config.json'):
    """Initialize and return an Asana API client using v4 SDK."""
    config = load_config(config_path)
    personal_access_token = config.get('api_key')
    if not personal_access_token:
        raise ValueError("api_key not found in configuration file.")
    
    configuration = asana.Configuration()
    configuration.access_token = personal_access_token
    return asana.ApiClient(configuration)

def load_user_dict(csv_path='asana_users.csv'):
    """Load user GID to name mapping from CSV file if present."""
    user_dict = {}
    if os.path.exists(csv_path):
        with open(csv_path, 'r', newline='', encoding='utf-8') as user_file:
            user_reader = csv.DictReader(user_file)
            for row in user_reader:
                user_id = row.get('id') or row.get('gid')
                if user_id:
                    user_dict[user_id] = row.get('name', '')
    return user_dict

