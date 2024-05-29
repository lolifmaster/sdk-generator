from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGODB_URI")

if uri is None:
    raise Exception("MONGODB_URI not found in .env file.")

client = MongoClient(uri)

try:
    client.admin.command("ping")
    db = client["sdk-gen"]["train_data"]
    print("Database connected successfully. (MongoDB)")
except Exception as e:
    print(e)
