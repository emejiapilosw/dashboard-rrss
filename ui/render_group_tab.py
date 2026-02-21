import streamlit as st
import plotly.express as px
from ui.table_style import style_table


def render_group_tab(results, key, group_col):

    if key not in results:
        st.warning("No hay datos disponibles para este análisis.")
        return

    df = results[key].copy()

    if df.empty:
        st.warning("No hay datos disponibles para este análisis.")
        return

    st.subheader(f"📊 Análisis por {group_col}")

    # =====================
    # Toggle Ejecutivo / Técnico
    # =====================

    view_mode = st.radio(
        "Vista",
        ["Ejecutiva", "Técnica"],
        horizontal=True,
        key=f"view_{key}"
    )

    # =====================
    # Top N inteligente
    # =====================

    total_rows = len(df)

    if total_rows <= 1:
        top_n = total_rows
    else:
        min_slider = 1
        max_slider = min(50, total_rows)
        default_value = min(10, max_slider)

        top_n = st.slider(
            "Top N",
            min_value=min_slider,
            max_value=max_slider,
            value=default_value,
            key=f"top_{key}"
        )

    df_exec = df.head(top_n).copy()

    # =====================
    # Gráfico DARK real
    # =====================

    if "Interacciones" in df_exec.columns:

        fig = px.bar(
            df_exec,
            x="Interacciones",
            y=group_col,
            orientation="h",
            text="Interacciones"
        )

        fig.update_layout(
            height=450,
            paper_bgcolor="#0b1220",
            plot_bgcolor="#0b1220",
            font=dict(color="#f8fafc"),
            yaxis=dict(
                categoryorder="total ascending",
                showgrid=False
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor="#1f2937"
            ),
            margin=dict(l=20, r=20, t=30, b=20)
        )

        # Colores dinámicos (Top 1 destacado)
        colors = ["#38bdf8"] * len(df_exec)
        if len(colors) > 0:
            colors[0] = "#22c55e"

        fig.update_traces(
            marker_color=colors,
            texttemplate="%{text:,.0f}",
            textposition="outside"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("No existe la columna 'Interacciones' para graficar.")

    st.divider()

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

        available_cols = [c for c in cols_exec if c in df_exec.columns]

        if not available_cols:
            st.warning("No hay columnas disponibles para mostrar.")
            return

        df_to_show = df_exec[available_cols].copy()

        st.dataframe(
            style_table(df_to_show),
            use_container_width=True
        )

    else:

        st.dataframe(
            style_table(df),
            use_container_width=True
        )
