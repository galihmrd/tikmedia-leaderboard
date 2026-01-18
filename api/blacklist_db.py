import os
from pymongo import MongoClient
from typing import Dict
import dns.resolver


dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
db = os.getenv("DATABASE_URL")
client = MongoClient(db)
db = client['blacklist']
collection = db.user

def remove_from_blacklist(user_id: str) -> Dict:
    try:
        result = collection.delete_one({"user_id": user_id})
            
        if result.deleted_count == 0:
            return {
                "success": False,
                "message": f"User {user_id} not found in blacklist"
            }
            
        return {
            "success": True,
            "message": f"User {user_id} removed from blacklist",
            "deleted_count": result.deleted_count
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error removing user from blacklist: {str(e)}"
        }
