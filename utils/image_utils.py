import cv2
import numpy as np

def estimate_blur(image_path, bbox):
    img = cv2.imread(image_path)
    x, y, w, h = bbox
    roi = img[y:y+h, x:x+w]
    if roi.size == 0: return 0.0
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    return float(cv2.Laplacian(gray, cv2.CV_64F).var())

def draw_bbox(image_path, bbox, color=(0,255,0), thickness=3):
    img = cv2.imread(image_path)
    x, y, w, h = bbox
    cv2.rectangle(img, (x, y), (x+w, y+h), color, thickness)
    return img
