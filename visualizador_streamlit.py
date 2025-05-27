import streamlit as st
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
import io

st.set_page_config(layout="wide")
st.title("🧠 Visualizador de Cerebro en NIfTI")

# Subida de archivo
uploaded_file = st.file_uploader("Sube un archivo NIfTI (.nii o .nii.gz)", type=["nii", "gz"])

if uploaded_file is not None:
    # Leer archivo como NIfTI
    img = nib.load(io.BytesIO(uploaded_file.read()))
    data = img.get_fdata()
    shape = data.shape
    st.success(f"Imagen cargada con forma: {shape}")

    # Sliders para cortes
    col1, col2, col3 = st.columns(3)

    with col1:
        idx_axial = st.slider("Corte axial", 0, shape[2] - 1, shape[2] // 2)
        fig, ax = plt.subplots()
        ax.imshow(np.rot90(data[:, :, idx_axial]), cmap='gray')
        ax.axis("off")
        st.pyplot(fig)

    with col2:
        idx_coronal = st.slider("Corte coronal", 0, shape[1] - 1, shape[1] // 2)
        fig, ax = plt.subplots()
        ax.imshow(np.rot90(data[:, idx_coronal, :]), cmap='gray')
        ax.axis("off")
        st.pyplot(fig)

    with col3:
        idx_sagital = st.slider("Corte sagital", 0, shape[0] - 1, shape[0] // 2)
        fig, ax = plt.subplots()
        ax.imshow(np.rot90(data[idx_sagital, :, :]), cmap='gray')
        ax.axis("off")
        st.pyplot(fig)
