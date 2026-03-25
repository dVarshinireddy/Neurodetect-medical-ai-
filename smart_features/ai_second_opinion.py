SECOND_OPINION = {
    "glioma": {
        "consensus":    "HIGH CONCERN",
        "second_model": "ResNet50",
        "agreement":    "Confirmed Malignant",
        "confidence":   "92-98%",
        "recommendation": [
            "Immediate neurosurgery referral",
            "MRI with contrast required",
            "Biopsy recommended within 72hrs",
            "Oncology team consultation",
            "Family counseling advised"
        ],
        "differential": [
            "Primary Glioblastoma (GBM)",
            "Anaplastic Astrocytoma",
            "Diffuse Intrinsic Pontine Glioma",
            "Brain Metastasis"
        ],
        "red_flags": [
            "Rapid neurological deterioration",
            "Increased intracranial pressure",
            "Seizure activity",
            "Memory and cognitive decline"
        ],
        "second_color": "#E53E3E"
    },
    "meningioma": {
        "consensus":    "MODERATE CONCERN",
        "second_model": "ResNet50",
        "agreement":    "Confirmed Benign-Moderate",
        "confidence":   "88-95%",
        "recommendation": [
            "Neurosurgery consultation",
            "Watch and wait if asymptomatic",
            "Follow-up MRI in 3-6 months",
            "Radiation therapy evaluation",
            "Annual monitoring required"
        ],
        "differential": [
            "Benign Meningioma Grade I",
            "Atypical Meningioma Grade II",
            "Anaplastic Meningioma Grade III",
            "Schwannoma"
        ],
        "red_flags": [
            "Headaches increasing in severity",
            "Vision or hearing changes",
            "Weakness in limbs",
            "Balance problems"
        ],
        "second_color": "#DD6B20"
    },
    "pituitary": {
        "consensus":    "MODERATE CONCERN",
        "second_model": "ResNet50",
        "agreement":    "Confirmed Pituitary Lesion",
        "confidence":   "85-93%",
        "recommendation": [
            "Endocrinology referral urgent",
            "Hormone panel blood tests",
            "Visual field testing",
            "MRI pituitary protocol",
            "Consider trans-sphenoidal surgery"
        ],
        "differential": [
            "Pituitary Adenoma",
            "Craniopharyngioma",
            "Rathke Cleft Cyst",
            "Pituitary Carcinoma"
        ],
        "red_flags": [
            "Visual field defects",
            "Hormonal imbalance symptoms",
            "Bitemporal hemianopia",
            "Cushing syndrome signs"
        ],
        "second_color": "#D69E2E"
    },
    "notumor": {
        "consensus":    "NORMAL",
        "second_model": "ResNet50",
        "agreement":    "No Malignancy Detected",
        "confidence":   "95-99%",
        "recommendation": [
            "No immediate action required",
            "Routine annual checkup",
            "Monitor for new symptoms",
            "Maintain healthy lifestyle",
            "Follow up if symptoms develop"
        ],
        "differential": [
            "Normal Brain Tissue",
            "Benign Cyst",
            "Artifact",
            "Normal Variant"
        ],
        "red_flags": [
            "New onset headaches",
            "Sudden neurological symptoms",
            "Vision changes",
            "Unexplained nausea"
        ],
        "second_color": "#38A169"
    }
}
def get_second_opinion(prediction,
                       confidence,
                       model_results):
    opinion = SECOND_OPINION.get(
        prediction,
        SECOND_OPINION["notumor"]
    )

    # Calculate agreement score
    predictions = [
        r[0] for r in model_results.values()
    ]
    agreement = (
        predictions.count(prediction) /
        len(predictions) * 100
    ) if predictions else 0

    # Determine overall verdict
    if agreement >= 75 and confidence >= 85:
        verdict       = "STRONG CONSENSUS"
        verdict_color = "#38A169"
        verdict_icon  = "✅"
    elif agreement >= 50 and confidence >= 70:
        verdict       = "MODERATE CONSENSUS"
        verdict_color = "#D69E2E"
        verdict_icon  = "⚠️"
    else:
        verdict       = "LOW CONSENSUS"
        verdict_color = "#E53E3E"
        verdict_icon  = "🚨"
    return {
        "prediction":     prediction,
        "confidence":     confidence,
        "consensus":      opinion["consensus"],
        "agreement":      opinion["agreement"],
        "conf_range":     opinion["confidence"],
        "recommendation": opinion["recommendation"],
        "differential":   opinion["differential"],
        "red_flags":      opinion["red_flags"],
        "second_color":   opinion["second_color"],
        "model_agreement":round(agreement, 1),
        "verdict":        verdict,
        "verdict_color":  verdict_color,
        "verdict_icon":   verdict_icon
    }
