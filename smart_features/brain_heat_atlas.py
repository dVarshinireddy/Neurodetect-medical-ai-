import numpy as np
import cv2
BRAIN_REGIONS = {
    "frontal_lobe": {
        "name":     "Frontal Lobe",
        "center":   (0.45, 0.25),
        "radius":   0.18,
        "functions":["Executive function",
                     "Motor control",
                     "Speech production",
                     "Personality"],
        "risk_if_tumor": "HIGH"
    },
    "temporal_lobe": {
        "name":     "Temporal Lobe",
        "center":   (0.25, 0.55),
        "radius":   0.15,
        "functions":["Memory formation",
                     "Language comprehension",
                     "Hearing",
                     "Emotion"],
        "risk_if_tumor": "HIGH"
    },
    "parietal_lobe": {
        "name":     "Parietal Lobe",
        "center":   (0.55, 0.35),
        "radius":   0.15,
        "functions":["Sensory processing",
                     "Spatial awareness",
                     "Reading",
                     "Navigation"],
        "risk_if_tumor": "MODERATE"
    },
    "occipital_lobe": {
        "name":     "Occipital Lobe",
        "center":   (0.50, 0.70),
        "radius":   0.12,
        "functions":["Visual processing",
                     "Color recognition",
                     "Motion detection",
                     "Depth perception"],
        "risk_if_tumor": "MODERATE"
    },
    "cerebellum": {
        "name":     "Cerebellum",
        "center":   (0.50, 0.85),
        "radius":   0.12,
        "functions":["Balance",
                     "Coordination",
                     "Fine motor skills",
                     "Posture"],
        "risk_if_tumor": "HIGH"
    },
    "brainstem": {
        "name":     "Brain Stem",
        "center":   (0.50, 0.78),
        "radius":   0.07,
        "functions":["Breathing",
                     "Heart rate",
                     "Blood pressure",
                     "Consciousness"],
        "risk_if_tumor": "CRITICAL"
    },
    "pituitary": {
        "name":     "Pituitary Gland",
        "center":   (0.48, 0.60),
        "radius":   0.05,
        "functions":["Hormone regulation",
                     "Growth control",
                     "Metabolism",
                     "Reproduction"],
        "risk_if_tumor": "MODERATE"
    }
}
TUMOR_LOCATION_MAP = {
    "glioma":     ["frontal_lobe",
                   "temporal_lobe",
                   "parietal_lobe"],
    "meningioma": ["frontal_lobe",
                   "parietal_lobe",
                   "occipital_lobe"],
    "pituitary":  ["pituitary"],
    "notumor":    []
}
def generate_heat_atlas(
    prediction,
    confidence,
    img_size = (300, 300)
):
    h, w = img_size
    atlas = np.zeros((h, w, 3),
                     dtype=np.uint8)
    atlas[:] = (240, 245, 250)

    affected = TUMOR_LOCATION_MAP.get(
        prediction, []
    )
    for region_key, region in \
            BRAIN_REGIONS.items():
        cx = int(region["center"][0] * w)
        cy = int(region["center"][1] * h)
        r  = int(region["radius"]
                 * min(w, h))

        is_affected = region_key in affected

        if is_affected:
            intensity = int(
                confidence * 2.55
            )
            color = (
                0,
                max(0, 100 - intensity),
                min(255, intensity + 100)
            )
            # Heat glow
            for i in range(3, 0, -1):
                cv2.circle(
                    atlas,
                    (cx, cy),
                    r + i * 8,
                    (0, 50,
                     min(255,
                         intensity//2)),
                    -1
                )
        else:
            color = (180, 200, 210)

        cv2.circle(
            atlas, (cx, cy),
            r, color, -1
        )
        cv2.circle(
            atlas, (cx, cy),
            r, (100, 120, 140), 2
        )

        # Label
        font_scale = 0.35
        label = region["name"].split()[0]
        text_size = cv2.getTextSize(
            label,
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale, 1
        )[0]
        tx = cx - text_size[0] // 2
        ty = cy + text_size[1] // 2
        cv2.putText(
            atlas, label,
            (tx, ty),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            (255, 255, 255) \
                if is_affected \
                else (80, 80, 80),
            1, cv2.LINE_AA
        )
    return atlas
def get_affected_regions(prediction):
    affected_keys = TUMOR_LOCATION_MAP.get(
        prediction, []
    )
    return [
        BRAIN_REGIONS[k]
        for k in affected_keys
        if k in BRAIN_REGIONS
    ]
