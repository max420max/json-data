####################################################################################
#  Grafana HTTP API : Downlaod Dashbaord : /api/dashboards/uid/{dashboard_uid}
#  
####################################################################################

import requests
import json
from requests.auth import HTTPBasicAuth
import configparser

def get_dashboard_details(api_url, username, password, dashboard_uid , output_file):
    
    print(f"CALLING :get_dashboard_details method..........")
    # Grafana API endpoint for getting dashboard details by UID
    endpoint = f"{api_url}/api/dashboards/uid/{dashboard_uid}"

    # Prepare headers with basic authentication
    auth = HTTPBasicAuth(username, password)

    # Make a GET request to retrieve dashboard details
    response = requests.get(endpoint, auth=auth)
    # Check for successful request (HTTP status code 200)
    if response.status_code == 200:
        # Store the JSON response in a file
        with open(output_file, 'w') as file:
            file.write(response.text)

        # Parse the JSON response
        dashboard_data = response.json()
        dashboard_data['dashboard']['version'] += 1
        dashboard_data['dashboard']['id'] = None

        # Print updated dashboard UID and version
        print(f"Dashboard UID: {dashboard_data['dashboard']['uid']}")
        print(f"Dashboard Title: {dashboard_data['dashboard']['title']}")
        print(f"Updated Dashboard ID: {dashboard_data['dashboard']['id']}")
        print(f"Updated Dashboard Version: {dashboard_data['dashboard']['version']}")

        # Update the JSON template with the new version and id = null
        with open(output_file, 'w') as file:
            json.dump(dashboard_data, file, indent=2)

            return exit

    else:
        print(f"Error getting dashboard details. Status code: {response.status_code}")
        print(response.text)


def read_dashboard_details_from_file(file_path):
    # Read JSON from the stored file
    print(f"CALLING :read_dashboard_details_from_file method..........")
    with open(file_path, 'r') as file:
        dashboard_data = json.load(file)

    return dashboard_data

if __name__ == "__main__":
    # Read configuration from the 'config.ini' file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Get Grafana API details from the config file
    api_url = config.get('grafana', 'api_url')
    username = config.get('grafana', 'username')
    password = config.get('grafana', 'password')
    output_file = config.get('grafana', 'json_file')

    read_dashboard_details_from_file(output_file)
    dashboard_data_from_file = read_dashboard_details_from_file(output_file)
    
    dashboard_uid = dashboard_data_from_file['dashboard']['uid']
    dashboard_version = dashboard_data_from_file['dashboard']['version']
    #dashboard_title = dashboard_data_from_file['dashboard']['title']
    dashboard_id = dashboard_data_from_file['dashboard']['id']
    
    print(f"xxx Dashboard dashboard_version: {dashboard_version}")
    print(f"xxx Dashboard dashboard_uid: {dashboard_uid}")
    print(f"xxx Dashboard dashboard_id: {dashboard_id}")

    get_dashboard_details(api_url, username, password , dashboard_uid , output_file)
