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
    .login-container {
        background: rgba(15, 23, 42, 0.85);
        padding: 40px;
        border-radius: 16px;
        border: 1px solid #1e293b;
        max-width: 400px;
        margin: auto;
        margin-top: 100px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    st.title("🔐 Login")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    # Botón con contraste real
    st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #38bdf8;
        color: #0b1220;
        font-weight: 600;
        border-radius: 8px;
        height: 42px;
    }
    div.stButton > button:first-child:hover {
        background-color: #0ea5e9;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("Ingresar", use_container_width=True):
        if check_password(username, password):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

    st.markdown("</div>", unsafe_allow_html=True)

    return False
