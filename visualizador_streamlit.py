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
        start_x, end_x = max(center_x - size_x // 2, 0), min(center_x + size_x // 2, corte.shape[0])
        start_y, end_y = max(center_y - size_y // 2, 0), min(center_y + size_y // 2, corte.shape[1])
        corte_zoom = corte[start_x:end_x, start_y:end_y]

        fig, ax = plt.subplots()
        ax.imshow(np.rot90(corte_zoom), cmap='gray', vmin=vmin, vmax=vmax)
        ax.set_title(title)
        ax.axis("off")
        st.pyplot(fig)

    def get_mm_coords(i, j, k):
        voxel = np.array([i, j, k, 1])
        mm = affine @ voxel
        return f"{mm[0]:.2f} mm, {mm[1]:.2f} mm, {mm[2]:.2f} mm"

    # Layout tipo cuadrante 2x2
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🟥 Axial")
        corte = data[:, :, idx_axial]
        mostrar_corte(corte, f"Axial ({idx_axial}) - {get_mm_coords(0, 0, idx_axial)}")

    with col2:
        st.markdown("### 🟪 Vista 3D (placeholder)")
        st.info("Aquí podría ir una futura vista 3D con PyVista o Plotly")

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### 🟩 Coronal")
        corte = data[:, idx_coronal, :]
        mostrar_corte(corte, f"Coronal ({idx_coronal}) - {get_mm_coords(0, idx_coronal, 0)}")

    with col4:
        st.markdown("### 🟦 Sagital")
        corte = data[idx_sagital, :, :]
        mostrar_corte(corte, f"Sagital ({idx_sagital}) - {get_mm_coords(idx_sagital, 0, 0)}")
