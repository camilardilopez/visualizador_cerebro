import streamlit as st
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import tempfile

st.set_page_config(layout="wide")
st.title("🧠 Visualizador tipo 3D Slicer (compacto)")

uploaded_file = st.file_uploader("Sube un archivo NIfTI (.nii o .nii.gz)", type=["nii", "gz"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".nii.gz") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    img = nib.load(tmp_file_path)
    data = img.get_fdata()
    affine = img.affine
    shape = data.shape
    st.success(f"Dimensiones del volumen: {shape}")

    # Brillo y contraste
    vmin = st.slider("🔅 Brillo mínimo", float(np.min(data)), float(np.max(data)), float(np.min(data)))
    vmax = st.slider("🔆 Contraste máximo", float(np.min(data)), float(np.max(data)), float(np.max(data)))

    # Zoom
    zoom = st.slider("🔎 Zoom", 1, 5, 1)

    def mostrar_corte(corte, title):
        zoom_factor = 1 / zoom
        cx, cy = corte.shape[0] // 2, corte.shape[1] // 2
        sx, sy = int(corte.shape[0] * zoom_factor), int(corte.shape[1] * zoom_factor)
        x0, x1 = max(cx - sx // 2, 0), min(cx + sx // 2, corte.shape[0])
        y0, y1 = max(cy - sy // 2, 0), min(cy + sy // 2, corte.shape[1])
        corte_zoom = corte[x0:x1, y0:y1]

        fig, ax = plt.subplots(figsize=(3, 3))
        ax.imshow(np.rot90(corte_zoom), cmap='gray', vmin=vmin, vmax=vmax)
        ax.set_title(title, fontsize=10)
        ax.axis("off")
        st.pyplot(fig)

    def get_mm_coords(i, j, k):
        mm = affine @ np.array([i, j, k, 1])
        return f"{mm[0]:.2f} mm, {mm[1]:.2f} mm, {mm[2]:.2f} mm"

    # Fila superior: Axial + Placeholder 3D
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🟥 Axial")
        idx_axial = st.slider("Corte axial", 0, shape[2] - 1, shape[2] // 2, key="axial")
        corte = data[:, :, idx_axial]
        mostrar_corte(corte, f"Axial ({idx_axial}) - {get_mm_coords(0, 0, idx_axial)}")

    with col2:
        st.markdown("### 🟪 Vista 3D (placeholder)")
        st.info("Aquí puede ir una vista 3D futura con PyVista o Plotly")

    # Fila inferior: Coronal + Sagital
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 🟩 Coronal")
        idx_coronal = st.slider("Corte coronal", 0, shape[1] - 1, shape[1] // 2, key="coronal")
        corte = data[:, idx_coronal, :]
        mostrar_corte(corte, f"Coronal ({idx_coronal}) - {get_mm_coords(0, idx_coronal, 0)}")

    with col4:
        st.markdown("### 🟦 Sagital")
        idx_sagital = st.slider("Corte sagital", 0, shape[0] - 1, shape[0] // 2, key="sagital")
        corte = data[idx_sagital, :, :]
        mostrar_corte(corte, f"Sagital ({idx_sagital}) - {get_mm_coords(idx_sagital, 0, 0)}")
