import streamlit as st

# ===============================
# CONFIGURACIÓN
# ===============================

st.set_page_config(
    page_title="Dashboard RRSS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===============================
# IMPORTS INTERNOS
# ===============================

from ui.theme import apply_theme
from core.auth import login
from analytics.engine import compute_all
from ui.kpi_cards import render_kpis
from ui.render_group_tab import render_group_tab

import pandas as pd


# ===============================
# THEME
# ===============================

apply_theme()


# ===============================
# LOGIN
# ===============================

if not login():
    st.stop()


# ===============================
# HEADER
# ===============================

st.title("Dashboard Redes Sociales")
st.markdown("Análisis avanzado de desempeño digital")


# ===============================
# FILE UPLOADER
# ===============================

uploaded_file = st.file_uploader(
    "📂 Cargar archivo Excel",
    type=["xlsx"],
    help="Sube el archivo con los datos de redes sociales"
)

if uploaded_file is None:
    st.info("⬆ Sube un archivo Excel para comenzar el análisis.")
    st.stop()


# ===============================
# PROCESAMIENTO (CACHE)
# ===============================

@st.cache_data(show_spinner=True)
def process_file(file):
    df = pd.read_excel(file)
    return compute_all(df)


results = process_file(uploaded_file)


# ===============================
# KPI
# ===============================

render_kpis(results)


# ===============================
# TABS
# ===============================

tabs = st.tabs([
    "📱 Plataforma",
    "🎭 Género",
    "📦 Formato",
    "🧩 Content Format",
    "🗂 Content Group",
    "📝 Título",
    "📊 Ejecutivo"
])

with tabs[0]:
    render_group_tab(results, "platform", "Platform")

with tabs[1]:
    render_group_tab(results, "genre", "Género")

with tabs[2]:
    render_group_tab(results, "format", "Formato")

with tabs[3]:
    render_group_tab(results, "content_format", "Content Format")

with tabs[4]:
    render_group_tab(results, "content_group", "Content Group")

with tabs[5]:
    render_group_tab(results, "title", "Título")

with tabs[6]:
    render_group_tab(results, "platform", "Resumen Ejecutivo")
