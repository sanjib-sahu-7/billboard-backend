from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime
from pymongo import MongoClient
from config import MONGO_URI, DB_NAME

user_bp = Blueprint("user", __name__)

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_col = db["users"]

# ---------------- Signup ----------------
@user_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    full_name = data.get("full_name")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not username or not password or not email or not full_name:
        return jsonify({"success": False, "message": "All fields are required"}), 400

    # Check if user already exists
    if users_col.find_one({"username": username}):
        return jsonify({"success": False, "message": "User already exists"}), 400

    # Save new user in MongoDB
    users_col.insert_one({
        "username": username,
        "password": password,  # ⚠️ later replace with bcrypt hashing
        "full_name": full_name,
        "email": email
    })

    return jsonify({"success": True, "message": "Signup successful"}), 201


# ---------------- Login ----------------
@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = users_col.find_one({"username": username})

    if user and user["password"] == password:
        access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(days=1))
        return jsonify({
            "success": True,
            "message": "Login successful",
            "token": access_token,
            "username": username,
            "full_name": user.get("full_name"),
            "email": user.get("email")
        }), 200

    return jsonify({"success": False, "message": "Invalid credentials"}), 401


# ---------------- Profile (protected) ----------------
@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify({"username": current_user, "message": "This is a protected route"})
