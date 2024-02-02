###################################################################
#  Grafana HTTP API : Create a Dashbaord : /api/dashboards/db 
###################################################################

import requests
import json
from requests.auth import HTTPBasicAuth
import configparser

def process_dashboard_json(json_file_path):
    # Read JSON template from the file
    with open(json_file_path, 'r') as file:
        dashboard_json = json.load(file)
    # Check if dashboard ID is null, make it null
    if 'id' in dashboard_json['dashboard'] and dashboard_json['dashboard']['id'] is not None:
        dashboard_json['dashboard']['id'] = None
        print(f"Dashboard: ID is NOT null..... Kindly make it null into Dashbaord template !!!")
    else:
        print(f"dashboard: ID is already NULL.. Please continue !!!")

    # Check if dashboard UID is the same as the title 
    # if dashboard_json['dashboard']['title'] != dashboard_json['dashboard']['title']:
     #   dashboard_json['dashboard']['uid'] = None  # Set to null if not the same as title
    #else:
        # Append a unique number to UID if it's the same as the title
       # dashboard_json['dashboard']['uid'] = append_unique_number(api_url, username, password, dashboard_json['dashboard']['title'])

        

def import_dashboard(api_url, username, password, json_file_path):
    # Read JSON template from the file
    with open(json_file_path, 'r') as file:
        dashboard_json = json.load(file)

    # Grafana API endpoint for importing dashboards
    endpoint = f"{api_url}/api/dashboards/db"

    # Prepare headers with basic authentication
    auth = HTTPBasicAuth(username, password)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    # Make a POST request to import the dashboard
    response = requests.post(endpoint, headers=headers, auth=auth, json=dashboard_json)

    # Check for successful import (HTTP status code 200 or 201)
    if response.status_code in (200, 201):
        print("Dashboard successfully imported!")
        print(response.json())
    else:
        print(f"Error importing dashboard. Status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    api_url = config.get('grafana', 'api_url')
    username = config.get('grafana', 'username')
    password = config.get('grafana', 'password')
    json_file = config.get('grafana', 'json_file')

    process_dashboard_json(json_file)
    import_dashboard(api_url, username, password, json_file)
