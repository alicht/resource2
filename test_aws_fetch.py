import boto3

session = boto3.Session(region_name="us-east-1")
cloudwatch = session.client("cloudwatch")

try:
    metrics = cloudwatch.list_metrics(Namespace="AWS/EC2")
    print("Successfully fetched metrics:", metrics)
except Exception as e:
    print("Error fetching metrics:", e)
