import os
from pymongo import MongoClient, DESCENDING
from datetime import datetime
import dns.resolver

dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

db = os.getenv("DATABASE_URL")
# Koneksi ke MongoDB
client = MongoClient(db)
db = client['rank_user']
collection = db.user

# Fungsi untuk menambah atau update ranking
def update_ranking(user_id, action_count=1):
    """
    Menambah jumlah aktivitas user
    Args:
        user_id: ID unik user
        action_count: Jumlah aktivitas yang ditambahkan (default: 1)
    """
    result = collection.update_one(
        {'user_id': user_id},
        {
            '$inc': {'total_actions': action_count},
            '$set': {'last_updated': datetime.now()}
        },
        upsert=True
    )
    return result

# Fungsi untuk mendapatkan ranking user tertentu
def get_user_ranking(user_id):
    """Mengambil data ranking user berdasarkan ID"""
    user = collection.find_one({'user_id': user_id})
    if user:
        # Hitung posisi ranking
        rank = collection.count_documents({
            'total_actions': {'$gt': user['total_actions']}
        }) + 1
        user['rank'] = rank
    return user

# Fungsi untuk mendapatkan top rankings
def get_top_rankings(limit=10):
    """
    Mengambil top N user dengan aktivitas terbanyak
    Args:
        limit: Jumlah user yang ditampilkan (default: 10)
    """
    rankings = collection.find().sort('total_actions', DESCENDING).limit(limit)
    result = []
    for idx, user in enumerate(rankings, 1):
        user['rank'] = idx
        result.append(user)
    return result

# Fungsi untuk reset ranking user
def reset_user_ranking(user_id):
    """Mereset ranking user ke 0"""
    result = collection.update_one(
        {'user_id': user_id},
        {'$set': {'total_actions': 0, 'last_updated': datetime.now()}}
    )
    return result

# Fungsi untuk menghapus data user
def delete_user(user_id):
    """Menghapus data ranking user"""
    result = collection.delete_one({'user_id': user_id})
    return result

# Fungsi untuk mendapatkan total user
def get_total_users():
    """Menghitung total user dalam ranking"""
    return collection.count_documents({})
