import streamlit as st
import datetime
import pytz
import time
import requests
from io import BytesIO
import data
import pandas as pd
import video

# Configuración de la página
st.set_page_config(page_title="Movie Recommendation", page_icon='🎦', layout="wide")

# Cargar datos
df = data.data_genre_explode()

# Estilos y Bootstrap
bootstrap_css = """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
"""

custom_css = """
<style>
    .navbar { background-color: #333; }
    .navbar-brand, .nav-link { color: white !important; }
    .dropdown-menu { background-color: #333; }
    .dropdown-item { color: white !important; }
    .dropdown-item:hover { background-color: #555; }
</style>
"""

# Navbar HTML
navbar_html = """
<nav class="navbar navbar-expand-lg">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">Movie Recommendations</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link" href="#" onclick="handleNavClick('Home')">Home</a>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Genres
          </a>
          <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
            <li><a class="dropdown-item" href="#" onclick="handleNavClick('Drama')">Drama</a></li>
            <li><a class="dropdown-item" href="#" onclick="handleNavClick('Action')">Action</a></li>
          </ul>
        </li>
        <li class="dropdown">
         <a class="btn btn-secondary dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Dropdown link
         </a>
         <ul class="nav-item dropdown-menu">
            <li><a class="dropdown-item" href="#">Action</a></li>
            <li><a class="dropdown-item" href="#">Another action</a></li>
            <li><a class="dropdown-item" href="#">Something else here</a></li>
         </ul>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#" onclick="handleNavClick('Top Rated')">Top Rated</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#" onclick="handleNavClick('New Releases')">New Releases</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#" onclick="handleNavClick('Community')">Community</a>
        </li>
      </ul>
      <form class="d-flex">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form>
    </div>
  </div>
</nav>

<script>
function handleNavClick(page) {
    // Use Streamlit's JavaScript API to update the app state
    Streamlit.setComponentValue(page);
}
</script>
"""

# Mostrar navbar
st.markdown(bootstrap_css + custom_css + navbar_html, unsafe_allow_html=True)

# Manejar la navegación
if 'nav' not in st.session_state:
    st.session_state.nav = 'Home'

nav = st.session_state.nav

# Contenido de la página basado en la navegación
if nav == "Home":
    st.title("Welcome to Movie Recommendations")
    st.write("Discover your next favorite movie!")
elif nav in df['genres_x'].unique():
    st.title(f"Exploring {nav} movies")
    df_genre = df[df['genres_x'] == nav].sort_values(by='averageRating', ascending=False)
    # ... (rest of your genre-specific code)
elif nav == "Top Rated":
    st.title("Top Rated Movies")
    st.write("Check out the highest-rated films")
elif nav == "New Releases":
    st.title("New Releases")
    st.write("The latest movies to hit the screens")
elif nav == "Community":
    st.title("Community")
    st.write("Connect with other movie enthusiasts")

# Actualizar la navegación basada en la interacción del usuario
new_nav = st.query_params.get('nav', None)
if new_nav:
    st.session_state.nav = new_nav
    st.rerun()