import streamlit as st
import pandas as pd

from analytics.engine import compute_all
from ui.kpi_cards import render_kpis
from auth import login


# ======================
# Configuración base
# ======================

st.set_page_config(
    page_title="Dashboard RRSS",
    page_icon="📊",
    layout="wide"
)

# ======================
# Login
# ======================

if not login():
    st.stop()

# ======================
# Título
# ======================

st.title("📊 Dashboard Redes Sociales")

# ======================
# Carga de archivo
# ======================

uploaded_file = st.file_uploader(
    "Sube tu archivo Excel",
    type=["xlsx"]
)

if uploaded_file is None:
    st.info("Carga un archivo para comenzar el análisis.")
    st.stop()

# ======================
# Lectura Excel
# ======================

try:
    df = pd.read_excel(uploaded_file)
except Exception as e:
    st.error("Error leyendo el archivo Excel.")
    st.stop()

# ======================
# Validación mínima de columnas
# ======================

required_cols = [
    "Impressions",
    "Reach",
    "Views",
    "Interacciones",
    "E.R.",
    "Platform"
]

missing = [c for c in required_cols if c not in df.columns]

if missing:
    st.error(f"Faltan columnas obligatorias: {missing}")
    st.stop()

# ======================
# Cálculo
# ======================

results = compute_all(df)

# ======================
# Render KPIs
# ======================

render_kpis(results)

# ======================
# Preview opcional
# ======================

with st.expander("Ver datos cargados"):
    st.dataframe(df.head())
