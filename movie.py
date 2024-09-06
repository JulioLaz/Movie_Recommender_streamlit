import streamlit as st
import text_desplazado as tdz
import menu
import styles
import big_fans
import select_genres
import title_poster_genre as tpg
import img_home 
import view_posters as view_posters
import just_for_you
import search_movies
import community
import top_rated
import most_populars

num_movies =8

styles.styles_main()
css_style = """
<style>
* {
    gap:0px 4px!important;
}
.st-emotion-cache-1wmy9hl{
    gap: none!important;
}
.st-emotion-cache-16txtl3 {
    padding: 1rem 1.3rem;
}
</style>
"""

st.markdown(css_style, unsafe_allow_html=True)

menu_data,over_theme,menu_id=menu.menu()

if menu_id == "Home":
    tdz.title_poster('', 'Welcome to Movie Recommendations!')
    img_home.create_movie_welcome_page()

elif menu_id == "Most Populars":
    most_populars.most_populars()

elif menu_id == "Top Rated":
    top_rated.top_rated()

elif menu_id == "Community": #
    community.community()

elif menu_id == "Big fans":
    big_fans.big_fans()
    
elif menu_id == "Just for you":
    just_for_you.just_for_you_section()

elif menu_id == "Search movies":
    search_movies.search_movies()

elif menu_id == "Login":
    st.title("Login")
    st.write("Please log in to access personalized recommendations")

elif menu_id == "Genres":
    st.write("")

else:
    select_genres.select_genres()

placeholder = st.empty()