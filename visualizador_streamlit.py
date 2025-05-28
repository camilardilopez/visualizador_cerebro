import streamlit as st
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import tempfile

st.set_page_config(layout="wide")
st.title("🧠 Visualizador tipo 3D Slicer (optimizado)")

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

    # Brillo/contraste y zoom global
    vmin = st.slider("🔅 Brillo mínimo", float(np.min(data)), float(np.max(data)), float(np.min(data)))
    vmax = st.slider("🔆 Contraste máximo", float(np.min(data)), float(np.max(data)), float(np.max(data)))
    zoom = st.slider("🔍 Zoom", 1, 5, 1)

    # Funciones utilitarias
    def get_mm(i, j, k):
        return affine @ np.array([i, j, k, 1])

    def format_mm(mm_val):
        return f"{mm_val:.2f} mm"

    def mostrar_corte(corte, zoom):
        zoom_factor = 1 / zoom
        cx, cy = corte.shape[0] // 2, corte.shape[1] // 2
        sx, sy = int(corte.shape[0] * zoom_factor), int(corte.shape[1] * zoom_factor)
        x0, x1 = max(cx - sx // 2, 0), min(cx + sx // 2, corte.shape[0])
        y0, y1 = max(cy - sy // 2, 0), min(cy + sy // 2, corte.shape[1])
        corte_zoom = corte[x0:x1, y0:y1]
        fig, ax = plt.subplots(figsize=(2.8, 2.8))
        ax.imshow(np.rot90(corte_zoom), cmap='gray', vmin=vmin, vmax=vmax)
        ax.axis("off")
        st.pyplot(fig, use_container_width=True)

    # Layout 2x2 compacto
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🟥 Axial")
        idx_axial = st.slider(
            "Corte axial (mm)",
            0, shape[2] - 1, shape[2] // 2,
            format_func=lambda i: format_mm(get_mm(0, 0, i)[2]),
            key="axial"
        )
        mostrar_corte(data[:, :, idx_axial], zoom)

    with col2:
        st.markdown("### 🟪 Vista 3D (placeholder)")
        st.info("Aquí puede ir una vista 3D futura con PyVista o Plotly.")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 🟩 Coronal")
        idx_coronal = st.slider(
            "Corte coronal (mm)",
            0, shape[1] - 1, shape[1] // 2,
            format_func=lambda i: format_mm(get_mm(0, i, 0)[1]),
            key="coronal"
        )
        mostrar_corte(data[:, idx_coronal, :], zoom)

    with col4:
        st.markdown("### 🟦 Sagital")
        idx_sagital = st.slider(
            "Corte sagital (mm)",
            0, shape[0] - 1, shape[0] // 2,
            format_func=lambda i: format_mm(get_mm(i, 0, 0)[0]),
            key="sagital"
        )
        mostrar_corte(data[idx_sagital, :, :], zoom)
