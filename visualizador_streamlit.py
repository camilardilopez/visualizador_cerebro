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

    # Columnas principales: izquierda (30%) y derecha (70%)
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

        # Cuadrícula 2x2 dentro de la columna derecha
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 🟥 Axial")
            axial_labels = [f"{get_mm(0, 0, i)[2]:.2f} mm" for i in range(shape[2])]
            idx_axial_label = st.select_slider("Corte axial (mm)", options=axial_labels, value=axial_labels[shape[2] // 2], key="axial")
            idx_axial = axial_labels.index(idx_axial_label)
            mostrar_corte(data[:, :, idx_axial], zoom)

        with c2:
            st.markdown("### 🟪 Vista 3D (placeholder)")
            st.info("Aquí puede ir una vista 3D futura con PyVista o Plotly.")

        c3, c4 = st.columns(2)
        with c3:
            st.markdown("### 🟩 Coronal")
            coronal_labels = [f"{get_mm(0, i, 0)[1]:.2f} mm" for i in range(shape[1])]
            idx_coronal_label = st.select_slider("Corte coronal (mm)", options=coronal_labels, value=coronal_labels[shape[1] // 2], key="coronal")
            idx_coronal = coronal_labels.index(idx_coronal_label)
            mostrar_corte(data[:, idx_coronal, :], zoom)

        with c4:
            st.markdown("### 🟦 Sagital")
            sagital_labels = [f"{get_mm(i, 0, 0)[0]:.2f} mm" for i in range(shape[0])]
            idx_sagital_label = st.select_slider("Corte sagital (mm)", options=sagital_labels, value=sagital_labels[shape[0] // 2], key="sagital")
            idx_sagital = sagital_labels.index(idx_sagital_label)
            mostrar_corte(data[idx_sagital, :, :], zoom)
