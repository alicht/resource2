import os
import openai
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Verify the API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("API Key not loaded from .env")
else:
    print(f"Loaded API Key: {api_key}")

# Set OpenAI API key
openai.api_key = api_key

# Test the OpenAI API
try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the capital of France?"}
        ]
    )
    print("API Response:", response["choices"][0]["message"]["content"])
except openai.error.AuthenticationError as auth_error:
    print(f"Authentication Error: {auth_error}")
except Exception as e:
    print(f"Error: {e}")
