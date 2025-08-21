from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime

user_bp = Blueprint("user", __name__)

# In-memory user DB (replace with MongoDB in production)
users_db = {}

# Signup route
@user_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    full_name = data.get("full_name")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not username or not password or not email or not full_name:
        return jsonify({"error": "All fields are required"}), 400

    if username in users_db:
        return jsonify({"error": "User already exists"}), 400

    # Save all user details (using dict instead of just password)
    users_db[username] = {
        "password": password,
        "full_name": full_name,
        "email": email
    }

    return jsonify({"message": "Signup successful"}), 201


# Login route - returns JWT token
@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = users_db.get(username)

    if user and user["password"] == password:
        # Create JWT token valid for 1 day
        access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(days=1))

        return jsonify({
            "message": "Login successful",
            "token": access_token,
            "username": username,
            "full_name": user.get("full_name"),
            "email": user.get("email")
        })

    return jsonify({"error": "Invalid credentials"}), 401

# Example protected route (optional)
@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify({"username": current_user, "message": "This is a protected route"})
