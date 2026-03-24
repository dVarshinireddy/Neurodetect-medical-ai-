# NeuroDetect - treatment_timeline.py
# Feature 26: Treatment Timeline

TIMELINES = {
    "glioma": [
        {
            "week":    "Week 1-2",
            "phase":   "Diagnosis",
            "color":   "#E53E3E",
            "tasks": [
                "Complete MRI with contrast",
                "Biopsy procedure",
                "Pathology results",
                "Multidisciplinary team meeting"
            ]
        },
        {
            "week":    "Week 3-4",
            "phase":   "Surgery",
            "color":   "#DD6B20",
            "tasks": [
                "Pre-surgical assessment",
                "Craniotomy or tumor resection",
                "Post-op ICU monitoring",
                "Recovery and stabilization"
            ]
        },
        {
            "week":    "Week 5-10",
            "phase":   "Radiation",
            "color":   "#D69E2E",
            "tasks": [
                "Radiation planning CT",
                "30 sessions radiotherapy",
                "Concurrent Temozolomide",
                "Weekly blood counts"
            ]
        },
        {
            "week":    "Month 3-8",
            "phase":   "Chemotherapy",
            "color":   "#2E86C1",
            "tasks": [
                "6 cycles Temozolomide",
                "Monthly MRI monitoring",
                "Neurological assessments",
                "Quality of life support"
            ]
        },
        {
            "week":    "Month 9+",
            "phase":   "Monitoring",
            "color":   "#38A169",
            "tasks": [
                "MRI every 3 months",
                "Neuropsychological testing",
                "Rehabilitation therapy",
                "Long term follow up"
            ]
        }
    ],
    "meningioma": [
        {
            "week":    "Week 1-2",
            "phase":   "Assessment",
            "color":   "#DD6B20",
            "tasks": [
                "Full neurological exam",
                "MRI with gadolinium",
                "Visual field testing",
                "Surgical risk assessment"
            ]
        },
        {
            "week":    "Week 3-4",
            "phase":   "Decision",
            "color":   "#D69E2E",
            "tasks": [
                "MDT meeting",
                "Watch and wait vs surgery",
                "Stereotactic radiosurgery eval",
                "Patient counseling"
            ]
        },
        {
            "week":    "Week 5-8",
            "phase":   "Treatment",
            "color":   "#2E86C1",
            "tasks": [
                "Surgery if indicated",
                "Gamma knife radiosurgery",
                "Post treatment monitoring",
                "Steroid management"
            ]
        },
        {
            "week":    "Month 3+",
            "phase":   "Follow Up",
            "color":   "#38A169",
            "tasks": [
                "MRI every 6 months",
                "Neurological monitoring",
                "Seizure management",
                "Annual reviews"
            ]
        }
    ],
    "pituitary": [
        {
            "week":    "Week 1",
            "phase":   "Diagnosis",
            "color":   "#D69E2E",
            "tasks": [
                "Hormone panel blood tests",
                "Pituitary MRI protocol",
                "Visual field perimetry",
                "Ophthalmology referral"
            ]
        },
        {
            "week":    "Week 2-3",
            "phase":   "Medical Treatment",
            "color":   "#2E86C1",
            "tasks": [
                "Start dopamine agonists",
                "Hormone replacement",
                "Endocrinology follow up",
                "Response assessment"
            ]
        },
        {
            "week":    "Week 4-8",
            "phase":   "Surgery",
            "color":   "#DD6B20",
            "tasks": [
                "Trans-sphenoidal surgery",
                "Post-op hormone check",
                "Visual field retest",
                "Recovery monitoring"
            ]
        },
        {
            "week":    "Month 3+",
            "phase":   "Follow Up",
            "color":   "#38A169",
            "tasks": [
                "MRI every 6 months",
                "Hormone monitoring",
                "Medication adjustment",
                "Quality of life review"
            ]
        }
    ],
    "notumor": [
        {
            "week":    "Now",
            "phase":   "Reassurance",
            "color":   "#38A169",
            "tasks": [
                "Confirm normal findings",
                "Patient reassurance",
                "Symptom management",
                "Lifestyle advice"
            ]
        },
        {
            "week":    "Month 6",
            "phase":   "Follow Up",
            "color":   "#2E86C1",
            "tasks": [
                "Routine MRI if needed",
                "Neurological check",
                "Monitor new symptoms",
                "General health review"
            ]
        },
        {
            "week":    "Year 1+",
            "phase":   "Monitoring",
            "color":   "#1B4F72",
            "tasks": [
                "Annual health checkup",
                "MRI only if symptomatic",
                "Continue healthy habits",
                "Report new symptoms"
            ]
        }
    ]
}

def get_treatment_timeline(prediction):
    return TIMELINES.get(
        prediction,
        TIMELINES["notumor"]
    )

def get_current_phase(prediction,
                      weeks_since_diagnosis=0):
    timeline = get_treatment_timeline(
        prediction
    )
    if weeks_since_diagnosis < 2:
        return timeline[0]
    elif weeks_since_diagnosis < 4:
        return timeline[1] \
            if len(timeline) > 1 \
            else timeline[0]
    else:
        return timeline[-1]