import streamlit as st
import bcrypt


def check_password(username, password):
    if username not in st.secrets["users"]:
        return False
    stored_hash = st.secrets["users"][username]
    return bcrypt.checkpw(password.encode(), stored_hash.encode())


def login():

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    # Fondo limpio
    st.markdown("""
        <style>
        .stTextInput input {
            background-color: #0f172a !important;
            color: #f8fafc !important;
        }

        div.stButton > button {
            background-color: #38bdf8;
            color: #0b1220;
            font-weight: 600;
            border-radius: 10px;
            height: 45px;
        }

        div.stButton > button:hover {
            background-color: #0ea5e9;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🔐 Acceso Seguro")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar", use_container_width=True):
        if check_password(username, password):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

    return False
