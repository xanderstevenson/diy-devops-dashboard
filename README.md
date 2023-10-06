<h1 align="center">Do-It-Yourself (DIY) DevOps Dashboard<h1>

<p align="center"><img src="https://github.com/xanderstevenson/diy-devops-dashboard/assets/27918923/3fa23d01-5f42-42a2-98ff-50aba621be3f"></p>

## Description

I made this project as a way for those new to DevOps to get started with the basic technologies invlolved. It requires setting up the basic technologies and then provides the user with an all-in-one place to see their progress and to better understand how these different tools interact in the DevOps lifecycle. 

<br>

<p align="center">
  <em><strong style="color: blue;">*** This project is for demo purposes only and should not be used in a production environment. ***</strong></em>
</p>

<br>

## Prerequisites

GitHub, GitLab, Terraform, and Elastic-Cloud accounts must be created and the credentials placed in the .env file in order for the data from those platforms to display properly in the dashboard. Jenkins projects and Docker containers will also need to be present locally, for that data to be populated in the dashboard. THe Docker Engine must be running for the Docker commands below to be successful.

<br>

## Installation

1. Create a virtual environment locally and activate it.

<br>

2. Clone this repo and cd into it.

```git clone https://github.com/xanderstevenson/diy-devops-dashboard.git```

```cd diy-devops-dashboard```

<br>

3. Make sure you have account set-up with [GitHub](https://github.com/), [GitLab](https://gitlab.com/), [Terraform](https://app.terraform.io/), and [Elastic Cloud](https://www.elastic.co/cloud/)

<br>

4. Place your credentials from those accounts in the .env-example file and rename it to .env

`GITHUB_USERNAME="your_username"`<br>
`GITHUB_ACCESS_TOKEN="your_access_token"`<br>
`...`<br>
`...`

<br>

## Usage

1. Build the Docker image by running the following command in the project directory (make sure Docker Engine is running):

```docker build -t diy-devops-dashboard .```

<br>


2. Run the Docker container by executing the following. command:

```docker run --name diy-devops-dashboard -v /var/run/docker.sock:/var/run/docker.sock -p 8000:8000 diy-devops-dashboard```

This command starts the container and forwards the container's port 8000 to the host's port 8000, allowing you to access the web app at http://localhost:8000.

<br>

3. Navigate to http://127.0.0.1:8000 or http://localhost:8000 to view the dashboard

<p align="center">
<img src="https://github.com/xanderstevenson/diy-devops-dashboard/assets/27918923/713de122-8a0b-4596-afa7-ae0092703cc3" width="700">
</p>

<br>

4. To stop the container, type Ctrl + C one or twice in the virtual directory in which you ran the docker commands.

<br>

## Functionality

Text within each section that is surrounded by box is clickable and will take you to the web page for that resource.

<p align="center">
<img src="https://github.com/xanderstevenson/diy-devops-dashboard/assets/27918923/7e46a9a4-14de-4239-8ef5-8dc06e2e029a" width="500">
</p>

More blocks for additional tools can be added to [templates/index.html](https://github.com/xanderstevenson/diy-devops-dashboard/blob/main/templates/index.html) and a additional functions would need to be added to [app.py](https://github.com/xanderstevenson/diy-devops-dashboard/blob/main/app.py)
