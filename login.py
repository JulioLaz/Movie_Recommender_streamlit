import streamlit as st
import hydralit_components as hc
import datetime
import pytz
import time
import requests
from io import BytesIO
import data
import pandas as pd

st.set_page_config(page_title="movie recommendation", page_icon='🎦', layout="wide")

df = data.data_genre_explode()

def get_current_time():
    return datetime.datetime.now(pytz.timezone('US/Eastern')).strftime("%H:%M:%S")

element_style = '''<style>
#root > div:nth-child(1) > div.withScreencast > div > div > header{
display: none}
#root > div:nth-child(1) > div.withScreencast > div > div > div > section.main.st-emotion-cache-bm2z3a.ea3mdgi8 > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5{
padding:0 !important;
}
#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(5),
#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div > div > div > div:nth-child(6){
display: none}
'''
st.markdown(element_style, unsafe_allow_html=True)

# Define the menu
menu_data = [
    {'icon': "fas fa-film", 'label': "Genres", 'submenu': [
        {'icon': "🎭", 'label': "Drama"},
        {'icon': "🎬", 'label': "Action"},
        {'icon': "🗺️", 'label': "Adventure"},
        {'icon': "💕", 'label': "Romance"},
        {'icon': "🤠", 'label': "Western"},
        {'icon': "🏛️", 'label': "History"},
        {'icon': "👻", 'label': "Horror"},
        {'icon': "🕵️", 'label': "Mystery"},
        {'icon': "😱", 'label': "Thriller"},
        {'icon': "😂", 'label': "Comedy"},
        {'icon': "👪", 'label': "Family"},
        {'icon': "🦹", 'label': "Crime"},
        {'icon': "⚔️", 'label': "War"},
        {'icon': "🚀", 'label': "Sci-Fi"},
        {'icon': "🎵", 'label': "Music"},
        {'icon': "🎭", 'label': "Musical"},
        {'icon': "⚽", 'label': "Sport"},
        {'icon': "📜", 'label': "Biography"},
        {'icon': "🎞️", 'label': "Film-Noir"},
        {'icon': "🧙", 'label': "Fantasy"},
        {'icon': "🎨", 'label': "Animation"},
        {'icon': "🎥", 'label': "Documentary"},
        {'icon': "🔞", 'label': "Adult"},
        {'icon': "📰", 'label': "News"},
        {'icon': "📺", 'label': "Reality-TV"}
    ]},
    {'icon': "fas fa-star", 'label': "Top Rated"},
    {'icon': "fas fa-calendar-alt", 'label': "New Releases"},
    {'icon': "fas fa-users", 'label': "Community"},
]

over_theme = {'txc_inactive': 'blue','menu_background':'gray','txc_active':'yellow','option_active':'black'}

# Create the navbar
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='Home',
    login_name='Login',
    hide_streamlit_markers=True,
    sticky_nav=False,
    sticky_mode='none',
)

# Function to handle login
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Log In"):
        # Here you would typically check the username and password against a database
        # For this example, we'll use a simple check
        if username == "admin" and password == "password":
            st.success("Logged in successfully!")
            st.session_state['logged_in'] = True
        else:
            st.error("Incorrect username or password")

# Check if user is logged in
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if menu_id == "Login":
    if not st.session_state['logged_in']:
        login()
    else:
        st.write("You are already logged in!")
        if st.button("Log Out"):
            st.session_state['logged_in'] = False
            st.experimental_rerun()
elif menu_id == "Home":
    st.title("Welcome to Movie Recommendations")
    st.write("Discover your next favorite movie!")
elif menu_id == "Genres":
    st.title("Movie Genres")
    st.write("Explore movies by genre")
elif menu_id == "Top Rated":
    st.title("Top Rated Movies")
    st.write("Check out the highest-rated films")
elif menu_id == "New Releases":
    st.title("New Releases")
    st.write("The latest movies to hit the screens")
elif menu_id == "Community":
    st.title("Community")
    st.write("Connect with other movie enthusiasts")
else:
    st.title(f"Exploring {menu_id} movies")
    df_genre = df[df['genres_x'] == menu_id].sort_values(by='averageRating', ascending=False)
    lista_poster = list(df_genre['poster_path'].head(5))
    lista_originalTitle = list(df_genre['originalTitle'].head(5))

    def load_image_from_url(url):
        response = requests.get(url)
        return BytesIO(response.content)

    st.title(f"Movie Posters {menu_id.upper()} Top 5")
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            try:
                image = load_image_from_url(lista_poster[i])
                st.image(image, use_column_width=True, caption=lista_originalTitle[i])
            except IndexError:
                st.error(f"Index {i} out of range for the title list.")
            except Exception as e:
                st.markdown(
                    f"""
                    <div style="background-color:black;color:white;padding:20px;text-align:center;">
                        <b>{lista_originalTitle[i]}</b>
                    </div>
                    """, unsafe_allow_html=True
                )

    st.write(f"Here are some great {menu_id} movies for you")

placeholder = st.empty()