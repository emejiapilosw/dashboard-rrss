import streamlit as st

def render_kpis(kpis):
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Posts", f"{kpis['posts']:,}")
    col2.metric("Impressions", f"{kpis['impressions']:,}")
    col3.metric("Reach", f"{kpis['reach']:,}")
    col4.metric("Interacciones", f"{kpis['interactions']:,}")
    col5.metric("Avg ER", f"{kpis['avg_er']:.2f}%")