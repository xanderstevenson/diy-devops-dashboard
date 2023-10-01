from kubernetes import client, config


def generate_k8s_resources():
    try:
        # Load Kubernetes configuration from the default kubeconfig file
        config.load_kube_config("../k8s/config")

        # Create an instance of the Kubernetes API client
        api_instance = client.AppsV1Api()

        # Define the Deployment manifest
        deployment_manifest = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": "my-deployment",
                "labels": {"app": "my-app"},
            },
            "spec": {
                "replicas": 3,  # Number of replicas
                "selector": {
                    "matchLabels": {"app": "my-app"},
                },
                "template": {
                    "metadata": {"labels": {"app": "my-app"}},
                    "spec": {
                        "containers": [
                            {
                                "name": "my-container",
                                "image": "your-image:latest",
                                # Add more container settings as needed
                            }
                        ]
                    },
                },
            },
        }

        # Create the Deployment
        api_instance.create_namespaced_deployment(
            namespace="default", body=deployment_manifest
        )

        # Define the Service manifest
        service_manifest = {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": "my-service",
            },
            "spec": {
                "selector": {"app": "my-app"},
                "ports": [
                    {
                        "protocol": "TCP",
                        "port": 80,
                        "targetPort": 8080,  # Port exposed by the container
                    }
                ],
                "type": "LoadBalancer",
            },
        }

        # Create the Service
        api_instance.create_namespaced_service(
            namespace="default", body=service_manifest
        )

        print("Kubernetes resources created successfully!")

    except Exception as e:
        print(f"Failed to create Kubernetes resources: {e}")


if __name__ == "__main__":
    generate_k8s_resources()
