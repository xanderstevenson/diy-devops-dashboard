# diy-devops-dashboard
## Do-It-Yourself (DIY) DevOps Dashboard

### Description

I made this project as a way for those new to DevOps to get started with the basic technologies invlolved. 


### Prerequisites

GitHub, GitLab, Terraform, and Elastic-Cloud accounts must be created and the credentials placed in the .env file in order for the data from those platforms to display properly in the dashboard. Jenkins projects and Docker containers will also need to be present locally, for that data to be populated in the dashboard. THe Docker Engine must be running for the Docker commands below to be successful.


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
