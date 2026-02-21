import streamlit as st
import pandas as pd

from analytics.engine import compute_all
from ui.kpi_cards import render_kpis
from ui.render_group_tab import render_group_tab
from auth import login


st.set_page_config(
    page_title="Dashboard RRSS",
    page_icon="📊",
    layout="wide"
)

# ======================
# LOGIN
# ======================

if not login():
    st.stop()

st.title("📊 Dashboard Redes Sociales")

# ======================
# FILE UPLOADER
# ======================

uploaded_file = st.file_uploader(
    "Sube tu archivo Excel",
    type=["xlsx"]
)

if uploaded_file is None:
    st.info("Carga un archivo para comenzar.")
    st.stop()

try:
    df = pd.read_excel(uploaded_file)
except:
    st.error("Error leyendo el archivo.")
    st.stop()

results = compute_all(df)

# ======================
# KPIs
# ======================

render_kpis(results)

# ======================
# TABS
# ======================

tabs = st.tabs([
    "Platform",
    "Género",
    "Formato",
    "Content Format",
    "Content Group",
    "Título"
])

with tabs[0]:
    render_group_tab("Platform", results["platform"], "Platform")

with tabs[1]:
    render_group_tab("Género", results["genre"], "Género")

with tabs[2]:
    render_group_tab("Formato", results["format"], "Formato")

with tabs[3]:
    render_group_tab("Content Format", results["content_format"], "PV_Content Format")

with tabs[4]:
    render_group_tab("Content Group", results["content_group"], "PV_Content Format Group")

with tabs[5]:
    render_group_tab("Título", results["title"], "Título")
