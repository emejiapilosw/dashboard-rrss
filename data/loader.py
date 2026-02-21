import pandas as pd
import streamlit as st

@st.cache_data
def load_excel(file):
    df = pd.read_excel(file)
    return df