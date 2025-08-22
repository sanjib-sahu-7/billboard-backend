import cv2
import numpy as np
from utils.image_utils import estimate_blur, draw_bbox
from config import MIN_AREA, BLUR_THRESHOLD

def detect_billboards(image_path):
    """
    Detect rectangular billboards in the image.
    Returns (bboxes, confs, H, W)
    """
    img = cv2.imread(image_path)
    if img is None:
        return [], [], 0, 0

    H, W = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 7, 50, 50)

    thr = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 25, 10
    )
    edges = cv2.Canny(thr, 50, 150)
    edges = cv2.dilate(edges, np.ones((3, 3), np.uint8), 1)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = []

    for c in contours:
        area = cv2.contourArea(c)
        if area < MIN_AREA:
            continue

        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) != 4:
            continue

        x, y, w, h = cv2.boundingRect(approx)
        ar = w / float(h) if h > 0 else 0

        if not (0.5 <= ar <= 6.0):
            continue

        rect_area = w * h
        rect_score = area / rect_area if rect_area > 0 else 0
        score = rect_score * rect_area
        candidates.append((score, (x, y, w, h)))

    if not candidates:
        return [], [], H, W

    # Sort by score (best first)
    candidates.sort(key=lambda x: x[0], reverse=True)

    bboxes, confs = [], []
    for score, (x, y, w, h) in candidates:
        conf = min(0.99, 0.4 + score / (100000 + score))
        bboxes.append((x, y, w, h))
        confs.append(conf)

    return bboxes, confs, H, W


def apply_violation_rules(image_path, bboxes, confs, H, W):
    """
    Apply oversize, unsafe placement, blur, and other rules.
    Returns a list of violation dictionaries.
    """
    violations = []
    for bbox, conf in zip(bboxes, confs):
        x, y, w, h = bbox
        reasons = []

        # Rule 1: Oversized
        if (w * h) / (H * W) > 0.4:
            reasons.append("Oversized")

        # Rule 2: Unsafe placement (too close to borders)
        margin = 0.05
        if (x < margin * W or y < margin * H or
            (x + w) > (1 - margin) * W or
            (y + h) > (1 - margin) * H):
            reasons.append("Unsafe placement")

        # Rule 3: Blurry / Old
        blur = estimate_blur(image_path, bbox)
        if blur < BLUR_THRESHOLD:
            reasons.append("Old/Blurry")

        violations.append({
            "bbox": {"x": x, "y": y, "w": w, "h": h},
            "confidence": round(conf, 2),
            "reasons": reasons
        })

    return violations





# import cv2
# import numpy as np
# from utils.image_utils import estimate_blur, draw_bbox
# from config import MIN_AREA, BLUR_THRESHOLD

# def detect_billboards(image_path):
#     """
#     Detect rectangular billboards in the image.
#     Returns a list of tuples: (bbox, confidence)
#     """
#     img = cv2.imread(image_path)
#     if img is None: return [], []

#     H, W = img.shape[:2]
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     gray = cv2.bilateralFilter(gray, 7, 50, 50)
#     thr = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                 cv2.THRESH_BINARY_INV,25,10)
#     edges = cv2.Canny(thr, 50,150)
#     edges = cv2.dilate(edges, np.ones((3,3),np.uint8),1)

#     contours,_ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     candidates=[]
#     for c in contours:
#         area = cv2.contourArea(c)
#         if area<MIN_AREA: continue
#         peri=cv2.arcLength(c,True)
#         approx=cv2.approxPolyDP(c,0.02*peri,True)
#         if len(approx)!=4: continue
#         x,y,w,h=cv2.boundingRect(approx)
#         ar=w/float(h) if h>0 else 0
#         if not(0.5<=ar<=6.0): continue
#         rect_area=w*h
#         rect_score=area/rect_area if rect_area>0 else 0
#         score=rect_score*rect_area
#         candidates.append((score,(x,y,w,h)))

#     if not candidates: return [], []

#     # Sort by score
#     candidates.sort(key=lambda x:x[0], reverse=True)
#     bboxes, confs = [], []
#     for score, (x,y,w,h) in candidates:
#         conf = min(0.99, 0.4 + score/(100000+score))
#         bboxes.append((x,y,w,h))
#         confs.append(conf)
#     return bboxes, confs

# def apply_violation_rules(image_path, bboxes, confs, H, W):
#     """
#     Apply oversize, unsafe placement, blur, and other rules.
#     Returns a list of violation dictionaries.
#     """
#     violations = []
#     for bbox, conf in zip(bboxes, confs):
#         x,y,w,h = bbox
#         reasons = []

#         # Rule 1: Oversized
#         if (w*h)/(H*W) > 0.4:
#             reasons.append("Oversized")

#         # Rule 2: Unsafe placement
#         margin = 0.05
#         if x<margin*W or y<margin*H or (x+w)>(1-margin)*W or (y+h)>(1-margin)*H:
#             reasons.append("Unsafe placement")

#         # Rule 3: Blurry / Old
#         blur = estimate_blur(image_path, bbox)
#         if blur < BLUR_THRESHOLD:
#             reasons.append("Old/Blurry")

#         violations.append({
#             "bbox": {"x":x, "y":y, "w":w, "h":h},
#             "confidence": round(conf,2),
#             "reasons": reasons
#         })

#     return violations
