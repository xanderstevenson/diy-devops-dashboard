# a Python script that uses the GitHub API to fetch repository data:

import requests

# Set your GitHub username and access token
username = "xanderstevenson"
access_token = "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"

# Make a GET request to fetch repository data
response = requests.get(f"https://api.github.com/users/{username}/repos",
                        headers={"Authorization": f"Token {access_token}"})

if response.status_code == 200:
    repositories = response.json()

    # Fetch and sort repository activity
    for repo in repositories:
        activity_response = requests.get(f"https://api.github.com/repos/{username}/{repo['name']}/commits",
                                         headers={"Authorization": f"Token {access_token}"})
        if activity_response.status_code == 200:
            activity = activity_response.json()
            if len(activity) > 0:
                latest_commit = activity[0]['commit']
                repo['latest_commit_date'] = latest_commit['author']['date']
            else:
                repo['latest_commit_date'] = None
        else:
            print(f"Failed to fetch activity for repository '{repo['name']}'. Error: {activity_response.text}")
            repo['latest_commit_date'] = None

    sorted_repositories = sorted(repositories, key=lambda x: x['latest_commit_date'] or '', reverse=True)

    # Display sorted repository information
    for repo in sorted_repositories:
        print(f"Repository: {repo['name']}")
        print(f"Description: {repo['description']}")
        print(f"URL: {repo['html_url']}")
        print(f"Visibility: {'Public' if not repo['private'] else 'Private'}")
        if repo['language']:
            print(f"Primary Language: {repo['language']}")
        else:
            print("Primary Language: Not specified")
        if repo['latest_commit_date']:
            print(f"Latest Commit Date: {repo['latest_commit_date']}")
        else:
            print("Latest Commit Date: No commits")
        print("\n")
else:
    print(f"Failed to fetch repositories. Error: {response.text}")