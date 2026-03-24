# NeuroDetect - emergency_alert.py
# Feature 25: Emergency Alert System

from datetime import datetime
import json
import os

ALERTS_FILE = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    ),
    "history",
    "emergency_alerts.json"
)

EMERGENCY_CRITERIA = {
    "glioma": {
        "is_emergency":  True,
        "alert_level":   "CRITICAL",
        "response_time": "Within 24 hours",
        "department":    "Neurosurgery + Oncology",
        "actions": [
            "🚨 Alert neurosurgery team immediately",
            "📋 Schedule emergency MRI with contrast",
            "💊 Start dexamethasone if symptomatic",
            "📞 Contact patient family",
            "🏥 Consider immediate hospitalization"
        ]
    },
    "meningioma": {
        "is_emergency":  False,
        "alert_level":   "HIGH",
        "response_time": "Within 48-72 hours",
        "department":    "Neurosurgery",
        "actions": [
            "⚠️ Schedule neurosurgery consultation",
            "📋 Order contrast MRI",
            "👁️ Visual field test required",
            "📊 Monitor neurological status",
            "💊 Pain management if needed"
        ]
    },
    "pituitary": {
        "is_emergency":  False,
        "alert_level":   "HIGH",
        "response_time": "Within 48 hours",
        "department":    "Endocrinology + Neurosurgery",
        "actions": [
            "⚠️ Endocrinology referral urgent",
            "🩸 Order hormone panel tests",
            "👁️ Visual field assessment",
            "📋 Pituitary MRI protocol",
            "💊 Hormone replacement evaluation"
        ]
    },
    "notumor": {
        "is_emergency":  False,
        "alert_level":   "NONE",
        "response_time": "Routine",
        "department":    "General Neurology",
        "actions": [
            "✅ No emergency action needed",
            "📋 Routine follow-up in 6 months",
            "📊 Monitor for new symptoms",
            "💊 Continue current medications",
            "🏃 Encourage healthy lifestyle"
        ]
    }
}

def generate_alert(
    patient_name,
    prediction,
    confidence,
    doctor_name,
    patient_mrn = "WALK-IN"
):
    criteria  = EMERGENCY_CRITERIA.get(
        prediction,
        EMERGENCY_CRITERIA["notumor"]
    )

    alert = {
        "id":            len(load_alerts()) + 1,
        "timestamp":     datetime.now().strftime(
                             "%Y-%m-%d %H:%M:%S"
                         ),
        "patient_name":  patient_name,
        "patient_mrn":   patient_mrn,
        "prediction":    prediction,
        "confidence":    confidence,
        "doctor_name":   doctor_name,
        "alert_level":   criteria["alert_level"],
        "is_emergency":  criteria["is_emergency"],
        "response_time": criteria["response_time"],
        "department":    criteria["department"],
        "actions":       criteria["actions"],
        "status":        "ACTIVE"
    }

    # Save alert
    alerts = load_alerts()
    alerts.append(alert)
    save_alerts(alerts)

    return alert

def load_alerts():
    try:
        os.makedirs(
            os.path.dirname(ALERTS_FILE),
            exist_ok=True
        )
        if not os.path.exists(ALERTS_FILE):
            return []
        with open(ALERTS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_alerts(alerts):
    try:
        os.makedirs(
            os.path.dirname(ALERTS_FILE),
            exist_ok=True
        )
        with open(ALERTS_FILE, "w") as f:
            json.dump(alerts, f, indent=4)
    except:
        pass

def get_active_alerts():
    return [
        a for a in load_alerts()
        if a.get("status") == "ACTIVE"
    ]

def get_critical_alerts():
    return [
        a for a in load_alerts()
        if a.get("alert_level") == "CRITICAL"
    ]

def dismiss_alert(alert_id):
    alerts = load_alerts()
    for a in alerts:
        if a["id"] == alert_id:
            a["status"] = "DISMISSED"
    save_alerts(alerts)
