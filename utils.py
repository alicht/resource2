import os
from dotenv import load_dotenv

def load_environment_variables(env_file_path=".env"):
    """
    Load environment variables from the specified .env file.
    :param env_file_path: Path to the .env file.
    """
    if os.path.exists(env_file_path):
        load_dotenv(env_file_path)
    else:
        raise FileNotFoundError(f"{env_file_path} file not found.")
