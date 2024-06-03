import os
import requests
import sys
from jenkins import JenkinsException
from dotenv import load_dotenv

load_dotenv()

URL_of_Jenkins = os.getenv('url')
JOB_NAME = os.getenv('jobname')
USERNAME = os.getenv('username')
API_TOKEN = os.getenv('api')



def trigger_pipeline(JOB_NAME):
    url = f'{URL_of_Jenkins}/job/{JOB_NAME}/build'
    try:
       response = requests.post(url, auth=(USERNAME, API_TOKEN))
       if response.status_code == 201:
          print(f"Build triggered for job '{JOB_NAME}'.")
       elif response.status_code == 403:
          print(f"Authetication failed. Please check your username and API token.")
       elif response.status_code == 404:
          print(f"Authetication failed. Please check your username and API token.")
       else:
          print(f"Failed to trigger the pipeline.Status code:{response.status_code}")
    except requests.exceptions.RequestException as e:
       print(f"A error occurred: {e}")

       
       
       
       
def get_logs(JOB_NAME, build_number):
   # Fetches and prints logs of the last build
   last_build_url = f'{URL_of_Jenkins}/job/{JOB_NAME}/{build_number}/consoleText'
   try:
      response = requests.get(last_build_url, auth=(USERNAME, API_TOKEN))
      if response.status_code == 200:
         logs = response.text
         if logs:
            print(logs)
         else:
            print("No logs availabe.")
      elif response.status_code == 404:
          print(f"Job or build not found.")
      else:
          print(f"Failed to fetch logs.Status code:{response.status_code}")
   except requests.exceptions.RequestException as e:
       print(f"A error occurred: {e}")



def get_status():
    last_build_url = f'{URL_of_Jenkins}/job/{JOB_NAME}/lastBuild/api/json'
    try:
       response = requests.get(last_build_url, auth=(USERNAME, API_TOKEN))
       if response.status_code == 200:
          build_info = response.json()
          result = build_info['result']
          if result:
             print(f"Status:{result}")
          else:
             print("No status available.")
       elif response.status_code == 404:
          print(f"Job or build not found.")
       else:
          print(f"Failed to fetch status.Status code:{response.status_code}")
    except requests.exceptions.RequestException as e:
       print(f"A error occurred: {e}")
   



if __name__ == "__main__":
   if len(sys.argv)<2:
      print("use-python pythonscript.py [trigger|logs|status]")
      sys.exit(1)
      	
      
   command = sys.argv[1]
   if command == "trigger":
      trigger_pipeline()
   elif command == "logs":
      get_logs()
   elif command == "status":
      get_status()
   else:
      print("Invalid")
      



































