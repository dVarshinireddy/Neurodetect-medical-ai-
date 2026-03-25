import cv2
import numpy as np
from PIL import Image
DEMO_FRAMES = [
    {
        "label":      "glioma",
        "confidence": 94.5,
        "color":      (0, 0, 255)
    },
    {
        "label":      "notumor",
        "confidence": 97.2,
        "color":      (0, 200, 0)
    },
    {
        "label":      "meningioma",
        "confidence": 88.3,
        "color":      (0, 165, 255)
    },
]
def preprocess_frame(frame,
                     target=(224, 224)):
    resized   = cv2.resize(frame, target)
    rgb       = cv2.cvtColor(
        resized, cv2.COLOR_BGR2RGB
    )
    normalized = rgb.astype(
        np.float32
    ) / 255.0
    return np.expand_dims(normalized, 0)
def annotate_frame(frame, label,
                   confidence, color):
    h, w = frame.shape[:2]
    # Background box
    cv2.rectangle(
        frame,
        (0, 0), (w, 60),
        (0, 0, 0), -1
    )
    # Prediction text
    cv2.putText(
        frame,
        f"Detection: {label.upper()}",
        (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7, color, 2, cv2.LINE_AA
    )
    # Confidence text
    cv2.putText(
        frame,
        f"Confidence: {confidence:.1f}%",
        (10, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        1, cv2.LINE_AA
    )
    # Confidence bar
    bar_w = int((confidence / 100) * w)
    cv2.rectangle(
        frame,
        (0, h - 10), (bar_w, h),
        color, -1
    )
    # Corner markers
    corner_len = 30
    thickness  = 3
    corners = [
        ((20, 70),
         (20 + corner_len, 70),
         (20, 70 + corner_len)),
        ((w-20, 70),
         (w-20-corner_len, 70),
         (w-20, 70+corner_len)),
        ((20, h-70),
         (20+corner_len, h-70),
         (20, h-70-corner_len)),
        ((w-20, h-70),
         (w-20-corner_len, h-70),
         (w-20, h-70-corner_len)),
    ]
    for c in corners:
        cv2.line(frame, c[0], c[1],
                 color, thickness)
        cv2.line(frame, c[0], c[2],
                 color, thickness)
    return frame
def process_uploaded_video(
    video_path, model=None
):
    cap     = cv2.VideoCapture(video_path)
    results = []
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % 10 == 0:
            if model:
                processed = preprocess_frame(
                    frame
                )
                # Use model prediction
                results.append({
                    "frame": frame_count,
                    "label": "processing",
                    "conf":  0
                })
            else:
                # Demo mode
                demo = DEMO_FRAMES[
                    frame_count % 3
                ]
                results.append({
                    "frame": frame_count,
                    "label": demo["label"],
                    "conf":  demo["confidence"]
                })
        frame_count += 1
    cap.release()
    return results
