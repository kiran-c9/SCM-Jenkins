import os
import requests
import sys
from dotenv import load_dotenv

load_dotenv()

URL_of_Jenkins = os.getenv('url')
JOB_NAME = os.getenv('jobname')
USERNAME = os.getenv('username')
API_TOKEN = os.getenv('api')



def trigger_pipeline():
    url = f'{URL_of_Jenkins}/job/{JOB_NAME}/build'
    try:
        response = requests.post(url, auth=(USERNAME, API_TOKEN))
        if response.status_code == 201:
            print(f"Build triggered for job '{JOB_NAME}'.")
            return True  # Indicate success
        elif response.status_code == 403:
            print("Authentication failed. Please check your username and API token.")
        elif response.status_code == 404:
            print("Job or build not found.")
        else:
            print(f"Failed to trigger the pipeline. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return False  


def get_logs():
    last_build_url = f'{URL_of_Jenkins}/job/{JOB_NAME}/lastBuild/consoleText'
    try:
        response = requests.get(last_build_url, auth=(USERNAME, API_TOKEN))
        response.raise_for_status()  
        if response.status_code == 200:
            logs = response.text
            if logs:
                print(logs)
            else:
                print("No logs available.")
        elif response.status_code == 404:
            print("Job or build not found.")
        else:
            print(f"Failed to fetch logs. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise e  


def get_status():
    last_build_url = f'{URL_of_Jenkins}/job/{JOB_NAME}/lastBuild/api/json'
    try:
        response = requests.get(last_build_url, auth=(USERNAME, API_TOKEN))
        response.raise_for_status() 
        if response.status_code == 200:
            build_info = response.json()
            result = build_info.get('result')
            if result:
                print(f"Status: {result}")
                return result  
            else:
                print("No status available.")
        elif response.status_code == 404:
            print("Job or build not found.")
        else:
            print(f"Failed to fetch status. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise e  

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("Usage: python script.py [trigger|logs|status]")
        sys.exit(1)

    
    
    command = sys.argv[1]
    if command not in ['trigger', 'logs', 'status']:
        print("Invalid command.")
        sys.exit(1)
    if command == "trigger":
        trigger_pipeline()
    elif command == "logs":
        get_logs()
    elif command == "status":
        get_status()
    else:
        print("Invalid command.")
