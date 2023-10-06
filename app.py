# Standard library imports
from datetime import datetime
import json
import time

# Related third-party imports
from decouple import config
from flask import Flask, render_template
import docker
import requests
import schedule

app = Flask(__name__)  # Create the Flask app instance

# Function to fetch GitHub data
def fetch_github_data():
    # Get GitHub username and access token from environment variables
    username = config("GITHUB_USERNAME")
    access_token = config("GITHUB_ACCESS_TOKEN")

    # Check if the variables are set
    if username is None or access_token is None:
        raise ValueError(
            "GitHub username or access token not set in environment variables"
        )

    # Fetch GitHub repositories
    response = requests.get(
        f"https://api.github.com/users/{username}/repos",
        headers={"Authorization": f"Token {access_token}"},
    )

    if response.status_code == 200:
        repositories = response.json()

        # Fetch and sort repository activity
        for repo in repositories:
            activity_response = requests.get(
                f"https://api.github.com/repos/{username}/{repo['name']}/commits",
                headers={"Authorization": f"Token {access_token}"},
            )
            if activity_response.status_code == 200:
                activity = activity_response.json()
                if len(activity) > 0:
                    latest_commit = activity[0]["commit"]
                    commit_date_iso = latest_commit["author"]["date"]
                    commit_date = datetime.strptime(
                        commit_date_iso, "%Y-%m-%dT%H:%M:%SZ"
                    )
                    repo["latest_commit_date"] = commit_date.strftime(
                        "%m-%d-%Y %H:%M:%S"
                    )
                else:
                    repo["latest_commit_date"] = None
            else:
                print(
                    f"Failed to fetch activity for repository '{repo['name']}'. Error: {activity_response.text}"
                )
                repo["latest_commit_date"] = None

            # Generate the URL for the repository
            repo["url"] = f"https://github.com/{username}/{repo['name']}"
        # Sort repositories in descending order by latest_commit_date (most recent first)
        sorted_repositories = sorted(
            repositories,
            key=lambda x: datetime.strptime(
                x["latest_commit_date"], "%m-%d-%Y %H:%M:%S"
            )
            if "latest_commit_date" in x and x["latest_commit_date"]
            else datetime.min,
            reverse=True,
        )

        return sorted_repositories
    else:
        error_message = f"Failed to fetch repositories. Error: {response.text}"
        return []


# Function to fetch Docker data
def fetch_docker_data():
    try:
        # Initialize the Docker client
        client = docker.from_env()

        # Fetch container information
        containers = client.containers.list(all=True)

        # Extract relevant container data
        docker_data = []

        for container in containers:
            # Print all attributes of the container
            # for key, value in container.attrs.items():
            #     print(f"{key}: {value}")
            # print(container.short_id)
            data = {
                "container_id": container.short_id,
                "name": container.name,
                "status": container.status,
            }

            docker_data.append(data)

        return docker_data
    except docker.errors.APIError as e:
        print(f"Failed to fetch Docker data: {e}")
        return []


# Function to fetch GitLab data
def fetch_gitlab_data():
    # Get GitLab private token, username, and group ID from environment variables
    private_token = config("GITLAB_TOKEN")
    gitlab_username = config("GITLAB_USERNAME")
    group_id = config("GITLAB_GROUP_ID")

    # GitLab API URL for projects within the specified group
    url = f"https://gitlab.com/api/v4/groups/{group_id}/projects"
    headers = {"PRIVATE-TOKEN": private_token}

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            projects = response.json()

            # Parse and format the last_activity_at date for each project
            for project in projects:
                last_activity_at = project.get("last_activity_at")
                if last_activity_at:
                    last_activity_date = datetime.strptime(
                        last_activity_at, "%Y-%m-%dT%H:%M:%S.%fZ"
                    )
                    project["last_activity_at_mdy"] = last_activity_date.strftime(
                        "%m-%d-%Y"
                    )
                    project["last_activity_at_hms"] = last_activity_date.strftime(
                        "%H:%M:%S"
                    )

            return projects
        else:
            print(
                f"Failed to fetch GitLab projects. Status code: {response.status_code}"
            )
            return []
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to GitLab: {e}")
        return []


# Function to fetch Jenkins data
def fetch_jenkins_data():
    # Get Jenkins API token from environment variables
    jenkins_api_token = config("JENKINS_TOKEN")

    try:
        # Use host.docker.internal to access Jenkins on the host machine
        response = requests.get(
            "http://host.docker.internal:8080/api/json",
            auth=(
                "alexstev",
                jenkins_api_token,
            ),
        )
        if response.status_code == 200:
            jenkins_data = response.json()
            return jenkins_data
        else:
            print(f"Failed to fetch Jenkins data. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to Jenkins: {e}")

    # Return an empty dictionary if there was an error
    return {}


# Function to fetch Terraform data
def fetch_terraform_data():
    TOKEN = config("TERRAFORM_TOKEN")
    # Define the URL for TFC organizations
    org_url = "https://app.terraform.io/api/v2/organizations/"
    headers = {
        "Authorization": "Bearer " + TOKEN,
        "Content-Type": "application/vnd.api+json",
    }
    try:
        # Send a GET request to fetch TFC organizations
        org_response = requests.get(org_url, headers=headers)
        if org_response.status_code == 200:
            orgs_data = json.loads(org_response.content.decode("utf-8"))

            terraform_data = []

            # Iterate over organizations to fetch workspaces
            for org in orgs_data["data"]:
                org_id = org["id"]
                workspace_url = (
                    f"https://app.terraform.io/api/v2/organizations/{org_id}/workspaces"
                )
                workspace_response = requests.get(workspace_url, headers=headers)

                if workspace_response.status_code == 200:
                    workspaces_data = json.loads(
                        workspace_response.content.decode("utf-8")
                    )
                    org["workspaces"] = workspaces_data["data"]
                else:
                    print(f"Failed to fetch workspaces for organization {org_id}...")
                    org["workspaces"] = []
            return orgs_data["data"]
        else:
            print("Failed to get the required response for organizations...")
            print(org_response.content)
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

    # Return None if there was an error
    return None


# Function to fetch Elastic Cloud deployment data
def fetch_elastic_data():
    # Get the Elastic API key from environment variables
    elastic_api_key = config("ELASTIC_API_KEY")

    # Check if the API key is set
    if elastic_api_key is None:
        raise ValueError("Elastic API key not set in environment variables")

    # Define the API endpoint URL
    elastic_api_url = "https://api.elastic-cloud.com/api/v1/deployments"

    # Define headers with the API key
    headers = {
        "Authorization": f"ApiKey {elastic_api_key}",
    }

    try:
        # Send a GET request to fetch Elastic Cloud deployments
        response = requests.get(elastic_api_url, headers=headers)

        if response.status_code == 200:
            elastic_data = response.json()
            return elastic_data
        else:
            print(
                f"Failed to fetch Elastic Cloud deployments. Status code: {response.status_code}"
            )
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to Elastic Cloud API: {e}")
        return {}


@app.route("/")
def index():
    github_data = fetch_github_data()
    docker_data = fetch_docker_data()
    gitlab_data = fetch_gitlab_data()
    jenkins_data = fetch_jenkins_data()
    terraform_data = fetch_terraform_data()
    elastic_data = fetch_elastic_data()
    return render_template(
        "index.html",
        repositories=github_data,
        docker_data=docker_data,
        gitlab_data=gitlab_data,
        jenkins_data=jenkins_data,
        terraform_data=terraform_data,
        elastic_data=elastic_data,
    )


if __name__ == "__main__":
    schedule.every(5).minutes.do(fetch_github_data)
    schedule.every(5).minutes.do(fetch_docker_data)
    schedule.every(5).minutes.do(fetch_gitlab_data)
    schedule.every(5).minutes.do(fetch_jenkins_data)
    schedule.every(5).minutes.do(fetch_terraform_data)
    schedule.every(5).minutes.do(fetch_elastic_data)

    import threading

    flask_thread = threading.Thread(
        target=app.run, kwargs={"host": "0.0.0.0", "port": 8000, "debug": False}
    )
    flask_thread.start()

    while True:
        schedule.run_pending()
        time.sleep(1)
