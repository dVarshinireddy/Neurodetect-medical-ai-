import json, os, re
from datetime import datetime
HISTORY_FILE = "history/prediction_history.json"
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE) as f:
            return json.load(f)
    except:
        return []
def parse_size(size_label):
    if not size_label or size_label=="N/A":
        return 0.0
    try:
        nums = re.findall(r'\d+\.?\d*', size_label)
        if nums:
            return float(nums[0])
    except:
        pass
    return 0.0
def analyze_tumor_growth(patient_name):
    history = load_history()
    scans   = sorted(
        [h for h in history
         if h.get("patient_name","").lower()
         == patient_name.lower()],
        key=lambda x: x.get("timestamp","")
    )
    if len(scans) < 2:
        return {
            "status":  "insufficient_data",
            "message": f"Need at least 2 scans for {patient_name}. Only {len(scans)} found.",
            "scans":   scans
        }
    fmt    = "%Y-%m-%d %H:%M:%S"
    first  = scans[0]
    last   = scans[-1]
    s1     = parse_size(first.get("tumor_size",""))
    s2     = parse_size(last.get("tumor_size",""))
    change = s2 - s1
    d1   = datetime.strptime(first["timestamp"],fmt)
    d2   = datetime.strptime(last["timestamp"],fmt)
    days = max((d2-d1).days, 1)
    gpm  = round((change/days)*30, 2)

    if change > 0.5:
        trend = "GROWING"
        color = "#E53E3E"
        icon  = "📈"
        rec   = "URGENT: Tumor growing! Immediate attention required."
    elif change < -0.5:
        trend = "SHRINKING"
        color = "#38A169"
        icon  = "📉"
        rec   = "GOOD: Tumor shrinking. Continue treatment."
    else:
        trend = "STABLE"
        color = "#D69E2E"
        icon  = "➡️"
        rec   = "STABLE: No significant change. Continue monitoring."
    return {
        "status":           "success",
        "patient_name":     patient_name,
        "total_scans":      len(scans),
        "size_change_cm":   round(change,2),
        "growth_per_month": gpm,
        "days_monitored":   days,
        "trend":            trend,
        "trend_color":      color,
        "trend_icon":       icon,
        "recommendation":   rec
    }
