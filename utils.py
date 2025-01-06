import os
from dotenv import load_dotenv

def load_environment_variables():
    """
    Load environment variables from a .env file.
    Raises an error if required variables are missing.
    """
    load_dotenv()  # Load variables from .env file if present

    required_env_vars = [
        "OPENAI_API_KEY",
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_REGION"
    ]
    for var in required_env_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Required environment variable {var} is missing. Please check your .env file.")
