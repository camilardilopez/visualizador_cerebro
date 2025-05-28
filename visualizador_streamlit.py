import streamlit as st
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import tempfile

st.set_page_config(layout="wide")
st.title("🧠 Visualizador tipo 3D Slicer")

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

    # Estilo de color por slider
    st.markdown("""
        <style>
        .stSlider > div > div > div > div { height: 4px; }
        </style>
    """, unsafe_allow_html=True)

    # Columnas principales
    col_izq, col_der = st.columns([3, 7])

    with col_izq:
        st.markdown("### 🛠️ Controles (en construcción)")
        st.markdown("Aquí irán herramientas y menús futuros.")

    with col_der:
        # Brillo/contraste y zoom
        vmin = st.slider("🔅 Brillo mínimo", float(np.min(data)), float(np.max(data)), float(np.min(data)))
        vmax = st.slider("🔆 Contraste máximo", float(np.min(data)), float(np.max(data)), float(np.max(data)))
        zoom = st.slider("🔍 Zoom", 1, 5, 1)

        def get_mm(i, j, k):
            return affine @ np.array([i, j, k, 1])

        def mostrar_corte(corte, zoom):
            zoom_factor = 1 / zoom
            cx, cy = corte.shape[0] // 2, corte.shape[1] // 2
            sx, sy = int(corte.shape[0] * zoom_factor), int(corte.shape[1] * zoom_factor)
            x0, x1 = max(cx - sx // 2, 0), min(cx + sx // 2, corte.shape[0])
            y0, y1 = max(cy - sy // 2, 0), min(cy + sy // 2, corte.shape[1])
            corte_zoom = corte[x0:x1, y0:y1]
            fig, ax = plt.subplots(figsize=(2.5, 2.5))
            ax.imshow(np.rot90(corte_zoom), cmap='gray', vmin=vmin, vmax=vmax)
            ax.axis("off")
            st.pyplot(fig, use_container_width=True)

        # Cuadrícula 2x2
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div style="color:#c0392b; font-size:14px;">🟥 Axial</div>', unsafe_allow_html=True)
            axial_vals = [get_mm(0, 0, i)[2] for i in range(shape[2])]
            idx_axial = st.slider("", 0, shape[2] - 1, shape[2] // 2, key="axial")
            st.markdown(f"<div style='color:#c0392b; font-size:12px;'>Posición: {axial_vals[idx_axial]:.2f} mm</div>", unsafe_allow_html=True)
            mostrar_corte(data[:, :, idx_axial], zoom)

        with c2:
            st.markdown('<div style="color:#8e44ad; font-size:14px;">🟪 Vista 3D (placeholder)</div>', unsafe_allow_html=True)
            st.info("Aquí puede ir una vista 3D futura con PyVista o Plotly.")

        c3, c4 = st.columns(2)
        with c3:
            st.markdown('<div style="color:#27ae60; font-size:14px;">🟩 Coronal</div>', unsafe_allow_html=True)
            coronal_vals = [get_mm(0, i, 0)[1] for i in range(shape[1])]
            idx_coronal = st.slider("", 0, shape[1] - 1, shape[1] // 2, key="coronal")
            st.markdown(f"<div style='color:#27ae60; font-size:12px;'>Posición: {coronal_vals[idx_coronal]:.2f} mm</div>", unsafe_allow_html=True)
            mostrar_corte(data[:, idx_coronal, :], zoom)

        with c4:
            st.markdown('<div style="color:#2980b9; font-size:14px;">🟦 Sagital</div>', unsafe_allow_html=True)
            sagittal_vals = [get_mm(i, 0, 0)[0] for i in range(shape[0])]
            idx_sagital = st.slider("", 0, shape[0] - 1, shape[0] // 2, key="sagital")
            st.markdown(f"<div style='color:#2980b9; font-size:12px;'>Posición: {sagittal_vals[idx_sagital]:.2f} mm</div>", unsafe_allow_html=True)
            mostrar_corte(data[idx_sagital, :, :], zoom)
