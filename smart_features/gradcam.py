import numpy as np
import cv2
import tensorflow as tf
ANATOMY_MAP = {
    (0,  21): {"name":"Frontal Lobe",    "hemisphere":"Left",  "lobe":"Frontal",   "function":"Motor & Cognition"},
    (21, 42): {"name":"Parietal Lobe",   "hemisphere":"Right", "lobe":"Parietal",  "function":"Sensory Processing"},
    (42, 60): {"name":"Temporal Lobe",   "hemisphere":"Left",  "lobe":"Temporal",  "function":"Memory & Language"},
    (60, 80): {"name":"Occipital Lobe",  "hemisphere":"Right", "lobe":"Occipital", "function":"Vision Processing"},
    (80,100): {"name":"Cerebellum",      "hemisphere":"Both",  "lobe":"Posterior", "function":"Balance & Coordination"},
}
def get_anatomy(cx, cy, w, h):
    pct = int((cy / h) * 100)
    for (lo, hi), info in ANATOMY_MAP.items():
        if lo <= pct < hi:
            return info
    return {"name":"Central","hemisphere":"Central","lobe":"Central","function":"Multiple Functions"}
def get_size_info(area_px, total_px):
    pct = (area_px / total_px) * 100
    if pct < 2:
        d, s, g, st = 1.2, "Small",    "Grade I-II",  "Stage I"
    elif pct < 5:
        d, s, g, st = 2.5, "Medium",   "Grade II-III","Stage II"
    elif pct < 10:
        d, s, g, st = 3.8, "Large",    "Grade III",   "Stage III"
    else:
        d, s, g, st = 5.2, "Very Large","Grade IV",   "Stage IV"
    area_cm2 = round(pct * 0.15, 2)
    return {
        "size_label":  s,
        "stage":       st,
        "who_grade":   g,
        "diameter_cm": d,
        "area_cm2":    area_cm2
    }
def generate_gradcam(model, img_array):
    try:
        last_conv = None
        for layer in reversed(model.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                last_conv = layer.name
                break
        if not last_conv:
            return None

        grad_model = tf.keras.models.Model(
            inputs  = model.inputs,
            outputs = [
                model.get_layer(last_conv).output,
                model.output
            ]
        )
        batch = np.expand_dims(img_array, 0)
        with tf.GradientTape() as tape:
            conv_out, preds = grad_model(batch)
            pred_idx = tf.argmax(preds[0])
            loss     = preds[:, pred_idx]

        grads   = tape.gradient(loss, conv_out)
        weights = tf.reduce_mean(grads, axis=(0,1,2))
        cam     = np.zeros(conv_out.shape[1:3])
        for i, w in enumerate(weights):
            cam += float(w) * conv_out[0,:,:,i].numpy()

        cam = np.maximum(cam, 0)
        if cam.max() > 0:
            cam = cam / cam.max()
        return cam
    except:
        return None

def full_tumor_analysis(model, img_array):
    try:
        h, w   = img_array.shape[:2]
        cam    = generate_gradcam(model, img_array)

        if cam is None:
            return None

        cam_resized = cv2.resize(cam, (w, h))
        heatmap     = cv2.applyColorMap(
            (cam_resized * 255).astype(np.uint8),
            cv2.COLORMAP_JET
        )
        heatmap_rgb = cv2.cvtColor(
            heatmap, cv2.COLOR_BGR2RGB
        )

        img_uint8 = (img_array * 255).astype(np.uint8) \
            if img_array.max() <= 1.0 \
            else img_array.astype(np.uint8)

        overlay   = cv2.addWeighted(
            img_uint8, 0.6,
            heatmap_rgb, 0.4, 0
        )

        # Tumor boundary
        thresh = (cam_resized > 0.5).astype(np.uint8) * 255
        contours, _ = cv2.findContours(
            thresh,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        annotated = overlay.copy()
        cx = cy = w//2
        area_px = 0

        if contours:
            largest = max(contours, key=cv2.contourArea)
            area_px = int(cv2.contourArea(largest))
            cv2.drawContours(
                annotated, [largest], -1,
                (255,255,255), 2
            )
            M = cv2.moments(largest)
            if M["m00"] > 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(annotated,(cx,cy),5,(255,255,0),-1)

        anatomy   = get_anatomy(cx, cy, w, h)
        size_info = get_size_info(
            area_px, w * h
        )

        return {
            "heatmap":  heatmap_rgb / 255.0,
            "annotated":annotated  / 255.0,
            "anatomy":  anatomy,
            "size_info":size_info
        }
    except Exception as e:
        return None
