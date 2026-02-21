import streamlit as st
import plotly.express as px
from ui.table_style import style_table

def render_platform(results):

    df = results["platform"]

    st.subheader("🚀 Performance por Plataforma")

    # Gráfico
    fig = px.bar(
        df,
        x="Interacciones",
        y="Platform",
        orientation="h",
        text="Interacciones"
    )

    fig.update_layout(
        template="plotly_dark",
        yaxis=dict(categoryorder="total ascending")
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(style_table(df), use_container_width=True)