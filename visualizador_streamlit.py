import streamlit as st
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import tempfile

st.set_page_config(layout="wide")
st.title("🧠 Visualizador de Cerebro tipo 3D Slicer (simplificado)")

uploaded_file = st.file_uploader("Sube un archivo NIfTI (.nii o .nii.gz)", type=["nii", "gz"])

if uploaded_file is not None:
    # Guardar el archivo con extensión correcta
    with tempfile.NamedTemporaryFile(delete=False, suffix=".nii.gz") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    img = nib.load(tmp_file_path)
    data = img.get_fdata()
    shape = data.shape
    st.success(f"Imagen cargada con forma: {shape}")

    # Configuración global
    vista = st.radio("👁️ Selecciona qué vista mostrar", ["Todas", "Axial", "Coronal", "Sagital"])

    # Sliders globales de brillo/contraste
    vmin = st.slider("🔅 Brillo mínimo (vmin)", float(np.min(data)), float(np.max(data)), float(np.min(data)))
    vmax = st.slider("🔆 Contraste máximo (vmax)", float(np.min(data)), float(np.max(data)), float(np.max(data)))

    def mostrar_corte(img_data, plano, idx, title):
        fig, ax = plt.subplots()
        if plano == 'axial':
            corte = img_data[:, :, idx]
        elif plano == 'coronal':
            corte = img_data[:, idx, :]
        elif plano == 'sagital':
            corte = img_data[idx, :, :]
        else:
            corte = np.zeros((10, 10))  # Fallback en caso de error

        ax.imshow(np.rot90(corte), cmap='gray', vmin=vmin, vmax=vmax)
        ax.set_title(title)
        ax.axis("off")
        st.pyplot(fig)

    # Vistas
    if vista in ["Todas", "Axial"]:
        st.markdown("### 🟥 Corte Axial")
        col1, col2 = st.columns([4, 1])
        with col1:
            idx_axial = st.slider("Posición axial", 0, shape[2] - 1, shape[2] // 2, key="axial")
            mostrar_corte(data, 'axial', idx_axial, f"Axial ({idx_axial})")
        with col2:
            if st.button("🔁 Reset axial"):
                st.experimental_rerun()

    if vista in ["Todas", "Coronal"]:
        st.markdown("### 🟩 Corte Coronal")
        col1, col2 = st.columns([4, 1])
        with col1:
            idx_coronal = st.slider("Posición coronal", 0, shape[1] - 1, shape[1] // 2, key="coronal")
            mostrar_corte(data, 'coronal', idx_coronal, f"Coronal ({idx_coronal})")
        with col2:
            if st.button("🔁 Reset coronal"):
                st.experimental_rerun()

    if vista in ["Todas", "Sagital"]:
        st.markdown("### 🟦 Corte Sagital")
        col1, col2 = st.columns([4, 1])
        with col1:
            idx_sagital = st.slider("Posición sagital", 0, shape[0] - 1, shape[0] // 2, key="sagital")
            mostrar_corte(data, 'sagital', idx_sagital, f"Sagital ({idx_sagital})")
        with col2:
            if st.button("🔁 Reset sagital"):
                st.experimental_rerun()
