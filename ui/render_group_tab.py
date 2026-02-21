import streamlit as st
import plotly.express as px
from ui.table_style import style_table


def render_group_tab(results, key, group_col):

    df = results[key].copy()

    st.subheader(f"📊 Análisis por {group_col}")

    # =====================
    # Selector Vista
    # =====================

    view_mode = st.radio(
        "Vista",
        ["Ejecutiva", "Técnica"],
        horizontal=True,
        key=f"view_{key}"
    )

    # =====================
    # Selector Top N
    # =====================

    top_n = st.slider(
        "Top N",
        min_value=5,
        max_value=min(50, len(df)),
        value=min(10, len(df)),
        key=f"top_{key}"
    )

    df_exec = df.head(top_n)

    # =====================
    # Gráfico
    # =====================

    fig = px.bar(
        df_exec,
        x="Interacciones",
        y=group_col,
        orientation="h",
        text="Interacciones"
    )

    fig.update_layout(
        template="plotly_dark",
        yaxis=dict(categoryorder="total ascending"),
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

    # =====================
    # Tabla
    # =====================

    if view_mode == "Ejecutiva":

        cols_exec = [
            group_col,
            "Posts",
            "Interacciones",
            "ER"
        ]

        st.dataframe(
            style_table(df_exec[cols_exec]),
            use_container_width=True
        )

    else:
        st.dataframe(
            style_table(df),
            use_container_width=True
        )