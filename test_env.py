# test_env.py
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Print environment variables
print("AWS_ACCESS_KEY_ID:", os.getenv("AWS_ACCESS_KEY_ID"))
print("AWS_SECRET_ACCESS_KEY:", os.getenv("AWS_SECRET_ACCESS_KEY"))
print("AWS_REGION:", os.getenv("AWS_REGION"))
