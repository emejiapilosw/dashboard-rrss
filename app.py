import streamlit as st
import pandas as pd

from core.auth import login
from data.loader import load_excel
from analytics.engine import compute_all
from ui.theme import apply_theme
from ui.kpi_cards import render_kpis
from ui.render_group_tab import render_group_tab

# ==========================
# CONFIG
# ==========================

st.set_page_config(
    page_title="Dashboard RRSS",
    layout="wide",
    page_icon="📊"
)

apply_theme()

# ==========================
# LOGIN
# ==========================

if not login():
    st.stop()

# ==========================
# SIDEBAR
# ==========================

st.sidebar.title("📂 Cargar archivo")

uploaded_file = st.sidebar.file_uploader(
    "Sube el Excel",
    type=["xlsx"]
)

if uploaded_file is None:
    st.stop()

df = load_excel(uploaded_file)

# ==========================
# MOTOR ANALÍTICO
# ==========================

results = compute_all(df)

# ==========================
# HEADER
# ==========================

st.markdown('<div class="big-title">Dashboard Redes Sociales</div>', unsafe_allow_html=True)
st.write(" ")

render_kpis(results["kpis"])

st.divider()

# ==========================
# TABS
# ==========================

tabs = st.tabs([
    "📈 Plataforma",
    "🎭 Género",
    "📦 Formato",
    "🧩 Content Format",
    "🗂 Content Group",
    "🏷 Título"
])

with tabs[0]:
    render_group_tab(results, "platform", "Platform")

with tabs[1]:
    render_group_tab(results, "genre", "Género")

with tabs[2]:
    render_group_tab(results, "format", "Formato")

with tabs[3]:
    render_group_tab(results, "content_format", "PV_Content Format")

with tabs[4]:
    render_group_tab(results, "content_group", "PV_Content Format Group")

with tabs[5]:
    render_group_tab(results, "title", "Título")