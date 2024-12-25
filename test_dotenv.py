from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Test by retrieving a variable from the .env file
test_variable = os.getenv("TEST_VARIABLE")

if test_variable:
    print(f"Test Variable: {test_variable}")
else:
    print("TEST_VARIABLE is not set or .env file is missing.")
