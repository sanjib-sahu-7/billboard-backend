from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME, COLLECTION_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
reports_col = db["user_reports"] 

history_bp = Blueprint("history", __name__)

@history_bp.route("/", methods=["GET"])
@jwt_required()
def get_user_history():
    current_user = get_jwt_identity()
    # Query MongoDB for reports where reported_by equals current user
    records = list(reports_col.find({"reported_by": current_user}, {"_id": 0}))
    return jsonify(records)
