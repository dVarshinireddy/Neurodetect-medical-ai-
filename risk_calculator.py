# NeuroDetect - risk_calculator.py
# Feature 24: Risk Score Calculator

RISK_WEIGHTS = {
    "tumor_type": {
        "glioma":     40,
        "meningioma": 25,
        "pituitary":  20,
        "notumor":    0
    },
    "confidence": {
        "high":   15,  # >85%
        "medium": 10,  # 70-85%
        "low":    5    # <70%
    },
    "age_group": {
        "child":   10,  # <18
        "young":   5,   # 18-40
        "middle":  15,  # 40-60
        "senior":  20   # >60
    },
    "size": {
        "Very Large": 20,
        "Large":      15,
        "Medium":     10,
        "Small":      5,
        "N/A":        5
    }
}

def calculate_risk_score(
    prediction,
    confidence,
    age,
    tumor_size = "N/A",
    symptoms   = None
):
    score = 0
    breakdown = {}

    # Tumor type score
    tumor_score = RISK_WEIGHTS[
        "tumor_type"
    ].get(prediction, 0)
    score += tumor_score
    breakdown["Tumor Type"] = tumor_score

    # Confidence score
    if confidence >= 85:
        conf_score = RISK_WEIGHTS[
            "confidence"
        ]["high"]
    elif confidence >= 70:
        conf_score = RISK_WEIGHTS[
            "confidence"
        ]["medium"]
    else:
        conf_score = RISK_WEIGHTS[
            "confidence"
        ]["low"]
    score += conf_score
    breakdown["AI Confidence"] = conf_score

    # Age score
    try:
        age_int = int(age)
        if age_int < 18:
            age_score = RISK_WEIGHTS[
                "age_group"
            ]["child"]
        elif age_int < 40:
            age_score = RISK_WEIGHTS[
                "age_group"
            ]["young"]
        elif age_int < 60:
            age_score = RISK_WEIGHTS[
                "age_group"
            ]["middle"]
        else:
            age_score = RISK_WEIGHTS[
                "age_group"
            ]["senior"]
    except:
        age_score = 10
    score += age_score
    breakdown["Age Factor"] = age_score

    # Size score
    size_score = RISK_WEIGHTS[
        "size"
    ].get(tumor_size, 5)
    score += size_score
    breakdown["Tumor Size"] = size_score

    # Symptoms score
    symptom_score = 0
    if symptoms:
        symptom_score = min(
            len(symptoms) * 3, 15
        )
    score += symptom_score
    breakdown["Symptoms"] = symptom_score

    # Cap at 100
    score = min(score, 100)

    # Risk level
    if score >= 70:
        level = "CRITICAL"
        color = "#E53E3E"
        icon  = "🚨"
        action = "Immediate medical intervention required!"
    elif score >= 50:
        level = "HIGH"
        color = "#DD6B20"
        icon  = "⚠️"
        action = "Urgent specialist consultation needed!"
    elif score >= 30:
        level = "MODERATE"
        color = "#D69E2E"
        icon  = "⚡"
        action = "Schedule appointment within 2 weeks."
    else:
        level = "LOW"
        color = "#38A169"
        icon  = "✅"
        action = "Routine monitoring recommended."

    return {
        "score":      score,
        "level":      level,
        "color":      color,
        "icon":       icon,
        "action":     action,
        "breakdown":  breakdown,
        "max_score":  100
    }
