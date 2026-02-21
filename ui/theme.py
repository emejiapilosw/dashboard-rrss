import streamlit as st

def apply_theme():
    st.markdown("""
        <style>
        .stApp {
            background-color: #0f172a;
            color: white;
        }

        div[data-testid="metric-container"] {
            background-color: #1e293b;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #334155;
        }

        .big-title {
            font-size: 32px;
            font-weight: 700;
            color: #38bdf8;
        }
        </style>
    """, unsafe_allow_html=True)