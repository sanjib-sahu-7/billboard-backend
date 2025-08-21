from flask import Blueprint, jsonify
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
images_col = db[COLLECTION_NAME]

history_bp = Blueprint("history", __name__)

@history_bp.route("/", methods=["GET"])
def get_history():
    """
    Return all records from MongoDB
    """
    records = list(images_col.find({}, {"_id": 0}))
    return jsonify(records)
