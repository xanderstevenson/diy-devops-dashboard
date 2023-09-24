# from flask import Flask, render_template, request
# import requests
# import schedule
# import time
# import os
# from decouple import config

# app = Flask(__name__)

# import requests
# from decouple import config  # Import the config function from python-decouple

# def fetch_jenkins_data():
#     # Get Jenkins API token from environment variables
#     jenkins_api_token = config("JENKINS_TOKEN")

#     try:
#         # Use host.docker.internal to access Jenkins on the host machine
#         response = requests.get(
#             "http://host.docker.internal:8080/api/json",
#             auth=("alexstev", jenkins_api_token),  # Replace "username" with your Jenkins username
#         )
#         if response.status_code == 200:
#             jenkins_data = response.json()
#             return jenkins_data
#         else:
#             print(f"Failed to fetch Jenkins data. Status code: {response.status_code}")
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to connect to Jenkins: {e}")

#     # Return an empty dictionary if there was an error
#     return {}


# # Function to fetch GitHub data
# def fetch_github_data():
#     # Get GitHub username and access token from environment variables
#     username = config("GITHUB_USERNAME")
#     access_token = config("GITHUB_ACCESS_TOKEN")

#     # Check if the variables are set
#     if username is None or access_token is None:
#         raise ValueError("GitHub username or access token not set in environment variables")

#     # Fetch GitHub repositories
#     response = requests.get(f"https://api.github.com/users/{username}/repos",
#                             headers={"Authorization": f"Token {access_token}"})

#     if response.status_code == 200:
#         repositories = response.json()

#         # Fetch and sort repository activity
#         for repo in repositories:
#             activity_response = requests.get(f"https://api.github.com/repos/{username}/{repo['name']}/commits",
#                                              headers={"Authorization": f"Token {access_token}"})
#             if activity_response.status_code == 200:
#                 activity = activity_response.json()
#                 if len(activity) > 0:
#                     latest_commit = activity[0]['commit']
#                     repo['latest_commit_date'] = latest_commit['author']['date']
#                 else:
#                     repo['latest_commit_date'] = None
#             else:
#                 print(f"Failed to fetch activity for repository '{repo['name']}'. Error: {activity_response.text}")
#                 repo['latest_commit_date'] = None

#         sorted_repositories = sorted(repositories, key=lambda x: x['latest_commit_date'] or '', reverse=True)

#         # Fetch Jenkins data
#         jenkins_data = fetch_jenkins_data()

#         return render_template('index.html', repositories=sorted_repositories, jenkins_data=jenkins_data)
#     else:
#         error_message = f"Failed to fetch repositories. Error: {response.text}"
#         return render_template('error.html', error_message=error_message)

# @app.route('/')
# def index():
#     return fetch_github_data()

# if __name__ == '__main__':
#     schedule.every(5).minutes.do(fetch_github_data)

#     import threading
#     flask_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 8000, 'debug': False})
#     flask_thread.start()

#     while True:
#         schedule.run_pending()
#         time.sleep(1)


from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/credentials.html")
def credentials():
    return render_template("credentials.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
