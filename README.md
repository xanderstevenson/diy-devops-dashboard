<h1 align="center">Do-It-Yourself (DIY) DevOps Dashboard<h1>

<p align="center"><img src="https://github.com/xanderstevenson/diy-devops-dashboard/assets/27918923/3fa23d01-5f42-42a2-98ff-50aba621be3f"></p>
<img src="https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg">

## Description

I made this project as a way for those new to DevOps to get started with the basic technologies invlolved. It requires setting up the basic accounts and then provides the user with an all-in-one place to see their progress and to better understand how these different tools interact in the DevOps lifecycle.

This project runs a Flask App inside a Docker container, which serves the web dashboard. It is written in Python and most of the data is collected via external API calls, with Docker and Jenkins data being collected straight from your machine.

Besides displaying all your DevOps data neatly organized in the dashboard, you can send the data to a Webex space via message by clicking the 'Post to Webex' button in the menu.

_This project runs as a Flask app. The original project, [diy-devops-dashboard-in-docker](https://github.com/xanderstevenson/diy-devops-dashboard-in-docker/tree/main), also runs as a Flask app, but in a Docker container. The Docker version would not pass the initial vulnerability scanning for acceptance into the [Cisco Code Exchange](https://developer.cisco.com/codeexchange), so I made this version, which the automated vulnerability scanning finds more agreeable._

<br>

## Prerequisites

GitHub, GitLab, Terraform, and Elastic-Cloud accounts must be created and the credentials placed in the .env file in order for the data from those platforms to display properly in the dashboard. Jenkins projects and Docker containers will also need to be present locally, for that data to be populated in the dashboard. 

- You will need [Python](https://www.python.org/downloads/) installed. This code has been successfully tested in Python 3.9.5
- Docker will need to be installed. I'm runnning [Docker Desktop](https://www.docker.com/products/docker-desktop/) on Mac. The Docker Engine must be running for the dashboard to load.

<br>

## Installation

1. Create a virtual environment locally and activate it.

<br>

2. Clone this repo and cd into it.

```git clone https://github.com/xanderstevenson/diy-devops-dashboard.git```

```cd diy-devops-dashboard```

<br>

3. Install the required dependencies

```pip install -r requirements.txt```

<br>

4. Make sure you have account set-up with [GitHub](https://github.com/), [GitLab](https://gitlab.com/), [Terraform](https://app.terraform.io/), and [Elastic Cloud](https://www.elastic.co/cloud/)

<br>

5. Create a file called .env in the same directory as app.py and place your credentials from those accounts into .env. The required credentials are listed in the [.env-example](https://github.com/xanderstevenson/diy-devops-dashboard/blob/main/.env-example) file. Do not place any credentials in .env-example!

`GITHUB_USERNAME="your_username"`<br>
`GITHUB_ACCESS_TOKEN="your_access_token"`<br>
`...`<br>
`...`

_*** The .env file is listed in the [.gitignore](https://github.com/xanderstevenson/diy-devops-dashboard/blob/main/.gitignore) file, so .env will not be pushed to GitHub if you decide to fork this project. ***_

<br>

## Usage

1. Run the Flask app from the project root directory

```python3 app.py``` or ```python app.py```   

<br>



2. Navigate to http://127.0.0.1:8000 or http://localhost:8000 to view the dashboard

<p align="center">
<img src="https://github.com/xanderstevenson/diy-devops-dashboard/assets/27918923/713de122-8a0b-4596-afa7-ae0092703cc3" width="700">
</p>

<br>


3. To stop the container, type Ctrl + C one or twice in the virtual directory in which you ran the docker commands.

<br>

### Functionality

- Text within each section that is surrounded by a box is clickable and will take you to the web page for that resource.

<p align="center">
<img src="https://github.com/xanderstevenson/diy-devops-dashboard/assets/27918923/7e46a9a4-14de-4239-8ef5-8dc06e2e029a" width="500">
</p>
<br>

- By clicking on the hamburger menu icon on the top left, you can view the button to 'Post to Webex'. Push this once and it will send the data for this dashboard, truncated to five results per tool, to the Webex space indicated in the .env file. This will take up to 15 seconds. To make the button disappear, click on the hamburger menu icon again.

<p align="center"><img src="https://github.com/xanderstevenson/diy-devops-dashboard/assets/27918923/2bf9c2b9-6a58-429d-bc14-6454b8f21ca4" width="400">
</p>

<br>

- The entire page will reload every 5 minutes, thanks to the JavaScript at the bottom of /templates/index.html. You can also refresh the page manually by clicking on the "Refresh" button under the marquee at the top of the page.

<p align="center">
<img width="400" src="https://github.com/xanderstevenson/diy-devops-dashboard/assets/27918923/afba8a5a-f0ab-4d79-84b2-b8ae58d8bf21">
</p>

Both actions reload the data to be presented.

<br>

- More blocks for additional tools can be added to [templates/index.html](https://github.com/xanderstevenson/diy-devops-dashboard/blob/main/templates/index.html) and additional functions would need to be added to [app.py](https://github.com/xanderstevenson/diy-devops-dashboard/blob/main/app.py)

<br>

## Video: 'DevOps Dashboards featuring DIY DevOps Dashboard'

- In this video we present an overview of DevOps Dashboards, including their definition and purpose, as well as their key components and functionality. Next, we discuss 5 popular DevOps Dashboard platforms, listing their main features, as well as their advantages and disadvantages. Then, we explore the key takeaways and considerations for choosing a suitable DevOps Dashboard. Finally, we explore the DIY DevOps Dashboard, a dashboard I’ve put together, which is an excellent starting point for those new to DevOps. It helps learners organize their DevOps tools in one place to observe their statuses and to better understand how they work together in a DevOps lifecycle.

<p align="center">
<a href="https://www.youtube.com/watch?v=fzBCqMisNcU" target="_blank">
  <img src="https://github.com/xanderstevenson/diy-devops-dashboard/blob/main/static/small-devops-dashboard-thumbnail.png" alt="DevOps Dashboards featuring DIY DevOps Dashboard" width="500"/>
</a>
<br><i>Click on the image to watch the video</i>
</p>
<br>

You can find out more about the DIY DevOps Dashboard on Cisco Code Exchange: http://cs.co/diy-devops-dashboard

Don’t forget to check out the DevOps Group Hub on the Cisco Community: https://cs.co/devops-community

<br> 

## Disclaimer

<br>

<p align="center">
  <em><strong style="color: blue;">This project is for demo purposes only and should not be used in a production environment.</strong></em>
</p>

