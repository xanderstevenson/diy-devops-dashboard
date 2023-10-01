from kubernetes import config as kubernetes_config
from kubernetes import client


def list_resources_in_all_namespaces_with_pods():
    try:
        # Load Kubernetes configuration from the specified kubeconfig file
        kubeconfig_path = "/Users/xander/.kube/config"
        kubernetes_config.load_kube_config(config_file=kubeconfig_path)

        # Create an instance of the Kubernetes API client
        api_instance = client.CoreV1Api()

        # List all namespaces
        namespaces = api_instance.list_namespace()

        for namespace in namespaces.items:
            # List resources in the current namespace
            resources = api_instance.list_namespaced_pod(namespace.metadata.name)

            # Only display namespaces with pods
            if resources.items:
                print(f"Namespace: {namespace.metadata.name}")
                print("Resources:")

                for resource in resources.items:
                    print(f"  Pod: {resource.metadata.name}")

                print("\n")

    except Exception as e:
        print(f"Failed to fetch Kubernetes data: {e}")


list_resources_in_all_namespaces_with_pods()
