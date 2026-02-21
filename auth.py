import streamlit as st
import bcrypt

def check_password(username, password):
    if username not in st.secrets["users"]:
        return False

    stored_hash = st.secrets["users"][username].encode()
    return bcrypt.checkpw(password.encode(), stored_hash)


def login():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.title("🔐 Login")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if check_password(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

    return False


def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()