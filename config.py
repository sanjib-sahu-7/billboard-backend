import os

# Folders
UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

# MongoDB
MONGO_URI = "mongodb+srv://xyz869601:Pe8XHiHtG9GgaXkz@cluster0.zagyai9.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "billboardDB"
COLLECTION_NAME = "images"

# Detection thresholds
MIN_AREA = 1000
CONFIDENCE_THRESHOLD = 0.45
BLUR_THRESHOLD = 50

# Content violation keywords
BANNED_KEYWORDS = ["alcohol","tobacco","gambling","adult"]
