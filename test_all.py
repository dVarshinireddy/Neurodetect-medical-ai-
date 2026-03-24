import sys
sys.path.append('smart_features')

print('Testing all smart features...')
print()

try:
    from audit_logger import log_action, AuditActions, get_recent_logs
    log_action('admin', AuditActions.LOGIN, 'Test', status='SUCCESS')
    logs = get_recent_logs(5)
    print(f'✅ audit_logger      - {len(logs)} logs found')
except Exception as e:
    print(f'❌ audit_logger      - {e}')

try:
    from patient_system import save_patient
    p = save_patient(
        first_name='Test',
        last_name='Patient',
        date_of_birth='1990-01-01',
        gender='Male',
        blood_group='A+',
        phone='1234567890'
    )
    print(f'✅ patient_system    - MRN: {p["mrn"]}')
except Exception as e:
    print(f'❌ patient_system    - {e}')

try:
    from appointment_manager import save_appointment
    a = save_appointment(
        patient_name     = 'Test Patient',
        doctor_name      = 'Dr. Smith',
        date             = '2026-03-10',
        time             = '10:00 AM',
        appointment_type = 'Consultation'
    )
    print(f'✅ appointment_mgr   - ID: {a["id"]}')
except Exception as e:
    print(f'❌ appointment_mgr   - {e}')

try:
    from drug_checker import get_drug_report
    r = get_drug_report('glioma', ['Warfarin'])
    print(f'✅ drug_checker      - {r["total_interactions"]} interactions')
except Exception as e:
    print(f'❌ drug_checker      - {e}')

try:
    from doctor_dashboard import get_dashboard_stats
    s = get_dashboard_stats()
    print(f'✅ doctor_dashboard  - Scans: {s["total_scans"]}')
except Exception as e:
    print(f'❌ doctor_dashboard  - {e}')

try:
    from tumor_growth_tracker import analyze_tumor_growth
    r = analyze_tumor_growth('Test')
    print(f'✅ tumor_growth      - Status: {r["status"]}')
except Exception as e:
    print(f'❌ tumor_growth      - {e}')

try:
    from gradcam import full_tumor_analysis
    print('✅ gradcam           - Imported OK')
except Exception as e:
    print(f'❌ gradcam           - {e}')

try:
    from confidence_meter import get_full_confidence_report
    r = get_full_confidence_report(
        'glioma', 95.0,
        [0.95, 0.02, 0.01, 0.02]
    )
    print(f'✅ confidence_meter  - Risk: {r["risk_level"]}')
except Exception as e:
    print(f'❌ confidence_meter  - {e}')

try:
    from treatment_advisor import get_treatment_info
    t = get_treatment_info('glioma')
    print(f'✅ treatment_advisor - ICD10: {t["icd10_code"]}')
except Exception as e:
    print(f'❌ treatment_advisor - {e}')

try:
    from history_tracker import get_summary
    s = get_summary()
    print(f'✅ history_tracker   - Total: {s["total_scans"]}')
except Exception as e:
    print(f'❌ history_tracker   - {e}')

print()
print('=' * 45)
print('All tests complete!')
print('=' * 45)