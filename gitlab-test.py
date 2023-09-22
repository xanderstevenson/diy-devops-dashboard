import gitlab
from decouple import config
import requests

# GitLab API URL and your private token
gitlab_url = 'https://gitlab.com'  # Replace with your GitLab instance URL
private_token = config("GITLAB_TOKEN")
gitlab_username = config("GITLAB_USERNAME")  # Replace with the username of the user you want to filter by
group = "devops"  # Replace with the name of the group containing the project
group_id = config("GITLAB_GROUP_ID")  # Replace with your group ID

url = f"https://gitlab.com/api/v4/groups/{group_id}/projects"
headers = {"PRIVATE-TOKEN": private_token}

try:
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        projects = response.json()
        for project in projects:
            print("Project Name:", project["name"])
            print("Project URL:", project["web_url"])
    else:
        print(f"Failed to fetch projects. Status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Failed to connect to GitLab: {e}")