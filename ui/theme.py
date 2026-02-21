import streamlit as st

def apply_theme():
    st.markdown("""
        <style>
        .stApp {
            background-color: #0f172a;
            color: #f1f5f9;
        }

        /* Texto general */
        html, body, [class*="css"]  {
            color: #f1f5f9;
        }

        /* Labels */
        label {
            color: #e2e8f0 !important;
        }

        /* Radio / Slider */
        .stSlider, .stRadio {
            color: #e2e8f0 !important;
        }

        /* Metric cards */
        div[data-testid="metric-container"] {
            background-color: #1e293b;
            padding: 18px;
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
