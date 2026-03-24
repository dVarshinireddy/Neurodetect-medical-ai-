CLASSES = ["glioma", "meningioma", "notumor", "pituitary"]
# RISK MAPPING
RISK_MAP = {
    "glioma": {
        "risk_level":  "CRITICAL",
        "risk_color":  "#FF0000",
        "risk_emoji":  "🔴",
        "description": "Glioma is the most dangerous "
                       "brain tumor requiring immediate "
                       "medical attention",
        "alert_threshold": 0.80
    },
    "meningioma": {
        "risk_level":  "HIGH",
        "risk_color":  "#FF6B00",
        "risk_emoji":  "🟠",
        "description": "Meningioma is usually benign "
                       "but requires prompt medical "
                       "evaluation",
        "alert_threshold": 0.75
    },
    "pituitary": {
        "risk_level":  "MODERATE",
        "risk_color":  "#FFD700",
        "risk_emoji":  "🟡",
        "description": "Pituitary tumor affects hormone "
                       "production and requires "
                       "specialist consultation",
        "alert_threshold": 0.70
    },
    "notumor": {
        "risk_level":  "NONE",
        "risk_color":  "#00C851",
        "risk_emoji":  "🟢",
        "description": "No tumor detected. Brain scan "
                       "appears normal. Routine "
                       "checkup recommended",
        "alert_threshold": 1.0
    }
}

# ─────────────────────────────────────────
# CLINICAL THRESHOLDS
# ─────────────────────────────────────────
CLINICAL_THRESHOLDS = {
    "definitive":  90,
    "probable":    70,
    "possible":    50,
    "inconclusive": 0
}
# GET CONFIDENCE LEVEL
def get_confidence_level(confidence):
    if confidence >= 90:
        return "Definitive",   "#00C851", "⭐⭐⭐⭐⭐"
    elif confidence >= 70:
        return "Probable",     "#FFD700", "⭐⭐⭐⭐"
    elif confidence >= 50:
        return "Possible",     "#FF6B00", "⭐⭐⭐"
    else:
        return "Inconclusive", "#FF0000", "⭐⭐"
# GET RISK INFO
def get_risk_info(prediction):
    return RISK_MAP.get(
        prediction,
        RISK_MAP["notumor"]
    )
# CHECK DOCTOR ALERT
def check_doctor_alert(prediction, confidence):
    risk    = RISK_MAP.get(prediction)
    if not risk:
        return False, ""

    conf_decimal = confidence / 100

    if conf_decimal >= risk["alert_threshold"]:
        if prediction == "glioma":
            return True, (
                "🚨 CODE RED: High confidence Glioma "
                "detected! Immediate neurosurgeon "
                "consultation required within 24 hours!"
            )
        elif prediction == "meningioma":
            return True, (
                "⚠️ CODE ORANGE: Meningioma detected! "
                "Schedule neurologist appointment "
                "within 48 hours!"
            )
        elif prediction == "pituitary":
            return True, (
                "⚠️ CODE YELLOW: Pituitary tumor "
                "detected! Consult endocrinologist "
                "within 1-2 weeks!"
            )
    return False, ""
# GET SENSITIVITY SPECIFICITY
def get_clinical_metrics(prediction, probabilities):
    pred_prob = max(probabilities)
    other_max = sorted(probabilities)[-2]

    sensitivity = pred_prob * 100
    specificity = (1 - other_max) * 100
    ppv         = pred_prob / (
        pred_prob + other_max
    ) * 100
    npv         = (1 - other_max) / (
        (1 - other_max) + (1 - pred_prob)
    ) * 100

    return {
        "sensitivity": round(sensitivity, 2),
        "specificity": round(specificity, 2),
        "ppv":         round(ppv, 2),
        "npv":         round(npv, 2)
    }
# FULL CONFIDENCE REPORT
def get_full_confidence_report(
    prediction, confidence, probabilities
):
    conf_label, conf_color, stars = \
        get_confidence_level(confidence)
    risk_info   = get_risk_info(prediction)
    alert, msg  = check_doctor_alert(
        prediction, confidence
    )
    metrics     = get_clinical_metrics(
        prediction, probabilities
    )

    return {
        "prediction":       prediction,
        "confidence":       confidence,
        "confidence_label": conf_label,
        "confidence_color": conf_color,
        "stars":            stars,
        "risk_level":       risk_info["risk_level"],
        "risk_color":       risk_info["risk_color"],
        "risk_emoji":       risk_info["risk_emoji"],
        "description":      risk_info["description"],
        "doctor_alert":     alert,
        "alert_message":    msg,
        "sensitivity":      metrics["sensitivity"],
        "specificity":      metrics["specificity"],
        "ppv":              metrics["ppv"],
        "npv":              metrics["npv"]
    }

if __name__ == "__main__":
    # Test
    test_probs = [0.95, 0.03, 0.01, 0.01]
    report = get_full_confidence_report(
        "glioma", 95.0, test_probs
    )
    print("🧠 Confidence Report Test:")
    for k, v in report.items():
        print(f"  {k}: {v}")
