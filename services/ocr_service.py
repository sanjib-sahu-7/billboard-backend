import pytesseract
import cv2
from config import BANNED_KEYWORDS

def check_text_violation(image_path, bbox):
    """
    Extract text from the given ROI (bounding box) in the image
    and check against banned keywords.
    Returns a list of violation reasons.
    """
    x, y, w, h = bbox
    img = cv2.imread(image_path)

    if img is None:
        return ["Error: Unable to read image"]

    # Crop ROI safely
    roi = img[y:y+h, x:x+w]
    if roi.size == 0:
        return ["Error: Empty ROI"]

    # Preprocess for OCR
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Run OCR
    text = pytesseract.image_to_string(thresh).strip()
    print(f"[OCR] Extracted text: {text}")  # Debugging log

    # Check for banned keywords
    reasons = []
    for word in BANNED_KEYWORDS:
        if word.lower() in text.lower():
            reasons.append(f"Content Violation: {word}")

    return reasons



# import pytesseract
# from config import BANNED_KEYWORDS

# # Set Tesseract executable path (Windows)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# def check_text_violation(image_path, bbox):
#     """
#     Extract text from ROI and check against banned keywords.
#     Returns list of violation reasons.
#     """
#     import cv2
#     x, y, w, h = bbox
#     img = cv2.imread(image_path)
#     roi = img[y:y+h, x:x+w]
#     text = pytesseract.image_to_string(roi)
#     reasons = []

#     for word in BANNED_KEYWORDS:
#         if word.lower() in text.lower():
#             reasons.append(f"Content Violation: {word}")
#     return reasons
