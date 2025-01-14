import re
import streamlit as st
from utils.fonctions import *

st.set_page_config(
    page_title="Netflix Clone",
    page_icon="🎬",
    layout="wide"
)

#css
load_css("style.css")

with st.sidebar:
    call_chatbot()

movies = load_movies()


if "query" in st.session_state:
    query = st.session_state["query"]
    
    st.markdown("<h2>Résultats de recherche</h2>", unsafe_allow_html=True)
    st.markdown("<h4>Films correspondants à votre recherche</h4>", unsafe_allow_html=True)
    
    titles = movies["title"].tolist()
    results = fuzzy_search(query, titles)
    
    if results:
        matched_titles = [res[0] for res in results]
        matched_movies = movies[movies["title"].isin(matched_titles)]
        matched_movies = matched_movies.drop_duplicates(subset='id_tmdb')
        cols = st.columns(5)
        
        for idx, (_, film) in enumerate(matched_movies.iterrows()):
            col = cols[idx % 5]
            with col:
                with st.container():
                    st.markdown(f"""
                        <div class="movie-card">
                            <img src="{film['lien_photos']}" style="width: 100%; border-radius: 4px;">
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(
                        film['title'],
                        key=f"btn_{idx}",
                        use_container_width=True,
                    ):
                        st.session_state["selected_film"] = film.to_dict()
                        st.switch_page("pages/page_3.py")
    else:
        st.warning("Aucun résultat trouvé pour votre recherche.")
        if st.button("Retour à la page principale"):
            st.switch_page("pages/main.py")
else:
    st.error("Aucune recherche détectée. Veuillez effectuer une recherche depuis la page principale.")
    if st.button("Retour à la page principale"):
        st.switch_page("pages/main.py")

#button navigation 
col1, col2, col3 = st.columns([1,2, 1])
with col3:
    if st.button("→ Page suivante"):
        st.switch_page("pages\page_3.py")
with col1 : 
    if st.button("← Page précédente"):
        st.switch_page("pages\main.py")
