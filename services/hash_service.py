import hashlib
from datetime import datetime, timezone

def generate_image_hash(image_path):
    with open(image_path, "rb") as f:
        filehash = hashlib.md5(f.read()).hexdigest()
    return filehash

def check_duplicate(image_hash, images_col, days_threshold=180):
    """
    Check if image hash exists in MongoDB and is older than threshold.
    Returns True if expired duplicate, else False
    """
    record = images_col.find_one({"hash": image_hash})
    if record:
        timestamp = record.get("result", {}).get("timestamp")
        if timestamp:
            from dateutil.parser import parse
            ts = parse(timestamp)
            delta_days = (datetime.now(timezone.utc) - ts).days
            if delta_days > days_threshold:
                return True
    return False
