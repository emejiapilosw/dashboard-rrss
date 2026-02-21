import streamlit as st

PRIMARY = "#38bdf8"
PRIMARY_HOVER = "#0ea5e9"
BACKGROUND_TOP = "#0b1220"
BACKGROUND_BOTTOM = "#0f172a"
CARD_BG = "rgba(15, 23, 42, 0.85)"
BORDER = "#1e293b"
TEXT_MAIN = "#f8fafc"
TEXT_SECONDARY = "#94a3b8"

def apply_theme():

    st.markdown(f"""
    <style>

    /* ===== APP BACKGROUND ===== */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(180deg, {BACKGROUND_TOP} 0%, {BACKGROUND_BOTTOM} 100%);
        color: {TEXT_MAIN};
    }}

    /* ===== HEADINGS ===== */
    h1, h2, h3 {{
        color: {PRIMARY} !important;
    }}

    /* ===== KPI CARDS ===== */
    [data-testid="metric-container"] {{
        background-color: {CARD_BG};
        border: 1px solid {BORDER};
        padding: 15px;
        border-radius: 12px;
    }}

    [data-testid="metric-container"] label {{
        color: {TEXT_SECONDARY} !important;
    }}

    [data-testid="metric-container"] div {{
        color: {TEXT_MAIN} !important;
        font-weight: 600;
    }}

    /* ===== TABS ===== */
    button[data-baseweb="tab"] {{
        color: {TEXT_SECONDARY} !important;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {PRIMARY} !important;
    }}

    /* ===== BUTTONS ===== */
    .stButton>button {{
        background-color: {PRIMARY};
        color: {BACKGROUND_TOP};
        border-radius: 8px;
        font-weight: 600;
        border: none;
    }}

    .stButton>button:hover {{
        background-color: {PRIMARY_HOVER};
        color: white;
    }}

    </style>
    """, unsafe_allow_html=True)
