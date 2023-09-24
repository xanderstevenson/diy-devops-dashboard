python
import requests


def search_documents(index, query):
    # Define the Elasticsearch API endpoint
    api_url = f"http://your-elasticsearch-host/{index}/_search"

    # Set the required headers for authentication and content type
    headers = {"Content-Type": "application/json"}

    # Define the search query
    payload = {"query": {"match": {"content": query}}}

    try:
        # Send a POST request to the Elasticsearch API to search for documents
        response = requests.post(api_url, headers=headers, json=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the response JSON
            data = response.json()

            # Extract relevant information from the response
            hits = data.get("hits", {}).get("hits", [])
            documents = []
            for hit in hits:
                doc_id = hit.get("_id")
                doc_source = hit.get("_source", {})
                documents.append({"id": doc_id, "source": doc_source})

            # Return the list of documents
            return documents
        else:
            # If the request was not successful, print the error message
            print(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        # If an error occurred during the request, print the exception
        print(f"Request Error: {e}")

    # Return an empty list if there was an error
    return []
