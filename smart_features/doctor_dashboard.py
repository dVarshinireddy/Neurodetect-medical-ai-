import json, os
from datetime import datetime, timedelta
from collections import defaultdict
HISTORY_FILE = "history/prediction_history.json"
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE) as f:
            return json.load(f)
    except:
        return []
def get_dashboard_stats():
    history = load_history()
    if not history:
        return {
            "total_scans":0,"today_scans":0,
            "critical_cases":0,"pending_review":0,
            "tumor_rate":0,"avg_confidence":0,
            "by_type":{},"by_risk":{},
            "by_doctor":{},"recent_cases":[],
            "weekly_trend":[],"critical_patients":[]
        }
    today       = datetime.now().date()
    fmt         = "%Y-%m-%d %H:%M:%S"
    today_scans = [h for h in history
        if datetime.strptime(h["timestamp"],fmt).date()==today]
    critical    = [h for h in history
        if h.get("risk_level")=="CRITICAL"]
    pending     = [h for h in history
        if h.get("risk_level") in ["CRITICAL","HIGH"]]
    tumor_cases = [h for h in history
        if h.get("prediction")!="notumor"]
    confs    = [h.get("confidence",0) for h in history]
    avg_conf = sum(confs)/len(confs) if confs else 0
    by_type   = defaultdict(int)
    by_risk   = defaultdict(int)
    by_doctor = defaultdict(int)
    for h in history:
        by_type[h.get("prediction","unknown")] += 1
        by_risk[h.get("risk_level","UNKNOWN")]  += 1
        by_doctor[h.get("doctor_name","Unknown")] += 1
    weekly = []
    for i in range(7):
        day   = today - timedelta(days=i)
        count = len([h for h in history
            if datetime.strptime(h["timestamp"],fmt).date()==day])
        weekly.append({"date":day.strftime("%m/%d"),"count":count})
    weekly.reverse()

    return {
        "total_scans":       len(history),
        "today_scans":       len(today_scans),
        "critical_cases":    len(critical),
        "pending_review":    len(pending),
        "tumor_rate":        round(len(tumor_cases)/len(history)*100,1),
        "avg_confidence":    round(avg_conf,1),
        "by_type":           dict(by_type),
        "by_risk":           dict(by_risk),
        "by_doctor":         dict(by_doctor),
        "recent_cases":      sorted(history,key=lambda x:x["timestamp"],reverse=True)[:5],
        "weekly_trend":      weekly,
        "critical_patients": critical[-5:]
    }
def get_doctor_performance():
    history = load_history()
    doctors = defaultdict(lambda:{"total":0,"critical":0,"tumor":0,"no_tumor":0})
    for h in history:
        doc = h.get("doctor_name","Unknown")
        doctors[doc]["total"] += 1
        if h.get("risk_level")=="CRITICAL":
            doctors[doc]["critical"] += 1
        if h.get("prediction")!="notumor":
            doctors[doc]["tumor"] += 1
        else:
            doctors[doc]["no_tumor"] += 1
    return dict(doctors)
