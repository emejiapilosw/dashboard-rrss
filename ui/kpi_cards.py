import streamlit as st


def render_kpis(results):

    kpis = results.get("kpis", {})

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric("Posts", f"{kpis.get('posts',0):,}")
    col2.metric("Impressions", f"{kpis.get('impressions',0):,}")
    col3.metric("Reach", f"{kpis.get('reach',0):,}")
    col4.metric("Views", f"{kpis.get('views',0):,}")
    col5.metric("Interacciones", f"{kpis.get('interactions',0):,}")
    col6.metric("Avg ER", f"{kpis.get('avg_er',0):.2%}")
