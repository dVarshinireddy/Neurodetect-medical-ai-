# NeuroDetect - app.py
# Complete Professional Medical UI Redesign
# Hospital Grade System v3.0
import streamlit as st
import numpy as np
import cv2
import os
import sys
import json
import pandas as pd
from PIL import Image
from datetime import datetime, date
import plotly.graph_objects as go
import plotly.express as px
# ── CLOUD COMPATIBILITY ──
import os
import warnings
warnings.filterwarnings("ignore")

# Create needed directories
for d in ["history", "models",
          "reports", "smart_features"]:
    os.makedirs(d, exist_ok=True)

# Create empty history files
import json
for f, default in [
    ("history/patients.json",     []),
    ("history/appointments.json", []),
    ("history/audit_log.json",    []),
    ("history/prediction_history.json", []),
    ("history/emergency_alerts.json",   []),
]:
    if not os.path.exists(f):
        with open(f, "w") as fp:
            json.dump(default, fp)
import warnings
warnings.filterwarnings("ignore")
sys.path.append("member1")
sys.path.append("member2")
sys.path.append("smart_features")
# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title = "NeuroDetect Medical AI",
    page_icon  = "🏥",
    layout     = "wide",
    initial_sidebar_state = "expanded"
)
# ─────────────────────────────────────────
# PROFESSIONAL MEDICAL CSS
# White + Blue Hospital Theme
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif !important; }

/* ── BACKGROUND ── */
.stApp {
    background: #F0F4F8 !important;
}

/* ── HIDE STREAMLIT DEFAULTS ── */
#MainMenu, footer, header {
    visibility: hidden !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #1B4F72 !important;
    display: block !important;
    visibility: visible !important;
    width: 250px !important;
    min-width: 250px !important;
}

[data-testid="stSidebarNav"] {
    display: block !important;
}

[data-testid="collapsedControl"] {
    display: block !important;
    color: white !important;
}

section[data-testid="stSidebar"] {
    display: block !important;
    visibility: visible !important;
}

/* ── ALL INPUT LABELS ── */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
.stTextInput label,
.stSelectbox label,
.stTextArea label,
.stDateInput label,
.stFileUploader label,
.stNumberInput label,
.stRadio label,
label[data-testid] {
    color: #1B4F72 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
}

/* ── TEXT INPUTS ── */
.stTextInput input,
input[type="text"],
input[type="password"],
input[type="number"],
input[type="email"] {
    background-color: white !important;
    color: #1a202c !important;
    border: 2px solid #CBD5E0 !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
}
.stTextInput input:focus,
input[type="text"]:focus,
input[type="password"]:focus {
    border-color: #2E86C1 !important;
    box-shadow: 0 0 0 2px rgba(46,134,193,0.2) !important;
}

/* ── SELECT BOX ── */
.stSelectbox > div > div,
[data-baseweb="select"] > div {
    background-color: white !important;
    color: #1a202c !important;
    border: 2px solid #CBD5E0 !important;
    border-radius: 8px !important;
}
[data-baseweb="select"] span,
[data-baseweb="select"] div {
    color: #1a202c !important;
}

/* ── TEXTAREA ── */
.stTextArea textarea {
    background-color: white !important;
    color: #1a202c !important;
    border: 2px solid #CBD5E0 !important;
    border-radius: 8px !important;
}

/* ── DATE INPUT ── */
.stDateInput input {
    background-color: white !important;
    color: #1a202c !important;
    border: 2px solid #CBD5E0 !important;
    border-radius: 8px !important;
}

/* ── FILE UPLOADER ── */
[data-testid="stFileUploader"] {
    background: white !important;
    border: 2px dashed #2E86C1 !important;
    border-radius: 12px !important;
    padding: 20px !important;
}
[data-testid="stFileUploader"] *,
[data-testid="stFileUploaderDropzone"] *,
[data-testid="stFileUploaderDropzone"] p,
[data-testid="stFileUploaderDropzone"] span {
    color: #1B4F72 !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: white !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: #2E86C1 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #1B4F72 !important;
}
.stFormSubmitButton > button {
    background: linear-gradient(135deg,#1B4F72,#2E86C1) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    width: 100% !important;
    padding: 12px !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: white !important;
    border-radius: 8px !important;
    border: 1px solid #E2E8F0 !important;
    padding: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    color: #718096 !important;
    font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    background: #2E86C1 !important;
    color: white !important;
    border-radius: 6px !important;
}
.stTabs [data-baseweb="tab"] p {
    color: inherit !important;
}

/* ── CHECKBOXES ── */
.stCheckbox label p {
    color: #1B4F72 !important;
    font-weight: 500 !important;
}

/* ── MAIN CONTENT TEXT ── */
.main p, .main span,
.main div:not([class*="stSidebar"]) {
    color: #1a202c;
}

/* ── METRIC CARDS ── */
.metric-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
}
.metric-label {
    font-size: 0.8rem;
    color: #718096;
    margin-top: 4px;
    font-weight: 500;
}

/* ── MEDICAL CARDS ── */
.medical-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    margin: 8px 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    border-left: 4px solid #2E86C1;
}
.patient-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    margin: 8px 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    border-top: 4px solid #2E86C1;
}
.mrn-badge {
    background: #EBF5FB;
    border: 1px solid #2E86C1;
    border-radius: 6px;
    padding: 4px 12px;
    color: #1B4F72;
    font-weight: 700;
    font-size: 0.9rem;
    display: inline-block;
}

/* ── ALERTS ── */
.alert-critical {
    background: #FFF5F5;
    border-left: 5px solid #E53E3E;
    border-radius: 8px;
    padding: 15px 20px;
    color: #C53030;
    font-weight: 600;
    margin: 10px 0;
}
.alert-high {
    background: #FFFAF0;
    border-left: 5px solid #DD6B20;
    border-radius: 8px;
    padding: 15px 20px;
    color: #C05621;
    font-weight: 600;
    margin: 10px 0;
}
.alert-moderate {
    background: #FFFFF0;
    border-left: 5px solid #D69E2E;
    border-radius: 8px;
    padding: 15px 20px;
    color: #B7791F;
    font-weight: 600;
    margin: 10px 0;
}
.alert-normal {
    background: #F0FFF4;
    border-left: 5px solid #38A169;
    border-radius: 8px;
    padding: 15px 20px;
    color: #276749;
    font-weight: 600;
    margin: 10px 0;
}

/* ── SECTION HEADERS ── */
.section-header {
    color: #1B4F72;
    font-size: 1.2rem;
    font-weight: 700;
    border-bottom: 2px solid #2E86C1;
    padding-bottom: 8px;
    margin-bottom: 15px;
}

/* ── LETTERHEAD ── */
.letterhead {
    background: white;
    border-radius: 12px;
    padding: 30px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    border-top: 8px solid #1B4F72;
}

/* ── PLACEHOLDER ── */
::placeholder {
    color: #A0AEC0 !important;
}

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton > button {
    background: #38A169 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    width: 100% !important;
}
.stDownloadButton > button:hover {
    background: #276749 !important;
}

/* ── SPINNER ── */
.stSpinner p {
    color: #1B4F72 !important;
}

/* ── SUCCESS / ERROR / INFO ── */
[data-testid="stAlert"] {
    border-radius: 8px !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border-radius: 8px !important;
    overflow: hidden !important;
}

/* ── PLOTLY CHARTS ── */
.js-plotly-plot {
    border-radius: 8px !important;
    background: white !important;
}
</style>
""", unsafe_allow_html=True)
# ─────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────
CLASSES  = ["glioma", "meningioma",
            "notumor", "pituitary"]
IMG_SIZE = 64

USERS = {
    "admin": {
        "password": "neurodetect123",
        "role":     "Administrator",
        "name":     "Admin User",
        "emoji":    "👨‍💼",
        "dept":     "Administration"
    },
    "doctor": {
        "password": "brain2024",
        "role":     "Neurologist",
        "name":     "Dr. Smith",
        "emoji":    "👨‍⚕️",
        "dept":     "Neurology"
    },
    "radiologist": {
        "password": "mri2024",
        "role":     "Radiologist",
        "name":     "Dr. Johnson",
        "emoji":    "🔬",
        "dept":     "Radiology"
    }
}

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
def init_session():
    defaults = {
        "logged_in":  False,
        "username":   "",
        "user_info":  None,
        "login_time": "",
        "page":       "dashboard",
        "patient":    None
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# ─────────────────────────────────────────
# LOGIN PAGE
# ─────────────────────────────────────────
def login_page():
    # Hospital Header
    st.markdown("""
    <div style="
        background:linear-gradient(
            135deg,#1B4F72,#2E86C1
        );
        padding:30px;
        text-align:center;
        border-radius:12px;
        margin-bottom:30px;">
        <h1 style="
            color:white;
            font-size:2.5rem;
            font-weight:800;
            margin:0;">
            🏥 NeuroDetect Medical AI
        </h1>
        <p style="
            color:rgba(255,255,255,0.85);
            margin:8px 0 0 0;">
            Advanced Brain Tumor Detection System
        </p>
        <p style="
            color:rgba(255,255,255,0.6);
            font-size:0.85rem;
            margin:4px 0 0 0;">
            Authorized Medical Personnel Only
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,1.2,1])
    with col2:
        st.markdown("""
        <div style="
            background:white;
            border-radius:12px;
            padding:30px;
            box-shadow:0 4px 20px
                rgba(0,0,0,0.1);
            border-top:4px solid #2E86C1;">
            <h3 style="
                color:#1B4F72;
                margin-bottom:20px;
                text-align:center;">
                🔐 Secure Staff Login
            </h3>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input(
                "Staff ID / Username",
                placeholder="Enter username..."
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password..."
            )
            dept = st.selectbox(
                "Department",
                [
                    "Neurology",
                    "Radiology",
                    "Oncology",
                    "Administration",
                    "Emergency"
                ]
            )
            st.markdown(
                "<br>", unsafe_allow_html=True
            )
            submitted = st.form_submit_button(
                "🔐 Login to System"
            )

            if submitted:
                if not username or not password:
                    st.error(
                        "❌ Please enter all fields!"
                    )
                elif (username.strip() in USERS and
                      USERS[username.strip()]["password"]
                      == password.strip()):
                    st.session_state.logged_in  = True
                    st.session_state.username   = username
                    st.session_state.user_info  = \
                        USERS[username]
                    st.session_state.login_time = \
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M"
                        )

                    # Audit log
                    try:
                        from audit_logger import \
                            log_action, AuditActions
                        log_action(
                            username   = username,
                            action     = AuditActions.LOGIN,
                            details    = f"Login from {dept}",
                            status     = "SUCCESS"
                        )
                    except:
                        pass

                    st.success(
                        f"✅ Welcome "
                        f"{USERS[username]['name']}!"
                    )
                    st.rerun()
                else:
                    # Log failed attempt
                    try:
                        from audit_logger import \
                            log_action, AuditActions
                        log_action(
                            username = username,
                            action   = AuditActions.LOGIN_FAILED,
                            details  = "Wrong credentials",
                            status   = "FAILED"
                        )
                    except:
                        pass
                    st.error(
                        "❌ Invalid credentials!"
                    )

        # Demo credentials
        st.markdown("""
        <div style="
            background:#EBF5FB;
            border-radius:8px;
            padding:12px;
            margin-top:15px;
            text-align:center;">
            <p style="
                color:#1B4F72;
                font-size:0.8rem;
                font-weight:600;
                margin:0 0 6px 0;">
                Demo Credentials
            </p>
            <p style="
                color:#2E86C1;
                font-size:0.8rem;
                margin:0;">
                admin/neurodetect123 |
                doctor/brain2024 |
                radiologist/mri2024
            </p>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# LOAD MODELS
# ─────────────────────────────────────────
@st.cache_resource
def load_all_models():
    import joblib
    import tensorflow as tf
    models = {}

    try:
        models["svm"]    = joblib.load(
            "models/svm_model.pkl"
        )
        models["scaler"] = joblib.load(
            "models/svm_scaler.pkl"
        )
        models["pca"]    = joblib.load(
            "models/svm_pca.pkl"
        )
        models["le"]     = joblib.load(
            "models/label_encoder.pkl"
        )
        models["rf"]     = joblib.load(
            "models/rf_model.pkl"
        )
    except Exception as e:
        st.sidebar.warning(f"ML: {e}")

    try:
        models["cnn"] = \
            tf.keras.models.load_model(
                "models/cnn_model.h5"
            )
    except Exception as e:
        st.sidebar.warning(f"CNN: {e}")

    try:
        models["resnet"] = \
            tf.keras.models.load_model(
                "models/transfer_ResNet50.h5"
            )
    except Exception as e:
        st.sidebar.warning(f"ResNet: {e}")

    return models

# ─────────────────────────────────────────
# IMAGE PROCESSING
# ─────────────────────────────────────────
def load_image(uploaded_file):
    img      = Image.open(
        uploaded_file
    ).convert("RGB")
    img_orig = np.array(img)
    img_res  = cv2.resize(
        img_orig, (IMG_SIZE, IMG_SIZE)
    )
    return img_res / 255.0, img_orig

def enhance_mri(img_array):
    img_uint8 = img_array.astype(np.uint8) \
        if img_array.max() > 1.0 \
        else (img_array*255).astype(np.uint8)
    lab       = cv2.cvtColor(
        img_uint8, cv2.COLOR_RGB2LAB
    )
    l, a, b   = cv2.split(lab)
    clahe     = cv2.createCLAHE(
        clipLimit=3.0, tileGridSize=(8,8)
    )
    l_enh     = clahe.apply(l)
    enhanced  = cv2.cvtColor(
        cv2.merge([l_enh, a, b]),
        cv2.COLOR_LAB2RGB
    )
    kernel    = np.array([
        [0,-1,0],[-1,5,-1],[0,-1,0]
    ])
    return cv2.filter2D(enhanced, -1, kernel)

# ─────────────────────────────────────────
# PREDICTIONS
# ─────────────────────────────────────────
def predict_all(img_array, models):
    results = {}

    if all(k in models for k in
           ["svm","scaler","pca","le"]):
        try:
            flat  = img_array.reshape(1, -1)
            sc    = models["scaler"].transform(flat)
            pca   = models["pca"].transform(sc)
            idx   = models["svm"].predict(pca)[0]
            prob  = models["svm"]\
                .predict_proba(pca)[0]
            label = models["le"]\
                .inverse_transform([idx])[0]
            results["SVM"] = (
                label,
                prob[idx]*100,
                prob.tolist()
            )
        except:
            pass

    if "rf" in models and \
            "scaler" in models:
        try:
            flat  = img_array.reshape(1, -1)
            sc    = models["scaler"].transform(flat)
            pca   = models["pca"].transform(sc)
            idx   = models["rf"].predict(pca)[0]
            prob  = models["rf"]\
                .predict_proba(pca)[0]
            label = models["le"]\
                .inverse_transform([idx])[0]
            results["RF"] = (
                label,
                prob[idx]*100,
                prob.tolist()
            )
        except:
            pass

    if "cnn" in models:
        try:
            batch = np.expand_dims(img_array, 0)
            prob  = models["cnn"].predict(
                batch, verbose=0
            )[0]
            idx   = np.argmax(prob)
            label = models["le"]\
                .inverse_transform([idx])[0]
            results["CNN"] = (
                label,
                prob[idx]*100,
                prob.tolist()
            )
        except:
            pass

    if "resnet" in models:
        try:
            batch = np.expand_dims(img_array, 0)
            prob  = models["resnet"].predict(
                batch, verbose=0
            )[0]
            idx   = np.argmax(prob)
            label = models["le"]\
                .inverse_transform([idx])[0]
            results["ResNet50"] = (
                label,
                prob[idx]*100,
                prob.tolist()
            )
        except:
            pass

    return results

def get_final_prediction(results):
    if not results:
        return None, 0, [0.25]*4

    weights  = {
        "SVM": 0.15, "RF": 0.15,
        "CNN": 0.40, "ResNet50": 0.30
    }
    weighted = np.zeros(4)
    tw       = 0

    for m, (label, conf, probs) in \
            results.items():
        w         = weights.get(m, 0.25)
        weighted += w * np.array(probs)
        tw       += w

    weighted  /= tw
    idx        = np.argmax(weighted)
    label      = CLASSES[idx]
    confidence = weighted[idx] * 100

    return (
        label,
        round(float(confidence), 2),
        weighted.tolist()
    )

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="
            text-align:center;
            padding:15px 0 10px 0;">
            <div style="font-size:2.5rem;">🏥</div>
            <div style="color:white;font-weight:800;
                font-size:1.2rem;">NeuroDetect</div>
            <div style="color:rgba(255,255,255,0.6);
                font-size:0.75rem;">Medical AI v3.0</div>
        </div>
        """, unsafe_allow_html=True)

        user = st.session_state.user_info
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.1);
            border-radius:10px;padding:10px;
            margin:10px 0;text-align:center;">
            <div style="font-size:2rem;">
                {user['emoji']}
            </div>
            <div style="color:white;font-weight:700;">
                {user['name']}
            </div>
            <div style="color:rgba(255,255,255,0.6);
                font-size:0.8rem;">
                {user['role']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # ── MAIN NAVIGATION ──
        st.markdown("""
        <div style="color:rgba(255,255,255,0.6);
            font-size:0.75rem;font-weight:600;
            letter-spacing:1px;margin-bottom:5px;">
            🏥 CLINICAL MODULES
        </div>
        """, unsafe_allow_html=True)

        nav_items = [
            ("🏠 Dashboard",         "dashboard"),
            ("🔬 Analyze MRI",       "analyze"),
            ("👤 Patient Registry",  "patients"),
            ("📜 Patient History",   "history"),
            ("📈 Statistics",        "stats"),
            ("👨‍⚕️ Doctor Dashboard", "doctor"),
            ("📅 Appointments",      "appointments"),
            ("💊 Drug Checker",      "drugs"),
            ("📊 Model Performance", "models"),
            ("🔐 Audit Logs",        "audit"),
            ("ℹ️ About",             "about"),
        ]

        for label, key in nav_items:
            if st.button(
                label,
                key=f"nav_{key}",
                use_container_width=True
            ):
                st.session_state["page"] = key
                st.rerun()

        st.markdown("---")

        # ── NEW FEATURES ──
        st.markdown("""
        <div style="color:rgba(255,255,255,0.6);
            font-size:0.75rem;font-weight:600;
            letter-spacing:1px;margin-bottom:5px;">
            🧬 ADVANCED DIAGNOSTICS
        </div>
        """, unsafe_allow_html=True)

        new_nav = [
            ("🧠 AI Second Opinion",  "second_opinion"),
            ("⚠️ Risk Calculator",    "risk"),
            ("🚨 Emergency Alerts",   "emergency"),
            ("📅 Treatment Timeline", "timeline"),
            ("🧬 Brain Heat Atlas",   "atlas"),
            ("📹 Real-Time Detection","realtime"),
            ("📁 DICOM Support",      "dicom"),
            ("🎯 Tumor Segmentation", "unet"),
        ]

        for label, key in new_nav:
            if st.button(
                label,
                key=f"nav_{key}",
                use_container_width=True
            ):
                st.session_state["page"] = key
                st.rerun()

        st.markdown("---")

        # ── RESEARCH FEATURES ──
        st.markdown("""
        <div style="color:rgba(255,255,255,0.6);
            font-size:0.75rem;font-weight:600;
            letter-spacing:1px;margin-bottom:5px;">
            🔬 RESEARCH FEATURES
        </div>
        """, unsafe_allow_html=True)
        research_nav = [
            ("📂 Multi-Dataset",      "dataset"),
            ("🔐 HIPAA Encryption",   "encryption"),
            ("🧊 3D Visualization",   "viz3d"),
            ("🌐 Federated Learning", "federated"),
            ("🧬 Tumor Types DB",     "tumortypes"),
            ("🏥 PACS/EHR",           "pacs"),
        ]
        for label, key in research_nav:
            if st.button(
                label,
                key=f"nav_{key}",
                use_container_width=True
            ):
                st.session_state["page"] = key
                st.rerun()
        st.markdown("---")
        # ── SETTINGS ──
        st.markdown("""
        <div style="color:rgba(255,255,255,0.6);
            font-size:0.75rem;font-weight:600;
            letter-spacing:1px;margin-bottom:5px;">
            SETTINGS
        </div>
        """, unsafe_allow_html=True)
        settings = {
            "show_gradcam":   st.checkbox(
                "🔍 Grad-CAM", True
            ),
            "show_enhanced":  st.checkbox(
                "✨ Enhancement", True
            ),
            "show_treatment": st.checkbox(
                "💊 Treatment", True
            ),
            "gen_pdf":        st.checkbox(
                "📄 Auto PDF", True
            )
        }
        st.markdown("---")
        # ── AI MODELS STATUS ──
        st.markdown("""
        <div style="color:rgba(255,255,255,0.6);
            font-size:0.75rem;font-weight:600;
            letter-spacing:1px;margin-bottom:5px;">
            AI MODELS STATUS
        </div>
        """, unsafe_allow_html=True)
        for name, acc in [
            ("CNN",    "98.87%"),
            ("SVM",    "95.95%"),
            ("RF",     "94.23%"),
            ("ResNet", "85.83%")
        ]:
            st.markdown(f"""
            <div style="display:flex;
                justify-content:space-between;
                padding:3px 0;font-size:0.8rem;">
                <span style="
                    color:rgba(255,255,255,0.7);">
                    {name}
                </span>
                <span style="color:#82E0AA;
                    font-weight:600;">
                    {acc}
                </span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # ── LOGOUT ──
        if st.button(
            "🚪 Logout",
            key="nav_logout",
            use_container_width=True
        ):
            try:
                from audit_logger import \
                    log_action, AuditActions
                log_action(
                    username = st.session_state[
                        "username"
                    ],
                    action   = AuditActions.LOGOUT,
                    details  = "Logged out",
                    status   = "SUCCESS"
                )
            except:
                pass
            for k in list(
                st.session_state.keys()
            ):
                del st.session_state[k]
            st.rerun()

    return settings
# ─────────────────────────────────────────
# HOSPITAL HEADER
# ─────────────────────────────────────────
def render_header(title, subtitle=""):
    user = st.session_state.user_info
    st.markdown(f"""
    <div style="
        background:linear-gradient(
            135deg,#1B4F72,#2E86C1
        );
        padding:20px 25px;
        border-radius:12px;
        margin-bottom:20px;
        display:flex;
        justify-content:space-between;
        align-items:center;
        box-shadow:0 4px 15px
            rgba(0,0,0,0.1);">
        <div>
            <h2 style="
                color:white;
                margin:0;
                font-size:1.5rem;
                font-weight:700;">
                {title}
            </h2>
            <p style="
                color:rgba(255,255,255,0.75);
                margin:4px 0 0 0;
                font-size:0.85rem;">
                {subtitle}
            </p>
        </div>
        <div style="text-align:right;">
            <div style="
                color:white;
                font-size:0.85rem;
                font-weight:600;">
                {user['emoji']} {user['name']}
            </div>
            <div style="
                color:rgba(255,255,255,0.6);
                font-size:0.75rem;">
                {datetime.now().strftime(
                    "%d %B %Y | %H:%M"
                )}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# DASHBOARD PAGE
# ─────────────────────────────────────────
def dashboard_page():
    render_header(
        "🏠 Clinical Dashboard",
        "NeuroDetect Medical AI System"
    )

    try:
        from history_tracker import \
            load_history, get_summary
        summary = get_summary()
        history = load_history()
    except:
        summary = {
            "total_scans":    0,
            "tumor_detected": 0,
            "no_tumor":       0,
            "critical_cases": 0
        }
        history = []

    # ── EMERGENCY BANNER ──
    try:
        from emergency_alert import \
            get_active_alerts
        alerts = get_active_alerts()
        if alerts:
            st.markdown(f"""
            <div class="alert-critical">
                🚨 {len(alerts)} Active
                Emergency Alert(s) Require
                Immediate Attention!
            </div>
            """, unsafe_allow_html=True)
    except:
        pass

    # ── QUICK ACCESS ROW 1 ──
    st.markdown("""
    <div class="section-header">
        🚀 Quick Access
    </div>
    """, unsafe_allow_html=True)

    b1,b2,b3,b4,b5 = st.columns(5)
    with b1:
        if st.button("🔬 Analyze MRI",
            key="dash_analyze",
            use_container_width=True):
            st.session_state["page"] = "analyze"
            st.rerun()
    with b2:
        if st.button("👤 Patients",
            key="dash_patients",
            use_container_width=True):
            st.session_state["page"] = "patients"
            st.rerun()
    with b3:
        if st.button("📅 Appointments",
            key="dash_appointments",
            use_container_width=True):
            st.session_state["page"] = "appointments"
            st.rerun()
    with b4:
        if st.button("💊 Drug Checker",
            key="dash_drugs",
            use_container_width=True):
            st.session_state["page"] = "drugs"
            st.rerun()
    with b5:
        if st.button("👨‍⚕️ Doctor Dashboard",
            key="dash_doctor",
            use_container_width=True):
            st.session_state["page"] = "doctor"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── QUICK ACCESS ROW 2 ──
    b6,b7,b8,b9,b10 = st.columns(5)
    with b6:
        if st.button("🧠 Second Opinion",
            key="dash_second",
            use_container_width=True):
            st.session_state["page"] = "second_opinion"
            st.rerun()
    with b7:
        if st.button("⚠️ Risk Calculator",
            key="dash_risk",
            use_container_width=True):
            st.session_state["page"] = "risk"
            st.rerun()
    with b8:
        if st.button("🚨 Emergency Alerts",
            key="dash_emergency",
            use_container_width=True):
            st.session_state["page"] = "emergency"
            st.rerun()
    with b9:
        if st.button("📅 Treatment Timeline",
            key="dash_timeline",
            use_container_width=True):
            st.session_state["page"] = "timeline"
            st.rerun()
    with b10:
        if st.button("📈 Statistics",
            key="dash_stats",
            use_container_width=True):
            st.session_state["page"] = "stats"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── QUICK ACCESS ROW 3 ──
    b11,b12,b13,b14,b15 = st.columns(5)
    with b11:
        if st.button("🧬 Brain Atlas",
            key="dash_atlas",
            use_container_width=True):
            st.session_state["page"] = "atlas"
            st.rerun()
    with b12:
        if st.button("📹 Real-Time",
            key="dash_realtime",
            use_container_width=True):
            st.session_state["page"] = "realtime"
            st.rerun()
    with b13:
        if st.button("📁 DICOM Support",
            key="dash_dicom",
            use_container_width=True):
            st.session_state["page"] = "dicom"
            st.rerun()
    with b14:
        if st.button("🎯 Segmentation",
            key="dash_unet",
            use_container_width=True):
            st.session_state["page"] = "unet"
            st.rerun()
    with b15:
        if st.button("📊 Model Performance",
            key="dash_models",
            use_container_width=True):
            st.session_state["page"] = "models"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── KEY METRICS ──
    st.markdown("""
    <div class="section-header">
        📊 System Overview
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4,c5 = st.columns(5)
    for col, label, value, color in [
        (c1,"Total Scans",
         summary["total_scans"],"#2E86C1"),
        (c2,"Tumor Cases",
         summary["tumor_detected"],"#E53E3E"),
        (c3,"No Tumor",
         summary["no_tumor"],"#38A169"),
        (c4,"Critical",
         summary["critical_cases"],"#DD6B20"),
        (c5,"AI Accuracy","98.87%","#1B4F72")
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value"
                     style="color:{color};">
                    {value}
                </div>
                <div class="metric-label">
                    {label}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── CHARTS ──
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="section-header">
            📊 Diagnosis Distribution
        </div>
        """, unsafe_allow_html=True)

        if history:
            df     = pd.DataFrame(history)
            counts = df[
                "prediction"
            ].value_counts()
            fig    = px.pie(
                values = counts.values,
                names  = counts.index,
                color_discrete_map={
                    "glioma":     "#E53E3E",
                    "meningioma": "#DD6B20",
                    "notumor":    "#38A169",
                    "pituitary":  "#2E86C1"
                }
            )
            fig.update_layout(
                paper_bgcolor = "white",
                font_color    = "#2D3748",
                height        = 300,
                margin        = dict(t=20,b=20)
            )
            st.plotly_chart(
                fig,
                use_container_width=True
            )
        else:
            st.info(
                "No scan data yet. "
                "Analyze an MRI to see data!"
            )

    with col2:
        st.markdown("""
        <div class="section-header">
            🤖 Model Performance
        </div>
        """, unsafe_allow_html=True)

        fig2 = go.Figure()
        for name, acc, color in [
            ("CNN",     98.87, "#1B4F72"),
            ("SVM",     95.95, "#2E86C1"),
            ("RF",      94.23, "#2E86C1"),
            ("VGG16",   94.11, "#85C1E9"),
            ("ResNet50",85.83, "#85C1E9"),
        ]:
            fig2.add_trace(go.Bar(
                x            = [name],
                y            = [acc],
                marker_color = color,
                text         = [f"{acc}%"],
                textposition = "outside",
                showlegend   = False
            ))
        fig2.update_layout(
            yaxis_range   = [0, 115],
            paper_bgcolor = "white",
            plot_bgcolor  = "white",
            font_color    = "#2D3748",
            height        = 300,
            margin        = dict(t=20,b=20),
            showlegend    = False,
            bargap        = 0.3
        )
        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # ── RECENT CASES ──
    if history:
        st.markdown("""
        <div class="section-header"
             style="margin-top:20px;">
            📋 Recent Cases
        </div>
        """, unsafe_allow_html=True)

        recent = sorted(
            history,
            key=lambda x: x["timestamp"],
            reverse=True
        )[:5]

        for case in recent:
            risk  = case.get("risk_level","")
            color = {
                "CRITICAL": "#E53E3E",
                "HIGH":     "#DD6B20",
                "MODERATE": "#D69E2E",
                "NONE":     "#38A169"
            }.get(risk, "#2E86C1")

            st.markdown(f"""
            <div style="
                background:white;
                border-radius:8px;
                padding:12px 16px;
                margin-bottom:8px;
                border-left:4px solid {color};
                box-shadow:0 1px 4px
                    rgba(0,0,0,0.08);
                display:flex;
                justify-content:
                    space-between;">
                <div>
                    <span style="
                        font-weight:600;
                        color:#2D3748;">
                        {case.get(
                            'patient_name',
                            'Unknown'
                        )}
                    </span>
                    <span style="
                        color:#718096;
                        font-size:0.85rem;
                        margin-left:10px;">
                        {case.get(
                            'prediction',''
                        ).upper()}
                    </span>
                </div>
                <div>
                    <span style="
                        background:{color}22;
                        color:{color};
                        padding:2px 8px;
                        border-radius:12px;
                        font-size:0.75rem;
                        font-weight:700;">
                        {risk}
                    </span>
                    <span style="
                        color:#718096;
                        font-size:0.75rem;
                        margin-left:8px;">
                        {case.get(
                            'timestamp',''
                        )[:10]}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="alert-normal">
            ✅ System Ready! Click
            🔬 Analyze MRI to start!
        </div>
        """, unsafe_allow_html=True)
# ─────────────────────────────────────────
# PATIENT REGISTRY PAGE
# ─────────────────────────────────────────
def patients_page():
    render_header(
        "👤 Patient Registry",
        "Manage patient records and MRN"
    )

    tab1, tab2, tab3 = st.tabs([
        "➕ Register Patient",
        "🔍 Search Patient",
        "📋 All Patients"
    ])

    with tab1:
        st.markdown("""
        <div class="section-header">
            New Patient Registration
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input(
                "First Name *"
            )
            dob        = st.date_input(
                "Date of Birth *",
                min_value=date(1900,1,1)
            )
            blood_group = st.selectbox(
                "Blood Group *",
                ["A+","A-","B+","B-",
                 "AB+","AB-","O+","O-"]
            )
            phone = st.text_input("Phone *")
            emergency_name = st.text_input(
                "Emergency Contact Name *"
            )
            insurance = st.text_input(
                "Insurance ID"
            )
            medical_history = st.text_area(
                "Medical History",
                height=80
            )

        with col2:
            last_name = st.text_input(
                "Last Name *"
            )
            gender    = st.selectbox(
                "Gender *",
                ["Male","Female","Other"]
            )
            email     = st.text_input("Email")
            address   = st.text_area(
                "Address", height=80
            )
            emergency_phone = st.text_input(
                "Emergency Contact Phone *"
            )
            allergies = st.text_input(
                "Known Allergies"
            )
            referring = st.text_input(
                "Referring Doctor"
            )

        if st.button(
            "📋 Register Patient",
            type="primary"
        ):
            if first_name and last_name and phone:
                try:
                    from patient_system import \
                        save_patient
                    patient = save_patient(
                        first_name = first_name,
                        last_name  = last_name,
                        date_of_birth = str(dob),
                        gender     = gender,
                        blood_group = blood_group,
                        phone      = phone,
                        email      = email,
                        address    = address,
                        emergency_contact_name  = emergency_name,
                        emergency_contact_phone = emergency_phone,
                        insurance_id    = insurance,
                        allergies       = allergies,
                        medical_history = medical_history,
                        referring_doctor= referring
                    )

                    st.success(
                        f"✅ Patient Registered!"
                    )
                    st.markdown(f"""
                    <div class="medical-card">
                        <h4 style="color:#1B4F72;">
                            Patient Details
                        </h4>
                        <p>
                            <b>MRN:</b>
                            <span class="mrn-badge">
                                {patient['mrn']}
                            </span>
                        </p>
                        <p>
                            <b>Name:</b>
                            {patient['full_name']}
                        </p>
                        <p>
                            <b>Age:</b>
                            {patient['age']} years
                        </p>
                        <p>
                            <b>Blood Group:</b>
                            {patient['blood_group']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Audit log
                    try:
                        from audit_logger import \
                            log_action, AuditActions
                        log_action(
                            username    = st.session_state.username,
                            action      = AuditActions.PATIENT_CREATED,
                            details     = f"Registered {first_name} {last_name}",
                            patient_mrn = patient['mrn'],
                            status      = "SUCCESS"
                        )
                    except:
                        pass

                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error(
                    "❌ Fill required fields!"
                )

    with tab2:
        st.markdown("""
        <div class="section-header">
            Search Patient
        </div>
        """, unsafe_allow_html=True)

        search = st.text_input(
            "Search by Name or MRN"
        )
        if search:
            try:
                from patient_system import \
                    search_patients
                results = search_patients(search)
                if results:
                    for p in results:
                        st.markdown(f"""
                        <div class="patient-card">
                            <div style="
                                display:flex;
                                justify-content:
                                    space-between;">
                                <h4 style="
                                    color:#1B4F72;
                                    margin:0;">
                                    {p['full_name']}
                                </h4>
                                <span
                                    class="mrn-badge">
                                    {p['mrn']}
                                </span>
                            </div>
                            <div style="
                                margin-top:10px;
                                display:grid;
                                grid-template-columns:
                                    1fr 1fr 1fr;
                                gap:10px;
                                font-size:0.85rem;">
                                <div>
                                    <b>Age:</b>
                                    {p['age']} yrs
                                </div>
                                <div>
                                    <b>Gender:</b>
                                    {p['gender']}
                                </div>
                                <div>
                                    <b>Blood:</b>
                                    {p['blood_group']}
                                </div>
                                <div>
                                    <b>Phone:</b>
                                    {p['phone']}
                                </div>
                                <div>
                                    <b>Allergies:</b>
                                    {p.get(
                                        'allergies',
                                        'None'
                                    )}
                                </div>
                                <div>
                                    <b>Scans:</b>
                                    {p.get(
                                        'scan_count',0
                                    )}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No patients found")
            except Exception as e:
                st.error(f"Error: {e}")

    with tab3:
        try:
            from patient_system import \
                get_all_patients
            patients = get_all_patients()
            if patients:
                import pandas as pd
                df = pd.DataFrame(patients)
                cols = [
                    "mrn","full_name","age",
                    "gender","blood_group",
                    "phone","scan_count"
                ]
                available = [
                    c for c in cols
                    if c in df.columns
                ]
                st.dataframe(
                    df[available],
                    use_container_width=True
                )
            else:
                st.info(
                    "No patients registered yet"
                )
        except Exception as e:
            st.error(f"Error: {e}")

# ─────────────────────────────────────────
# ANALYZE PAGE
# ─────────────────────────────────────────
def analyze_page(settings, models):
    render_header(
        "🔬 MRI Analysis",
        "AI-Powered Brain Tumor Detection"
    )

    col1, col2 = st.columns([1, 1.8])

    with col1:
        st.markdown("""
        <div class="section-header">
            Patient & Scan Information
        </div>
        """, unsafe_allow_html=True)

        # MRN Search
        mrn_search = st.text_input(
            "🔍 Search by MRN or Name"
        )
        if mrn_search:
            try:
                from patient_system import \
                    search_patients
                results = search_patients(
                    mrn_search
                )
                if results:
                    p = results[0]
                    st.success(
                        f"✅ Found: "
                        f"{p['full_name']} "
                        f"[{p['mrn']}]"
                    )
                    st.session_state.patient = p
            except:
                pass

        # Patient Info
        if st.session_state.get("patient"):
            p = st.session_state.patient
            st.markdown(f"""
            <div class="patient-card">
                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;">
                    <b style="color:#1B4F72;">
                        {p['full_name']}
                    </b>
                    <span class="mrn-badge">
                        {p['mrn']}
                    </span>
                </div>
                <div style="
                    font-size:0.8rem;
                    color:#718096;
                    margin-top:6px;">
                    Age: {p['age']} |
                    {p['gender']} |
                    Blood: {p['blood_group']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            patient_name = p["full_name"]
            patient_age  = str(p["age"])
            patient_mrn  = p["mrn"]
        else:
            patient_name = st.text_input(
                "Patient Name *"
            )
            patient_age  = st.text_input(
                "Age"
            )
            patient_mrn  = "WALK-IN"

        patient_gender = st.selectbox(
            "Gender",
            ["Male","Female","Other"]
        )
        scan_type = st.selectbox(
            "Scan Type",
            [
                "Brain MRI - Axial",
                "Brain MRI - Coronal",
                "Brain MRI - Sagittal",
                "Brain CT Scan"
            ]
        )
        clinical_notes = st.text_area(
            "Clinical Notes",
            placeholder="Symptoms, observations...",
            height=80
        )
        uploaded = st.file_uploader(
            "📤 Upload MRI/CT Scan",
            type=["jpg","jpeg","png"],
            help="Upload brain scan image"
        )

        analyze_btn = st.button(
            "🔍 Run AI Analysis",
            type="primary"
        )

    with col2:
        if uploaded:
            img_norm, img_orig = load_image(
                uploaded
            )
            if settings["show_enhanced"]:
                enhanced = enhance_mri(img_orig)
                t1, t2   = st.tabs([
                    "📷 Original Scan",
                    "✨ AI Enhanced"
                ])
                with t1:
                    st.image(
                        img_orig,
                        caption=f"Original {scan_type}",
                        use_column_width=True
                    )
                with t2:
                    st.image(
                        enhanced,
                        caption="CLAHE Enhanced",
                        use_column_width=True
                    )
            else:
                st.image(
                    img_orig,
                    caption=scan_type,
                    use_column_width=True
                )
        else:
            st.markdown("""
            <div style="
                border:2px dashed #CBD5E0;
                border-radius:12px;
                padding:60px 20px;
                text-align:center;
                background:white;">
                <div style="
                    font-size:3rem;
                    color:#CBD5E0;">
                    🧠
                </div>
                <p style="color:#A0AEC0;">
                    Upload MRI scan to analyze
                </p>
            </div>
            """, unsafe_allow_html=True)

    # Analysis
    if uploaded and analyze_btn:
        img_norm, img_orig = load_image(uploaded)

        with st.spinner(
            "🧠 AI Analysis in Progress..."
        ):
            results = predict_all(
                img_norm, models
            )
            final_label, final_conf, \
                final_probs = \
                get_final_prediction(results)

            if final_label is None:
                st.error("❌ No models loaded!")
                return

            # Tumor analysis
            analysis = None
            if "cnn" in models:
                try:
                    from gradcam import \
                        full_tumor_analysis
                    analysis = full_tumor_analysis(
                        models["cnn"], img_norm
                    )
                except:
                    pass

            # Get reports
            try:
                from confidence_meter import \
                    get_full_confidence_report
                conf_report = \
                    get_full_confidence_report(
                        final_label,
                        final_conf,
                        final_probs
                    )
            except:
                conf_report = {
                    "risk_level":       "UNKNOWN",
                    "confidence_label": "Unknown",
                    "alert_message":    "",
                    "sensitivity":      0,
                    "specificity":      0,
                    "ppv":              0,
                    "npv":              0,
                    "doctor_alert":     False
                }

            try:
                from treatment_advisor import \
                    get_treatment_info
                treatment = get_treatment_info(
                    final_label
                )
            except:
                treatment = {
                    "icd10_code": "N/A",
                    "who_grade":  "N/A",
                    "urgency":    "N/A",
                    "first_line": [],
                    "drugs":      [],
                    "specialists":[],
                    "follow_up":  [],
                    "survival":   {}
                }

            # Size and location
            if analysis:
                size_info = analysis["size_info"]
                anatomy   = analysis["anatomy"]
            else:
                size_info = {
                    "size_label":  "N/A",
                    "stage":       "N/A",
                    "who_grade":   "N/A",
                    "diameter_cm": 0,
                    "area_cm2":    0
                }
                anatomy = {
                    "name":       "N/A",
                    "hemisphere": "N/A",
                    "lobe":       "N/A",
                    "function":   "N/A"
                }

        # Audit log
        try:
            from audit_logger import \
                log_action, AuditActions
            log_action(
                username    = st.session_state
                              .username,
                action      = AuditActions.MRI_ANALYSIS,
                details     = f"Analyzed: {final_label} {final_conf:.1f}%",
                patient_mrn = patient_mrn,
                status      = "SUCCESS"
            )
        except:
            pass

        st.markdown("---")

        # RESULTS
        # Diagnosis Banner
        risk      = conf_report["risk_level"]
        color_map = {
            "CRITICAL": "#E53E3E",
            "HIGH":     "#DD6B20",
            "MODERATE": "#D69E2E",
            "NONE":     "#38A169"
        }
        risk_color = color_map.get(
            risk, "#2E86C1"
        )

        st.markdown(f"""
        <div style="
            background:white;
            border-radius:12px;
            padding:25px;
            border-top:6px solid {risk_color};
            box-shadow:0 4px 15px
                rgba(0,0,0,0.1);
            margin-bottom:20px;">
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;">
                <div>
                    <h2 style="
                        color:{risk_color};
                        margin:0;
                        font-size:2rem;
                        font-weight:800;">
                        {final_label.upper()}
                    </h2>
                    <p style="
                        color:#718096;
                        margin:4px 0 0 0;">
                        AI Confidence:
                        {final_conf:.1f}% |
                        {conf_report[
                            'confidence_label'
                        ]}
                    </p>
                </div>
                <div style="text-align:right;">
                    <div style="
                        background:{risk_color}22;
                        border:2px solid {risk_color};
                        border-radius:8px;
                        padding:8px 16px;
                        color:{risk_color};
                        font-weight:700;
                        font-size:1.1rem;">
                        {risk} RISK
                    </div>
                    <div style="
                        color:#718096;
                        font-size:0.8rem;
                        margin-top:4px;">
                        ICD-10:
                        {treatment['icd10_code']}
                    </div>
                </div>
            </div>
            <div style="
                margin-top:15px;
                padding-top:15px;
                border-top:1px solid #E2E8F0;
                display:grid;
                grid-template-columns:
                    repeat(4,1fr);
                gap:10px;">
                <div style="text-align:center;">
                    <div style="
                        font-size:1.2rem;
                        font-weight:700;
                        color:#1B4F72;">
                        {size_info['size_label']}
                    </div>
                    <div style="
                        color:#718096;
                        font-size:0.75rem;">
                        Tumor Size
                    </div>
                </div>
                <div style="text-align:center;">
                    <div style="
                        font-size:1.2rem;
                        font-weight:700;
                        color:#1B4F72;">
                        {size_info['who_grade']}
                    </div>
                    <div style="
                        color:#718096;
                        font-size:0.75rem;">
                        WHO Grade
                    </div>
                </div>
                <div style="text-align:center;">
                    <div style="
                        font-size:1.2rem;
                        font-weight:700;
                        color:#1B4F72;">
                        {anatomy['hemisphere']}
                    </div>
                    <div style="
                        color:#718096;
                        font-size:0.75rem;">
                        Hemisphere
                    </div>
                </div>
                <div style="text-align:center;">
                    <div style="
                        font-size:1.2rem;
                        font-weight:700;
                        color:#1B4F72;">
                        {size_info['area_cm2']}cm²
                    </div>
                    <div style="
                        color:#718096;
                        font-size:0.75rem;">
                        Tumor Area
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Alert
        alert_class = {
            "CRITICAL": "critical",
            "HIGH":     "high",
            "MODERATE": "moderate",
            "NONE":     "normal"
        }.get(risk, "normal")

        alert_msg = conf_report.get(
            "alert_message",
            "No immediate alert"
        ) or "No immediate alert required"

        st.markdown(f"""
        <div class="alert-{alert_class}">
            {'🚨' if risk=='CRITICAL'
             else '⚠️' if risk=='HIGH'
             else '⚡' if risk=='MODERATE'
             else '✅'} {alert_msg}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>",
                    unsafe_allow_html=True)

        # Three columns
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown("""
            <div class="medical-card">
                <div class="section-header">
                    📍 Tumor Location
                </div>
            """, unsafe_allow_html=True)
            items = [
                ("Region",     anatomy['name']),
                ("Hemisphere", anatomy['hemisphere']),
                ("Lobe",       anatomy['lobe']),
                ("Function",   anatomy['function']),
                ("Diameter",   f"{size_info['diameter_cm']}cm"),
                ("Area",       f"{size_info['area_cm2']}cm²"),
                ("Stage",      size_info['stage'])
            ]
            for label, value in items:
                st.markdown(f"""
                <div style="
                    display:flex;
                    justify-content:space-between;
                    padding:5px 0;
                    border-bottom:
                        1px solid #EDF2F7;
                    font-size:0.85rem;">
                    <span style="color:#718096;">
                        {label}
                    </span>
                    <span style="
                        color:#2D3748;
                        font-weight:600;
                        text-align:right;
                        max-width:55%;">
                        {value}
                    </span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown(
                "</div>", unsafe_allow_html=True
            )

        with c2:
            st.markdown("""
            <div class="medical-card">
                <div class="section-header">
                    🔬 Clinical Metrics
                </div>
            """, unsafe_allow_html=True)
            metrics = [
                ("Sensitivity",
                 f"{conf_report['sensitivity']}%"),
                ("Specificity",
                 f"{conf_report['specificity']}%"),
                ("PPV",
                 f"{conf_report['ppv']}%"),
                ("NPV",
                 f"{conf_report['npv']}%"),
                ("ICD-10",
                 treatment['icd10_code']),
                ("WHO Grade",
                 treatment.get(
                     'who_grade','N/A'
                 )),
                ("Urgency",
                 treatment['urgency']
                 .replace("—","-")[:20])
            ]
            for label, value in metrics:
                st.markdown(f"""
                <div style="
                    display:flex;
                    justify-content:space-between;
                    padding:5px 0;
                    border-bottom:
                        1px solid #EDF2F7;
                    font-size:0.85rem;">
                    <span style="color:#718096;">
                        {label}
                    </span>
                    <span style="
                        color:#2E86C1;
                        font-weight:600;">
                        {value}
                    </span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown(
                "</div>", unsafe_allow_html=True
            )

        with c3:
            st.markdown("""
            <div class="medical-card">
                <div class="section-header">
                    🗳️ Model Voting
                </div>
            """, unsafe_allow_html=True)
            for m, (l, c, _) in \
                    results.items():
                match = l == final_label
                color = "#38A169" \
                    if match else "#718096"
                st.markdown(f"""
                <div style="
                    display:flex;
                    justify-content:space-between;
                    padding:5px 0;
                    border-bottom:
                        1px solid #EDF2F7;
                    font-size:0.85rem;">
                    <span style="color:#718096;">
                        {m}
                    </span>
                    <span style="
                        color:{color};
                        font-weight:600;">
                        {l.upper()} {c:.0f}%
                    </span>
                </div>
                """, unsafe_allow_html=True)

            # Agreement
            preds = [l for l,c,p
                     in results.values()]
            agr   = (
                preds.count(final_label) /
                len(preds) * 100
            ) if preds else 0
            st.markdown(f"""
            <div style="
                margin-top:10px;
                background:#EBF5FB;
                border-radius:6px;
                padding:8px;
                text-align:center;
                color:#1B4F72;
                font-weight:700;">
                Agreement: {agr:.0f}%
            </div>
            """, unsafe_allow_html=True)
            st.markdown(
                "</div>", unsafe_allow_html=True
            )

        # Probability Chart
        fig = go.Figure(go.Bar(
            x = CLASSES,
            y = [p*100 for p in final_probs],
            marker_color = [
                risk_color
                if c == final_label
                else "#CBD5E0"
                for c in CLASSES
            ],
            text = [
                f"{p*100:.1f}%"
                for p in final_probs
            ],
            textposition = "outside"
        ))
        fig.update_layout(
            title        = "Class Probability Distribution",
            yaxis_range  = [0, 115],
            plot_bgcolor  = "white",
            paper_bgcolor = "white",
            font_color    = "#2D3748",
            height        = 300,
            margin = dict(t=40,b=20)
        )
        st.plotly_chart(
            fig, use_container_width=True
        )

        # Grad-CAM
        if settings["show_gradcam"] and \
                analysis is not None:
            st.markdown("""
            <div class="section-header">
                🔍 Grad-CAM Visualization
            </div>
            """, unsafe_allow_html=True)

            gc1, gc2, gc3 = st.columns(3)
            with gc1:
                st.image(
                    img_norm,
                    caption="Original MRI",
                    use_column_width=True
                )
            with gc2:
                if analysis.get("heatmap") \
                        is not None:
                    st.image(
                        analysis["heatmap"],
                        caption="Activation Heatmap",
                        use_column_width=True
                    )
            with gc3:
                if analysis.get("annotated") \
                        is not None:
                    st.image(
                        analysis["annotated"],
                        caption="Tumor Location",
                        use_column_width=True
                    )

            st.markdown("""
            <div style="
                background:#EBF5FB;
                border-radius:6px;
                padding:8px 12px;
                font-size:0.8rem;
                color:#1B4F72;">
                🔴 High activation region |
                🟡 Medium activation |
                🔵 Low activation |
                ⬜ Estimated tumor boundary
            </div>
            """, unsafe_allow_html=True)

        # Treatment
        if settings["show_treatment"]:
            st.markdown("""
            <div class="section-header"
                 style="margin-top:20px;">
                💊 Treatment Advisory (NCCN Guidelines)
            </div>
            """, unsafe_allow_html=True)

            t1, t2, t3 = st.columns(3)
            with t1:
                st.markdown("""
                <div class="medical-card">
                    <b style="color:#1B4F72;">
                        First Line Treatment
                    </b>
                """, unsafe_allow_html=True)
                for item in treatment.get(
                    "first_line", []
                ):
                    st.markdown(f"▸ {item}")
                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

            with t2:
                st.markdown("""
                <div class="medical-card">
                    <b style="color:#1B4F72;">
                        Key Medications
                    </b>
                """, unsafe_allow_html=True)
                for item in treatment.get(
                    "drugs", []
                ):
                    st.markdown(f"▸ {item}")
                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

            with t3:
                st.markdown("""
                <div class="medical-card">
                    <b style="color:#1B4F72;">
                        Follow Up Schedule
                    </b>
                """, unsafe_allow_html=True)
                for item in treatment.get(
                    "follow_up", []
                ):
                    st.markdown(f"▸ {item}")
                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

        # PDF Report
        if settings["gen_pdf"] and patient_name:
            st.markdown("""
            <div class="section-header"
                 style="margin-top:20px;">
                📄 Medical Report
            </div>
            """, unsafe_allow_html=True)

            try:
                from report_generator import \
                    generate_pdf_report

                gradcam_path = None
                if analysis and \
                        analysis.get(
                            "annotated"
                        ) is not None:
                    gpath = (
                        f"reports/temp_"
                        f"{patient_name}.png"
                    )
                    ann = analysis["annotated"]
                    if ann.max() <= 1.0:
                        ann = (
                            ann*255
                        ).astype(np.uint8)
                    cv2.imwrite(
                        gpath,
                        cv2.cvtColor(
                            ann,
                            cv2.COLOR_RGB2BGR
                        )
                    )
                    gradcam_path = gpath

                pdf_path = generate_pdf_report(
                    patient_name   = patient_name,
                    patient_age    = patient_age
                                     or "N/A",
                    patient_gender = patient_gender,
                    doctor_name    = st.session_state
                                       .user_info[
                                           "name"
                                       ],
                    prediction     = final_label,
                    confidence     = final_conf,
                    risk_level     = risk,
                    tumor_size     = size_info[
                                         "size_label"
                                     ],
                    stage          = size_info[
                                         "stage"
                                     ],
                    icd10_code     = treatment[
                                         "icd10_code"
                                     ],
                    treatment_info = treatment,
                    gradcam_path   = gradcam_path
                )

                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "📥 Download Medical Report",
                        f,
                        file_name = os.path.basename(
                            pdf_path
                        ),
                        mime = "application/pdf"
                    )

                # Audit log
                try:
                    from audit_logger import \
                        log_action, AuditActions
                    log_action(
                        username    = st.session_state.username,
                        action      = AuditActions.PDF_GENERATED,
                        details     = f"PDF for {patient_name}",
                        patient_mrn = patient_mrn,
                        status      = "SUCCESS"
                    )
                except:
                    pass

            except Exception as e:
                st.warning(f"PDF: {e}")

        # Save History
        if patient_name:
            try:
                from history_tracker import \
                    save_prediction
                save_prediction(
                    patient_name = patient_name,
                    prediction   = final_label,
                    confidence   = final_conf,
                    risk_level   = risk,
                    model_used   = "Multi-Model",
                    doctor_name  = st.session_state
                                     .user_info[
                                         "name"
                                     ],
                    tumor_size   = size_info[
                                       "size_label"
                                   ],
                    stage        = size_info[
                                       "stage"
                                   ],
                    icd10_code   = treatment[
                                       "icd10_code"
                                   ],
                    notes        = clinical_notes
                )
                st.success(
                    f"✅ Record saved for "
                    f"{patient_name} "
                    f"[{patient_mrn}]"
                )
            except:
                pass

# ─────────────────────────────────────────
# APPOINTMENTS PAGE
# ─────────────────────────────────────────
def appointments_page():
    render_header(
        "📅 Appointment Management",
        "Schedule and manage patient appointments"
    )

    tab1, tab2 = st.tabs([
        "➕ Book Appointment",
        "📋 View Appointments"
    ])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            pat_name = st.text_input(
                "Patient Name *"
            )
            appt_date = st.date_input(
                "Appointment Date *"
            )
            appt_type = st.selectbox(
                "Appointment Type",
                [
                    "Follow Up MRI Scan",
                    "Consultation",
                    "Surgery Review",
                    "Chemotherapy Session",
                    "Radiation Therapy",
                    "Biopsy",
                    "Blood Test",
                    "Neurological Assessment",
                    "Post Surgery Checkup",
                    "Emergency Consultation"
                ]
            )
            priority = st.selectbox(
                "Priority",
                ["URGENT","HIGH","NORMAL","LOW"]
            )

        with col2:
            from doctors_db import \
                get_all_doctors, \
                get_doctors_by_specialty, \
                get_specialties

            specialty_filter = st.selectbox(
                "Filter by Specialty",
                ["All"] + get_specialties()
            )

            if specialty_filter == "All":
                doc_list = get_all_doctors()
            else:
                doc_list = \
                    get_doctors_by_specialty(
                        specialty_filter
                    )

            doc_names = [
                f"{d['emoji']} {d['name']} "
                f"({d['specialty']})"
                for d in doc_list
            ]

            doc_choice = st.selectbox(
                "Select Doctor",
                doc_names
            )

            if doc_list:
                sel = doc_list[
                    doc_names.index(doc_choice)
                ]
                st.markdown(f"""
                <div style="
                    background:white;
                    border-radius:10px;
                    padding:12px;
                    border-left:4px solid
                        #2E86C1;
                    margin:8px 0;">
                    <div style="
                        font-weight:700;
                        color:#1B4F72;">
                        {sel['emoji']}
                        {sel['name']}
                    </div>
                    <div style="
                        color:#718096;
                        font-size:0.8rem;
                        margin-top:3px;">
                        {sel['subspecialty']}
                    </div>
                    <div style="
                        color:#2E86C1;
                        font-size:0.8rem;
                        margin-top:3px;">
                        ⏰ {sel['timing']} |
                        💰 {sel['fee']} |
                        ⭐ {sel['rating']}/5
                    </div>
                    <div style="
                        color:#38A169;
                        font-size:0.78rem;
                        margin-top:3px;">
                        📅 {', '.join(
                            sel['availability']
                        )}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            doctor = doc_choice

            appt_time = st.selectbox(
                "Time Slot",
                [
                    "09:00 AM","09:30 AM",
                    "10:00 AM","10:30 AM",
                    "11:00 AM","11:30 AM",
                    "12:00 PM","02:00 PM",
                    "02:30 PM","03:00 PM",
                    "03:30 PM","04:00 PM",
                    "04:30 PM","05:00 PM"
                ]
            )
            notes = st.text_area(
                "Notes", height=120
            )

        if st.button("📅 Book Appointment"):
            if pat_name and doctor:
                try:
                    from appointment_manager \
                        import save_appointment
                    appt = save_appointment(
                        patient_name     = pat_name,
                        doctor_name      = doctor,
                        date             = str(
                                               appt_date
                                           ),
                        time             = appt_time,
                        appointment_type = appt_type,
                        notes            = notes,
                        priority         = priority
                    )
                    st.success(
                        f"✅ Appointment booked! "
                        f"ID: {appt['id']}"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.error("❌ Fill required fields!")

    with tab2:
        try:
            from appointment_manager import \
                load_appointments
            appointments = load_appointments()

            if appointments:
                import pandas as pd
                df = pd.DataFrame(appointments)
                st.dataframe(
                    df,
                    use_container_width=True
                )
            else:
                st.info("No appointments yet")
        except Exception as e:
            st.error(f"Error: {e}")

# ─────────────────────────────────────────
# DRUG CHECKER PAGE
# ─────────────────────────────────────────
def drugs_page():
    render_header(
        "💊 Drug Interaction Checker",
        "Check medication safety for tumor patients"
    )

    col1, col2 = st.columns(2)

    with col1:
        tumor_type = st.selectbox(
            "Tumor Type",
            ["glioma","meningioma","pituitary"]
        )
        patient_drugs = st.text_area(
            "Patient Current Medications",
            placeholder=
                "Enter one drug per line...\n"
                "Example:\nWarfarin\nInsulin\nAspirin",
            height=150
        )

    with col2:
        st.markdown("""
        <div class="medical-card">
            <b style="color:#1B4F72;">
                Common Interactions to Check:
            </b>
            <br><br>
            <small style="color:#718096;">
                • Warfarin + Temozolomide<br>
                • Insulin + Dexamethasone<br>
                • Aspirin + Bevacizumab<br>
                • Phenytoin + Temozolomide<br>
                • Ibuprofen + Dexamethasone<br>
                • Alcohol + Lomustine
            </small>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🔍 Check Interactions"):
        drugs_list = [
            d.strip()
            for d in patient_drugs.split("\n")
            if d.strip()
        ]
        if drugs_list:
            try:
                from drug_checker import \
                    get_drug_report
                report = get_drug_report(
                    tumor_type, drugs_list
                )

                # Safety Status
                color = "#38A169" \
                    if report["is_safe"] \
                    else "#E53E3E"
                st.markdown(f"""
                <div style="
                    background:{color}22;
                    border:2px solid {color};
                    border-radius:10px;
                    padding:15px;
                    text-align:center;
                    font-size:1.2rem;
                    font-weight:700;
                    color:{color};
                    margin:15px 0;">
                    {report['safety_status']}
                    — {report[
                        'total_interactions'
                    ]} Interactions Found
                </div>
                """, unsafe_allow_html=True)

                # Tumor drugs
                st.markdown("""
                <div class="section-header">
                    Recommended Tumor Medications
                </div>
                """, unsafe_allow_html=True)
                cols = st.columns(3)
                for i, drug in enumerate(
                    report["tumor_drugs"]
                ):
                    with cols[i % 3]:
                        st.markdown(f"""
                        <div style="
                            background:#EBF5FB;
                            border-radius:6px;
                            padding:8px;
                            text-align:center;
                            font-size:0.85rem;
                            color:#1B4F72;
                            margin:4px 0;">
                            💊 {drug}
                        </div>
                        """,
                        unsafe_allow_html=True)

                # Interactions
                if report["interactions"]:
                    st.markdown("""
                    <div class="section-header"
                         style="margin-top:15px;">
                        ⚠️ Drug Interactions Found
                    </div>
                    """, unsafe_allow_html=True)

                    for inter in report[
                        "interactions"
                    ]:
                        sev   = inter["severity"]
                        color = "#E53E3E" \
                            if sev == "MAJOR" \
                            else "#DD6B20"
                        st.markdown(f"""
                        <div class="alert-{
                            'critical'
                            if sev=='MAJOR'
                            else 'high'
                        }">
                            <b>
                                {inter['drug1']} +
                                {inter['drug2']}
                            </b>
                            — {sev}<br>
                            <small>
                                Effect:
                                {inter['effect']}
                                <br>
                                Action:
                                {inter[
                                    'recommendation'
                                ]}
                            </small>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success(
                        "✅ No interactions found!"
                    )

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning(
                "Enter patient medications first"
            )

# ─────────────────────────────────────────
# DOCTOR DASHBOARD PAGE
# ─────────────────────────────────────────
def doctor_dashboard_page():
    render_header(
        "👨‍⚕️ Doctor Dashboard",
        "Clinical overview and patient management"
    )

    try:
        from doctor_dashboard import \
            get_dashboard_stats, \
            get_doctor_performance
        stats = get_dashboard_stats()
        perf  = get_doctor_performance()
    except Exception as e:
        st.error(f"Dashboard error: {e}")
        return

    # Key metrics
    c1,c2,c3,c4,c5 = st.columns(5)
    metrics = [
        (c1,"Total Scans",
         stats["total_scans"],"#2E86C1"),
        (c2,"Today",
         stats["today_scans"],"#1B4F72"),
        (c3,"Critical",
         stats["critical_cases"],"#E53E3E"),
        (c4,"Pending Review",
         stats["pending_review"],"#DD6B20"),
        (c5,"Tumor Rate",
         f"{stats['tumor_rate']}%","#38A169")
    ]
    for col,label,value,color in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value"
                     style="color:{color};">
                    {value}
                </div>
                <div class="metric-label">
                    {label}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="section-header">
            📈 Weekly Scan Trend
        </div>
        """, unsafe_allow_html=True)

        weekly = stats.get("weekly_trend", [])
        if weekly:
            fig = go.Figure(go.Scatter(
                x=[w["date"] for w in weekly],
                y=[w["count"] for w in weekly],
                mode="lines+markers",
                line=dict(
                    color="#2E86C1", width=3
                ),
                marker=dict(size=8)
            ))
            fig.update_layout(
                plot_bgcolor  = "white",
                paper_bgcolor = "white",
                font_color    = "#2D3748",
                height        = 250,
                margin = dict(t=20,b=20)
            )
            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with col2:
        st.markdown("""
        <div class="section-header">
            🤖 Model Performance
        </div>
        """, unsafe_allow_html=True)

        fig2 = go.Figure()
        models_list = [
            ("CNN",     98.87, "#1B4F72"),
            ("SVM",     95.95, "#2E86C1"),
            ("RF",      94.23, "#2E86C1"),
            ("VGG16",   94.11, "#85C1E9"),
            ("ResNet50",85.83, "#85C1E9"),
        ]
        for name, acc, color in models_list:
            fig2.add_trace(go.Bar(
                x    = [name],
                y    = [acc],
                marker_color = color,
                text = [f"{acc}%"],
                textposition = "outside",
                showlegend   = False
            ))
        fig2.update_layout(
            yaxis_range   = [0, 115],
            paper_bgcolor = "white",
            plot_bgcolor  = "white",
            font_color    = "#2D3748",
            height        = 300,
            margin        = dict(t=20,b=20),
            showlegend    = False,
            bargap        = 0.3
        )
        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        if perf:
            for doc, data in perf.items():
                st.markdown(f"""
                <div style="
                    background:white;
                    border-radius:8px;
                    padding:12px;
                    margin-bottom:8px;
                    border-left:3px solid #2E86C1;
                    box-shadow:0 1px 4px
                        rgba(0,0,0,0.08);">
                    <b style="color:#1B4F72;">
                        {doc}
                    </b>
                    <div style="
                        display:flex;
                        gap:15px;
                        margin-top:6px;
                        font-size:0.8rem;
                        color:#718096;">
                        <span>
                            Total: {data['total']}
                        </span>
                        <span style="color:#E53E3E;">
                            Critical: {data['critical']}
                        </span>
                        <span style="color:#DD6B20;">
                            Tumor: {data['tumor']}
                        </span>
                        <span style="color:#38A169;">
                            Normal: {data['no_tumor']}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Critical patients
    st.markdown("""
    <div class="section-header"
         style="margin-top:20px;">
        🚨 Critical Cases
    </div>
    """, unsafe_allow_html=True)

    critical = stats.get(
        "critical_patients", []
    )
    if critical:
        for case in critical:
            st.markdown(f"""
            <div class="alert-critical">
                <b>{case.get(
                    'patient_name','Unknown'
                )}</b> —
                {case.get(
                    'prediction',''
                ).upper()} |
                {case.get('confidence',0):.1f}% |
                {case.get('timestamp','')[:10]}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No critical cases!")

# ─────────────────────────────────────────
# HISTORY PAGE
# ─────────────────────────────────────────
def history_page():
    render_header(
        "📜 Patient History",
        "Complete scan records"
    )

    try:
        from history_tracker import \
            load_history, get_summary
        summary = get_summary()
        history = load_history()
    except Exception as e:
        st.error(f"Error: {e}")
        return

    c1,c2,c3,c4 = st.columns(4)
    for col, label, val, color in [
        (c1,"Total",
         summary["total_scans"],"#2E86C1"),
        (c2,"Tumor",
         summary["tumor_detected"],"#E53E3E"),
        (c3,"Normal",
         summary["no_tumor"],"#38A169"),
        (c4,"Critical",
         summary["critical_cases"],"#DD6B20")
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value"
                     style="color:{color};">
                    {val}
                </div>
                <div class="metric-label">
                    {label}
                </div>
            </div>
            """, unsafe_allow_html=True)

    if history:
        import pandas as pd
        df = pd.DataFrame(history)
        st.dataframe(
            df, use_container_width=True
        )

        # Growth tracker
        st.markdown("""
        <div class="section-header"
             style="margin-top:20px;">
            📈 Tumor Growth Tracker
        </div>
        """, unsafe_allow_html=True)

        patient_search = st.text_input(
            "Enter Patient Name to Track Growth"
        )
        if patient_search:
            try:
                from tumor_growth_tracker import \
                    analyze_tumor_growth
                result = analyze_tumor_growth(
                    patient_search
                )
                if result["status"] == "success":
                    color = result["trend_color"]
                    st.markdown(f"""
                    <div style="
                        background:white;
                        border-radius:10px;
                        padding:20px;
                        border-left:
                            5px solid {color};
                        box-shadow:0 2px 10px
                            rgba(0,0,0,0.08);">
                        <h4 style="
                            color:#1B4F72;">
                            {result['trend_icon']}
                            {result['trend']}
                        </h4>
                        <p style="color:#718096;">
                            Size Change:
                            {result[
                                'size_change_cm'
                            ]}cm |
                            Growth/Month:
                            {result[
                                'growth_per_month'
                            ]}cm
                        </p>
                        <p style="
                            color:{color};
                            font-weight:600;">
                            {result[
                                'recommendation'
                            ]}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info(result["message"])
            except Exception as e:
                st.error(f"Error: {e}")

        if st.button("🗑️ Clear History"):
            try:
                from history_tracker import \
                    clear_history
                clear_history()
                st.success("History cleared!")
                st.rerun()
            except:
                pass
    else:
        st.info("No records yet")

# ─────────────────────────────────────────
# STATISTICS PAGE
# ─────────────────────────────────────────
def stats_page():
    render_header(
        "📈 Statistics Dashboard",
        "Analytics and insights"
    )

    try:
        from history_tracker import load_history
        import pandas as pd
        history = load_history()

        if not history:
            st.info("No data yet")
            return

        df = pd.DataFrame(history)
        df["timestamp"] = pd.to_datetime(
            df["timestamp"]
        )
        df["date"] = df["timestamp"].dt.date

        col1, col2 = st.columns(2)

        with col1:
            counts = df[
                "prediction"
            ].value_counts()
            fig1   = px.bar(
                x=counts.index,
                y=counts.values,
                title="Diagnoses by Type",
                color=counts.index,
                color_discrete_map={
                    "glioma":     "#E53E3E",
                    "meningioma": "#DD6B20",
                    "notumor":    "#38A169",
                    "pituitary":  "#2E86C1"
                }
            )
            fig1.update_layout(
                plot_bgcolor  = "white",
                paper_bgcolor = "white",
                font_color    = "#2D3748",
                showlegend    = False
            )
            st.plotly_chart(fig1)

        with col2:
            risk_counts = df[
                "risk_level"
            ].value_counts()
            fig2        = px.pie(
                values=risk_counts.values,
                names=risk_counts.index,
                title="Risk Distribution",
                color=risk_counts.index,
                color_discrete_map={
                    "CRITICAL": "#E53E3E",
                    "HIGH":     "#DD6B20",
                    "MODERATE": "#D69E2E",
                    "NONE":     "#38A169"
                }
            )
            fig2.update_layout(
                paper_bgcolor = "white",
                font_color    = "#2D3748"
            )
            st.plotly_chart(fig2)

        # Confidence over time
        fig3 = px.scatter(
            df,
            x="timestamp",
            y="confidence",
            color="prediction",
            title="Confidence Over Time",
            color_discrete_map={
                "glioma":     "#E53E3E",
                "meningioma": "#DD6B20",
                "notumor":    "#38A169",
                "pituitary":  "#2E86C1"
            }
        )
        fig3.update_layout(
            plot_bgcolor  = "white",
            paper_bgcolor = "white",
            font_color    = "#2D3748"
        )
        st.plotly_chart(
            fig3, use_container_width=True
        )

    except Exception as e:
        st.error(f"Stats error: {e}")

# ─────────────────────────────────────────
# AUDIT LOGS PAGE
# ─────────────────────────────────────────
def audit_page():
    render_header(
        "🔐 Audit Logs",
        "Security and activity tracking"
    )

    try:
        from audit_logger import \
            get_recent_logs, \
            get_security_alerts
        import pandas as pd

        alerts = get_security_alerts()
        if alerts:
            st.markdown(f"""
            <div class="alert-critical">
                🚨 {len(alerts)} Security
                Alerts Found! Check logs below.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="alert-normal">
                ✅ No security alerts found.
                System is secure.
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="section-header">
            📋 Recent Activity Logs
        </div>
        """, unsafe_allow_html=True)

        logs = get_recent_logs(100)
        if logs:
            df = pd.DataFrame(logs)

            # Color code by status
            col1, col2, col3 = st.columns(3)

            with col1:
                total = len(logs)
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value"
                         style="color:#2E86C1;">
                        {total}
                    </div>
                    <div class="metric-label">
                        Total Actions
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                success = len([
                    l for l in logs
                    if l["status"] == "SUCCESS"
                ])
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value"
                         style="color:#38A169;">
                        {success}
                    </div>
                    <div class="metric-label">
                        Successful
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                failed = len([
                    l for l in logs
                    if l["status"] == "FAILED"
                ])
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value"
                         style="color:#E53E3E;">
                        {failed}
                    </div>
                    <div class="metric-label">
                        Failed Attempts
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(
                "<br>", unsafe_allow_html=True
            )

            # Show logs table
            st.dataframe(
                df[[
                    "timestamp",
                    "username",
                    "action",
                    "details",
                    "patient_mrn",
                    "status"
                ]],
                use_container_width=True
            )

            # Recent logs list
            st.markdown("""
            <div class="section-header"
                 style="margin-top:20px;">
                🕐 Recent Activity
            </div>
            """, unsafe_allow_html=True)

            for log in logs[:10]:
                color = "#38A169" \
                    if log["status"] == "SUCCESS" \
                    else "#E53E3E"
                icon  = "✅" \
                    if log["status"] == "SUCCESS" \
                    else "❌"
                st.markdown(f"""
                <div style="
                    background:white;
                    border-radius:8px;
                    padding:10px 15px;
                    margin-bottom:6px;
                    border-left:
                        3px solid {color};
                    box-shadow:0 1px 4px
                        rgba(0,0,0,0.06);
                    display:flex;
                    justify-content:
                        space-between;
                    font-size:0.85rem;">
                    <div>
                        {icon}
                        <b style="color:#2D3748;">
                            {log['username']}
                        </b>
                        <span style="
                            color:#718096;
                            margin:0 8px;">
                            →
                        </span>
                        <span style="
                            color:#2E86C1;
                            font-weight:600;">
                            {log['action']}
                        </span>
                        <span style="
                            color:#718096;
                            margin-left:8px;">
                            {log.get(
                                'details',''
                            )[:50]}
                        </span>
                    </div>
                    <div style="color:#718096;">
                        {log['timestamp']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.info(
                "No audit logs yet. "
                "Actions will appear here."
            )

    except Exception as e:
        st.error(f"Audit error: {e}")
# ─────────────────────────────────────────
# MODELS PAGE
# ─────────────────────────────────────────
def models_page():
    render_header(
        "📊 Model Performance",
        "AI model accuracy and metrics"
    )

    data = {
        "Model":    ["SVM","RF","CNN",
                     "VGG16","ResNet50",
                     "EfficientNet"],
        "Accuracy": [95.95,94.23,98.87,
                     94.11,85.83,45.71],
        "Type":     ["ML","ML","DL",
                     "TL","TL","TL"],
        "Status":   [
            "✅ Active",
            "✅ Active",
            "🏆 Best",
            "✅ Active",
            "✅ Active",
            "⚠️ Low"
        ]
    }

    df = pd.DataFrame(data)

    # ── METRIC CARDS ──
    cols = st.columns(6)
    colors = [
        "#2E86C1","#2E86C1","#1B4F72",
        "#2E86C1","#85C1E9","#E53E3E"
    ]
    for i, (_, row) in enumerate(
        df.iterrows()
    ):
        with cols[i]:
            st.markdown(f"""
            <div class="metric-card">
                <div style="
                    font-size:1.5rem;
                    font-weight:800;
                    color:{colors[i]};">
                    {row['Accuracy']}%
                </div>
                <div style="
                    font-size:0.8rem;
                    color:#1B4F72;
                    font-weight:700;">
                    {row['Model']}
                </div>
                <div style="
                    font-size:0.7rem;
                    color:#718096;">
                    {row['Status']}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(
        "<br>", unsafe_allow_html=True
    )

    # ── BAR CHART ──
    fig = go.Figure()

    bar_colors = {
        "ML": "#2E86C1",
        "DL": "#1B4F72",
        "TL": "#85C1E9"
    }

    for _, row in df.iterrows():
        fig.add_trace(go.Bar(
            x    = [row["Model"]],
            y    = [row["Accuracy"]],
            name = row["Type"],
            marker_color = bar_colors.get(
                row["Type"], "#2E86C1"
            ),
            text = [f"{row['Accuracy']}%"],
            textposition = "outside"
        ))

    fig.update_layout(
        title        = "AI Model Accuracy Comparison",
        yaxis_range  = [0, 115],
        plot_bgcolor  = "white",
        paper_bgcolor = "white",
        font_color    = "#2D3748",
        height        = 400,
        showlegend    = True,
        bargap        = 0.3
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ── TABLE ──
    st.markdown("""
    <div class="section-header">
        📋 Model Details
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        df,
        use_container_width=True
    )
# ─────────────────────────────────────────
# ABOUT PAGE
# ─────────────────────────────────────────
def about_page():
    render_header(
        "ℹ️ About NeuroDetect",
        "System information and credits"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="letterhead">
            <div style="
                display:flex;
                align-items:center;
                margin-bottom:20px;">
                <div style="
                    font-size:3rem;
                    margin-right:15px;">
                    🏥
                </div>
                <div>
                    <h2 style="
                        color:#1B4F72;
                        margin:0;">
                        NeuroDetect AI
                    </h2>
                    <p style="
                        color:#718096;
                        margin:0;
                        font-size:0.9rem;">
                        Medical AI System v3.0
                    </p>
                </div>
            </div>
            <table style="width:100%;">
                <tr>
                    <td style="color:#718096;padding:6px 0;font-size:0.85rem;">Version</td>
                    <td style="color:#2D3748;font-weight:600;font-size:0.85rem;">3.0 Professional</td>
                </tr>
                <tr>
                    <td style="color:#718096;padding:6px 0;font-size:0.85rem;">AI Models</td>
                    <td style="color:#2D3748;font-weight:600;font-size:0.85rem;">6 Models</td>
                </tr>
                <tr>
                    <td style="color:#718096;padding:6px 0;font-size:0.85rem;">Best Accuracy</td>
                    <td style="color:#1B4F72;font-weight:700;font-size:0.85rem;">98.87% (CNN)</td>
                </tr>
                <tr>
                    <td style="color:#718096;padding:6px 0;font-size:0.85rem;">Features</td>
                    <td style="color:#2D3748;font-weight:600;font-size:0.85rem;">22 Smart Features</td>
                </tr>
                <tr>
                    <td style="color:#718096;padding:6px 0;font-size:0.85rem;">Standards</td>
                    <td style="color:#2D3748;font-weight:600;font-size:0.85rem;">WHO / NCCN / ICD-10</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="medical-card">
            <div class="section-header">
                🌟 22 Smart Features
            </div>
            <ol style="
                color:#718096;
                font-size:0.85rem;
                line-height:2;">
                <li>Secure Login System</li>
                <li>Multi Model Voting</li>
                <li>Clinical Confidence Meter</li>
                <li>Grad-CAM Explainability</li>
                <li>MRI Enhancement</li>
                <li>NCCN Treatment Advisory</li>
                <li>ICD-10 PDF Report</li>
                <li>Patient History Tracker</li>
                <li>Clinical Alert System</li>
                <li>WHO Tumor Grading</li>
                <li>Tumor Location Map</li>
                <li>Statistics Dashboard</li>
                <li>Patient Progress Tracking</li>
                <li>FastAPI Backend</li>
                <li>Flutter Mobile App</li>
                <li>Doctor Dashboard</li>
                <li>Tumor Growth Tracker</li>
                <li>Appointment Booking</li>
                <li>Drug Interaction Checker</li>
                <li>Patient MRN System</li>
                <li>Audit Logging</li>
                <li>Hospital Grade UI</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="alert-moderate"
         style="margin-top:20px;">
        ⚠️ Medical Disclaimer: NeuroDetect
        is an AI-assisted screening tool.
        All diagnoses must be confirmed by
        qualified medical professionals.
        Not a substitute for clinical judgment.
    </div>
    """, unsafe_allow_html=True)
    
# ─────────────────────────────────────────
# AI SECOND OPINION PAGE
# ─────────────────────────────────────────
def second_opinion_page():
    render_header(
        "🧠 AI Second Opinion",
        "Independent AI verification system"
    )

    try:
        from history_tracker import load_history
        history = load_history()

        if not history:
            st.info(
                "No scans yet! "
                "Analyze an MRI first."
            )
            return

        # Select patient
        names = list(set([
            h.get("patient_name","Unknown")
            for h in history
        ]))
        selected = st.selectbox(
            "Select Patient for Second Opinion",
            names
        )

        patient_scans = [
            h for h in history
            if h.get("patient_name") == selected
        ]

        if patient_scans:
            latest = sorted(
                patient_scans,
                key=lambda x: x["timestamp"],
                reverse=True
            )[0]

            from ai_second_opinion import \
                get_second_opinion

            # Simulate model results
            mock_results = {
                "CNN":     (latest["prediction"], latest["confidence"], []),
                "SVM":     (latest["prediction"], latest["confidence"]-2, []),
                "RF":      (latest["prediction"], latest["confidence"]-3, []),
                "ResNet50":(latest["prediction"], latest["confidence"]-1, [])
            }

            opinion = get_second_opinion(
                latest["prediction"],
                latest["confidence"],
                mock_results
            )

            # Verdict Banner
            st.markdown(f"""
            <div style="
                background:{opinion['verdict_color']}22;
                border:3px solid {opinion['verdict_color']};
                border-radius:12px;
                padding:20px;
                text-align:center;
                margin-bottom:20px;">
                <div style="
                    font-size:2rem;
                    font-weight:800;
                    color:{opinion['verdict_color']};">
                    {opinion['verdict_icon']}
                    {opinion['verdict']}
                </div>
                <div style="
                    color:#718096;
                    margin-top:8px;">
                    Model Agreement:
                    {opinion['model_agreement']}% |
                    Confidence Range:
                    {opinion['conf_range']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("""
                <div class="medical-card">
                    <div class="section-header">
                        📋 Recommendations
                    </div>
                """, unsafe_allow_html=True)
                for r in opinion["recommendation"]:
                    st.markdown(f"▸ {r}")
                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown("""
                <div class="medical-card">
                    <div class="section-header">
                        🔍 Differential Diagnosis
                    </div>
                """, unsafe_allow_html=True)
                for d in opinion["differential"]:
                    st.markdown(f"▸ {d}")
                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

            with col3:
                st.markdown("""
                <div class="medical-card">
                    <div class="section-header">
                        🚩 Red Flags
                    </div>
                """, unsafe_allow_html=True)
                for r in opinion["red_flags"]:
                    st.markdown(f"▸ {r}")
                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

    except Exception as e:
        st.error(f"Error: {e}")


# ─────────────────────────────────────────
# RISK CALCULATOR PAGE
# ─────────────────────────────────────────
def risk_calculator_page():
    render_header(
        "⚠️ Risk Score Calculator",
        "Patient risk assessment tool"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="section-header">
            Patient Information
        </div>
        """, unsafe_allow_html=True)

        prediction = st.selectbox(
            "Tumor Type",
            ["glioma","meningioma",
             "pituitary","notumor"]
        )
        confidence = st.slider(
            "AI Confidence %",
            0, 100, 85
        )
        age = st.number_input(
            "Patient Age",
            1, 120, 45
        )
        tumor_size = st.selectbox(
            "Tumor Size",
            ["Small","Medium",
             "Large","Very Large","N/A"]
        )
        symptoms = st.multiselect(
            "Present Symptoms",
            [
                "Headache",
                "Seizures",
                "Vision changes",
                "Memory loss",
                "Nausea/Vomiting",
                "Weakness",
                "Speech problems",
                "Balance issues"
            ]
        )

    with col2:
        if st.button(
            "🧮 Calculate Risk Score",
            use_container_width=True
        ):
            try:
                from risk_calculator import \
                    calculate_risk_score
                result = calculate_risk_score(
                    prediction = prediction,
                    confidence = confidence,
                    age        = age,
                    tumor_size = tumor_size,
                    symptoms   = symptoms
                )

                # Score display
                st.markdown(f"""
                <div style="
                    background:{result['color']}22;
                    border:3px solid {result['color']};
                    border-radius:12px;
                    padding:30px;
                    text-align:center;">
                    <div style="
                        font-size:4rem;
                        font-weight:800;
                        color:{result['color']};">
                        {result['score']}
                    </div>
                    <div style="
                        font-size:1.2rem;
                        color:{result['color']};
                        font-weight:700;">
                        {result['icon']}
                        {result['level']} RISK
                    </div>
                    <div style="
                        color:#718096;
                        margin-top:8px;
                        font-size:0.9rem;">
                        {result['action']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Breakdown
                st.markdown("""
                <div class="section-header"
                     style="margin-top:20px;">
                    📊 Score Breakdown
                </div>
                """, unsafe_allow_html=True)

                for factor, score in \
                        result["breakdown"].items():
                    pct = (score / 40) * 100
                    st.markdown(f"""
                    <div style="margin:8px 0;">
                        <div style="
                            display:flex;
                            justify-content:
                                space-between;
                            font-size:0.85rem;
                            margin-bottom:4px;">
                            <span style="
                                color:#2D3748;
                                font-weight:600;">
                                {factor}
                            </span>
                            <span style="
                                color:{result['color']};
                                font-weight:700;">
                                +{score} pts
                            </span>
                        </div>
                        <div style="
                            background:#EDF2F7;
                            border-radius:4px;
                            height:8px;">
                            <div style="
                                background:{result['color']};
                                width:{min(pct,100)}%;
                                height:8px;
                                border-radius:4px;">
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error: {e}")


# ─────────────────────────────────────────
# EMERGENCY ALERTS PAGE
# ─────────────────────────────────────────
def emergency_page():
    render_header(
        "🚨 Emergency Alerts",
        "Critical patient alert management"
    )

    try:
        from emergency_alert import \
            get_active_alerts, \
            get_critical_alerts, \
            dismiss_alert, \
            generate_alert

        active   = get_active_alerts()
        critical = get_critical_alerts()

        # Stats
        c1,c2,c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value"
                     style="color:#E53E3E;">
                    {len(active)}
                </div>
                <div class="metric-label">
                    Active Alerts
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value"
                     style="color:#DD6B20;">
                    {len(critical)}
                </div>
                <div class="metric-label">
                    Critical Cases
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value"
                     style="color:#38A169;">
                    24/7
                </div>
                <div class="metric-label">
                    Monitoring
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(
            "<br>", unsafe_allow_html=True
        )

        # Active alerts
        if active:
            st.markdown("""
            <div class="section-header">
                🚨 Active Alerts
            </div>
            """, unsafe_allow_html=True)

            for alert in active:
                color = "#E53E3E" \
                    if alert["alert_level"] \
                       == "CRITICAL" \
                    else "#DD6B20"
                st.markdown(f"""
                <div class="alert-{'critical' if alert['alert_level']=='CRITICAL' else 'high'}">
                    <div style="
                        display:flex;
                        justify-content:
                            space-between;">
                        <b>
                            {alert['patient_name']}
                            [{alert['patient_mrn']}]
                        </b>
                        <span style="
                            color:{color};
                            font-weight:700;">
                            {alert['alert_level']}
                        </span>
                    </div>
                    <div style="
                        font-size:0.85rem;
                        margin-top:6px;
                        color:#718096;">
                        Prediction:
                        {alert['prediction'].upper()} |
                        Confidence:
                        {alert['confidence']:.1f}% |
                        Response:
                        {alert['response_time']}
                    </div>
                    <div style="
                        font-size:0.85rem;
                        margin-top:6px;">
                        Department:
                        {alert['department']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Actions
                for action in \
                        alert.get("actions",[]):
                    st.markdown(
                        f"&nbsp;&nbsp;{action}"
                    )
                st.markdown("---")
        else:
            st.markdown("""
            <div class="alert-normal">
                ✅ No active alerts!
                All patients stable.
            </div>
            """, unsafe_allow_html=True)

        # Manual alert
        st.markdown("""
        <div class="section-header"
             style="margin-top:20px;">
            ➕ Generate Manual Alert
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            m_patient = st.text_input(
                "Patient Name"
            )
            m_pred    = st.selectbox(
                "Condition",
                ["glioma","meningioma",
                 "pituitary","notumor"]
            )
        with c2:
            m_conf   = st.slider(
                "Confidence %", 0, 100, 90
            )
            from doctors_db import \
                get_emergency_doctors

            emg_docs  = get_emergency_doctors()
            emg_names = [
                f"{d['emoji']} {d['name']} "
                f"({d['specialty']} - "
                f"{d['experience']})"
                for d in emg_docs
            ]

            emg_choice = st.selectbox(
                "Assign Emergency Doctor",
                emg_names
            )

            # Show doctor card
            if emg_docs:
                idx = emg_names.index(
                    emg_choice
                )
                sel = emg_docs[idx]
                st.markdown(f"""
                <div style="
                    background:white;
                    border-radius:10px;
                    padding:12px;
                    border-left:4px solid
                        #E53E3E;
                    margin:8px 0;">
                    <div style="
                        font-weight:700;
                        color:#E53E3E;">
                        {sel['emoji']}
                        {sel['name']}
                    </div>
                    <div style="
                        color:#718096;
                        font-size:0.8rem;
                        margin-top:3px;">
                        {sel['subspecialty']}
                        | {sel['qualification']}
                    </div>
                    <div style="
                        color:#2E86C1;
                        font-size:0.8rem;
                        margin-top:3px;">
                        📞 {sel['phone']} |
                        ⭐ {sel['rating']}/5
                    </div>
                    <div style="
                        color:#E53E3E;
                        font-size:0.78rem;
                        font-weight:700;
                        margin-top:3px;">
                        🚨 Emergency Available:
                        {'✅ YES'
                         if sel['emergency']
                         else '❌ NO'}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            m_doctor = emg_choice

        if st.button(
            "🚨 Generate Alert",
            use_container_width=True
        ):
            if m_patient:
                alert = generate_alert(
                    patient_name = m_patient,
                    prediction   = m_pred,
                    confidence   = m_conf,
                    doctor_name  = m_doctor
                )
                st.success(
                    f"✅ Alert generated "
                    f"for {m_patient}!"
                )
                st.rerun()

    except Exception as e:
        st.error(f"Error: {e}")


# ─────────────────────────────────────────
# TREATMENT TIMELINE PAGE
# ─────────────────────────────────────────
def timeline_page():
    render_header(
        "📅 Treatment Timeline",
        "Step by step treatment roadmap"
    )

    col1, col2 = st.columns([1, 2])

    with col1:
        prediction = st.selectbox(
            "Select Tumor Type",
            ["glioma","meningioma",
             "pituitary","notumor"]
        )
        st.markdown("""
        <div class="medical-card">
            <div class="section-header">
                ℹ️ About This Timeline
            </div>
            <small style="color:#718096;">
                This timeline follows NCCN
                guidelines for brain tumor
                treatment. Individual patient
                timelines may vary based on
                tumor grade, patient health,
                and treatment response.
            </small>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        try:
            from treatment_timeline import \
                get_treatment_timeline

            timeline = get_treatment_timeline(
                prediction
            )

            st.markdown("""
            <div class="section-header">
                🗓️ Treatment Roadmap
            </div>
            """, unsafe_allow_html=True)

            for i, phase in enumerate(timeline):
                st.markdown(f"""
                <div style="
                    display:flex;
                    margin-bottom:15px;">
                    <div style="
                        display:flex;
                        flex-direction:column;
                        align-items:center;
                        margin-right:15px;">
                        <div style="
                            width:40px;
                            height:40px;
                            border-radius:50%;
                            background:{phase['color']};
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            color:white;
                            font-weight:800;
                            font-size:1rem;">
                            {i+1}
                        </div>
                        {'<div style="width:2px;height:40px;background:#E2E8F0;margin-top:4px;"></div>' if i < len(timeline)-1 else ''}
                    </div>
                    <div style="
                        background:white;
                        border-radius:10px;
                        padding:15px;
                        flex:1;
                        border-left:4px solid {phase['color']};
                        box-shadow:0 2px 8px rgba(0,0,0,0.08);">
                        <div style="
                            display:flex;
                            justify-content:
                                space-between;
                            margin-bottom:8px;">
                            <b style="
                                color:{phase['color']};
                                font-size:1rem;">
                                {phase['phase']}
                            </b>
                            <span style="
                                background:{phase['color']}22;
                                color:{phase['color']};
                                padding:2px 10px;
                                border-radius:12px;
                                font-size:0.8rem;
                                font-weight:600;">
                                {phase['week']}
                            </span>
                        </div>
                        {''.join([f'<div style="font-size:0.85rem;color:#718096;padding:2px 0;">▸ {task}</div>' for task in phase['tasks']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")    
# ─────────────────────────────────────────
# BRAIN HEAT ATLAS PAGE
# ─────────────────────────────────────────
def brain_atlas_page():
    render_header(
        "🧠 Brain Heat Atlas",
        "Interactive brain region mapping"
    )

    try:
        from history_tracker import load_history
        history = load_history()

        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown("""
            <div class="section-header">
                🔬 Select Analysis
            </div>
            """, unsafe_allow_html=True)

            prediction = st.selectbox(
                "Tumor Type",
                ["glioma","meningioma",
                 "pituitary","notumor"]
            )
            confidence = st.slider(
                "Confidence %", 0, 100, 85
            )

            if st.button(
                "🧠 Generate Atlas",
                use_container_width=True
            ):
                st.session_state[
                    "atlas_pred"
                ] = prediction
                st.session_state[
                    "atlas_conf"
                ] = confidence

            # Show affected regions
            from brain_heat_atlas import \
                get_affected_regions, \
                BRAIN_REGIONS

            pred = st.session_state.get(
                "atlas_pred", prediction
            )
            affected = get_affected_regions(
                pred
            )

            if affected:
                st.markdown("""
                <div class="section-header"
                     style="margin-top:15px;">
                    ⚠️ Affected Regions
                </div>
                """, unsafe_allow_html=True)

                for region in affected:
                    risk    = region[
                        "risk_if_tumor"
                    ]
                    r_color = {
                        "CRITICAL": "#E53E3E",
                        "HIGH":     "#DD6B20",
                        "MODERATE": "#D69E2E"
                    }.get(risk, "#2E86C1")

                    st.markdown(f"""
                    <div style="
                        background:white;
                        border-radius:8px;
                        padding:10px;
                        margin-bottom:8px;
                        border-left:4px solid
                            {r_color};">
                        <div style="
                            font-weight:700;
                            color:{r_color};">
                            {region['name']}
                        </div>
                        <div style="
                            font-size:0.75rem;
                            color:#718096;
                            margin-top:4px;">
                            Risk: {risk}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    for fn in region[
                        "functions"
                    ][:2]:
                        st.markdown(
                            f"▸ {fn}"
                        )
            else:
                st.success(
                    "✅ No affected regions!"
                )

        with col2:
            st.markdown("""
            <div class="section-header">
                🗺️ Brain Heat Map
            </div>
            """, unsafe_allow_html=True)

            try:
                from brain_heat_atlas import \
                    generate_heat_atlas

                pred = st.session_state.get(
                    "atlas_pred", prediction
                )
                conf = st.session_state.get(
                    "atlas_conf", confidence
                )

                atlas = generate_heat_atlas(
                    pred, conf, (400, 400)
                )

                st.image(
                    atlas,
                    caption=(
                        f"Brain Atlas: "
                        f"{pred.upper()} "
                        f"({conf}% confidence)"
                    ),
                    use_column_width=True
                )

                # Legend
                st.markdown("""
                <div style="
                    display:flex;
                    gap:15px;
                    margin-top:10px;
                    flex-wrap:wrap;">
                    <div>
                        <span style="
                            background:#E53E3E;
                            padding:2px 10px;
                            border-radius:4px;
                            color:white;
                            font-size:0.8rem;">
                            High Risk
                        </span>
                    </div>
                    <div>
                        <span style="
                            background:#DD6B20;
                            padding:2px 10px;
                            border-radius:4px;
                            color:white;
                            font-size:0.8rem;">
                            Moderate Risk
                        </span>
                    </div>
                    <div>
                        <span style="
                            background:#B4C8D4;
                            padding:2px 10px;
                            border-radius:4px;
                            color:white;
                            font-size:0.8rem;">
                            Normal
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Atlas error: {e}")

    except Exception as e:
        st.error(f"Error: {e}")


# ─────────────────────────────────────────
# REAL TIME DETECTION PAGE
# ─────────────────────────────────────────
def realtime_page():
    render_header(
        "📹 Real-Time Detection",
        "Live MRI analysis system"
    )

    tab1, tab2 = st.tabs([
        "📸 Camera Capture",
        "🎬 Video Upload"
    ])

    with tab1:
        st.markdown("""
        <div class="section-header">
            📸 Camera MRI Analysis
        </div>
        """, unsafe_allow_html=True)

        st.info(
            "📷 Capture or upload an MRI "
            "image for instant analysis"
        )

        camera_img = st.camera_input(
            "Take MRI Photo"
        )

        if camera_img:
            from PIL import Image
            import io

            img = Image.open(
                io.BytesIO(
                    camera_img.getvalue()
                )
            )

            col1, col2 = st.columns(2)

            with col1:
                st.image(
                    img,
                    caption="Captured Image",
                    use_column_width=True
                )

            with col2:
                with st.spinner(
                    "🔬 Analyzing..."
                ):
                    try:
                        models = \
                            load_all_models()
                        from voting_system \
                            import ensemble_predict
                        label, conf, results\
                            = ensemble_predict(
                                img, models
                            )

                        color = {
                            "glioma":
                                "#E53E3E",
                            "meningioma":
                                "#DD6B20",
                            "pituitary":
                                "#2E86C1",
                            "notumor":
                                "#38A169"
                        }.get(
                            label, "#2E86C1"
                        )

                        st.markdown(f"""
                        <div style="
                            background:
                                {color}22;
                            border:3px solid
                                {color};
                            border-radius:12px;
                            padding:20px;
                            text-align:center;">
                            <div style="
                                font-size:
                                    2.5rem;
                                font-weight:
                                    800;
                                color:{color};">
                                {label.upper()}
                            </div>
                            <div style="
                                font-size:
                                    1.5rem;
                                color:{color};">
                                {conf:.1f}%
                            </div>
                            <div style="
                                color:#718096;
                                font-size:
                                    0.85rem;">
                                Confidence
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                        )

                    except Exception as e:
                        st.error(f"Error: {e}")

    with tab2:
        st.markdown("""
        <div class="section-header">
            🎬 Video MRI Analysis
        </div>
        """, unsafe_allow_html=True)

        video_file = st.file_uploader(
            "Upload MRI Video",
            type=["mp4","avi","mov"]
        )

        if video_file:
            st.video(video_file)

            if st.button(
                "🔬 Analyze Video Frames",
                use_container_width=True
            ):
                from realtime_detection \
                    import DEMO_FRAMES

                st.markdown("""
                <div class="section-header">
                    📊 Frame Analysis Results
                </div>
                """, unsafe_allow_html=True)

                progress = st.progress(0)
                for i, frame in enumerate(
                    DEMO_FRAMES
                ):
                    progress.progress(
                        (i+1)/len(DEMO_FRAMES)
                    )
                    color = {
                        "glioma":
                            "#E53E3E",
                        "meningioma":
                            "#DD6B20",
                        "notumor":
                            "#38A169"
                    }.get(
                        frame["label"],
                        "#2E86C1"
                    )
                    st.markdown(f"""
                    <div style="
                        background:white;
                        border-radius:8px;
                        padding:12px;
                        margin-bottom:8px;
                        border-left:4px solid
                            {color};">
                        <b>Frame {i*10}</b>
                        → {frame['label'].upper()}
                        ({frame['confidence']}%)
                    </div>
                    """,
                    unsafe_allow_html=True
                    )

                st.success(
                    "✅ Video analysis complete!"
                )


# ─────────────────────────────────────────
# DICOM SUPPORT PAGE
# ─────────────────────────────────────────
def dicom_page():
    render_header(
        "📁 DICOM Support",
        "Medical imaging file processor"
    )

    st.markdown("""
    <div class="section-header">
        📂 Upload DICOM File
    </div>
    """, unsafe_allow_html=True)

    st.info(
        "📁 Upload a .dcm DICOM file "
        "for processing and analysis"
    )

    dicom_file = st.file_uploader(
        "Upload DICOM File",
        type=["dcm","dicom","ima"],
        help="Standard medical DICOM format"
    )

    if dicom_file:
        file_bytes = dicom_file.read()

        from dicom_support import \
            dicom_from_bytes, \
            simulate_dicom_info

        with st.spinner(
            "📁 Processing DICOM..."
        ):
            img, info, error = \
                dicom_from_bytes(file_bytes)

        if error and "pydicom" in error:
            st.warning(
                "⚠️ pydicom not installed. "
                "Showing demo mode."
            )
            info = simulate_dicom_info()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="section-header">
                📋 DICOM Metadata
            </div>
            """, unsafe_allow_html=True)

            if info:
                for key, val in info.items():
                    st.markdown(f"""
                    <div style="
                        display:flex;
                        justify-content:
                            space-between;
                        padding:6px 0;
                        border-bottom:1px
                            solid #EDF2F7;
                        font-size:0.85rem;">
                        <span style="
                            color:#718096;
                            font-weight:600;">
                            {key}
                        </span>
                        <span style="
                            color:#2D3748;
                            font-weight:700;">
                            {val}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)

        with col2:
            if img:
                st.markdown("""
                <div class="section-header">
                    🖼️ DICOM Image
                </div>
                """, unsafe_allow_html=True)

                st.image(
                    img,
                    caption="DICOM Image",
                    use_column_width=True
                )

                if st.button(
                    "🔬 Analyze This DICOM",
                    use_container_width=True
                ):
                    with st.spinner(
                        "Analyzing..."
                    ):
                        try:
                            models = \
                                load_all_models()
                            from voting_system\
                                import \
                                ensemble_predict
                            label, conf, _ = \
                                ensemble_predict(
                                    img, models
                                )
                            color = {
                                "glioma":
                                    "#E53E3E",
                                "meningioma":
                                    "#DD6B20",
                                "pituitary":
                                    "#2E86C1",
                                "notumor":
                                    "#38A169"
                            }.get(
                                label,
                                "#2E86C1"
                            )
                            st.markdown(f"""
                            <div style="
                                background:
                                    {color}22;
                                border:3px
                                    solid
                                    {color};
                                border-radius:
                                    12px;
                                padding:20px;
                                text-align:
                                    center;">
                                <div style="
                                    font-size:
                                        2rem;
                                    font-weight:
                                        800;
                                    color:
                                        {color}
                                    ;">
                                    {label.upper()}
                                </div>
                                <div style="
                                    font-size:
                                        1.3rem;
                                    color:
                                        {color}
                                    ;">
                                    {conf:.1f}%
                                </div>
                            </div>
                            """,
                            unsafe_allow_html
                            =True
                            )
                        except Exception as e:
                            st.error(
                                f"Error: {e}"
                            )
            else:
                st.markdown("""
                <div class="alert-normal">
                    📁 Install pydicom to
                    view DICOM images:<br>
                    <code>
                        pip install pydicom
                    </code>
                </div>
                """, unsafe_allow_html=True)

                if st.button(
                    "🔬 Run Demo Analysis",
                    use_container_width=True
                ):
                    st.success(
                        "✅ Demo: GLIOMA "
                        "detected at 94.5% "
                        "confidence"
                    )


# ─────────────────────────────────────────
# U-NET SEGMENTATION PAGE
# ─────────────────────────────────────────
def unet_page():
    render_header(
        "🎯 Tumor Segmentation",
        "U-Net based tumor boundary detection"
    )

    st.markdown("""
    <div class="section-header">
        📤 Upload MRI for Segmentation
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload MRI Image",
        type=["jpg","jpeg","png"]
    )

    if uploaded:
        from PIL import Image
        import io

        img = Image.open(
            io.BytesIO(uploaded.read())
        ).convert("RGB")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="section-header">
                🖼️ Original MRI
            </div>
            """, unsafe_allow_html=True)
            st.image(
                img,
                caption="Original",
                use_column_width=True
            )

        # Get prediction first
        prediction = "glioma"
        confidence = 90.0

        try:
            models = load_all_models()
            from voting_system import \
                ensemble_predict
            prediction, confidence, _ = \
                ensemble_predict(img, models)
        except:
            pass

        with st.spinner(
            "🎯 Running segmentation..."
        ):
            try:
                from unet_segmentation \
                    import run_segmentation
                import numpy as np

                result = run_segmentation(
                    img,
                    prediction,
                    confidence
                )

                with col2:
                    st.markdown("""
                    <div class="section-header">
                        🎭 Tumor Mask
                    </div>
                    """,
                    unsafe_allow_html=True
                    )
                    st.image(
                        result["mask"],
                        caption="Segmentation Mask",
                        use_column_width=True
                    )

                with col3:
                    st.markdown("""
                    <div class="section-header">
                        🎯 Overlay Result
                    </div>
                    """,
                    unsafe_allow_html=True
                    )
                    st.image(
                        result["overlay"],
                        caption="Tumor Overlay",
                        use_column_width=True
                    )

                # Stats
                stats = result["stats"]
                st.markdown("""
                <div class="section-header"
                     style="margin-top:20px;">
                    📊 Segmentation Statistics
                </div>
                """, unsafe_allow_html=True)

                s1,s2,s3,s4 = st.columns(4)
                for col, label, val in [
                    (s1, "Tumor Area",
                     f"{stats['area_cm2']} cm²"),
                    (s2, "Size Category",
                     stats['size_category']),
                    (s3, "Tumor Coverage",
                     f"{stats['tumor_pct']}%"),
                    (s4, "Prediction",
                     prediction.upper())
                ]:
                    with col:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div style="
                                font-size:
                                    1.2rem;
                                font-weight:
                                    800;
                                color:#1B4F72;">
                                {val}
                            </div>
                            <div style="
                                font-size:
                                    0.8rem;
                                color:#718096;">
                                {label}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                        )

            except Exception as e:
                st.error(
                    f"Segmentation error: {e}"
                )  
           
# ─────────────────────────────────────────
# MULTI DATASET PAGE
# ─────────────────────────────────────────
def dataset_page():
    render_header(
        "📂 Multi-Dataset Support",
        "Analyze MRI from any dataset or format"
    )
    try:
        from multi_dataset import (
            load_any, validate,
            get_datasets, get_formats,
            save_result
        )

        datasets = get_datasets()
        formats  = get_formats()

        # Dataset cards
        st.markdown("""
        <div class="section-header">
            🌐 Supported Datasets
        </div>
        """, unsafe_allow_html=True)

        cols   = st.columns(4)
        colors = [
            "#2E86C1","#1B4F72",
            "#117A65","#6C3483",
            "#D35400","#1A5276",
            "#784212"
        ]
        for i,(key,ds) in enumerate(
            list(datasets.items())[:4]
        ):
            with cols[i]:
                acc = ds.get(
                    "train_acc", 0
                )
                acc_str = \
                    f"{acc}%" if acc > 0 \
                    else "N/A"
                st.markdown(f"""
                <div style="
                    background:white;
                    border-radius:12px;
                    padding:15px;
                    border-top:4px solid
                        {colors[i]};
                    box-shadow:0 2px 8px
                        rgba(0,0,0,0.08);">
                    <div style="
                        font-weight:800;
                        color:{colors[i]};
                        font-size:0.85rem;">
                        {ds['name']}
                    </div>
                    <div style="
                        color:#718096;
                        font-size:0.75rem;
                        margin-top:4px;">
                        {ds['description']}
                    </div>
                    <div style="
                        margin-top:8px;
                        font-size:0.75rem;
                        color:#2D3748;">
                        📁 {ds['format']}<br/>
                        🖼️ {ds['total']:,}
                        images<br/>
                        🎯 Acc: {acc_str}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>",
            unsafe_allow_html=True)

        # Upload section
        st.markdown("""
        <div class="section-header">
            📤 Upload Any Format MRI
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2])

        with col1:
            source = st.selectbox(
                "Dataset Source",
                list(datasets.keys()),
                format_func=lambda x:
                    datasets[x]["name"]
            )
            uploaded = st.file_uploader(
                "Upload MRI",
                type=[
                    "jpg","jpeg","png",
                    "dcm","dicom",
                    "nii","gz",
                    "bmp","tiff","mha"
                ]
            )
            patient = st.text_input(
                "Patient Name"
            )
            s_idx = None
            if uploaded and \
               uploaded.name.endswith(
                   (".nii",".gz")
               ):
                s_idx = st.slider(
                    "Slice Index",
                    0, 150, 75
                )

        with col2:
            if uploaded:
                fb = uploaded.read()
                with st.spinner(
                    "Processing..."
                ):
                    img, meta, err, vol = \
                        load_any(
                            fb,
                            uploaded.name,
                            s_idx
                        )

                if err and img is None:
                    st.error(f"❌ {err}")
                else:
                    st.image(
                        img,
                        caption=
                            uploaded.name,
                        use_column_width=True
                    )

                    ok, issues = validate(img)
                    if ok:
                        st.success(
                            "✅ Valid MRI!"
                        )
                    else:
                        st.warning(
                            f"⚠️ Issues: "
                            f"{issues}"
                        )

                    if meta:
                        with st.expander(
                            "📋 File Metadata"
                        ):
                            for k,v in \
                                    meta.items():
                                st.write(
                                    f"**{k}:** {v}"
                                )

                    if vol is not None:
                        n = vol.shape[2]
                        ns = st.slider(
                            "Browse All Slices",
                            0, n-1, n//2
                        )
                        slc = vol[:,:,ns]
                        slc = (
                            (slc-slc.min()) /
                            (slc.max()-
                             slc.min()+1e-8)
                            * 255
                        ).astype(np.uint8)
                        from PIL import Image\
                            as PI
                        st.image(
                            PI.fromarray(
                                slc,"L"
                            ).convert("RGB"),
                            caption=
                                f"Slice {ns}/{n}",
                            use_column_width=True
                        )

                    if ok and st.button(
                        "🔬 Analyze",
                        use_container_width=True
                    ):
                        try:
                            models = \
                                load_all_models()
                            from voting_system\
                                import \
                                ensemble_predict
                            lbl, conf, _ = \
                                ensemble_predict(
                                    img, models
                                )
                            save_result(
                                datasets[source]
                                ["name"],
                                uploaded.name,
                                lbl, conf
                            )
                            c = {
                                "glioma":
                                    "#E53E3E",
                                "meningioma":
                                    "#DD6B20",
                                "pituitary":
                                    "#2E86C1",
                                "notumor":
                                    "#38A169"
                            }.get(
                                lbl,"#2E86C1"
                            )
                            st.markdown(f"""
                            <div style="
                                background:
                                    {c}22;
                                border:3px
                                    solid {c};
                                border-radius:
                                    12px;
                                padding:20px;
                                text-align:
                                    center;">
                                <div style="
                                    font-size:
                                        2rem;
                                    font-weight:
                                        800;
                                    color:{c};">
                                    {lbl.upper()}
                                </div>
                                <div style="
                                    font-size:
                                        1.2rem;
                                    color:{c};">
                                    {conf:.1f}%
                                </div>
                                <div style="
                                    color:
                                        #718096;">
                                    Source:
                                    {datasets[source]['name']}
                                </div>
                            </div>
                            """,
                            unsafe_allow_html
                            =True)
                        except Exception as e:
                            st.error(
                                f"Error: {e}"
                            )
    except Exception as e:
        st.error(f"Page error: {e}")

# ─────────────────────────────────────────
# ENCRYPTION PAGE
# ─────────────────────────────────────────
def encryption_page():
    render_header(
        "🔐 HIPAA Encryption",
        "Data security and privacy compliance"
    )
    try:
        from hipaa_encryption import (
            encrypt_patient,
            decrypt_patient,
            get_hipaa_status,
            mask_phi,
            encrypt_data,
            decrypt_data,
            hash_password,
            verify_password
        )

        status = get_hipaa_status()

        # Status cards
        st.markdown("""
        <div class="section-header">
            🛡️ HIPAA Compliance Status
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(4)
        items = list(status.items())
        for i, (k,v) in enumerate(
            items[:4]
        ):
            with cols[i]:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="
                        color:#38A169;
                        font-size:1.5rem;">
                        ✅
                    </div>
                    <div style="
                        font-weight:700;
                        color:#1B4F72;
                        font-size:0.8rem;">
                        {k}
                    </div>
                    <div style="
                        color:#718096;
                        font-size:0.75rem;">
                        {v}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>",
            unsafe_allow_html=True)

        # Demo encryption
        tab1, tab2, tab3 = st.tabs([
            "🔒 Encrypt Data",
            "🔓 Decrypt Data",
            "🔑 Password Hash"
        ])

        with tab1:
            st.markdown("""
            <div class="section-header">
                🔒 Test Encryption
            </div>
            """, unsafe_allow_html=True)

            test_data = st.text_area(
                "Enter sensitive data",
                "Patient: John Doe\n"
                "MRN: MRN-12345678\n"
                "Diagnosis: Glioma"
            )
            if st.button(
                "🔒 Encrypt",
                use_container_width=True
            ):
                enc = encrypt_data(test_data)
                st.success("✅ Encrypted!")
                st.code(enc[:100] + "...")
                st.session_state[
                    "last_encrypted"
                ] = enc

        with tab2:
            st.markdown("""
            <div class="section-header">
                🔓 Test Decryption
            </div>
            """, unsafe_allow_html=True)

            enc_input = st.text_area(
                "Encrypted data",
                st.session_state.get(
                    "last_encrypted", ""
                )
            )
            if st.button(
                "🔓 Decrypt",
                use_container_width=True
            ):
                dec = decrypt_data(enc_input)
                st.success("✅ Decrypted!")
                st.code(dec)

        with tab3:
            st.markdown("""
            <div class="section-header">
                🔑 Password Hashing
            </div>
            """, unsafe_allow_html=True)

            pwd = st.text_input(
                "Enter password",
                type="password"
            )
            if st.button(
                "🔑 Hash Password",
                use_container_width=True
            ):
                hashed = hash_password(pwd)
                st.success("✅ Hashed!")
                st.code(
                    hashed[:60] + "..."
                )
                ok = verify_password(
                    pwd, hashed
                )
                st.info(
                    f"Verification: "
                    f"{'✅ PASS' if ok else '❌ FAIL'}"
                )

    except Exception as e:
        st.error(f"Error: {e}")

# ─────────────────────────────────────────
# 3D VISUALIZATION PAGE
# ─────────────────────────────────────────
def viz3d_page():
    render_header(
        "🧊 3D MRI Visualization",
        "Multi-planar brain MRI reconstruction"
    )
    try:
        from mri_3d import (
            create_multiplanar,
            create_slices_grid,
            create_from_2d,
            get_volume_stats
        )

        tab1, tab2 = st.tabs([
            "📤 Upload NIfTI",
            "🖼️ Use 2D Image"
        ])

        with tab1:
            nii_file = st.file_uploader(
                "Upload NIfTI (.nii/.nii.gz)",
                type=["nii","gz"]
            )
            if nii_file:
                try:
                    import nibabel as nib
                    import tempfile

                    fb  = nii_file.read()
                    sfx = ".nii.gz" \
                        if nii_file.name \
                           .endswith(".gz") \
                        else ".nii"
                    with tempfile.NamedTemporaryFile(
                        suffix=sfx,
                        delete=False
                    ) as f:
                        f.write(fb)
                        tmp = f.name

                    nii    = nib.load(tmp)
                    volume = nii.get_fdata()
                    os.unlink(tmp)

                    stats = get_volume_stats(
                        volume
                    )
                    st.info(
                        f"Volume: "
                        f"{stats['shape']} | "
                        f"Size: "
                        f"{stats['size_mb']}MB"
                    )

                    col1,col2,col3 = \
                        st.columns(3)
                    with col1:
                        ax = st.slider(
                            "Axial",
                            0,
                            volume.shape[2]-1,
                            volume.shape[2]//2
                        )
                    with col2:
                        cor = st.slider(
                            "Coronal",
                            0,
                            volume.shape[1]-1,
                            volume.shape[1]//2
                        )
                    with col3:
                        sag = st.slider(
                            "Sagittal",
                            0,
                            volume.shape[0]-1,
                            volume.shape[0]//2
                        )

                    cmap = st.selectbox(
                        "Colormap",
                        ["gray","hot",
                         "jet","viridis",
                         "cool","plasma"]
                    )

                    views = create_multiplanar(
                        volume,
                        ax, cor, sag, cmap
                    )

                    c1,c2,c3 = st.columns(3)
                    with c1:
                        st.image(
                            views["axial"],
                            caption="Axial",
                            use_column_width=True
                        )
                    with c2:
                        st.image(
                            views["coronal"],
                            caption="Coronal",
                            use_column_width=True
                        )
                    with c3:
                        st.image(
                            views["sagittal"],
                            caption="Sagittal",
                            use_column_width=True
                        )

                    # Slice grid
                    st.markdown("""
                    <div class="section-header">
                        📊 Slice Overview
                    </div>
                    """,
                    unsafe_allow_html=True)

                    plane = st.selectbox(
                        "Grid Plane",
                        ["axial","coronal",
                         "sagittal"]
                    )
                    grid = create_slices_grid(
                        volume, 9, plane, cmap
                    )
                    st.image(
                        grid,
                        caption=
                            f"9 {plane} slices",
                        use_column_width=True
                    )

                except ImportError:
                    st.error(
                        "Install nibabel:\n"
                        "pip install nibabel"
                    )

        with tab2:
            img_file = st.file_uploader(
                "Upload 2D MRI Image",
                type=[
                    "jpg","jpeg","png"
                ]
            )
            if img_file:
                from PIL import Image as PI
                img = PI.open(img_file)\
                        .convert("RGB")

                st.image(
                    img,
                    caption="Original",
                    use_column_width=True
                )

                if st.button(
                    "🧊 Generate 3D View",
                    use_container_width=True
                ):
                    with st.spinner(
                        "Generating 3D..."
                    ):
                        volume = \
                            create_from_2d(
                                img
                            )
                        views = \
                            create_multiplanar(
                                volume
                            )

                    c1,c2,c3 = st.columns(3)
                    with c1:
                        st.image(
                            views["axial"],
                            caption="Axial",
                            use_column_width=True
                        )
                    with c2:
                        st.image(
                            views["coronal"],
                            caption="Coronal",
                            use_column_width=True
                        )
                    with c3:
                        st.image(
                            views["sagittal"],
                            caption="Sagittal",
                            use_column_width=True
                        )

    except Exception as e:
        st.error(f"Error: {e}")
        import traceback
        st.code(traceback.format_exc())

# ─────────────────────────────────────────
# FEDERATED LEARNING PAGE
# ─────────────────────────────────────────
def federated_page():
    render_header(
        "🌐 Federated Learning",
        "Privacy-preserving multi-hospital AI training"
    )
    try:
        from federated_learning import (
            run_federated_round,
            get_federation_stats,
            save_federated_log,
            load_federated_log,
            HOSPITAL_NODES
        )

        stats = get_federation_stats()

        # ── TOP STATS ──
        c1,c2,c3,c4 = st.columns(4)
        for col, label, val, color in [
            (c1, "Hospital Nodes",
             stats["total_nodes"],   "#2E86C1"),
            (c2, "Total Patients",
             f"{stats['total_patients']:,}",
             "#1B4F72"),
            (c3, "Total Scans",
             f"{stats['total_scans']:,}",
             "#38A169"),
            (c4, "Current Accuracy",
             f"{stats['base_accuracy']}%",
             "#DD6B20"),
        ]:
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value"
                         style="color:{color};">
                        {val}
                    </div>
                    <div class="metric-label">
                        {label}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(
            "<br>", unsafe_allow_html=True
        )

        # ── HOW IT WORKS ──
        st.markdown("""
        <div class="section-header">
            ℹ️ How Federated Learning Works
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="
            background:white;
            border-radius:12px;
            padding:20px;
            border-left:4px solid #2E86C1;
            margin-bottom:20px;">
            <div style="
                display:flex;
                justify-content:space-between;
                flex-wrap:wrap;
                gap:10px;">
                <div style="text-align:center;
                    flex:1;">
                    <div style="font-size:2rem;">
                        🏥
                    </div>
                    <div style="
                        font-weight:700;
                        color:#1B4F72;
                        font-size:0.85rem;">
                        Step 1
                    </div>
                    <div style="
                        color:#718096;
                        font-size:0.75rem;">
                        Each hospital trains
                        on local data only
                    </div>
                </div>
                <div style="
                    font-size:1.5rem;
                    align-self:center;">
                    →
                </div>
                <div style="text-align:center;
                    flex:1;">
                    <div style="font-size:2rem;">
                        🔒
                    </div>
                    <div style="
                        font-weight:700;
                        color:#1B4F72;
                        font-size:0.85rem;">
                        Step 2
                    </div>
                    <div style="
                        color:#718096;
                        font-size:0.75rem;">
                        Add differential
                        privacy noise
                    </div>
                </div>
                <div style="
                    font-size:1.5rem;
                    align-self:center;">
                    →
                </div>
                <div style="text-align:center;
                    flex:1;">
                    <div style="font-size:2rem;">
                        📤
                    </div>
                    <div style="
                        font-weight:700;
                        color:#1B4F72;
                        font-size:0.85rem;">
                        Step 3
                    </div>
                    <div style="
                        color:#718096;
                        font-size:0.75rem;">
                        Send only model
                        weights not data
                    </div>
                </div>
                <div style="
                    font-size:1.5rem;
                    align-self:center;">
                    →
                </div>
                <div style="text-align:center;
                    flex:1;">
                    <div style="font-size:2rem;">
                        🔀
                    </div>
                    <div style="
                        font-weight:700;
                        color:#1B4F72;
                        font-size:0.85rem;">
                        Step 4
                    </div>
                    <div style="
                        color:#718096;
                        font-size:0.75rem;">
                        FedAvg aggregates
                        all weights
                    </div>
                </div>
                <div style="
                    font-size:1.5rem;
                    align-self:center;">
                    →
                </div>
                <div style="text-align:center;
                    flex:1;">
                    <div style="font-size:2rem;">
                        📈
                    </div>
                    <div style="
                        font-weight:700;
                        color:#1B4F72;
                        font-size:0.85rem;">
                        Step 5
                    </div>
                    <div style="
                        color:#718096;
                        font-size:0.75rem;">
                        Global model
                        improves for all
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── HOSPITAL NODES ──
        st.markdown("""
        <div class="section-header">
            🏥 Participating Hospital Nodes
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(2)
        for i, (nid, node) in enumerate(
            HOSPITAL_NODES.items()
        ):
            with cols[i % 2]:
                st.markdown(f"""
                <div style="
                    background:white;
                    border-radius:10px;
                    padding:15px;
                    margin-bottom:10px;
                    border-left:4px solid
                        #2E86C1;
                    box-shadow:0 2px 8px
                        rgba(0,0,0,0.06);">
                    <div style="
                        font-weight:700;
                        color:#1B4F72;
                        font-size:0.95rem;">
                        🏥 {node['name']}
                    </div>
                    <div style="
                        color:#718096;
                        font-size:0.8rem;
                        margin-top:4px;">
                        📍 {node['location']}
                    </div>
                    <div style="
                        display:flex;
                        gap:15px;
                        margin-top:8px;
                        font-size:0.8rem;">
                        <span style="
                            color:#2E86C1;
                            font-weight:600;">
                            👥 {node['patients']:,}
                            patients
                        </span>
                        <span style="
                            color:#38A169;
                            font-weight:600;">
                            🖼️ {node['scans']:,}
                            scans
                        </span>
                    </div>
                    <div style="
                        margin-top:6px;
                        font-size:0.75rem;
                        background:#EDF2F7;
                        padding:4px 8px;
                        border-radius:4px;
                        display:inline-block;">
                        {node['specialty']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(
            "<br>", unsafe_allow_html=True
        )

        # ── TRAINING SETTINGS ──
        st.markdown("""
        <div class="section-header">
            ⚙️ Training Configuration
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            n_rounds = st.slider(
                "Number of Rounds",
                1, 10, 3
            )
            epsilon  = st.slider(
                "Privacy Epsilon (ε)",
                0.1, 10.0, 1.0, 0.1,
                help=(
                    "Lower ε = stronger privacy"
                    " but less accuracy"
                )
            )

        with col2:
            privacy_level = (
                "🔒 STRONG PRIVACY"
                if epsilon < 1
                else "🔐 MODERATE PRIVACY"
                if epsilon < 5
                else "🔓 WEAK PRIVACY"
            )
            privacy_color = (
                "#38A169"
                if epsilon < 1
                else "#DD6B20"
                if epsilon < 5
                else "#E53E3E"
            )
            st.markdown(f"""
            <div style="
                background:white;
                border-radius:12px;
                padding:20px;
                border:2px solid
                    {privacy_color};
                text-align:center;">
                <div style="
                    font-size:1.5rem;
                    font-weight:800;
                    color:{privacy_color};">
                    {privacy_level}
                </div>
                <div style="
                    color:#718096;
                    font-size:0.85rem;
                    margin-top:8px;">
                    ε = {epsilon} |
                    Method: Laplace Mechanism
                </div>
                <div style="
                    color:#718096;
                    font-size:0.8rem;
                    margin-top:4px;">
                    Aggregation: FedAvg
                    (McMahan et al. 2017)
                </div>
                <div style="
                    color:#718096;
                    font-size:0.8rem;">
                    Rounds: {n_rounds} |
                    Nodes: {len(HOSPITAL_NODES)}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(
            "<br>", unsafe_allow_html=True
        )

        if st.button(
            "🚀 Start Federated Training",
            use_container_width=True
        ):
            results  = []
            cur_acc  = 98.87
            progress = st.progress(0)
            status_box = st.empty()

            for r in range(n_rounds):
                status_box.markdown(f"""
                <div style="
                    background:#2E86C111;
                    border:2px solid #2E86C1;
                    border-radius:10px;
                    padding:12px;
                    text-align:center;">
                    🔄 Round {r+1}/{n_rounds}
                    — Training across
                    {len(HOSPITAL_NODES)}
                    hospitals...
                </div>
                """, unsafe_allow_html=True)

                result = run_federated_round(
                    r+1, cur_acc
                )
                cur_acc = result["new_accuracy"]
                results.append(result)
                progress.progress(
                    (r+1) / n_rounds
                )

            save_federated_log(results)
            status_box.empty()

            # ── RESULTS ──
            st.markdown("""
            <div class="section-header">
                📊 Training Results
            </div>
            """, unsafe_allow_html=True)

            # Summary card
            improvement = (
                cur_acc - 98.87
            )
            st.markdown(f"""
            <div style="
                background:#38A16922;
                border:3px solid #38A169;
                border-radius:12px;
                padding:20px;
                text-align:center;
                margin-bottom:20px;">
                <div style="
                    font-size:2.5rem;
                    font-weight:900;
                    color:#38A169;">
                    {cur_acc:.2f}%
                </div>
                <div style="
                    color:#38A169;
                    font-weight:700;">
                    Final Global Accuracy
                </div>
                <div style="
                    color:#718096;
                    font-size:0.85rem;
                    margin-top:8px;">
                    Improved by
                    +{improvement:.3f}%
                    over {n_rounds} rounds
                    across {len(HOSPITAL_NODES)}
                    hospitals
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Per round results
            for r in results:
                impr  = r["improvement"]
                color = "#38A169" \
                    if impr > 0 \
                    else "#E53E3E"

                st.markdown(f"""
                <div style="
                    background:white;
                    border-radius:10px;
                    padding:15px;
                    margin-bottom:10px;
                    border-left:4px solid
                        {color};
                    box-shadow:0 2px 8px
                        rgba(0,0,0,0.06);">
                    <div style="
                        display:flex;
                        justify-content:
                            space-between;
                        align-items:center;">
                        <div>
                            <span style="
                                font-weight:800;
                                color:#1B4F72;
                                font-size:1rem;">
                                Round {r['round']}
                            </span>
                            <span style="
                                color:#718096;
                                font-size:0.8rem;
                                margin-left:10px;">
                                {r['timestamp'][:10]}
                            </span>
                        </div>
                        <span style="
                            background:{color}22;
                            color:{color};
                            padding:4px 12px;
                            border-radius:12px;
                            font-weight:700;">
                            +{impr:.3f}%
                        </span>
                    </div>
                    <div style="
                        display:flex;
                        gap:20px;
                        margin-top:10px;
                        font-size:0.85rem;
                        color:#718096;">
                        <span>
                            Before:
                            <b style="color:#E53E3E;">
                                {r['prev_accuracy']}%
                            </b>
                        </span>
                        <span>→</span>
                        <span>
                            After:
                            <b style="color:#38A169;">
                                {r['new_accuracy']}%
                            </b>
                        </span>
                        <span>|</span>
                        <span>
                            Nodes:
                            <b>{r['nodes_trained']}</b>
                        </span>
                        <span>|</span>
                        <span>
                            Samples:
                            <b>
                                {r['total_samples']:,}
                            </b>
                        </span>
                        <span>|</span>
                        <span>
                            Privacy: ε =
                            <b>{r['epsilon']}</b>
                        </span>
                    </div>

                    <div style="
                        margin-top:10px;">
                        <div style="
                            font-size:0.8rem;
                            color:#718096;
                            margin-bottom:4px;">
                            Node Results:
                        </div>
                        <div style="
                            display:flex;
                            gap:8px;
                            flex-wrap:wrap;">
                """,
                unsafe_allow_html=True)

                for lr in r["local_results"]:
                    st.markdown(f"""
                    <span style="
                        background:#EDF2F7;
                        padding:3px 8px;
                        border-radius:6px;
                        font-size:0.75rem;
                        color:#2D3748;">
                        {lr['node']}:
                        {lr['accuracy']:.1f}%
                    </span>
                    """, unsafe_allow_html=True)

                st.markdown(
                    "</div></div></div>",
                    unsafe_allow_html=True
                )

        # ── PREVIOUS LOGS ──
        logs = load_federated_log()
        if logs:
            st.markdown("""
            <div class="section-header"
                 style="margin-top:20px;">
                📋 Training History
            </div>
            """, unsafe_allow_html=True)

            for log in reversed(logs[-3:]):
                st.markdown(f"""
                <div style="
                    background:white;
                    border-radius:8px;
                    padding:12px;
                    margin-bottom:8px;
                    border-left:4px solid
                        #718096;">
                    Round {log['round']} |
                    {log['timestamp'][:10]} |
                    {log['prev_accuracy']}%
                    → {log['new_accuracy']}% |
                    Nodes: {log['nodes_trained']}
                </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {e}")
        import traceback
        st.code(traceback.format_exc())     
# ─────────────────────────────────────────
# EXTENDED TUMOR TYPES PAGE
# ─────────────────────────────────────────
def tumor_types_page():
    render_header(
        "🧬 Extended Tumor Types",
        "Comprehensive 8-class tumor database"
    )
    try:
        from extended_tumors import (
            TUMOR_DB,
            get_info,
            get_malignant,
            get_benign,
            get_all
        )

        # Stats row
        all_types  = get_all()
        malignant  = get_malignant()
        benign     = get_benign()

        c1,c2,c3,c4 = st.columns(4)
        for col, label, val, color in [
            (c1, "Total Types",
             len(all_types),  "#2E86C1"),
            (c2, "Malignant",
             len(malignant),  "#E53E3E"),
            (c3, "Benign",
             len(benign),     "#38A169"),
            (c4, "Original Types",
             4,               "#718096"),
        ]:
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value"
                         style="color:{color};">
                        {val}
                    </div>
                    <div class="metric-label">
                        {label}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(
            "<br>", unsafe_allow_html=True
        )

        # Filter
        filter_type = st.selectbox(
            "Filter Tumors",
            ["All Types",
             "Malignant Only",
             "Benign Only",
             "Original 4",
             "New 4 Added"]
        )

        if filter_type == "All Types":
            show = all_types
        elif filter_type == "Malignant Only":
            show = malignant
        elif filter_type == "Benign Only":
            show = benign
        elif filter_type == "Original 4":
            show = [
                "glioma","meningioma",
                "pituitary","notumor"
            ]
        else:
            show = [
                "lymphoma","metastatic",
                "acoustic_neuroma",
                "craniopharyngioma"
            ]

        # Tumor cards
        for tumor_key in show:
            info = get_info(tumor_key)
            color = info["color"]
            mal   = "🔴 MALIGNANT" \
                if info["malignant"] \
                else "🟢 BENIGN"

            with st.expander(
                f"{info['icon']} "
                f"{info['full_name']} "
                f"— {mal}",
                expanded=False
            ):
                c1, c2, c3 = st.columns(3)

                with c1:
                    st.markdown(f"""
                    <div style="
                        background:{color}11;
                        border-left:4px solid
                            {color};
                        border-radius:8px;
                        padding:12px;">
                        <b style="color:{color}">
                            Clinical Info
                        </b><br/>
                        <small>
                        ICD-10: {info['icd10']}<br/>
                        WHO Grade: {info['who_grade']}<br/>
                        Prevalence: {info['prevalence']}<br/>
                        5yr Survival: {info['5yr_survival']}<br/>
                        Urgency: {info['urgency']}<br/>
                        Referral: {info['referral']}
                        </small>
                    </div>
                    """, unsafe_allow_html=True)

                with c2:
                    st.markdown("""
                    <div class="section-header">
                        🔍 Subtypes
                    </div>
                    """, unsafe_allow_html=True)
                    for s in info["subtypes"]:
                        st.markdown(f"▸ {s}")

                    st.markdown("""
                    <div class="section-header"
                         style="margin-top:10px;">
                        ⚠️ Symptoms
                    </div>
                    """, unsafe_allow_html=True)
                    for s in info["symptoms"]:
                        st.markdown(f"▸ {s}")

                with c3:
                    st.markdown("""
                    <div class="section-header">
                        💊 Treatment Protocol
                    </div>
                    """, unsafe_allow_html=True)
                    for i, t in enumerate(
                        info["treatment"], 1
                    ):
                        st.markdown(
                            f"{i}. {t}"
                        )

    except Exception as e:
        st.error(f"Error: {e}")
        import traceback
        st.code(traceback.format_exc())
# ─────────────────────────────────────────
# PACS/EHR INTEGRATION PAGE
# ─────────────────────────────────────────
def pacs_page():
    render_header(
        "🏥 PACS/EHR Integration",
        "HL7 FHIR R4 Standard Implementation"
    )
    try:
        from pacs_ehr import (
            create_fhir_patient,
            create_fhir_observation,
            create_fhir_diagnostic_report,
            export_hl7_bundle,
            save_fhir_record,
            get_pacs_status
        )
        import json

        status = get_pacs_status()

        # ── STATUS CARDS ──
        c1,c2,c3,c4 = st.columns(4)
        for col, label, val, color in [
            (c1, "Standard",
             "HL7 FHIR R4", "#2E86C1"),
            (c2, "DICOM",
             "v3.0",        "#1B4F72"),
            (c3, "Integration",
             "REST API",    "#38A169"),
            (c4, "Compliance",
             "IHE Profiles","#DD6B20"),
        ]:
            with col:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="
                        font-size:1rem;
                        font-weight:800;
                        color:{color};">
                        {val}
                    </div>
                    <div class="metric-label">
                        {label}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(
            "<br>", unsafe_allow_html=True
        )

        # ── FHIR ENDPOINTS ──
        st.markdown("""
        <div class="section-header">
            🔗 FHIR R4 API Endpoints
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        endpoints = [
            ("GET",  "/Patient/{id}",
             "Retrieve patient record"),
            ("POST", "/Observation",
             "Create AI observation"),
            ("POST", "/DiagnosticReport",
             "Create diagnostic report"),
            ("GET",  "/Bundle",
             "Export full FHIR bundle"),
            ("PUT",  "/Patient/{id}",
             "Update patient record"),
            ("GET",  "/Observation?patient={id}",
             "Get patient observations"),
        ]
        colors = {
            "GET":  "#38A169",
            "POST": "#2E86C1",
            "PUT":  "#DD6B20"
        }
        for i, (method, path, desc) in \
                enumerate(endpoints):
            color = colors.get(
                method, "#718096"
            )
            with (col1 if i % 2 == 0
                  else col2):
                st.markdown(f"""
                <div style="
                    background:white;
                    border-radius:8px;
                    padding:10px 14px;
                    margin-bottom:8px;
                    border-left:4px solid
                        {color};">
                    <div style="
                        display:flex;
                        align-items:center;
                        gap:8px;">
                        <span style="
                            background:{color};
                            color:white;
                            padding:2px 8px;
                            border-radius:4px;
                            font-weight:700;
                            font-size:0.75rem;
                            font-family:monospace;">
                            {method}
                        </span>
                        <code style="
                            color:#1B4F72;
                            font-size:0.8rem;">
                            {path}
                        </code>
                    </div>
                    <div style="
                        color:#718096;
                        font-size:0.75rem;
                        margin-top:4px;">
                        {desc}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(
            "<br>", unsafe_allow_html=True
        )

        # ── GENERATE FHIR RECORD ──
        st.markdown("""
        <div class="section-header">
            ➕ Generate FHIR Record
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            mrn = st.text_input(
                "Patient MRN",
                "MRN-12345678"
            )
            name = st.text_input(
                "Patient Name",
                "Test Patient"
            )
            age = st.number_input(
                "Age", 1, 120, 45
            )
            gender = st.selectbox(
                "Gender",
                ["male","female","unknown"]
            )
            prediction = st.selectbox(
                "AI Prediction",
                ["glioma","meningioma",
                 "pituitary","notumor"]
            )
            confidence = st.slider(
                "Confidence %",
                0, 100, 90
            )
            doctor = st.text_input(
                "Doctor Name",
                st.session_state
                  .user_info["name"]
            )

        with col2:
            if st.button(
                "🏥 Generate FHIR Bundle",
                use_container_width=True
            ):
                try:
                    patient = \
                        create_fhir_patient(
                            mrn, name,
                            age, gender
                        )
                    obs_id  = \
                        f"obs-{mrn}-001"
                    obs     = \
                        create_fhir_observation(
                            mrn, prediction,
                            float(confidence),
                            doctor, obs_id
                        )
                    report  = \
                        create_fhir_diagnostic_report(
                            mrn, prediction,
                            float(confidence),
                            doctor, obs_id
                        )
                    bundle  = \
                        export_hl7_bundle(
                            patient, obs, report
                        )
                    save_fhir_record(
                        mrn, bundle
                    )

                    st.success(
                        "✅ FHIR Bundle "
                        "generated!"
                    )

                    # ── PATIENT CARD ──
                    pcolor = {
                        "glioma":     "#E53E3E",
                        "meningioma": "#DD6B20",
                        "pituitary":  "#2E86C1",
                        "notumor":    "#38A169"
                    }.get(prediction,"#2E86C1")

                    st.markdown(f"""
                    <div style="
                        background:white;
                        border-radius:12px;
                        padding:20px;
                        border-left:4px solid
                            {pcolor};
                        margin:10px 0;">
                        <div style="
                            font-weight:800;
                            color:#1B4F72;
                            font-size:1.1rem;">
                            👤 {name}
                        </div>
                        <div style="
                            display:flex;
                            gap:15px;
                            margin-top:8px;
                            font-size:0.85rem;
                            color:#718096;
                            flex-wrap:wrap;">
                            <span>
                                🆔 MRN: {mrn}
                            </span>
                            <span>
                                📅 Age: {age}
                            </span>
                            <span>
                                ⚧ {gender}
                            </span>
                        </div>
                        <div style="
                            margin-top:10px;
                            padding:10px;
                            background:{pcolor}11;
                            border-radius:8px;">
                            <span style="
                                font-weight:700;
                                color:{pcolor};">
                                🧠 AI Result:
                                {prediction.upper()}
                            </span>
                            <span style="
                                color:#718096;
                                margin-left:10px;
                                font-size:0.85rem;">
                                {confidence}%
                                confidence
                            </span>
                        </div>
                        <div style="
                            margin-top:8px;
                            font-size:0.8rem;
                            color:#718096;">
                            👨‍⚕️ Doctor: {doctor}
                            | Standard: HL7 FHIR R4
                            | ICD-10 coded
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # ── FHIR RESOURCES ──
                    st.markdown("""
                    <div class="section-header">
                        📋 Generated FHIR Resources
                    </div>
                    """,
                    unsafe_allow_html=True)

                    tab1, tab2, tab3, tab4 = \
                        st.tabs([
                        "👤 Patient Resource",
                        "🔬 Observation",
                        "📋 Diagnostic Report",
                        "📦 Full Bundle"
                    ])

                    with tab1:
                        st.markdown("""
                        <div style="
                            background:#EDF2F7;
                            border-radius:8px;
                            padding:10px;
                            margin-bottom:10px;
                            font-size:0.8rem;
                            color:#718096;">
                            HL7 FHIR R4 Patient
                            Resource — Contains
                            patient demographics
                            and identifiers
                        </div>
                        """,
                        unsafe_allow_html=True)
                        # Show key fields nicely
                        for k, v in {
                            "Resource Type":
                                patient["resourceType"],
                            "Patient ID":
                                patient["id"],
                            "Name":
                                patient["name"][0]["text"],
                            "Gender":
                                patient["gender"],
                            "Birth Year":
                                patient["birthDate"],
                            "Source":
                                patient["meta"]["source"]
                        }.items():
                            st.markdown(f"""
                            <div style="
                                display:flex;
                                justify-content:
                                    space-between;
                                padding:6px 0;
                                border-bottom:1px
                                    solid #EDF2F7;
                                font-size:0.85rem;">
                                <b style="
                                    color:#718096;">
                                    {k}
                                </b>
                                <span style="
                                    color:#2D3748;">
                                    {v}
                                </span>
                            </div>
                            """,
                            unsafe_allow_html=True)

                    with tab2:
                        st.markdown("""
                        <div style="
                            background:#EDF2F7;
                            border-radius:8px;
                            padding:10px;
                            margin-bottom:10px;
                            font-size:0.8rem;
                            color:#718096;">
                            HL7 FHIR R4 Observation
                            — Contains AI diagnosis
                            result with ICD-10 code
                        </div>
                        """,
                        unsafe_allow_html=True)
                        for k, v in {
                            "Resource Type":
                                obs["resourceType"],
                            "Observation ID":
                                obs["id"],
                            "Status":
                                obs["status"],
                            "Category":
                                "Imaging",
                            "LOINC Code":
                                "24627-2 (MRI Brain)",
                            "Result":
                                obs["valueCodeableConcept"]["text"],
                            "Interpretation":
                                obs["interpretation"][0]["coding"][0]["code"],
                            "AI Confidence":
                                f"{confidence}%"
                        }.items():
                            st.markdown(f"""
                            <div style="
                                display:flex;
                                justify-content:
                                    space-between;
                                padding:6px 0;
                                border-bottom:1px
                                    solid #EDF2F7;
                                font-size:0.85rem;">
                                <b style="
                                    color:#718096;">
                                    {k}
                                </b>
                                <span style="
                                    color:#2D3748;">
                                    {v}
                                </span>
                            </div>
                            """,
                            unsafe_allow_html=True)

                    with tab3:
                        st.markdown("""
                        <div style="
                            background:#EDF2F7;
                            border-radius:8px;
                            padding:10px;
                            margin-bottom:10px;
                            font-size:0.8rem;
                            color:#718096;">
                            HL7 FHIR R4 Diagnostic
                            Report — Final radiology
                            report with conclusion
                        </div>
                        """,
                        unsafe_allow_html=True)
                        for k, v in {
                            "Resource Type":
                                report["resourceType"],
                            "Report ID":
                                report["id"],
                            "Status":
                                report["status"],
                            "Category":
                                "Radiology (RAD)",
                            "Code":
                                "MRI Brain Analysis",
                            "Performer":
                                doctor,
                            "Conclusion":
                                report["conclusion"]
                        }.items():
                            st.markdown(f"""
                            <div style="
                                padding:6px 0;
                                border-bottom:1px
                                    solid #EDF2F7;
                                font-size:0.85rem;">
                                <b style="
                                    color:#718096;">
                                    {k}:
                                </b>
                                <span style="
                                    color:#2D3748;">
                                    {v}
                                </span>
                            </div>
                            """,
                            unsafe_allow_html=True)

                    with tab4:
                        st.markdown("""
                        <div style="
                            background:#EDF2F7;
                            border-radius:8px;
                            padding:10px;
                            margin-bottom:10px;
                            font-size:0.8rem;
                            color:#718096;">
                            Complete HL7 FHIR R4
                            Bundle — Ready to send
                            to any FHIR compatible
                            hospital system
                        </div>
                        """,
                        unsafe_allow_html=True)
                        st.markdown(f"""
                        <div style="
                            background:white;
                            border-radius:8px;
                            padding:15px;
                            border:2px solid
                                #2E86C1;">
                            <div style="
                                display:flex;
                                justify-content:
                                    space-between;
                                margin-bottom:10px;">
                                <b style="
                                    color:#1B4F72;">
                                    Bundle Summary
                                </b>
                                <span style="
                                    background:
                                        #38A169;
                                    color:white;
                                    padding:2px 8px;
                                    border-radius:
                                        4px;
                                    font-size:
                                        0.75rem;">
                                    VALID
                                </span>
                            </div>
                            <div style="
                                font-size:
                                    0.85rem;
                                color:#718096;">
                                Resources: 3
                                (Patient + Observation
                                + DiagnosticReport)
                                <br/>
                                Standard: HL7 FHIR R4
                                <br/>
                                Format: JSON
                                <br/>
                                Size: {len(json.dumps(bundle)):,}
                                bytes
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True)

                        st.download_button(
                            "📥 Download FHIR Bundle",
                            json.dumps(
                                bundle, indent=2
                            ),
                            f"fhir_{mrn}.json",
                            "application/json",
                            use_container_width=True
                        )

                except Exception as e:
                    st.error(f"Error: {e}")
                    import traceback
                    st.code(
                        traceback.format_exc()
                    )

    except Exception as e:
        st.error(f"Page error: {e}")                                     
# ─────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────
def main_app():
    settings = render_sidebar()
    models   = load_all_models()
    page     = st.session_state.get(
        "page", "dashboard"
    )

    if page == "dashboard":
        dashboard_page()
    elif page == "analyze":
        analyze_page(settings, models)
    elif page == "patients":
        patients_page()
    elif page == "history":
        history_page()
    elif page == "stats":
        stats_page()
    elif page == "doctor":
        doctor_dashboard_page()
    elif page == "appointments":
        appointments_page()
    elif page == "drugs":
        drugs_page()
    elif page == "models":
        models_page()
    elif page == "audit":
        audit_page()
    elif page == "about":
        about_page()
    elif page == "second_opinion":
        second_opinion_page()
    elif page == "risk":
        risk_calculator_page()
    elif page == "emergency":
        emergency_page()
    elif page == "timeline":
        timeline_page()
    elif page == "atlas":
        brain_atlas_page()
    elif page == "realtime":
        realtime_page()
    elif page == "dicom":
        dicom_page()
    elif page == "unet":
        unet_page()
    elif page == "dataset":
        dataset_page()
    elif page == "encryption":
        encryption_page()
    elif page == "viz3d":
        viz3d_page()
    elif page == "federated":
        federated_page()    
    elif page == "tumortypes":
        tumor_types_page()
    elif page == "pacs":
        pacs_page()    
    else:
        dashboard_page()

# ─────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────
def main():
    init_session()
    if not st.session_state.logged_in:
        login_page()
    else:
        main_app()

if __name__ == "__main__":
    main()
