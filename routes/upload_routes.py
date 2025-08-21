from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from datetime import datetime, timezone
import base64
import os
import cv2

from config import UPLOAD_FOLDER, RESULT_FOLDER, MONGO_URI, DB_NAME, COLLECTION_NAME, BANNED_KEYWORDS
from services.detection import detect_billboards, apply_violation_rules
from services.ocr_service import check_text_violation
from services.hash_service import generate_image_hash, check_duplicate
from utils.exif_utils import extract_exif_location
from services.gps_service import check_gps_violation
from flask_jwt_extended import jwt_required, get_jwt_identity

# Initialize MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
images_col = db[COLLECTION_NAME]
reports_col = db["user_reports"]

# Allowed zones example
ALLOWED_ZONES = [
    {"name":"Downtown","lat_min":20.30,"lat_max":20.40,"lon_min":85.80,"lon_max":85.85},
    {"name":"Uptown","lat_min":20.41,"lat_max":20.50,"lon_min":85.86,"lon_max":85.90},
]

upload_bp = Blueprint("upload", __name__)
report_bp = Blueprint("report", __name__)

# ----------------- Upload & Detect -----------------
@upload_bp.route("", methods=["POST"])
@jwt_required()
def upload_and_detect():
    current_user = get_jwt_identity()
    
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Convert to Base64 for storage
    with open(filepath, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode("utf-8")

    # Detect billboards
    bboxes, confs = detect_billboards(filepath)
    img = cv2.imread(filepath) if bboxes else None
    violations = []

    if bboxes:
        H, W = img.shape[:2]
        violations = apply_violation_rules(filepath, bboxes, confs, H, W)

        # OCR content check
        for v in violations:
            extra = check_text_violation(filepath, (v["bbox"]["x"], v["bbox"]["y"], v["bbox"]["w"], v["bbox"]["h"]))
            v["reasons"].extend(extra)

        # GPS violation check
        gps = extract_exif_location(filepath)
        if gps and check_gps_violation(gps, ALLOWED_ZONES):
            for v in violations:
                v["reasons"].append("Unauthorized Location")

        # Draw bounding boxes
        for v in violations:
            x, y, w, h = v["bbox"]["x"], v["bbox"]["y"], v["bbox"]["w"], v["bbox"]["h"]
            cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 3)

        # Save result image
        result_path = os.path.join(RESULT_FOLDER, filename)
        cv2.imwrite(result_path, img)
    else:
        violations = [{"bbox": None, "confidence": 0.0, "reasons": ["No billboard detected"]}]
        gps = extract_exif_location(filepath)

    # Duplicate / Expired check
    img_hash = generate_image_hash(filepath)
    if check_duplicate(img_hash, images_col):
        for v in violations:
            v["reasons"].append("Expired Billboard")

    output = {
        "filename": filename,
        "violation": any(v["reasons"] for v in violations),
        "violations": violations,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "image_url": f"http://{request.host}/uploads/{filename}",
        "result_url": f"http://{request.host}/results/{filename}",
        "latitude": gps['lat'] if gps else None,
        "longitude": gps['lon'] if gps else None,
        "hash": img_hash,
        "uploaded_by": current_user
    }

    # Save in MongoDB
    images_col.insert_one({
        "filename": filename,
        "image": encoded_image,
        "result": output,
        "hash": img_hash,
        "uploaded_by": current_user
    })

    return jsonify([output])

# ----------------- User Report -----------------
@report_bp.route("/report", methods=["POST"])
@jwt_required()
def report_unauthorized():
    current_user = get_jwt_identity()
    data = request.json
    report = {
        "reported_by": current_user,
        "description": data.get("description"),
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    reports_col.insert_one(report)
    return jsonify({"message": "Report submitted successfully"}), 201

# ----------------- Heatmap Data -----------------
@report_bp.route("/heatmap", methods=["GET"])
def get_heatmap_data():
    reports = list(reports_col.find({}, {"_id":0, "latitude":1, "longitude":1}))
    detections = list(images_col.find({}, {"_id":0, "latitude":1, "longitude":1, "violation":1}))
    return jsonify({"reports": reports, "detections": detections})
