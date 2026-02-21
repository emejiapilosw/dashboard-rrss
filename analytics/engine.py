import streamlit as st

@st.cache_data
def compute_all(df):

    results = {}

    # ======================
    # KPIs
    # ======================

    results["kpis"] = {
        "posts": len(df),
        "impressions": df["Impressions"].sum(),
        "reach": df["Reach"].sum(),
        "views": df["Views"].sum(),
        "interactions": df["Interacciones"].sum(),
        "avg_er": df["E.R."].mean()
    }

    # ======================
    # Agrupaciones base
    # ======================

    def build_group(col):
        grouped = (
            df.groupby(col)
            .agg(
                Posts=("Platform", "count"),
                Interacciones=("Interacciones", "sum"),
                Impressions=("Impressions", "sum"),
                Reach=("Reach", "sum"),
                Views=("Views", "sum"),
                ER=("E.R.", "mean")
            )
            .reset_index()
            .sort_values("Interacciones", ascending=False)
        )
        return grouped

    results["platform"] = build_group("Platform")
    results["genre"] = build_group("Género")
    results["format"] = build_group("Formato")
    results["content_format"] = build_group("PV_Content Format")
    results["content_group"] = build_group("PV_Content Format Group")
    results["title"] = build_group("Título")

    return results