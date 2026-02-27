from pymongo import MongoClient
from pymongo.errors import OperationFailure
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = MongoClient(MONGO_URI)
db = client["slot_machine_db"]

stats_collection = db["game_stats"]
users_collection = db["users"]

# Create unique index on username
try:
    users_collection.create_index("username", unique=True)
except OperationFailure:
    # Index already exists
    pass