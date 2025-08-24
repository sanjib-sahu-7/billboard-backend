from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME
from bson.objectid import ObjectId

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
reports_col = db["user_reports"] 

history_bp = Blueprint("history", __name__)


@history_bp.route("/", methods=["GET"])
@jwt_required()
def get_user_history():
    current_user = get_jwt_identity()
    
    records_cursor = reports_col.find({"reported_by": current_user})
    records = []
    for record in records_cursor:
        # Convert _id and any ObjectId fields to strings
        record['_id'] = str(record.get('_id', ''))
        
        # Convert image_file_id ObjectId to string if present
        if 'image_file_id' in record and isinstance(record['image_file_id'], ObjectId):
            record['image_file_id'] = str(record['image_file_id'])
        
        records.append(record)
    
    return jsonify(records)
