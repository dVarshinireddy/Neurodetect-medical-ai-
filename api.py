# NeuroDetect - api.py
# FastAPI Backend for Mobile App
# Connects AI Models to Flutter

import os
import sys
import cv2
import json
import math
import numpy as np
from PIL import Image
from datetime import datetime
from typing import Optional
import io
import base64

sys.path.append("member1")
sys.path.append("member2")
sys.path.append("smart_features")

from fastapi import (
    FastAPI, File, UploadFile,
    HTTPException, Form
)
from fastapi.middleware.cors import (
    CORSMiddleware
)
from fastapi.responses import (
    JSONResponse, FileResponse
)
from pydantic import BaseModel

# ─────────────────────────────────────────
# APP SETUP
# ─────────────────────────────────────────
app = FastAPI(
    title       = "NeuroDetect AI API",
    description = "Real Medical Brain Tumor Detection API",
    version     = "2.0.0"
)

# Allow Flutter to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["*"],
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"]
)

# ─────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────
CLASSES  = ["glioma", "meningioma",
            "notumor", "pituitary"]
IMG_SIZE = 64
USERS    = {
    "admin":       "neurodetect123",
    "doctor":      "brain2024",
    "radiologist": "mri2024"
}

# ─────────────────────────────────────────
# LOAD MODELS ON STARTUP
# ─────────────────────────────────────────
models = {}

@app.on_event("startup")
async def load_models():
    global models
    print("🔄 Loading AI Models...")

    try:
        import joblib
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
        print("✅ ML Models loaded!")
    except Exception as e:
        print(f"⚠️ ML Models: {e}")

    try:
        import tensorflow as tf
        models["cnn"] = \
            tf.keras.models.load_model(
                "models/cnn_model.h5"
            )
        print("✅ CNN loaded!")
    except Exception as e:
        print(f"⚠️ CNN: {e}")

    try:
        import tensorflow as tf
        models["resnet"] = \
            tf.keras.models.load_model(
                "models/transfer_ResNet50.h5"
            )
        print("✅ ResNet50 loaded!")
    except Exception as e:
        print(f"⚠️ ResNet50: {e}")

    print("✅ All models ready!")

# ─────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────
def preprocess_image(image_bytes):
    img      = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")
    img_arr  = np.array(img)
    img_orig = img_arr.copy()
    img_res  = cv2.resize(
        img_arr, (IMG_SIZE, IMG_SIZE)
    )
    return img_res / 255.0, img_orig

def predict_all_models(img_norm):
    results = {}

    # SVM
    if "svm" in models:
        try:
            flat  = img_norm.reshape(1, -1)
            sc    = models["scaler"].transform(
                flat
            )
            pca   = models["pca"].transform(sc)
            idx   = models["svm"].predict(pca)[0]
            prob  = models["svm"].predict_proba(
                pca
            )[0]
            label = models["le"].inverse_transform(
                [idx]
            )[0]
            results["SVM"] = {
                "prediction": label,
                "confidence": round(
                    float(prob[idx]) * 100, 2
                ),
                "probabilities": {
                    CLASSES[i]: round(
                        float(prob[i]) * 100, 2
                    )
                    for i in range(len(CLASSES))
                }
            }
        except Exception as e:
            print(f"SVM error: {e}")

    # RF
    if "rf" in models:
        try:
            flat  = img_norm.reshape(1, -1)
            sc    = models["scaler"].transform(flat)
            pca   = models["pca"].transform(sc)
            idx   = models["rf"].predict(pca)[0]
            prob  = models["rf"].predict_proba(
                pca
            )[0]
            label = models["le"].inverse_transform(
                [idx]
            )[0]
            results["RF"] = {
                "prediction": label,
                "confidence": round(
                    float(prob[idx]) * 100, 2
                ),
                "probabilities": {
                    CLASSES[i]: round(
                        float(prob[i]) * 100, 2
                    )
                    for i in range(len(CLASSES))
                }
            }
        except Exception as e:
            print(f"RF error: {e}")

    # CNN
    if "cnn" in models:
        try:
            import tensorflow as tf
            batch = np.expand_dims(img_norm, 0)
            prob  = models["cnn"].predict(
                batch, verbose=0
            )[0]
            idx   = np.argmax(prob)
            label = models["le"].inverse_transform(
                [idx]
            )[0]
            results["CNN"] = {
                "prediction": label,
                "confidence": round(
                    float(prob[idx]) * 100, 2
                ),
                "probabilities": {
                    CLASSES[i]: round(
                        float(prob[i]) * 100, 2
                    )
                    for i in range(len(CLASSES))
                }
            }
        except Exception as e:
            print(f"CNN error: {e}")

    # ResNet
    if "resnet" in models:
        try:
            import tensorflow as tf
            batch = np.expand_dims(img_norm, 0)
            prob  = models["resnet"].predict(
                batch, verbose=0
            )[0]
            idx   = np.argmax(prob)
            label = models["le"].inverse_transform(
                [idx]
            )[0]
            results["ResNet50"] = {
                "prediction": label,
                "confidence": round(
                    float(prob[idx]) * 100, 2
                ),
                "probabilities": {
                    CLASSES[i]: round(
                        float(prob[i]) * 100, 2
                    )
                    for i in range(len(CLASSES))
                }
            }
        except Exception as e:
            print(f"ResNet error: {e}")

    return results

def get_weighted_prediction(results):
    weights = {
        "SVM":      0.15,
        "RF":       0.15,
        "CNN":      0.40,
        "ResNet50": 0.30
    }
    weighted = np.zeros(4)
    tw       = 0

    for model_name, data in results.items():
        w  = weights.get(model_name, 0.25)
        probs = [
            data["probabilities"].get(c, 0) / 100
            for c in CLASSES
        ]
        weighted += w * np.array(probs)
        tw       += w

    weighted  /= tw
    idx        = np.argmax(weighted)
    label      = CLASSES[idx]
    confidence = round(
        float(weighted[idx]) * 100, 2
    )

    return label, confidence, {
        CLASSES[i]: round(
            float(weighted[i]) * 100, 2
        )
        for i in range(4)
    }

def image_to_base64(img_array):
    if img_array is None:
        return None
    if img_array.max() <= 1.0:
        img_array = (
            img_array * 255
        ).astype(np.uint8)
    img_pil = Image.fromarray(
        img_array.astype(np.uint8)
    )
    buffer  = io.BytesIO()
    img_pil.save(buffer, format="PNG")
    return base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

# ─────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────

# 1. ROOT
@app.get("/")
async def root():
    return {
        "message": "NeuroDetect AI API v2.0",
        "status":  "running",
        "models":  list(models.keys()),
        "endpoints": [
            "/predict",
            "/history",
            "/treatment",
            "/models",
            "/login",
            "/report"
        ]
    }

# 2. HEALTH CHECK
@app.get("/health")
async def health():
    return {
        "status":        "healthy",
        "models_loaded": len(models),
        "timestamp":     datetime.now().isoformat()
    }

# 3. LOGIN
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(request: LoginRequest):
    if (request.username in USERS and
            USERS[request.username] ==
            request.password):
        return {
            "success":  True,
            "username": request.username,
            "role": "Doctor" if
                request.username == "doctor"
                else "Administrator",
            "name": "Dr. Smith" if
                request.username == "doctor"
                else request.username.title(),
            "token": f"nd_{request.username}_token",
            "message": "Login successful"
        }
    raise HTTPException(
        status_code = 401,
        detail      = "Wrong credentials"
    )

# 4. PREDICT — Main endpoint
@app.post("/predict")
async def predict(
    file:           UploadFile = File(...),
    patient_name:   str = Form(default=""),
    patient_age:    str = Form(default=""),
    patient_gender: str = Form(default=""),
    doctor_name:    str = Form(default="")
):
    # Read image
    image_bytes = await file.read()

    # Preprocess
    img_norm, img_orig = preprocess_image(
        image_bytes
    )

    # Predict all models
    model_results = predict_all_models(img_norm)

    if not model_results:
        raise HTTPException(
            status_code = 500,
            detail      = "No models available"
        )

    # Get final prediction
    final_label, final_conf, final_probs = \
        get_weighted_prediction(model_results)

    # Get tumor analysis
    tumor_analysis = {}
    gradcam_b64    = None

    if "cnn" in models:
        try:
            from gradcam import full_tumor_analysis
            analysis = full_tumor_analysis(
                models["cnn"], img_norm
            )
            if analysis:
                tumor_analysis = {
                    "location": analysis[
                        "anatomy"
                    ]["name"],
                    "hemisphere": analysis[
                        "anatomy"
                    ]["hemisphere"],
                    "lobe": analysis[
                        "anatomy"
                    ]["lobe"],
                    "function": analysis[
                        "anatomy"
                    ]["function"],
                    "size_label": analysis[
                        "size_info"
                    ]["size_label"],
                    "diameter_cm": analysis[
                        "size_info"
                    ]["diameter_cm"],
                    "area_cm2": analysis[
                        "size_info"
                    ]["area_cm2"],
                    "who_grade": analysis[
                        "size_info"
                    ]["who_grade"],
                    "stage": analysis[
                        "size_info"
                    ]["stage"],
                    "color": analysis[
                        "size_info"
                    ]["color"]
                }
                # Gradcam image
                if analysis.get(
                    "annotated"
                ) is not None:
                    gradcam_b64 = image_to_base64(
                        analysis["annotated"]
                    )
        except Exception as e:
            print(f"Analysis error: {e}")

    # Get confidence report
    conf_data = {}
    try:
        from confidence_meter import \
            get_full_confidence_report
        conf_report = get_full_confidence_report(
            final_label,
            final_conf,
            list(final_probs.values())
        )
        conf_data = {
            "risk_level":        conf_report[
                                     "risk_level"
                                 ],
            "confidence_label":  conf_report[
                                     "confidence_label"
                                 ],
            "alert_message":     conf_report.get(
                                     "alert_message",
                                     ""
                                 ),
            "sensitivity":       conf_report[
                                     "sensitivity"
                                 ],
            "specificity":       conf_report[
                                     "specificity"
                                 ],
            "ppv":               conf_report["ppv"],
            "npv":               conf_report["npv"]
        }
    except Exception as e:
        print(f"Confidence error: {e}")

    # Get treatment
    treatment_data = {}
    try:
        from treatment_advisor import \
            get_treatment_info
        treatment = get_treatment_info(final_label)
        treatment_data = {
            "icd10_code":  treatment["icd10_code"],
            "who_grade":   treatment["who_grade"],
            "urgency":     treatment[
                               "urgency"
                           ].replace("—", "-"),
            "description": treatment["description"],
            "first_line":  treatment["first_line"],
            "second_line": treatment["second_line"],
            "drugs":       treatment["drugs"],
            "specialists": treatment["specialists"],
            "follow_up":   treatment["follow_up"],
            "survival":    treatment["survival"]
        }
    except Exception as e:
        print(f"Treatment error: {e}")

    # Save to history
    if patient_name:
        try:
            from history_tracker import \
                save_prediction
            save_prediction(
                patient_name = patient_name,
                prediction   = final_label,
                confidence   = final_conf,
                risk_level   = conf_data.get(
                                   "risk_level",
                                   "UNKNOWN"
                               ),
                model_used   = "Multi-Model API",
                doctor_name  = doctor_name,
                tumor_size   = tumor_analysis.get(
                                   "size_label",
                                   "N/A"
                               ),
                stage        = tumor_analysis.get(
                                   "stage", "N/A"
                               ),
                icd10_code   = treatment_data.get(
                                   "icd10_code",
                                   "N/A"
                               ),
                notes        = ""
            )
        except Exception as e:
            print(f"History error: {e}")

    return JSONResponse({
        "success":        True,
        "timestamp":      datetime.now().isoformat(),
        "patient": {
            "name":   patient_name,
            "age":    patient_age,
            "gender": patient_gender,
            "doctor": doctor_name
        },
        "prediction": {
            "final_label":      final_label,
            "final_confidence": final_conf,
            "probabilities":    final_probs,
            "model_results":    model_results
        },
        "tumor_analysis":  tumor_analysis,
        "clinical_data":   conf_data,
        "treatment":       treatment_data,
        "gradcam_image":   gradcam_b64
    })

# 5. GET TREATMENT
@app.get("/treatment/{tumor_type}")
async def get_treatment(tumor_type: str):
    try:
        from treatment_advisor import \
            get_treatment_info
        treatment = get_treatment_info(tumor_type)
        return {
            "success":   True,
            "tumor_type": tumor_type,
            "treatment": treatment
        }
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail      = str(e)
        )

# 6. GET HISTORY
@app.get("/history")
async def get_history():
    try:
        from history_tracker import load_history
        history = load_history()
        return {
            "success": True,
            "count":   len(history),
            "history": history
        }
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail      = str(e)
        )

# 7. GET SUMMARY
@app.get("/summary")
async def get_summary():
    try:
        from history_tracker import get_summary
        summary = get_summary()
        return {
            "success": True,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail      = str(e)
        )

# 8. GET MODELS INFO
@app.get("/models")
async def get_models():
    return {
        "success": True,
        "models": [
            {
                "name":     "Custom CNN",
                "accuracy": 98.87,
                "type":     "Deep Learning",
                "status":   "cnn" in models
            },
            {
                "name":     "SVM",
                "accuracy": 95.95,
                "type":     "Machine Learning",
                "status":   "svm" in models
            },
            {
                "name":     "Random Forest",
                "accuracy": 94.23,
                "type":     "Machine Learning",
                "status":   "rf" in models
            },
            {
                "name":     "ResNet50",
                "accuracy": 85.83,
                "type":     "Transfer Learning",
                "status":   "resnet" in models
            }
        ],
        "best_model": "Custom CNN",
        "best_accuracy": 98.87
    }

# 9. GENERATE PDF REPORT
@app.post("/report")
async def generate_report(
    file:           UploadFile = File(...),
    patient_name:   str = Form(...),
    patient_age:    str = Form(default="N/A"),
    patient_gender: str = Form(default="N/A"),
    doctor_name:    str = Form(
                        default="Dr. AI"
                    )
):
    image_bytes    = await file.read()
    img_norm, _    = preprocess_image(
        image_bytes
    )
    model_results  = predict_all_models(img_norm)
    final_label, \
    final_conf, \
    final_probs    = get_weighted_prediction(
        model_results
    )

    try:
        from treatment_advisor import \
            get_treatment_info
        from confidence_meter import \
            get_full_confidence_report
        from report_generator import \
            generate_pdf_report

        treatment   = get_treatment_info(
            final_label
        )
        conf_report = get_full_confidence_report(
            final_label, final_conf,
            list(final_probs.values())
        )

        pdf_path = generate_pdf_report(
            patient_name   = patient_name,
            patient_age    = patient_age,
            patient_gender = patient_gender,
            doctor_name    = doctor_name,
            prediction     = final_label,
            confidence     = final_conf,
            risk_level     = conf_report[
                                 "risk_level"
                             ],
            tumor_size     = "N/A",
            stage          = "N/A",
            icd10_code     = treatment[
                                 "icd10_code"
                             ],
            treatment_info = treatment
        )

        return FileResponse(
            pdf_path,
            media_type = "application/pdf",
            filename   = f"report_{patient_name}.pdf"
        )
    except Exception as e:
        raise HTTPException(
            status_code = 500,
            detail      = f"Report error: {str(e)}"
        )

# ─────────────────────────────────────────
# RUN SERVER
# ─────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host = "0.0.0.0",
        port = 8000,
        reload = False
    )
