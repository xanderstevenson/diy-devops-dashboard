import docker
import json
import requests
import schedule
import time
from decouple import config
from datetime import datetime
from flask import Flask, render_template, current_app

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


def fetch_terraform_data():
    TOKEN = config("TERRAFORM_TOKEN")
    # Define the URL for TFC organizations
    url = "https://app.terraform.io/api/v2/organizations/"
    headers = {
        "Authorization": "Bearer " + TOKEN,
        "Content-Type": "application/vnd.api+json",
    }

    try:
        # Send a GET request to fetch TFC organizations
        TFCListresponse = requests.get(url, headers=headers)
        if TFCListresponse.status_code == 200:
            print("Got a successful response...")
            my_orgs = json.loads(TFCListresponse.content.decode("utf-8"))
            terraform_data = my_orgs["data"]
            return terraform_data
        else:
            print("Failed to get the required response...")
            print(TFCListresponse.content)
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

    # Return None if there was an error
    return None


@app.route("/")
def index():
    github_data = fetch_github_data()
    docker_data = fetch_docker_data()
    gitlab_data = fetch_gitlab_data()
    jenkins_data = fetch_jenkins_data()
    terraform_data = fetch_terraform_data()
    return render_template(
        "index.html",
        repositories=github_data,
        docker_data=docker_data,
        gitlab_data=gitlab_data,
        jenkins_data=jenkins_data,
        terraform_data=terraform_data,
    )


@app.route("/credentials.html")
def credentials():
    # Read environment variables from .env file
    github_username = config("GITHUB_USERNAME")
    github_access_token = config("GITHUB_ACCESS_TOKEN")
    jenkins_token = config("JENKINS_TOKEN")
    gitlab_token = config("GITLAB_TOKEN")
    gitlab_username = config("GITLAB_USERNAME")
    gitlab_group_id = config("GITLAB_GROUP_ID")

    return render_template(
        "credentials.html",
        github_username=github_username,
        github_access_token=github_access_token,
        jenkins_token=jenkins_token,
        gitlab_token=gitlab_token,
        gitlab_username=gitlab_username,
        gitlab_group_id=gitlab_group_id,
    )


if __name__ == "__main__":
    schedule.every(5).minutes.do(fetch_github_data)
    schedule.every(5).minutes.do(fetch_docker_data)
    schedule.every(5).minutes.do(fetch_gitlab_data)
    schedule.every(5).minutes.do(fetch_jenkins_data)

    import threading

    flask_thread = threading.Thread(
        target=app.run, kwargs={"host": "0.0.0.0", "port": 8000, "debug": False}
    )
    flask_thread.start()

    while True:
        schedule.run_pending()
        time.sleep(1)
