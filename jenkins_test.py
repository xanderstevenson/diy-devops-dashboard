import requests

jenkins_url = "http://127.0.0.1:8080/api/json"  # Replace with your Jenkins URL
api_token = "1128e674179726edd13fa71fd64e291527"  # Replace with your Jenkins API token
username = "alexstev"

try:
    response = requests.get(
        jenkins_url,
        auth=(username, api_token),
    )
    if response.status_code == 200:
        jenkins_data = response.json()
        print("Jenkins Data:")
        print(jenkins_data)
    else:
        print(f"Failed to fetch Jenkins data. Status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Failed to connect to Jenkins: {e}")