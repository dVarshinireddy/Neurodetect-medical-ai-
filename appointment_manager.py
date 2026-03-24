# NeuroDetect - appointment_manager.py
import json, os
from datetime import datetime, timedelta

APPOINTMENTS_FILE = "history/appointments.json"

def load_appointments():
    if not os.path.exists(APPOINTMENTS_FILE):
        return []
    try:
        with open(APPOINTMENTS_FILE) as f:
            return json.load(f)
    except:
        return []

def save_appointment(patient_name,
    doctor_name, date, time,
    appointment_type, notes="",
    priority="NORMAL"):

    os.makedirs("history", exist_ok=True)
    appointments = load_appointments()
    appt = {
        "id":           len(appointments)+1,
        "patient_name": patient_name,
        "doctor_name":  doctor_name,
        "date":         date,
        "time":         time,
        "type":         appointment_type,
        "notes":        notes,
        "priority":     priority,
        "status":       "SCHEDULED",
        "created_at":   datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    appointments.append(appt)
    with open(APPOINTMENTS_FILE,"w") as f:
        json.dump(appointments, f, indent=4)
    return appt

def get_upcoming(days=7):
    today    = datetime.now().date()
    upcoming = []
    for a in load_appointments():
        try:
            appt_date = datetime.strptime(
                a["date"],"%Y-%m-%d"
            ).date()
            if today <= appt_date <= today + timedelta(days=days):
                upcoming.append(a)
        except:
            pass
    return sorted(upcoming,
        key=lambda x:(x["date"],x["time"]))
