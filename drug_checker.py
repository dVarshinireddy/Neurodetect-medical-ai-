# NeuroDetect - drug_checker.py

TUMOR_DRUGS = {
    "glioma":     ["Temozolomide","Bevacizumab","Lomustine","Dexamethasone","Levetiracetam"],
    "meningioma": ["Hydroxyurea","Octreotide","Dexamethasone","Mifepristone"],
    "pituitary":  ["Cabergoline","Bromocriptine","Octreotide LAR","Pegvisomant","Dexamethasone"]
}

INTERACTIONS = {
    ("Temozolomide","Warfarin"):      {"severity":"MAJOR",    "effect":"Increased bleeding risk",       "recommendation":"Avoid or monitor INR closely"},
    ("Temozolomide","Phenytoin"):     {"severity":"MODERATE", "effect":"Reduced TMZ effectiveness",     "recommendation":"Monitor drug levels regularly"},
    ("Bevacizumab","Aspirin"):        {"severity":"MODERATE", "effect":"Increased bleeding risk",       "recommendation":"Use with caution"},
    ("Dexamethasone","Insulin"):      {"severity":"MAJOR",    "effect":"Increased blood sugar",          "recommendation":"Monitor blood glucose frequently"},
    ("Dexamethasone","Ibuprofen"):    {"severity":"MODERATE", "effect":"Increased GI bleeding risk",    "recommendation":"Avoid NSAIDs, use Paracetamol"},
    ("Cabergoline","Antipsychotics"): {"severity":"MAJOR",    "effect":"Reduced effectiveness",         "recommendation":"Avoid combination if possible"},
    ("Lomustine","Alcohol"):          {"severity":"MAJOR",    "effect":"Severe liver damage",           "recommendation":"Strictly avoid alcohol"},
    ("Octreotide","Cyclosporine"):    {"severity":"MODERATE", "effect":"Reduced cyclosporine levels",   "recommendation":"Monitor cyclosporine levels"},
}

def check_drug_interactions(tumor_drugs, patient_drugs):
    found = []
    for td in tumor_drugs:
        for pd in patient_drugs:
            inter = INTERACTIONS.get((td,pd)) \
                 or INTERACTIONS.get((pd,td))
            if inter:
                found.append({
                    "drug1":          td,
                    "drug2":          pd,
                    "severity":       inter["severity"],
                    "effect":         inter["effect"],
                    "recommendation": inter["recommendation"]
                })
    return found

def get_drug_report(tumor_type, patient_drugs):
    tumor_drugs  = TUMOR_DRUGS.get(tumor_type,[])
    interactions = check_drug_interactions(
        tumor_drugs, patient_drugs
    )
    major    = [i for i in interactions if i["severity"]=="MAJOR"]
    moderate = [i for i in interactions if i["severity"]=="MODERATE"]
    return {
        "tumor_type":            tumor_type,
        "tumor_drugs":           tumor_drugs,
        "patient_drugs":         patient_drugs,
        "total_interactions":    len(interactions),
        "major_interactions":    len(major),
        "moderate_interactions": len(moderate),
        "interactions":          interactions,
        "is_safe":               len(major)==0,
        "safety_status":         "SAFE ✅" if len(major)==0 else "DANGER 🚨"
    }
