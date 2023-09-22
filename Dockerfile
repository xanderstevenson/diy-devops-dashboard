
# Use the official Python base image with a specific version tag
FROM python:3.9-slim-buster

# Set environment variables to ensure Python outputs everything to the terminal
ENV PYTHONUNBUFFERED 1

# Create and set the working directory in the container
WORKDIR /app

# Copy only the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install the 'sudo' package to have access to administrative commands like 'usermod'
RUN apt-get update && apt-get install -y sudo

# Create the 'docker' group
RUN groupadd -r docker

# Create the 'myuser' user and add it to the 'docker' group
RUN useradd -m -s /bin/bash myuser
RUN usermod -aG docker myuser

# Copy the rest of the project files to the container
COPY . .

# Expose the port on which the web app will run (optional, but useful for documentation)
EXPOSE 8000

# Define the command to run the web app
CMD ["python", "app.py"]
