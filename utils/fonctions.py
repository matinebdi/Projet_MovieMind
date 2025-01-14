import streamlit as st
import pandas as pd
import os
from fuzzywuzzy import process
import sqlite3

import streamlit as st

def afficher_films_sans_boutons(df_films, nb_colonnes=5):
    """
    Affiche les films en plusieurs lignes, nb_colonnes par ligne,
    SANS bouton (uniquement image + titre). Cette version utilise
    un conteneur HTML + classe CSS pour un rendu plus stylé.
    """
    for i in range(0, len(df_films), nb_colonnes):
        subset = df_films.iloc[i : i + nb_colonnes]
        
        # Toujours nb_colonnes (ex: 5)
        cols = st.columns(nb_colonnes)

        for j, (index, film) in enumerate(subset.iterrows()):
            with cols[j]:
                lien_photo = film.get("lien_photos", None)
                titre = film.get("title", None)
                cibles = film.get("cible" , None)

                if lien_photo:
                    # On injecte directement du HTML + classe CSS
                    st.markdown( f"""
                        <div class="custom-image">
                            <img src="{lien_photo}" alt="{titre}" />
                            <p>{titre}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.warning("Image indisponible.")


def afficher_films_par_cible(df_films, nb_colonnes=5, nb_cibles=4,  nb_films_par_cible=5):
    """
    Affiche des films organisés par catégories (cibles) avec des sections bien séparées.

    Args:
        df_films (pd.DataFrame): DataFrame contenant les films avec 'lien_photos', 'title', et 'cibles'.
        nb_colonnes (int): Nombre de colonnes par ligne pour l'affichage.
        nb_cibles (int): Nombre de cibles à sélectionner.
        nb_films_par_cible (int): Nombre de films à afficher pour chaque cible.
    """
    # Étape 1 : Sélectionner les cibles disponibles
    cibles_disponibles = df_films['cibles'].dropna().unique().tolist()[:nb_cibles]
    
    # Étape 2 : Filtrer et afficher les films pour chaque cible
    for cible in cibles_disponibles:
        st.markdown(f"<h3 style='margin-top: 2em;'>{cible}</h3>", unsafe_allow_html=True)
        
        # Récupérer les films pour cette cible
        films_cible = df_films[df_films['cibles'] == cible].head(nb_films_par_cible)
        
        # Diviser en colonnes
        rows = [films_cible.iloc[i : i + nb_colonnes] for i in range(0, len(films_cible), nb_colonnes)]
        for row in rows:
            cols = st.columns(nb_colonnes)
            for col, (_, film) in zip(cols, row.iterrows()):
                lien_photo = film.get("lien_photos", None)
                titre = film.get("title", "Titre indisponible")
                cible = film.get("cibles", "Cible inconnue")
                
                with col:
                    st.markdown(
                        f"""
                        <div class="custom-image" style="text-align: center; margin-bottom: 1.5em;">
                            <img src="{lien_photo}" alt="{titre}" />
                            <p><strong>{titre}</strong></p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

def afficher_films_avec_boutons(df_films, nb_colonnes=5, prefix="reco"):
    """
    Affiche les films en plusieurs lignes, nb_colonnes par ligne,
    AVEC un bouton. En cliquant, on stocke le film sélectionné
    dans la session et on passe en page 2.
    """
    for i in range(0, len(df_films), nb_colonnes):    
        subset = df_films.iloc[i : i + nb_colonnes]
        cols = st.columns(nb_colonnes)
        for j, (index, film) in enumerate(subset.iterrows()):
            with cols[j]:
                lien_photo = film.get("lien_photos", None)
                titre = film.get("title", None)
                cibles = film.get("cible" , None)
                if lien_photo:
                    st.image(lien_photo, caption=titre, use_container_width=True)
                else:
                    st.warning("Image indisponible.")

                # Bouton pour aller sur la page 2
                btn_key = f"{prefix}_{i}_{j}"
                if st.button(f"Voir '{titre}'", key=btn_key):
                    st.session_state["selected_film"] = film.to_dict()
                    # Redirection vers la page 2
                    st.switch_page("pages/page_3.py")
                    st.switch_page("pages/page_3.py")
            

def get_random_movies(df, count=20):
    
    """Retourne un échantillon aléatoire de films."""
    return df.groupby("cibles").sample(n=count)


def fuzzy_search(query, titles):
    """
    Recherche floue via fuzzywuzzy.process.extract.
    On ne garde que ceux dont le score >= 70.
    """
    matches = process.extract(query, titles, limit=10)
    return [m for m in matches if m[1] >= 70]


def load_css(file_name):
    """
    Charge un fichier CSS (dans un dossier 'styles' à côté).
    """
    css_path = os.path.join("styles", file_name)
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.error(f"Le fichier CSS '{file_name}' est introuvable.")

def load_movies():
    try:
        return pd.read_csv("data/recommendation_dataset.csv")  
    except FileNotFoundError:
        st.error("Le fichier de données est introuvable. Vérifiez le chemin.")
        return pd.DataFrame()
    
def connect_to_db(db_path="data/chroma.sqlite3"):
    """
    Connecte à la base SQLite et retourne l'objet connexion.
    """
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        st.error(f"Erreur lors de la connexion à la base de données : {e}")
        return None

def call_chatbot():
    from utils.chatbot import get_embeddings, get_conversation_chain, get_vectorstore
    
    # Tout le contenu de la sidebar
    with st.sidebar:
        st.title("Chatbot 🤖")
        
        # Initialisation des variables de session
        if "conversation" not in st.session_state:
            st.session_state.conversation = None
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Interface de chat
        st.markdown("""
        ### 👋 Bienvenue dans votre assistant de film
        Vous n'avez pas d'idée ? Nous sommes là pour vous proposer un film !
        """)

        # Champ de saisie utilisateur
        user_input = st.text_input(
            "Que souhaitez-vous comme film ?",
            key="user_input", 
            placeholder="Posez-moi des questions sur les films"
        )
        
        if user_input:
            try:
                # Chargement de la base de données vectorielle
                vectorstore = get_vectorstore()
                if st.session_state.conversation is None:
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                
                # Traitement de la requête utilisateur
                with st.spinner('Recherche du film parfait...'):
                    response = st.session_state.conversation.invoke({
                        "question": user_input,
                        "chat_history": st.session_state.chat_history
                    })
                    
                    # Mise à jour de l'historique
                    st.session_state.chat_history.append((user_input, response["answer"]))
                    
                    # Affichage de la réponse
                    st.markdown('<div class="chat-message assistant-message">', unsafe_allow_html=True)
                    st.markdown(response["answer"])
                    st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erreur : {e}")

        # Bouton pour réinitialiser la conversation
        if st.button("Réinitialiser la conversation"):
            # Réinitialisation des variables de session
            st.session_state.conversation = None
            st.session_state.chat_history = []
            # Rafraîchissement de la page
            st.rerun()



