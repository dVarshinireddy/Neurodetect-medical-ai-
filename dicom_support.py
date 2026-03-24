# NeuroDetect - dicom_support.py
# Feature 29: DICOM Support

import numpy as np
from PIL import Image
import io
import os

def load_dicom(file_path):
    try:
        import pydicom
        dcm  = pydicom.dcmread(file_path)
        info = extract_dicom_info(dcm)
        img  = dicom_to_image(dcm)
        return img, info, None
    except ImportError:
        return None, {}, \
            "pydicom not installed"
    except Exception as e:
        return None, {}, str(e)

def dicom_to_image(dcm):
    try:
        pixel_array = dcm.pixel_array
        # Normalize to 0-255
        arr = pixel_array.astype(float)
        arr = (arr - arr.min()) / \
              (arr.max() - arr.min() + 1e-8)
        arr = (arr * 255).astype(np.uint8)

        # Handle different modes
        if len(arr.shape) == 2:
            img = Image.fromarray(
                arr, mode="L"
            ).convert("RGB")
        else:
            img = Image.fromarray(arr)

        return img
    except Exception as e:
        return None

def extract_dicom_info(dcm):
    info = {}
    fields = [
        ("PatientName",      "Patient Name"),
        ("PatientID",        "Patient ID"),
        ("PatientAge",       "Age"),
        ("PatientSex",       "Sex"),
        ("StudyDate",        "Study Date"),
        ("Modality",         "Modality"),
        ("StudyDescription", "Description"),
        ("InstitutionName",  "Institution"),
        ("Manufacturer",     "Scanner Brand"),
        ("SliceThickness",   "Slice Thickness"),
        ("PixelSpacing",     "Pixel Spacing"),
        ("Rows",             "Image Rows"),
        ("Columns",          "Image Columns"),
        ("BitsAllocated",    "Bits Allocated"),
    ]
    for attr, label in fields:
        try:
            val = getattr(dcm, attr, None)
            if val is not None:
                info[label] = str(val)
        except:
            pass
    return info

def dicom_from_bytes(file_bytes):
    try:
        import pydicom
        dcm  = pydicom.dcmread(
            io.BytesIO(file_bytes)
        )
        info = extract_dicom_info(dcm)
        img  = dicom_to_image(dcm)
        return img, info, None
    except ImportError:
        return None, {}, \
            "pydicom not installed. " \
            "Run: pip install pydicom"
    except Exception as e:
        return None, {}, str(e)

def is_dicom_file(filename):
    return filename.lower().endswith(
        ('.dcm', '.dicom', '.ima')
    )

def simulate_dicom_info():
    return {
        "Patient Name":    "DEMO PATIENT",
        "Patient ID":      "MRN-12345678",
        "Age":             "045Y",
        "Sex":             "M",
        "Study Date":      "20250306",
        "Modality":        "MR",
        "Description":     "BRAIN MRI W/WO",
        "Institution":     "NeuroDetect Medical Center",
        "Scanner Brand":   "SIEMENS",
        "Slice Thickness": "5.0",
        "Pixel Spacing":   "[0.9375, 0.9375]",
        "Image Rows":      "512",
        "Image Columns":   "512",
        "Bits Allocated":  "16"
    }
