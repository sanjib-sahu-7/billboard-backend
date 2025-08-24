import os

# Folders
UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")
RESULT_FOLDER = os.environ.get("RESULT_FOLDER", "results")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# MongoDB connection info
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://xyz869601:Pe8XHiHtG9GgaXkz@cluster0.zagyai9.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DB_NAME", "billboardDB")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME", "images")

# Detection thresholds
MIN_AREA = float(os.environ.get("MIN_AREA", 1000))
CONFIDENCE_THRESHOLD = float(os.environ.get("CONFIDENCE_THRESHOLD", 0.45))
BLUR_THRESHOLD = float(os.environ.get("BLUR_THRESHOLD", 50))

# Content violation keywords (comma separated string from env or default list)
banned_keywords_env = os.environ.get("BANNED_KEYWORDS")
if banned_keywords_env:
    BANNED_KEYWORDS = [k.strip() for k in banned_keywords_env.split(",")]
else:
    BANNED_KEYWORDS = ["alcohol","tobacco","gambling","adult"]
