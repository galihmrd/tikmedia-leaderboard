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
        check = collection.find_one({"user_id": user_id})
        if "nsfw" in check["reason"].lower():
            return {
                "success": False,
                "message": f"Permanently blacklist. Reason: {check['reason']}"
            }
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

def check_blacklist(self, user_id: str) -> Dict:
    """
    Check if a user is in blacklist
        
    Args:
        user_id: User ID to check
            
    Returns:
        Dict with check result
    """
    try:
        document = collection.find_one({"user_id": user_id})
            
        if document:
            return {
                "is_blacklisted": True,
                "data": document
            }
            
        return {
            "is_blacklisted": False,
            "data": None
        }
    except Exception as e:
        return {
            "is_blacklisted": False,
            "error": str(e)
        }
