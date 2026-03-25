import numpy as np
import cv2
from PIL import Image
TUMOR_COLORS = {
    "glioma":     (255, 50,  50),
    "meningioma": (255, 165, 0),
    "pituitary":  (50,  150, 255),
    "notumor":    (50,  200, 50)
}
def create_segmentation_mask(
    image_array,
    prediction,
    confidence
):
    h, w = image_array.shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)
    if prediction == "notumor":
        return mask
    # Simulate tumor region based on
    # prediction type
    cx, cy = w // 2, h // 2

    offsets = {
        "glioma":     (-20, -30),
        "meningioma": (30,  -20),
        "pituitary":  (0,    20),
    }
    ox, oy = offsets.get(prediction, (0,0))
    cx += ox
    cy += oy
    # Size based on confidence
    radius = int(
        (confidence / 100) * (min(h,w) // 4)
    )
    radius = max(radius, 20)
    # Draw elliptical tumor region
    cv2.ellipse(
        mask,
        (cx, cy),
        (radius, int(radius * 0.8)),
        0, 0, 360,
        255, -1
    )
    # Smooth the mask
    mask = cv2.GaussianBlur(
        mask, (15, 15), 0
    )
    _, mask = cv2.threshold(
        mask, 100, 255, cv2.THRESH_BINARY
    )

    return mask
def apply_segmentation_overlay(
    image_array,
    mask,
    prediction,
    alpha = 0.4
):
    color = TUMOR_COLORS.get(
        prediction, (255, 50, 50)
    )
    overlay = image_array.copy()
    colored_mask = np.zeros_like(image_array)
    colored_mask[mask > 0] = color
    # Blend
    result = cv2.addWeighted(
        image_array, 1.0,
        colored_mask, alpha, 0
    )
    # Draw contour
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    cv2.drawContours(
        result, contours, -1,
        color, 2
    )
    return result
def get_segmentation_stats(mask, image):
    h, w = mask.shape
    total_pixels = h * w
    tumor_pixels = np.sum(mask > 0)
    tumor_pct    = (
        tumor_pixels / total_pixels * 100
    )

    if tumor_pct == 0:
        size_category = "None"
        area_cm2      = 0.0
    elif tumor_pct < 2:
        size_category = "Small"
        area_cm2      = round(
            tumor_pixels * 0.0009, 2
        )
    elif tumor_pct < 5:
        size_category = "Medium"
        area_cm2      = round(
            tumor_pixels * 0.0009, 2
        )
    elif tumor_pct < 10:
        size_category = "Large"
        area_cm2      = round(
            tumor_pixels * 0.0009, 2
        )
    else:
        size_category = "Very Large"
        area_cm2      = round(
            tumor_pixels * 0.0009, 2
        )

    return {
        "tumor_pixels":  int(tumor_pixels),
        "total_pixels":  int(total_pixels),
        "tumor_pct":     round(tumor_pct, 2),
        "size_category": size_category,
        "area_cm2":      area_cm2
    }
def run_segmentation(image, prediction,
                     confidence):
    if isinstance(image, Image.Image):
        img_array = np.array(
            image.convert("RGB")
        )
    else:
        img_array = image

    mask    = create_segmentation_mask(
        img_array, prediction, confidence
    )
    overlay = apply_segmentation_overlay(
        img_array, mask, prediction
    )
    stats   = get_segmentation_stats(
        mask, img_array
    )
    return {
        "original":  img_array,
        "mask":      mask,
        "overlay":   overlay,
        "stats":     stats
    }
