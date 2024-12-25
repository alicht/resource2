import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Load environment variables
load_dotenv()

try:
    # Ensure region is specified
    region = os.getenv("AWS_REGION")
    if not region:
        raise ValueError("AWS region is not set. Check your .env file.")

    # Initialize boto3 client
    client = boto3.client("ec2", region_name=region)

    # Test by listing regions
    regions = client.describe_regions()["Regions"]
    print("Available Regions:")
    for region in regions:
        print(region["RegionName"])
    print("AWS Credentials and Region Verified Successfully!")
except (NoCredentialsError, PartialCredentialsError) as e:
    print(f"Error verifying AWS credentials: {e}")
except ValueError as ve:
    print(f"Configuration Error: {ve}")
except Exception as e:
    print(f"Unexpected Error: {e}")
