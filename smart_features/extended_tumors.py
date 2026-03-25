TUMOR_DB = {
    # ── ORIGINAL 4 ──
    "glioma": {
        "full_name":    "Glioma",
        "icd10":        "C71.9",
        "who_grade":    "Grade III-IV",
        "malignant":    True,
        "prevalence":   "45% of primary tumors",
        "5yr_survival": "5-15%",
        "color":        "#E53E3E",
        "icon":         "🔴",
        "subtypes": [
            "Glioblastoma (GBM)",
            "Anaplastic Astrocytoma",
            "Diffuse Astrocytoma",
            "Oligodendroglioma"
        ],
        "symptoms": [
            "Severe progressive headaches",
            "Seizures",
            "Cognitive decline",
            "Personality changes",
            "Motor weakness"
        ],
        "treatment": [
            "Maximal safe resection",
            "Radiotherapy 60Gy/30fx",
            "Temozolomide chemotherapy",
            "Tumor Treating Fields (TTF)",
            "Bevacizumab for recurrence"
        ],
        "urgency": "IMMEDIATE",
        "referral": "Neurosurgery + Oncology"
    },
    "meningioma": {
        "full_name":    "Meningioma",
        "icd10":        "D32.9",
        "who_grade":    "Grade I-II",
        "malignant":    False,
        "prevalence":   "36% of brain tumors",
        "5yr_survival": "70-80%",
        "color":        "#DD6B20",
        "icon":         "🟠",
        "subtypes": [
            "Meningothelial",
            "Fibrous",
            "Transitional",
            "Atypical Grade II"
        ],
        "symptoms": [
            "Headaches",
            "Vision changes",
            "Hearing loss",
            "Memory problems",
            "Weakness in limbs"
        ],
        "treatment": [
            "Active surveillance if small",
            "Surgical resection",
            "Stereotactic radiosurgery",
            "Fractionated radiotherapy",
            "Annual MRI monitoring"
        ],
        "urgency": "MODERATE",
        "referral": "Neurosurgery"
    },
    "pituitary": {
        "full_name":    "Pituitary Adenoma",
        "icd10":        "D35.2",
        "who_grade":    "Grade I",
        "malignant":    False,
        "prevalence":   "15% of brain tumors",
        "5yr_survival": "95%+",
        "color":        "#2E86C1",
        "icon":         "🔵",
        "subtypes": [
            "Microadenoma (<10mm)",
            "Macroadenoma (>10mm)",
            "Prolactinoma",
            "Cushing adenoma"
        ],
        "symptoms": [
            "Vision field defects",
            "Hormonal imbalance",
            "Headaches",
            "Galactorrhea",
            "Acromegaly signs"
        ],
        "treatment": [
            "Dopamine agonists first",
            "Trans-sphenoidal surgery",
            "Radiation therapy",
            "Hormone replacement",
            "Endocrine monitoring"
        ],
        "urgency": "MODERATE",
        "referral": "Endocrinology + Neurosurgery"
    },
    "notumor": {
        "full_name":    "No Tumor",
        "icd10":        "Z03.89",
        "who_grade":    "N/A",
        "malignant":    False,
        "prevalence":   "Normal finding",
        "5yr_survival": "Normal",
        "color":        "#38A169",
        "icon":         "✅",
        "subtypes":     ["Normal brain tissue"],
        "symptoms":     ["None detected"],
        "treatment": [
            "No treatment required",
            "Routine annual checkup",
            "Monitor for new symptoms",
            "Healthy lifestyle advice"
        ],
        "urgency": "ROUTINE",
        "referral": "General neurology if symptomatic"
    },

    # ── NEW 4 TUMOR TYPES ──
    "lymphoma": {
        "full_name":    "Primary CNS Lymphoma",
        "icd10":        "C85.20",
        "who_grade":    "Grade IV",
        "malignant":    True,
        "prevalence":   "3% of brain tumors",
        "5yr_survival": "20-45%",
        "color":        "#6C3483",
        "icon":         "🟣",
        "subtypes": [
            "Diffuse Large B-cell",
            "T-cell lymphoma",
            "Burkitt lymphoma",
            "MALT lymphoma"
        ],
        "symptoms": [
            "Cognitive impairment",
            "Focal neurological deficits",
            "Headaches",
            "Seizures",
            "Personality changes"
        ],
        "treatment": [
            "High-dose Methotrexate",
            "Rituximab immunotherapy",
            "Whole brain radiotherapy",
            "Autologous stem cell transplant",
            "Corticosteroids"
        ],
        "urgency": "URGENT",
        "referral": "Neuro-Oncology + Hematology"
    },
    "metastatic": {
        "full_name":    "Brain Metastasis",
        "icd10":        "C79.31",
        "who_grade":    "Grade IV",
        "malignant":    True,
        "prevalence":   "20-40% of cancer patients",
        "5yr_survival": "8-12%",
        "color":        "#1A5276",
        "icon":         "🔷",
        "subtypes": [
            "Lung cancer metastasis",
            "Breast cancer metastasis",
            "Melanoma metastasis",
            "Renal cell carcinoma"
        ],
        "symptoms": [
            "Headaches (morning)",
            "Nausea and vomiting",
            "Cognitive changes",
            "Focal weakness",
            "Seizures"
        ],
        "treatment": [
            "Stereotactic radiosurgery",
            "Whole brain radiotherapy",
            "Surgery for single lesion",
            "Targeted systemic therapy",
            "Immunotherapy (PD-L1)"
        ],
        "urgency": "URGENT",
        "referral": "Neuro-Oncology + Primary Oncology"
    },
    "acoustic_neuroma": {
        "full_name":    "Acoustic Neuroma (Vestibular Schwannoma)",
        "icd10":        "D33.3",
        "who_grade":    "Grade I",
        "malignant":    False,
        "prevalence":   "8% of brain tumors",
        "5yr_survival": "95%+",
        "color":        "#117A65",
        "icon":         "🟢",
        "subtypes": [
            "Unilateral schwannoma",
            "Bilateral (NF2 associated)",
            "Intracanalicular",
            "Large vestibular"
        ],
        "symptoms": [
            "Unilateral hearing loss",
            "Tinnitus",
            "Balance problems",
            "Facial numbness",
            "Dizziness/vertigo"
        ],
        "treatment": [
            "Active surveillance (small)",
            "Gamma Knife radiosurgery",
            "Microsurgical resection",
            "Fractionated radiotherapy",
            "Hearing rehabilitation"
        ],
        "urgency": "LOW",
        "referral": "Neurotology + Neurosurgery"
    },
    "craniopharyngioma": {
        "full_name":    "Craniopharyngioma",
        "icd10":        "D44.4",
        "who_grade":    "Grade I",
        "malignant":    False,
        "prevalence":   "2-5% of brain tumors",
        "5yr_survival": "85%+",
        "color":        "#784212",
        "icon":         "🟤",
        "subtypes": [
            "Adamantinomatous (children)",
            "Papillary (adults)",
            "Mixed type",
            "Recurrent"
        ],
        "symptoms": [
            "Visual field defects",
            "Pituitary dysfunction",
            "Diabetes insipidus",
            "Growth failure (children)",
            "Obesity"
        ],
        "treatment": [
            "Surgical resection",
            "Intracavitary chemotherapy",
            "Radiotherapy",
            "Hormone replacement therapy",
            "Long-term monitoring"
        ],
        "urgency": "MODERATE",
        "referral": "Neurosurgery + Pediatric Endocrinology"
    }
}

def get_info(tumor_type):
    return TUMOR_DB.get(
        tumor_type,
        TUMOR_DB["notumor"]
    )
def get_all():
    return list(TUMOR_DB.keys())
def get_malignant():
    return [
        k for k,v in TUMOR_DB.items()
        if v["malignant"]
    ]
def get_benign():
    return [
        k for k,v in TUMOR_DB.items()
        if not v["malignant"]
    ]
def get_by_urgency(urgency):
    return [
        k for k,v in TUMOR_DB.items()
        if v["urgency"] == urgency
    ]

def get_icd10(tumor_type):
    return TUMOR_DB.get(
        tumor_type, {}
    ).get("icd10", "Z03.89")

def get_survival(tumor_type):
    return TUMOR_DB.get(
        tumor_type, {}
    ).get("5yr_survival", "Unknown")
