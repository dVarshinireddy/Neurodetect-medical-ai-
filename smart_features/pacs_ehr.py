import json
import os
from datetime import datetime
FHIR_BASE = "https://neurodetect.fhir.org/R4"
def create_fhir_patient(
    mrn, name, age,
    gender="unknown",
    phone="",
    address=""
):
    dob_year = datetime.now().year - int(age)
    return {
        "resourceType": "Patient",
        "id":            mrn,
        "meta": {
            "versionId":   "1",
            "lastUpdated": datetime.now()
                           .isoformat(),
            "source":      "NeuroDetect-AI-v3"
        },
        "identifier": [{
            "use":    "official",
            "system": "NeuroDetect/MRN",
            "value":  mrn
        }],
        "active": True,
        "name": [{
            "use":    "official",
            "text":   name,
            "family": name.split()[-1]
                      if " " in name
                      else name,
            "given":  [name.split()[0]]
        }],
        "gender":    gender,
        "birthDate": f"{dob_year}-01-01",
        "telecom": [{
            "system": "phone",
            "value":  phone,
            "use":    "mobile"
        }] if phone else [],
        "address": [{
            "text": address
        }] if address else []
    }

def create_fhir_observation(
    patient_mrn, prediction,
    confidence, doctor_name,
    obs_id=None
):
    if obs_id is None:
        obs_id = "obs-" + patient_mrn + \
            "-" + datetime.now()\
            .strftime('%Y%m%d%H%M%S')

    loinc_map = {
        "glioma":     ("C71.9",  "Glioma"),
        "meningioma": ("D32.9",  "Meningioma"),
        "pituitary":  ("D35.2",  "Pituitary Adenoma"),
        "notumor":    ("Z03.89", "No Tumor Detected")
    }
    icd10, display = loinc_map.get(
        prediction,
        ("Z03.89", "Unknown")
    )

    status = "final" \
        if confidence >= 80 \
        else "preliminary"

    interpretation = "POS" \
        if prediction != "notumor" \
        else "NEG"

    return {
        "resourceType": "Observation",
        "id":            obs_id,
        "meta": {
            "lastUpdated": datetime.now()
                           .isoformat(),
            "source":      "NeuroDetect-AI"
        },
        "status": status,
        "category": [{
            "coding": [{
                "system":  "http://terminology"
                           ".hl7.org/CodeSystem/"
                           "observation-category",
                "code":    "imaging",
                "display": "Imaging"
            }]
        }],
        "code": {
            "coding": [{
                "system":  "http://loinc.org",
                "code":    "24627-2",
                "display": "MRI Brain"
            }]
        },
        "subject": {
            "reference": f"Patient/{patient_mrn}",
            "display":   patient_mrn
        },
        "effectiveDateTime": datetime.now()
                             .isoformat(),
        "issued": datetime.now().isoformat(),
        "performer": [{
            "display": doctor_name
        }],
        "valueCodeableConcept": {
            "coding": [{
                "system":  "http://hl7.org/fhir/"
                           "sid/icd-10",
                "code":    icd10,
                "display": display
            }],
            "text": (
                f"{display} detected with "
                f"{confidence:.1f}% AI confidence"
            )
        },
        "interpretation": [{
            "coding": [{
                "system":  "http://terminology"
                           ".hl7.org/CodeSystem/"
                           "v3-ObservationInterpretation",
                "code":    interpretation
            }]
        }],
        "component": [{
            "code": {
                "text": "AI Confidence Score"
            },
            "valueQuantity": {
                "value":  round(confidence, 2),
                "unit":   "%",
                "system": "http://unitsofmeasure.org",
                "code":   "%"
            }
        }]
    }

def create_fhir_diagnostic_report(
    patient_mrn, prediction,
    confidence, doctor_name,
    obs_id
):
    return {
        "resourceType": "DiagnosticReport",
        "id":            f"dr-{patient_mrn}",
        "meta": {
            "lastUpdated": datetime.now()
                           .isoformat()
        },
        "status":   "final",
        "category": [{
            "coding": [{
                "system":  "http://loinc.org",
                "code":    "RAD",
                "display": "Radiology"
            }]
        }],
        "code": {
            "coding": [{
                "system":  "http://loinc.org",
                "code":    "24627-2",
                "display": "MRI Brain"
            }],
            "text": "NeuroDetect AI Brain MRI Analysis"
        },
        "subject": {
            "reference": f"Patient/{patient_mrn}"
        },
        "effectiveDateTime": datetime.now()
                             .isoformat(),
        "issued": datetime.now().isoformat(),
        "performer": [{
            "display": doctor_name
        }],
        "result": [{
            "reference": f"Observation/{obs_id}"
        }],
        "conclusion": (
            f"AI Analysis Result: "
            f"{prediction.upper()} "
            f"({confidence:.1f}% confidence). "
            f"Generated by NeuroDetect "
            f"Medical AI System v3.0. "
            f"Clinical correlation required."
        ),
        "presentedForm": [{
            "contentType": "application/json",
            "title":       "NeuroDetect Report"
        }]
    }

def export_hl7_bundle(
    patient, observation,
    diagnostic_report
):
    bundle_id = "bundle-" + \
        datetime.now().strftime('%Y%m%d')
    return {
        "resourceType": "Bundle",
        "id":            bundle_id,
        "type":          "collection",
        "timestamp":     datetime.now()
                         .isoformat(),
        "entry": [
            {
                "resource": patient,
                "request": {
                    "method": "PUT",
                    "url":    f"Patient/"
                              f"{patient['id']}"
                }
            },
            {
                "resource": observation,
                "request": {
                    "method": "POST",
                    "url":    "Observation"
                }
            },
            {
                "resource": diagnostic_report,
                "request": {
                    "method": "POST",
                    "url":    "DiagnosticReport"
                }
            }
        ]
    }

def save_fhir_record(
    patient_mrn, fhir_bundle
):
    path = os.path.join(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        ),
        "history",
        "fhir_records.json"
    )
    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )
    try:
        with open(path, "r") as f:
            records = json.load(f)
    except:
        records = {}

    records[patient_mrn] = {
        "timestamp": datetime.now()
                     .isoformat(),
        "bundle":    fhir_bundle
    }

    with open(path, "w") as f:
        json.dump(records, f, indent=2)

def get_pacs_status():
    return {
        "standard":     "HL7 FHIR R4",
        "dicom_support":"DICOM 3.0",
        "integration":  "REST API",
        "endpoints": [
            "GET  /Patient/{id}",
            "POST /Observation",
            "POST /DiagnosticReport",
            "GET  /Bundle"
        ],
        "compliance":   "IHE Radiology Profiles"
    }
