# NeuroDetect - history_tracker.py
# Smart Feature 7: Patient History Tracker

import os
import json
from datetime import datetime

HISTORY_FILE = "history/prediction_history.json"

# ─────────────────────────────────────────
# SAVE PREDICTION
# ─────────────────────────────────────────
def save_prediction(
    patient_name,
    prediction,
    confidence,
    risk_level,
    model_used,
    doctor_name,
    tumor_size  = "N/A",
    stage       = "N/A",
    icd10_code  = "N/A",
    notes       = ""
):
    os.makedirs("history", exist_ok=True)

    history = load_history()

    entry = {
        "id":           len(history) + 1,
        "timestamp":    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                        ),
        "patient_name": patient_name,
        "prediction":   prediction,
        "confidence":   round(confidence, 2),
        "risk_level":   risk_level,
        "model_used":   model_used,
        "doctor_name":  doctor_name,
        "tumor_size":   tumor_size,
        "stage":        stage,
        "icd10_code":   icd10_code,
        "notes":        notes
    }

    history.append(entry)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

    print(f"✅ Saved prediction for {patient_name}")
    return entry

# ─────────────────────────────────────────
# LOAD HISTORY
# ─────────────────────────────────────────
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE) as f:
            return json.load(f)
    except:
        return []

# ─────────────────────────────────────────
# GET PATIENT HISTORY
# ─────────────────────────────────────────
def get_patient_history(patient_name):
    history = load_history()
    return [
        h for h in history
        if h["patient_name"].lower() ==
           patient_name.lower()
    ]

# ─────────────────────────────────────────
# GET SUMMARY
# ─────────────────────────────────────────
def get_summary():
    history = load_history()
    if not history:
        return {
            "total_scans":    0,
            "tumor_detected": 0,
            "no_tumor":       0,
            "critical_cases": 0,
            "by_type":        {}
        }

    tumor    = [
        h for h in history
        if h["prediction"] != "notumor"
    ]
    critical = [
        h for h in history
        if h.get("risk_level") == "CRITICAL"
    ]

    by_type = {}
    for h in history:
        p = h["prediction"]
        by_type[p] = by_type.get(p, 0) + 1

    return {
        "total_scans":    len(history),
        "tumor_detected": len(tumor),
        "no_tumor":       len(history) - len(tumor),
        "critical_cases": len(critical),
        "by_type":        by_type
    }

# ─────────────────────────────────────────
# DELETE HISTORY
# ─────────────────────────────────────────
def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
        print("✅ History cleared!")
    else:
        print("⚠️ No history found!")

# ─────────────────────────────────────────
# SEARCH HISTORY
# ─────────────────────────────────────────
def search_history(keyword):
    history = load_history()
    results = []
    for h in history:
        if (keyword.lower() in
                h["patient_name"].lower() or
            keyword.lower() in
                h["prediction"].lower() or
            keyword.lower() in
                h["risk_level"].lower()):
            results.append(h)
    return results

# ─────────────────────────────────────────
# COMPARE PATIENT SCANS (Feature 10)
# ─────────────────────────────────────────
def compare_patient_scans(patient_name):
    records = get_patient_history(patient_name)

    if len(records) < 2:
        return None, "Need at least 2 scans to compare"

    latest   = records[-1]
    previous = records[-2]

    conf_change = (
        latest["confidence"] -
        previous["confidence"]
    )

    if latest["prediction"] == "notumor":
        progress = "✅ Tumor Resolved!"
        color    = "#00C851"
    elif conf_change < -5:
        progress = "✅ Improving — Confidence decreasing"
        color    = "#00C851"
    elif conf_change > 5:
        progress = "❌ Worsening — Confidence increasing"
        color    = "#FF0000"
    else:
        progress = "➡️ Stable — No significant change"
        color    = "#FFD700"

    comparison = {
        "patient_name":     patient_name,
        "previous_scan":    previous,
        "latest_scan":      latest,
        "confidence_change": round(conf_change, 2),
        "progress":         progress,
        "color":            color,
        "total_scans":      len(records)
    }

    return comparison, "Success"

if __name__ == "__main__":
    # Test
    save_prediction(
        patient_name = "John Doe",
        prediction   = "glioma",
        confidence   = 95.0,
        risk_level   = "CRITICAL",
        model_used   = "CNN",
        doctor_name  = "Dr. Smith",
        tumor_size   = "Large >4cm",
        stage        = "Grade IV Malignant",
        icd10_code   = "C71.9",
        notes        = "Urgent surgery required"
    )

    summary = get_summary()
    print("\n📊 History Summary:")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    history = load_history()
    print(f"\n📜 Total Records: {len(history)}")
    print(f"  Latest: {history[-1]}")