import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB URI from .env
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Create MongoDB client and connect to the database
client = MongoClient(MONGO_URI)
db = client.maxxmaicard

# Get collections
user_profiles_collection = db.user_profiles
statements_collection = db.statements

def insert_user_profile(profile_data):
    user_profiles_collection.insert_one(profile_data)

def get_user_profile(email):
    return user_profiles_collection.find_one({"email": email})

def insert_statement(statement_data):
    statements_collection.insert_one(statement_data)

def get_statements_by_user(email):
    return statements_collection.find({"user_email": email})
