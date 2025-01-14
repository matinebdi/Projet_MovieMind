import streamlit as st
import pandas as pd
from utils.fonctions import load_css
from utils.chatbot import get_embeddings

st.set_page_config(
    page_title="Netflix Clone - Connexion",
    page_icon="🎬",
    layout="wide"
)

load_css("style.css")

# Initialisation des variables de session
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login(username, password):

    if username == "admin" and password == "admin":
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
        return True
    return False

def main():
    # Container principal
    with st.container():
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        

        
        st.markdown('<h1 class="login-title">Connexion</h1>', unsafe_allow_html=True)
        
        # Formulaire de connexion
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Email ou numéro de téléphone")
            password = st.text_input("Mot de passe", type="password", placeholder="Mot de passe")
            
            if st.form_submit_button("Se connecter"):
                if login(email, password):
                    st.success("Connexion réussie!")
                    st.switch_page("pages/main.py")
                else:
                    st.markdown("""
                        <div class="error-message">
                            Désolé, nous ne trouvons pas de compte avec cette adresse email. 
                            Veuillez réessayer ou créer un nouveau compte.
                        </div>
                    """, unsafe_allow_html=True)
        
        # Liens supplémentaires
        st.markdown("""
            <div class="login-text">
                Première visite sur MovieMind ? 
                <a href="#" class="login-link">Inscrivez-vous</a>
            </div>
            
            <div class="divider"></div>
            
            <div class="login-text">
                Cette page est protégée par Google reCAPTCHA pour nous assurer que vous n'êtes pas un robot.
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    if not st.session_state['logged_in']:
        main()
    else:
        st.switch_page("login.py")

