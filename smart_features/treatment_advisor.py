TREATMENT_DB = {
    "glioma": {
        "full_name":    "Glioma (Malignant Brain Tumor)",
        "icd10_code":   "C71.9",
        "description":  (
            "Glioma is a malignant tumor originating "
            "from glial cells in the brain or spinal "
            "cord. It is the most aggressive primary "
            "brain tumor with high mortality rate."
        ),
        "who_grade":    "Grade III-IV",
        "first_line": [
            "Maximum safe surgical resection",
            "Temozolomide + Radiation (TMZ/RT)",
            "Adjuvant Temozolomide 6 cycles",
            "MGMT methylation testing"
        ],
        "second_line": [
            "Bevacizumab (Avastin) 10mg/kg IV",
            "Lomustine (CCNU) 110mg/m2",
            "Clinical trial enrollment",
            "Tumor treating fields (TTFields)"
        ],
        "radiation": (
            "60 Gy in 30 fractions — IMRT preferred"
        ),
        "drugs": [
            "Temozolomide (TMZ) 75mg/m2/day",
            "Bevacizumab 10mg/kg every 2 weeks",
            "Lomustine 110mg/m2 every 6 weeks",
            "Dexamethasone for edema"
        ],
        "specialists": [
            "Neurosurgeon",
            "Neuro-oncologist",
            "Radiation Oncologist",
            "Neurologist"
        ],
        "follow_up": [
            "MRI every 2-3 months",
            "Neurological assessment monthly",
            "Blood count weekly during TMZ",
            "Steroid taper as tolerated"
        ],
        "survival": {
            "grade_3": "2-3 years median survival",
            "grade_4": "14-16 months median survival",
            "5_year":  "5.6% for GBM Grade IV"
        },
        "urgency":      "CODE RED — Within 24-48 hours",
        "urgency_color": "#FF0000",
        "clinical_trials": (
            "Check clinicaltrials.gov for "
            "IDH mutation targeted therapy"
        )
    },

    "meningioma": {
        "full_name":    "Meningioma (Meningeal Tumor)",
        "icd10_code":   "D32.9",
        "description":  (
            "Meningioma arises from the meninges "
            "surrounding the brain and spinal cord. "
            "Most are benign but can cause symptoms "
            "due to pressure on brain tissue."
        ),
        "who_grade":    "Grade I-II (mostly benign)",
        "first_line": [
            "Active surveillance (small Grade I)",
            "Surgical resection (Simpson Grade I-II)",
            "Stereotactic radiosurgery (SRS)",
            "Gamma Knife radiosurgery"
        ],
        "second_line": [
            "Fractionated radiation therapy",
            "Hydroxyurea (recurrent cases)",
            "Somatostatin analogues",
            "Clinical trials"
        ],
        "radiation": (
            "54 Gy in 30 fractions for atypical"
        ),
        "drugs": [
            "Hydroxyurea 20mg/kg/day (recurrent)",
            "Octreotide (somatostatin analogue)",
            "Mifepristone (progesterone receptor)",
            "Dexamethasone for edema"
        ],
        "specialists": [
            "Neurosurgeon",
            "Neurologist",
            "Radiation Oncologist"
        ],
        "follow_up": [
            "MRI every 6 months for 2 years",
            "Annual MRI thereafter",
            "Neurological exam every 6 months",
            "Vision assessment if optic involved"
        ],
        "survival": {
            "grade_1": "90%+ at 10 years",
            "grade_2": "70-80% at 10 years",
            "grade_3": "Less than 60% at 5 years"
        },
        "urgency":      "CODE ORANGE — Within 1 week",
        "urgency_color": "#FF6B00",
        "clinical_trials": (
            "Check clinicaltrials.gov for "
            "anti-progesterone receptor therapy"
        )
    },

    "pituitary": {
        "full_name":    "Pituitary Adenoma",
        "icd10_code":   "D35.2",
        "description":  (
            "Pituitary adenoma is a benign tumor "
            "of the pituitary gland that can affect "
            "hormone production and cause visual "
            "disturbances due to optic nerve pressure."
        ),
        "who_grade":    "Mostly benign adenoma",
        "first_line": [
            "Dopamine agonists (Prolactinoma)",
            "Transsphenoidal surgery",
            "Somatostatin analogues (GH secreting)",
            "Hormone replacement therapy"
        ],
        "second_line": [
            "Stereotactic radiosurgery",
            "Fractionated radiation therapy",
            "Pasireotide for Cushings",
            "Pegvisomant for acromegaly"
        ],
        "radiation": (
            "45-54 Gy fractionated or SRS 12-25 Gy"
        ),
        "drugs": [
            "Cabergoline 0.5-2mg twice weekly",
            "Bromocriptine 2.5-15mg daily",
            "Octreotide LAR 20-30mg monthly",
            "Lanreotide 60-120mg monthly"
        ],
        "specialists": [
            "Endocrinologist",
            "Neurosurgeon",
            "Ophthalmologist",
            "Neurologist"
        ],
        "follow_up": [
            "MRI every 6-12 months",
            "Hormone levels every 3 months",
            "Visual field testing every 6 months",
            "Bone density annually"
        ],
        "survival": {
            "general":  "Excellent prognosis",
            "benign":   "Normal life expectancy",
            "5_year":   "Greater than 95%"
        },
        "urgency":      "CODE YELLOW — Within 1-2 weeks",
        "urgency_color": "#FFD700",
        "clinical_trials": (
            "Check clinicaltrials.gov for "
            "novel somatostatin receptor ligands"
        )
    },

    "notumor": {
        "full_name":    "No Tumor Detected",
        "icd10_code":   "Z03.89",
        "description":  (
            "No evidence of brain tumor detected "
            "in the MRI scan. Brain appears normal. "
            "Regular screening recommended for "
            "high risk individuals."
        ),
        "who_grade":    "N/A",
        "first_line": [
            "No treatment required",
            "Annual MRI screening",
            "Healthy lifestyle maintenance",
            "Regular neurological checkup"
        ],
        "second_line": [],
        "radiation":    "Not applicable",
        "drugs":        ["No medication required"],
        "specialists":  ["General Practitioner"],
        "follow_up": [
            "Annual MRI screening",
            "Regular health checkup",
            "Report new symptoms immediately",
            "Maintain healthy lifestyle"
        ],
        "survival": {
            "general": "Normal life expectancy",
            "5_year":  "Normal"
        },
        "urgency":      "CODE GREEN — Annual checkup",
        "urgency_color": "#00C851",
        "clinical_trials": "Not applicable"
    }
}
# GET TREATMENT INFO
def get_treatment_info(prediction):
    return TREATMENT_DB.get(
        prediction,
        TREATMENT_DB["notumor"]
    )
# GET FORMATTED REPORT
def get_treatment_report(prediction, confidence):
    info = get_treatment_info(prediction)

    report = f"""
╔══════════════════════════════════════╗
║     NEURODETECT TREATMENT ADVISORY   ║
╚══════════════════════════════════════╝

Diagnosis    : {info['full_name']}
ICD-10 Code  : {info['icd10_code']}
WHO Grade    : {info['who_grade']}
AI Confidence: {confidence:.1f}%
Urgency      : {info['urgency']}

DESCRIPTION:
{info['description']}

FIRST LINE TREATMENT:
"""
    for t in info['first_line']:
        report += f"  → {t}\n"

    if info['second_line']:
        report += "\nSECOND LINE TREATMENT:\n"
        for t in info['second_line']:
            report += f"  → {t}\n"

    report += f"\nRADIATION: {info['radiation']}\n"

    report += "\nKEY MEDICATIONS:\n"
    for d in info['drugs']:
        report += f"  → {d}\n"

    report += "\nSPECIALISTS:\n"
    for s in info['specialists']:
        report += f"  → {s}\n"

    report += "\nFOLLOW UP SCHEDULE:\n"
    for f in info['follow_up']:
        report += f"  → {f}\n"

    report += "\nSURVIVAL STATISTICS:\n"
    for k, v in info['survival'].items():
        report += f"  → {k}: {v}\n"

    report += f"""
CLINICAL TRIALS:
  → {info['clinical_trials']}

⚠️ DISCLAIMER:
This advisory is AI generated and based on
NCCN Guidelines. Final treatment decisions
must be made by qualified medical professionals.
"""
    return report

if __name__ == "__main__":
    # Test
    info   = get_treatment_info("glioma")
    report = get_treatment_report("glioma", 95.0)
    print(report)
