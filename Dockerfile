# Stage 1: Build the application and generate Kubernetes resources
FROM python:3.9-slim-buster as builder

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy the rest of the project files to the container
COPY . .

# Stage 2: Create the final image
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy the application code from the builder stage
COPY --from=builder /app /app

# Expose the port on which the web app will run (optional, but useful for documentation)
EXPOSE 8000

# Define the command to run the web app
CMD ["python", "app.py"]
