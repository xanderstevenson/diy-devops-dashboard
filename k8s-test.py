python
import requests


def get_pods():
    # Define the Kubernetes API endpoint for pods
    api_url = "https://your-kubernetes-cluster/api/v1/pods"

    # Set the required headers for authentication and content type
    headers = {
        "Authorization": "Bearer your-auth-token",
        "Content-Type": "application/json",
    }

    try:
        # Send a GET request to the Kubernetes API to retrieve pod information
        response = requests.get(api_url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the response JSON
            data = response.json()

            # Extract relevant information from the response
            pods = []
            for pod in data.get("items", []):
                pod_name = pod.get("metadata", {}).get("name")
                pod_status = pod.get("status", {}).get("phase")
                pods.append({"name": pod_name, "status": pod_status})

            # Return the list of pods
            return pods
        else:
            # If the request was not successful, print the error message
            print(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        # If an error occurred during the request, print the exception
        print(f"Request Error: {e}")

    # Return an empty list if there was an error
    return []


# Example usage
pods = get_pods()
for pod in pods:
    print(f"Pod Name: {pod['name']}, Status: {pod['status']}")
