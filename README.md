# diy-devops-dashboard
## Do-It-Yourself (DIY) DevOps Dashboard

1. Clone this repo
```git clone https://github.com/xanderstevenson/diy-devops-dashboard.git```

<br>

2. Go to GitHub -> Click your profile image in the upper-right -> Settings -> Developer Settings -> Personal access tokens and create a new token with the scope of repo, at least.

<br>

3. Place your token credentials in the .env-example file and rename it to .env

`GITHUB_USERNAME="your_username"`<br>
`GITHUB_ACCESS_TOKEN="your_access_token"`<br>
`...`<br>
`...`

<br>

4. Build the Docker image by running the following command in the project directory:

```docker build -t diy-devops-dashboard .```
<br>

5. Run the Docker container by executing the following. command:

```docker run --name diy-devops-dashboard -v /var/run/docker.sock:/var/run/docker.sock -p 8000:8000 diy-devops-dashboard```

This command starts the container and forwards the container's port 8000 to the host's port 8000, allowing you to access the web app at http://localhost:8000.
