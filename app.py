import streamlit as st
import plotly.express as px
from auth import login, logout
from data_processing import load_excel
from analytics import calculate_kpis, by_platform

st.set_page_config(
    page_title="Dashboard RRSS",
    page_icon="📊",
    layout="wide"
)

if not login():
    st.stop()

with st.sidebar:
    st.success(f"Usuario: {st.session_state.username}")
    if st.button("Cerrar sesión"):
        logout()

    uploaded_file = st.file_uploader("Sube archivo Excel", type=["xlsx"])

if uploaded_file is None:
    st.info("Sube un archivo para comenzar.")
    st.stop()

df = load_excel(uploaded_file)

kpis = calculate_kpis(df)

st.title("📊 Dashboard Redes Sociales")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Posts", kpis["posts"])
col2.metric("Impressions", f"{kpis['impressions']:,}")
col3.metric("Views", f"{kpis['views']:,}")
col4.metric("Interacciones", f"{kpis['interactions']:,}")

st.divider()

platform_data = by_platform(df)

if platform_data is not None:
    fig = px.bar(
        platform_data,
        x="Platform",
        y="Interacciones",
        color="Platform",
        title="Interacciones por Plataforma"
    )
    st.plotly_chart(fig, use_container_width=True)