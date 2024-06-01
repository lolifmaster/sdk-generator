from dotenv import load_dotenv
import os
import requests

load_dotenv()
# TODO: Find how to get the usage of the API (this is not working)
if __name__ == "__main__":
    response = requests.get(
        "https://api.openai.com/v1/usage",
        headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"},
    )
    print(response.json())
