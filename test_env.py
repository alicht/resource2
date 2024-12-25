from dotenv import load_dotenv
import os

# Reload the .env file
load_dotenv()

# Debug output
print(f"Current directory: {os.getcwd()}")
print(f"Environment variables: {os.environ}")
project_id = os.getenv("GCP_PROJECT_ID")
print(f"GCP_PROJECT_ID: {project_id}")
