import streamlit as st
import pandas as pd
import ast
from utils.fonctions import load_css , call_chatbot

st.set_page_config(page_title="NetflixClone", page_icon="🎬", layout="wide")
#css
load_css("style.css")

with st.sidebar:
    call_chatbot()

if "selected_film" not in st.session_state:
    st.session_state["selected_film"] = None


if st.session_state["selected_film"]:
    film = st.session_state["selected_film"]

    # En-tête du film
    st.markdown(f'<h1 class="movie-title">{film["title"]}</h1>', unsafe_allow_html=True)

    # Layout principal
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
            <div class="movie-container">
        """, unsafe_allow_html=True)
        st.image(film.get("lien_photos", ""), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="video-container">
            <h3 class="section-title">🎥 Bande-annonce</h3>
        """, unsafe_allow_html=True)
        
        if "trailers" in film and pd.notnull(film["trailers"]):
            try:
                trailers = ast.literal_eval(film["trailers"]) if isinstance(film["trailers"], str) else film["trailers"]
                if trailers:
                    selected_trailer = st.selectbox(
                        "Choisissez une bande-annonce :",
                        trailers,
                        key="trailer_select"
                    )
                    st.video(selected_trailer)
                else:
                    st.info("Aucune bande-annonce disponible.")
            except Exception as e:
                st.error(f"Erreur lors de la lecture des trailers : {e}")
        else:
            st.info("Aucune bande-annonce disponible.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Section description
    st.markdown("""
        <div class="movie-container">
        <h3 class="section-title">📖 Synopsis</h3>
        <div class="movie-description">
    """, unsafe_allow_html=True)
    st.write(film.get("overview", "Aucune description disponible."))
    st.markdown("</div></div>", unsafe_allow_html=True)

    # Section informations
    st.markdown("""
        <div class="movie-container">
        <h3 class="section-title">ℹ️ Informations</h3>
    """, unsafe_allow_html=True)
    
    # Note moyenne
    st.markdown(f"""
        <div class="movie-rating">
        ⭐ Note : {film.get('note_moyenne', 'N/A')}/10
        </div>
    """, unsafe_allow_html=True)

    # Casting
    st.markdown('<h3 class="section-title">🎭 Distribution</h3>', unsafe_allow_html=True)
    acteur_name = 'name_x'
    if acteur_name in film and pd.notnull(film[acteur_name]):
        try:
            cast = ast.literal_eval(film[acteur_name]) if isinstance(film[acteur_name], str) else film[acteur_name]
            st.markdown(f"""
                <div class="movie-cast">
                {", ".join(cast)}
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Erreur lors de la lecture des intervenants : {e}")
    else:
        st.write("Aucun intervenant disponible.")
    st.markdown("</div>", unsafe_allow_html=True)

    # Bouton retour
    if st.button("← Retour", use_container_width=False):
        st.switch_page("pages/page_3.py")
else:
    st.error("Aucun film sélectionné. Veuillez revenir à la page principale.")
    if st.button("Retour à la page principale"):
        st.switch_page("pages/main.py")