import pytesseract
from config import BANNED_KEYWORDS

# Set Tesseract executable path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def check_text_violation(image_path, bbox):
    """
    Extract text from ROI and check against banned keywords.
    Returns list of violation reasons.
    """
    import cv2
    x, y, w, h = bbox
    img = cv2.imread(image_path)
    roi = img[y:y+h, x:x+w]
    text = pytesseract.image_to_string(roi)
    reasons = []

    for word in BANNED_KEYWORDS:
        if word.lower() in text.lower():
            reasons.append(f"Content Violation: {word}")
    return reasons
