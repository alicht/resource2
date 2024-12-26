import boto3

def fetch_aws_metrics(region, access_key, secret_key):
    import boto3

    try:
        cloudwatch = boto3.client(
            "cloudwatch",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

        # Fetch metrics (example for EC2 CPU utilization)
        metrics = cloudwatch.list_metrics(
            Namespace="AWS/EC2", MetricName="CPUUtilization"
        )
        filtered_metrics = []

        for metric in metrics.get("Metrics", []):
            metric_data = {
                "Namespace": metric.get("Namespace"),
                "MetricName": metric.get("MetricName"),
                "Dimensions": [
                    f"{dim['Name']}={dim['Value']}" for dim in metric.get("Dimensions", [])
                ],
            }
            filtered_metrics.append(metric_data)

        return filtered_metrics
    except Exception as e:
        return {"error": str(e)}
