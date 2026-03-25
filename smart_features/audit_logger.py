import json
import os
from datetime import datetime
# FILE PATH
HISTORY_DIR = os.path.join(
    os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)
    )),
    "history"
)
AUDIT_FILE = os.path.join(
    HISTORY_DIR, "audit_log.json"
)
# AUDIT ACTION TYPES
class AuditActions:
    LOGIN           = "USER_LOGIN"
    LOGOUT          = "USER_LOGOUT"
    LOGIN_FAILED    = "LOGIN_FAILED"
    MRI_UPLOAD      = "MRI_UPLOAD"
    MRI_ANALYSIS    = "MRI_ANALYSIS"
    PDF_GENERATED   = "PDF_GENERATED"
    PATIENT_CREATED = "PATIENT_CREATED"
    PATIENT_VIEWED  = "PATIENT_VIEWED"
    HISTORY_VIEWED  = "HISTORY_VIEWED"
    REPORT_DOWNLOAD = "REPORT_DOWNLOAD"
    APPOINTMENT_SET = "APPOINTMENT_SET"
    UNAUTHORIZED    = "UNAUTHORIZED_ACCESS"
# LOAD LOGS
def load_logs():
    try:
        os.makedirs(HISTORY_DIR, exist_ok=True)
        if not os.path.exists(AUDIT_FILE):
            return []
        with open(AUDIT_FILE, "r",
                  encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(
                data, list
            ) else []
    except Exception as e:
        print(f"Load logs error: {e}")
        return []
# SAVE LOGS
def save_logs(logs):
    try:
        os.makedirs(HISTORY_DIR, exist_ok=True)
        with open(AUDIT_FILE, "w",
                  encoding="utf-8") as f:
            json.dump(logs, f,
                      indent=4,
                      ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Save logs error: {e}")
        return False
# LOG ACTION
def log_action(
    username,
    action,
    details     = "",
    patient_mrn = "",
    ip_address  = "localhost",
    status      = "SUCCESS"
):
    try:
        logs  = load_logs()
        entry = {
            "id":          len(logs) + 1,
            "timestamp":   datetime.now().strftime(
                               "%Y-%m-%d %H:%M:%S"
                           ),
            "username":    str(username),
            "action":      str(action),
            "details":     str(details),
            "patient_mrn": str(patient_mrn),
            "ip_address":  str(ip_address),
            "status":      str(status)
        }
        logs.append(entry)
        save_logs(logs)
        return entry
    except Exception as e:
        print(f"Log action error: {e}")
        return {}
# GET RECENT LOGS
def get_recent_logs(limit=50):
    try:
        logs = load_logs()
        return sorted(
            logs,
            key=lambda x: x.get(
                "timestamp", ""
            ),
            reverse=True
        )[:limit]
    except:
        return []
# GET SECURITY ALERTS
def get_security_alerts():
    try:
        logs = load_logs()
        return [
            l for l in logs
            if l.get("status") == "FAILED"
            or l.get("action") ==
               "UNAUTHORIZED_ACCESS"
        ]
    except:
        return []
# GET USER LOGS
def get_user_logs(username):
    try:
        return [
            l for l in load_logs()
            if l.get("username") == username
        ]
    except:
        return []
# CLEAR LOGS (Admin only)
def clear_logs():
    try:
        save_logs([])
        return True
    except:
        return False
# TEST
if __name__ == "__main__":
    print("Testing audit_logger...")
    print(f"Audit file: {AUDIT_FILE}")
    log_action(
        username    = "admin",
        action      = AuditActions.LOGIN,
        details     = "Test login",
        status      = "SUCCESS"
    )
    log_action(
        username    = "hacker",
        action      = AuditActions.LOGIN_FAILED,
        details     = "Wrong password",
        status      = "FAILED"
    )
    logs = get_recent_logs(10)
    print(f"\nTotal logs: {len(logs)}")
    for l in logs:
        print(
            f"  [{l['timestamp']}] "
            f"{l['username']} → "
            f"{l['action']} → "
            f"{l['status']}"
        )
    alerts = get_security_alerts()
    print(f"\nSecurity alerts: {len(alerts)}")
    print("✅ audit_logger working!")
