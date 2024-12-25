import boto3

def fetch_aws_metrics(region, access_key, secret_key):
    try:
        cloudwatch_client = boto3.client(
            "cloudwatch",
            region_name=region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        # Example AWS metric fetch (update with real queries if needed)
        response = cloudwatch_client.list_metrics()
        return response
    except Exception as e:
        return {"error": str(e)}
