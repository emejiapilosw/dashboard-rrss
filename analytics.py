import streamlit as st

@st.cache_data
def calculate_kpis(df):
    return {
        "posts": len(df),
        "impressions": df["Impressions"].sum() if "Impressions" in df else 0,
        "views": df["Views"].sum() if "Views" in df else 0,
        "reach": df["Reach"].sum() if "Reach" in df else 0,
        "interactions": df["Interacciones"].sum() if "Interacciones" in df else 0,
        "avg_er": df["E.R."].mean() if "E.R." in df else 0,
    }


@st.cache_data
def by_platform(df):
    if "Platform" not in df:
        return None

    return (
        df.groupby("Platform")
        .agg({
            "Interacciones": "sum",
            "E.R.": "mean"
        })
        .reset_index()
        .sort_values("Interacciones", ascending=False)
    )