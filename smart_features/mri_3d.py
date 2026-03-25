import numpy as np
import cv2
from PIL import Image
def get_axial_slice(volume, idx):
    slc = volume[:, :, idx]
    return normalize_slice(slc)
def get_coronal_slice(volume, idx):
    slc = volume[:, idx, :]
    return normalize_slice(slc
def get_sagittal_slice(volume, idx):
    slc = volume[idx, :, :]
    return normalize_slice(slc)
def normalize_slice(slc):
    slc = slc.astype(float)
    mn, mx = slc.min(), slc.max()
    if mx - mn < 1e-8:
        return np.zeros_like(slc,
            dtype=np.uint8)
    slc = ((slc - mn) /
           (mx - mn) * 255
    ).astype(np.uint8)
    return slc
def apply_colormap(slc, cmap="gray"):
    COLORMAPS = {
        "gray":  cv2.COLORMAP_BONE,
        "hot":   cv2.COLORMAP_HOT,
        "jet":   cv2.COLORMAP_JET,
        "viridis":cv2.COLORMAP_VIRIDIS,
        "cool":  cv2.COLORMAP_COOL,
        "plasma":cv2.COLORMAP_PLASMA
    }
    if cmap == "gray":
        rgb = cv2.cvtColor(
            slc, cv2.COLOR_GRAY2RGB
        )
    else:
        cv_map = COLORMAPS.get(
            cmap, cv2.COLORMAP_BONE
        )
        rgb = cv2.applyColorMap(slc, cv_map)
        rgb = cv2.cvtColor(
            rgb, cv2.COLOR_BGR2RGB
        )
    return rgb
def add_slice_info(
    img, plane, idx, total,
    prediction=None, color=(255,255,255)
):
    result = img.copy()
    cv2.putText(
        result,
        f"{plane} | Slice {idx}/{total}",
        (5, 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5, color, 1, cv2.LINE_AA
    )
    if prediction:
        cv2.putText(
            result,
            f"AI: {prediction.upper()}",
            (5, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4,
            (0, 255, 100),
            1, cv2.LINE_AA
        )
    return result
def create_multiplanar(
    volume,
    axial_idx=None,
    coronal_idx=None,
    sagittal_idx=None,
    cmap="gray",
    prediction=None
):
    shape = volume.shape
    if axial_idx is None:
        axial_idx = shape[2] // 2
    if coronal_idx is None:
        coronal_idx = shape[1] // 2
    if sagittal_idx is None:
        sagittal_idx = shape[0] // 2

    axial_idx    = max(0, min(
        axial_idx,    shape[2]-1))
    coronal_idx  = max(0, min(
        coronal_idx,  shape[1]-1))
    sagittal_idx = max(0, min(
        sagittal_idx, shape[0]-1))
    # Get slices
    axial    = get_axial_slice(
        volume, axial_idx
    )
    coronal  = get_coronal_slice(
        volume, coronal_idx
    )
    sagittal = get_sagittal_slice(
        volume, sagittal_idx
    )

    # Resize all to same size
    target = (256, 256)
    axial    = cv2.resize(axial,    target)
    coronal  = cv2.resize(coronal,  target)
    sagittal = cv2.resize(sagittal, target)

    # Apply colormap
    axial_c    = apply_colormap(
        axial,    cmap
    )
    coronal_c  = apply_colormap(
        coronal,  cmap
    )
    sagittal_c = apply_colormap(
        sagittal, cmap
    )

    # Add info labels
    axial_c = add_slice_info(
        axial_c, "AXIAL",
        axial_idx, shape[2]-1,
        prediction
    )
    coronal_c = add_slice_info(
        coronal_c, "CORONAL",
        coronal_idx, shape[1]-1
    )
    sagittal_c = add_slice_info(
        sagittal_c, "SAGITTAL",
        sagittal_idx, shape[0]-1
    )

    return {
        "axial":         axial_c,
        "coronal":       coronal_c,
        "sagittal":      sagittal_c,
        "axial_idx":     axial_idx,
        "coronal_idx":   coronal_idx,
        "sagittal_idx":  sagittal_idx,
        "shape":         shape
    }

def create_slices_grid(
    volume, n=9, plane="axial",
    cmap="gray"
):
    shape = volume.shape
    if plane == "axial":
        total = shape[2]
    elif plane == "coronal":
        total = shape[1]
    else:
        total = shape[0]

    indices = np.linspace(
        total//10,
        total - total//10,
        n, dtype=int
    )

    slices = []
    for idx in indices:
        if plane == "axial":
            slc = get_axial_slice(
                volume, idx
            )
        elif plane == "coronal":
            slc = get_coronal_slice(
                volume, idx
            )
        else:
            slc = get_sagittal_slice(
                volume, idx
            )
        slc_rgb = apply_colormap(
            cv2.resize(slc, (128,128)), cmap
        )
        cv2.putText(
            slc_rgb,
            str(idx),
            (3, 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.4, (255,255,255), 1
        )
        slices.append(slc_rgb)

    # Make 3x3 grid
    rows = []
    for i in range(0, min(n,9), 3):
        row_slices = slices[i:i+3]
        while len(row_slices) < 3:
            row_slices.append(
                np.zeros((128,128,3),
                dtype=np.uint8)
            )
        rows.append(
            np.hstack(row_slices)
        )
    grid = np.vstack(rows[:3])
    return grid

def create_from_2d(image, prediction=None):
    if isinstance(image, Image.Image):
        arr = np.array(
            image.convert("L")
        )
    else:
        arr = cv2.cvtColor(
            image, cv2.COLOR_RGB2GRAY
        )

    h, w  = arr.shape
    depth = min(h, w) // 4
    volume = np.zeros(
        (h, w, depth), dtype=arr.dtype
    )

    for i in range(depth):
        factor = 0.5 + (i/depth * 0.5)
        layer  = (arr * factor).astype(
            arr.dtype
        )
        layer  = cv2.GaussianBlur(
            layer,
            (3+(i%2)*2, 3+(i%2)*2), 0
        )
        volume[:, :, i] = layer

    return volume

def get_volume_stats(volume):
    return {
        "shape":     str(volume.shape),
        "slices_axial":    volume.shape[2]
                           if len(volume.shape)>2
                           else 1,
        "slices_coronal":  volume.shape[1]
                           if len(volume.shape)>1
                           else 1,
        "slices_sagittal": volume.shape[0],
        "min_val":  float(volume.min()),
        "max_val":  float(volume.max()),
        "mean_val": float(volume.mean()),
        "size_mb":  round(
            volume.nbytes / 1024 / 1024, 2
        )
    }
