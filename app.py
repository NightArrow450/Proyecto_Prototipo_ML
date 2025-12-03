import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="Predicción de Ingresos", layout="centered")
st.title("💰 Predicción de Ingresos Estimados")

st.markdown("""
Esta aplicación permite **estimar el ingreso mensual** de un cliente 
a partir de sus características.  
El objetivo es apoyar a aseguradoras en la **segmentación de clientes** 
y en el diseño de **ofertas personalizadas**.
""")

# Cargar modelo
try:
    with open("modelo_ingresos.pkl", "rb") as file:
        modelo = pickle.load(file)
except:
    st.error("❌ No se encontró 'modelo_ingresos.pkl'. Coloque el archivo en la misma carpeta del app.")
    st.stop()

# Panel lateral
st.sidebar.header("📋 Ingrese los datos del cliente")

edad = st.sidebar.number_input("Edad del cliente", min_value=18, max_value=100, value=30)
anios_dir = st.sidebar.number_input("Años viviendo en la dirección", min_value=0, max_value=80, value=5)
gasto_auto = st.sidebar.number_input("Gasto en auto (mensual)", min_value=0, max_value=500, value=50)
anios_empleo = st.sidebar.number_input("Años de empleo", min_value=0, max_value=60, value=3)
anios_residen = st.sidebar.number_input("Años de residencia", min_value=0, max_value=80, value=5)

# Botón de predicción
if st.button("🔍 Predecir ingreso"):
    entrada = pd.DataFrame({
        "edad": [edad],
        "AniosDireccion": [anios_dir],
        "Gastocoche": [gasto_auto],
        "Aniosempleo": [anios_empleo],
        "Aniosresiden": [anios_residen]
    })

    ingreso_pred = modelo.predict(entrada)[0]

    st.success(f"💰 **Ingreso estimado:** S/{ingreso_pred:.2f}")

    # Segmento
    if ingreso_pred < dataset['ingres_pred'].quantile(0.20):
        segmento = "Muy Bajo"
    elif ingreso_pred < dataset['ingres_pred'].quantile(0.40):
        segmento = "Bajo"
    elif ingreso_pred < dataset['ingres_pred'].quantile(0.60):
        segmento = "Medio"
    elif ingreso_pred < dataset['ingres_pred'].quantile(0.80):
        segmento = "Alto"
    else:
        segmento = "Muy Alto"

    st.info(f"📊 Segmento del cliente: **{segmento}**")
