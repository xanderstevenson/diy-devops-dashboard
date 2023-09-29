import subprocess
import json


def get_resources():
    try:
        # Run the Terraform command to output the resource state in JSON format
        cmd = ["terraform", "state", "pull"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Check if the command was successful
        if result.returncode == 0:
            # Check if the JSON output is empty
            if not result.stdout.strip():
                print("No resources found in Terraform state.")
                return []

            # Parse the JSON output
            output = json.loads(result.stdout)

            # Extract relevant information from the output
            resources = output.get("resources", [])
            resource_list = []
            for resource in resources:
                resource_type = resource.get("type")
                resource_name = resource.get("name")
                resource_list.append({"type": resource_type, "name": resource_name})

            # Return the list of resources
            return resource_list
        else:
            # If the command was not successful, print the error message
            print(f"Error: {result.stderr}")

    except subprocess.CalledProcessError as e:
        # If an error occurred during the command execution, print the exception
        print(f"Command Error: {e}")

    # Return an empty list if there was an error
    return []


# Example usage
resources = get_resources()
for resource in resources:
    print(f"Resource Type: {resource['type']}, Name: {resource['name']}")
