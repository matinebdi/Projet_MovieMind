import streamlit as st
from utils.fonctions import (
    load_css,
    get_random_movies,
    afficher_films_sans_boutons,
    load_movies,
    call_chatbot,
    afficher_films_par_cible
    
)
from utils.vectorestore import load_vectorstore

st.set_page_config(
    page_title="MovieMind",
    page_icon="🎬",
    layout="wide"
)

# Chargement du CSS personnalisé
load_css("style.css")



# Initialisation de l'état de session
if "selected_film" not in st.session_state:
    st.session_state["selected_film"] = None

# Chargement des films
movies = load_movies()

# Structure de la page principale
container = st.container()

#call chatbot
with st.sidebar:
    call_chatbot()


# Initialisation des variables de session
if "conversation" not in st.session_state:
    st.session_state.conversation = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "query" not in st.session_state:
    st.session_state.query = "spider_man"

# Initialisation du vectorstore
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = load_vectorstore()

# Contenu principal
with container:
    # En-tête
    st.markdown('<h1 class="main-title">MovieMind</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="subtitle">Explorez vos films préférés</h3>', unsafe_allow_html=True)
    # Bouton pour ouvrir le chatbot


    # Barre de recherche
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        query = st.text_input("", placeholder="Rechercher un film...", key="search_input")
    
    # Gestion de la recherche
    if query:
        st.session_state["query"] = query
        st.switch_page("pages/page_2.py")

    # Affichage des films suggérés
    if not query and not movies.empty:
        st.markdown('<h2 style="color: #999; margin: 1em 0;">Films suggérés pour vous</h2>', 
                   unsafe_allow_html=True)
        
        random_movies = get_random_movies(movies, count=20)
        afficher_films_par_cible(random_movies)
    elif movies.empty:
        st.error("Aucune donnée de films disponible. Vérifiez la base de données.")
    




