import pymongo
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Access environment variables
uri = os.getenv("MongoDBDriver")

client = pymongo.MongoClient(uri)
database = client["Backend"]

# Define JSON Schema for validation
user_schema = {
     "$jsonSchema": {
         "bsonType": "object",
        "required": ["name", "email", "username","password","address","tripCount"],
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "email": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "username": {
                "bsonType": "string",
                "description": "must be an string and is required"
            },
            "password": {
                "bsonType": "string",
                "description": "must be an string and is required"
            } ,
            "address": {
                "bsonType": "object",
                "required": ["street", "city", "province", "postal"],
                "properties": {
                    "street": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "city": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "province": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "postal": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    }
                }
            },
            "tripCount": {
                "bsonType":"int",
                "description":"must be an integer, default 0, increments 1 autogenerated is required"
            },
            "trips": {
                "bsonType": "array",
                "minItems": 0,
                "uniqueItems": False,
                "items": {
                    "bsonType":"objectId",
                    "required":["tripid"],
                    "properties": {
                        "tripid" : {
                            "bsonType": "objectId",
                            "description":"must be a string and is required"
                        }
                    }
                }
            }
        }
    }
}

# Create collection with schema validation
collection = database.create_collection("users")
database.command("collMod", "users", validator=user_schema)
# Add unique index on the email field
collection.create_index("email", unique=True)
collection.create_index("username", unique=True)