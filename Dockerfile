# Stage 1: Build the application and generate Kubernetes resources
FROM python:3.9-slim-buster as builder

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install the 'kubernetes' library
RUN pip install kubernetes

# Copy the rest of the project files to the container
COPY . .

# Create a directory for Kubernetes resources
RUN mkdir /k8s

COPY /k8s/config /k8s

# Stage 2: Create the final image
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install the 'kubernetes' library
RUN pip install kubernetes

# Copy the application code from the builder stage
COPY --from=builder /app /app

# Copy the generated Kubernetes resources from the builder stage
COPY --from=builder /k8s /k8s

# Expose the port on which the web app will run (optional, but useful for documentation)
EXPOSE 8000

# Define the command to run the web app
CMD ["python", "app.py"]
