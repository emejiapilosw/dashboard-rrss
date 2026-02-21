import streamlit as st

def apply_theme():
    st.markdown("""
        <style>

        /* Fondo general */
        .stApp {
            background-color: #0b1220;
        }

        /* Texto general */
        html, body, [class*="css"]  {
            color: #f8fafc !important;
        }

        /* Títulos */
        h1, h2, h3, h4 {
            color: #38bdf8 !important;
        }

        /* Labels */
        label {
            color: #e2e8f0 !important;
            font-weight: 500;
        }

        /* MÉTRICAS */
        div[data-testid="metric-container"] {
            background: #111827;
            border: 1px solid #1f2937;
            padding: 20px;
            border-radius: 14px;
        }

        div[data-testid="metric-container"] label {
            color: #94a3b8 !important;
            font-size: 14px !important;
        }

        div[data-testid="metric-container"] div {
            color: #ffffff !important;
            font-size: 28px !important;
            font-weight: 600 !important;
        }

        /* Tabs */
        button[role="tab"] {
            color: #cbd5e1 !important;
        }

        button[aria-selected="true"] {
            color: #38bdf8 !important;
        }

        /* Slider labels */
        .stSlider label {
            color: #e2e8f0 !important;
        }

        </style>
    """, unsafe_allow_html=True)
