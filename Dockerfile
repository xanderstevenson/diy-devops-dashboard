# Use the official Python base image with a specific version tag
FROM python:3.9-slim-buster

# Set environment variables to ensure Python outputs everything to the terminal
ENV PYTHONUNBUFFERED 1

# Create and set the working directory in the container
WORKDIR /app

# Copy only the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files to the container
COPY . .

# Expose the port on which the web app will run (optional, but useful for documentation)
EXPOSE 8000

# Define the command to run the web app
CMD ["python", "app.py"]
