import streamlit as st
import pandas as pd
from utils.fonctions import *
import datetime

st.set_page_config(page_title="NetflixClone", page_icon="🎬", layout="wide")
#css
load_css("style.css")

with st.sidebar:
    call_chatbot()


if "selected_film" in st.session_state and st.session_state["selected_film"]:
    film = st.session_state["selected_film"]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f'<h1 class="movie-title">{film["title"]}</h1>', unsafe_allow_html=True)
        st.markdown(f'<p class="movie-description">{film["overview"]}</p>', unsafe_allow_html=True)
        st.markdown("")
        
        st.markdown(f"""
        <div class="movie-info">
        ⭐ Note: {film.get('note_moyenne', 0) if pd.notna(film.get('note_moyenne')) else 0}/10<br>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.write("")
        
        col_btn1, col_btn2 = st.columns([1, 2])
        with col_btn2:
            if st.button("▶️ Voir plus de détails", use_container_width=True):
                st.switch_page("pages/page_4.py")
        with col_btn1:
            st.button("+ Ma Liste", use_container_width=True, icon="❤️")
    
    with col2:
        st.image(film["lien_photos"], use_container_width=True)

    st.markdown('<p class="category-title">Films recommendés</p>', unsafe_allow_html=True)
    recommendations = eval(film.get("recommendations", "[]"))
    movies = load_movies()
    recommended_movies = movies[movies["title"].isin(recommendations)]
    
    cols = st.columns(5)
    for idx, (_, movie) in enumerate(recommended_movies.iterrows()):
        with cols[idx % 5]:
            with st.container():
                st.markdown(f"""
                    <div class="movie-card">
                        <img src="{movie['lien_photos']}" style="width: 100%; border-radius: 4px;">
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(
                    movie["title"],
                    key=f"rec_{idx}",
                    use_container_width=True
                ):
                    st.session_state["selected_film"] = movie.to_dict()
                    st.rerun()

#button navigation 
col1, col2 , col3 = st.columns([1,2,1])
with col3:
    if st.button("→ Page suivante"):
        st.switch_page("pages\page_4.py")
with col1:
    if st.button("← Page précédente"):
        st.switch_page("pages\page_2.py")