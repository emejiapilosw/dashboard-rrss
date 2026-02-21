import streamlit as st
import plotly.express as px
from ui.table_style import format_table


def render_group_tab(title, df, group_column):

    st.subheader(f"Análisis por {title}")

    if df.empty:
        st.warning("No hay datos disponibles.")
        return

    # Orden por Interacciones descendente
    df = df.sort_values("Interacciones", ascending=False)

    # === GRÁFICA ===
    fig = px.bar(
        df,
        x=group_column,
        y="Interacciones",
        text="Interacciones"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

    # === TABLA ===
    st.dataframe(
        format_table(df),
        use_container_width=True
    )
