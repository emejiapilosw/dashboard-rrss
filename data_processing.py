import pandas as pd
import streamlit as st
import io

@st.cache_data
def load_excel(file):
    df = pd.read_excel(io.BytesIO(file.read()), engine="openpyxl")
    return clean_dataframe(df)


@st.cache_data
def clean_dataframe(df):
    df.columns = df.columns.str.strip()

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    numeric_cols = [
        "Impressions","Views","Reach","Likes",
        "Comments/Replies","Shares","Interacciones","E.R."
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "")
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    if "Interacciones" not in df.columns:
        interaction_cols = ["Likes","Comments/Replies","Shares"]
        df["Interacciones"] = 0
        for col in interaction_cols:
            if col in df.columns:
                df["Interacciones"] += df[col]

    if len(df) > 50000:
        st.warning("Máximo 50k registros permitidos.")
        st.stop()

    return df