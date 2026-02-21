import streamlit as st


def render_kpis(results):

    # Seguridad para evitar crashes
    kpis = results.get("kpis", {})

    posts = kpis.get("posts", 0)
    impressions = kpis.get("impressions", 0)
    reach = kpis.get("reach", 0)
    views = kpis.get("views", 0)
    interactions = kpis.get("interactions", 0)
    avg_er = kpis.get("avg_er", 0)

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric("Posts", f"{posts:,}")
    col2.metric("Impressions", f"{impressions:,}")
    col3.metric("Reach", f"{reach:,}")
    col4.metric("Views", f"{views:,}")
    col5.metric("Interacciones", f"{interactions:,}")
    col6.metric("Avg ER", f"{avg_er:.2%}")
