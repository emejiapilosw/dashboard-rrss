import streamlit as st

# ===============================
# CONFIGURACIÓN INICIAL
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
from data.loader import load_excel
from analytics_engine import compute_all
from ui.kpi_cards import render_kpis
from ui.render_group_tab import render_group_tab


# ===============================
# APLICAR THEME GLOBAL
# ===============================

apply_theme()


# ===============================
# AUTENTICACIÓN
# ===============================

if not login():
    st.stop()


# ===============================
# CARGA Y PROCESAMIENTO DE DATA
# ===============================

@st.cache_data(show_spinner=False)
def get_processed_data():
    df = load_excel("data.xlsx")
    return compute_all(df)

results = get_processed_data()


# ===============================
# HEADER
# ===============================

st.title("Dashboard Redes Sociales")
st.markdown("Análisis avanzado de desempeño digital")

render_kpis(results)


# ===============================
# TABS PRINCIPALES
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
