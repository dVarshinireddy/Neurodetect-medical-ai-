import json, os, random, string
from datetime import datetime
PATIENTS_FILE = "history/patients.json"
def generate_mrn():
    nums = ''.join(random.choices(string.digits, k=8))
    return f"MRN-{nums}"
def load_patients():
    if not os.path.exists(PATIENTS_FILE):
        return []
    try:
        with open(PATIENTS_FILE) as f:
            return json.load(f)
    except:
        return []
def save_patient(first_name, last_name,
    date_of_birth, gender, blood_group,
    phone, email="", address="",
    emergency_contact_name="",
    emergency_contact_phone="",
    insurance_id="", allergies="",
    medical_history="", referring_doctor=""):

    os.makedirs("history", exist_ok=True)
    patients  = load_patients()
    full_name = f"{first_name} {last_name}"

    existing = [p for p in patients
                if p["full_name"].lower()
                == full_name.lower()]
    if existing:
        return existing[0]
    try:
        dob = datetime.strptime(date_of_birth,"%Y-%m-%d")
        age = (datetime.now()-dob).days // 365
    except:
        age = 0
    patient = {
        "mrn":                    generate_mrn(),
        "first_name":             first_name,
        "last_name":              last_name,
        "full_name":              full_name,
        "date_of_birth":          date_of_birth,
        "age":                    age,
        "gender":                 gender,
        "blood_group":            blood_group,
        "phone":                  phone,
        "email":                  email,
        "address":                address,
        "emergency_contact_name": emergency_contact_name,
        "emergency_contact_phone":emergency_contact_phone,
        "insurance_id":           insurance_id,
        "allergies":              allergies,
        "medical_history":        medical_history,
        "referring_doctor":       referring_doctor,
        "registration_date":      datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "scan_count":             0
    }

    patients.append(patient)
    with open(PATIENTS_FILE,"w") as f:
        json.dump(patients, f, indent=4)
    return patient
def get_patient_by_mrn(mrn):
    for p in load_patients():
        if p["mrn"] == mrn:
            return p
    return None
def search_patients(keyword):
    results = []
    for p in load_patients():
        if (keyword.lower() in p["full_name"].lower()
            or keyword in p["mrn"]
            or keyword in p.get("phone","")):
            results.append(p)
    return results
def get_all_patients():
    return load_patients()
def update_scan_count(mrn):
    patients = load_patients()
    for p in patients:
        if p["mrn"] == mrn:
            p["scan_count"] = p.get("scan_count",0)+1
            p["last_scan"]  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            break
    with open(PATIENTS_FILE,"w") as f:
        json.dump(patients, f, indent=4)
