import streamlit as st
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import tempfile

st.set_page_config(layout="wide")
st.title("🧠 Visualizador tipo 3D Slicer (simplificado)")

uploaded_file = st.file_uploader("Sube un archivo NIfTI (.nii o .nii.gz)", type=["nii", "gz"])

if uploaded_file is not None:
    # Guardar archivo temporalmente
    with tempfile.NamedTemporaryFile(delete=False, suffix=".nii.gz") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    # Cargar imagen y datos
    img = nib.load(tmp_file_path)
    data = img.get_fdata()
    affine = img.affine
    shape = data.shape
    st.success(f"Dimensiones del volumen: {shape}")

    # Sliders de brillo/contraste
    vmin = st.slider("🔅 Brillo mínimo", float(np.min(data)), float(np.max(data)), float(np.min(data)))
    vmax = st.slider("🔆 Contraste máximo", float(np.min(data)), float(np.max(data)), float(np.max(data)))

    # Sliders de corte por vista
    idx_axial = st.slider("🟥 Corte Axial", 0, shape[2] - 1, shape[2] // 2)
    idx_coronal = st.slider("🟩 Corte Coronal", 0, shape[1] - 1, shape[1] // 2)
    idx_sagital = st.slider("🟦 Corte Sagital", 0, shape[0] - 1, shape[0] // 2)

    # Slider de zoom global (1 = sin zoom)
    zoom = st.slider("🔎 Zoom", 1, 5, 1)

    def mostrar_corte(corte, title):
        zoom_factor = 1 / zoom
        center_x, center_y = corte.shape[0] // 2, corte.shape[1] // 2
        size_x, size_y = int(corte.shape[0] * zoom_factor), int(corte.shape[1] * zoom_factor)
        start_x, end_x = max(center_x - size_
