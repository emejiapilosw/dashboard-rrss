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

    st.markdown("""
    <style>

    .login-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80vh;
    }

    .login-card {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(20px);
        padding: 50px;
        border-radius: 20px;
        border: 1px solid rgba(56, 189, 248, 0.2);
        width: 420px;
        box-shadow: 0 0 40px rgba(56, 189, 248, 0.1);
    }

    .login-title {
        font-size: 28px;
        font-weight: 600;
        color: #38bdf8;
        margin-bottom: 30px;
        text-align: center;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #38bdf8, #0ea5e9);
        color: white;
        font-weight: 600;
        border-radius: 12px;
        height: 48px;
        border: none;
    }

    div.stButton > button:hover {
        background: linear-gradient(90deg, #0ea5e9, #0284c7);
        color: white;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🔐 Acceso Seguro</div>', unsafe_allow_html=True)

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar", use_container_width=True):
        if check_password(username, password):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    return False
