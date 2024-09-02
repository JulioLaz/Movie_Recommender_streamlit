import streamlit as st
import populares as pop
import ddbb
import text_desplazado as tdz
import menu
import styles
import similitud as sim
import similitud_tfidf as sim_tfidf
import similitud_knn as sim_knn
import pandas as pd
import ver_poster
import star_rating as stars
from collections import Counter

# st.set_page_config(page_title="movie recomendation", page_icon='🎦', layout="wide")
# st.set_page_config(layout="wide")

df_movies = ddbb.df_merge_movies_ratings()

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
    padding: 1rem 1.2rem;
}
</style>
"""

# Apply the CSS style
st.markdown(css_style, unsafe_allow_html=True)

menu_data,over_theme,menu_id=menu.menu()

if menu_id == "Home":
    tdz.title_poster('', 'Welcome to Movie Recommendations!')

    # st.subheader("Welcome to Movie Recommendations")
    # st.write("Discover your next favorite movie!")
    st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://i.imgur.com/pkaSdxw.png" alt="Movie Poster" style="width:100vw; height:80vh;">
        </div>
        """,
        unsafe_allow_html=True
    )
elif menu_id == "Genres":
    st.title("Movie Genres")
    st.write("Explore movies by genre")


elif menu_id == "Most Populars":
    # st.title("Most popular movies among our users:")
    ver_poster.title_poster_genre('','Most popular movies among our users!')
    df=pop.recomendacion_populares()
    lista_poster = list(df['poster_path_full'].head(5))
    lista_originalTitle = list(df['title'].head(5))
    lista_tconst = list(df['imdb_id'].head(5))
    lista_averageRating = list(round(df['mean_rating'],1).head(5))
    ver_poster.view_poster(lista_poster,lista_originalTitle,lista_tconst,lista_averageRating)
    # vp.view_poster(lista_poster,lista_originalTitle,lista_tconst,lista_averageRating)

elif menu_id == "Top Rated":
    df_final=ddbb.df_final()
    df_final = df_final.drop_duplicates(subset='title', keep='first')
    col1, col2 = st.columns(2)
    with col1:
        ver_poster.title_poster_genre('','People who watched this movie also loved these!')

        # st.subheader("People who watched this movie also loved these!")
    with col2:
        movie_titles = df_final['title'].tolist()
        title='Titanic'
        default_index = movie_titles.index(title) if title in movie_titles else 0
        selected_title = st.selectbox("Select a movie you like: Connect with other movie enthusiasts and get personalized recommendations", movie_titles, index=default_index)

    if selected_title:
        movie_id = df_final[df_final['title'] == selected_title]['movieId'].values[0]
        recommended_movies = sim_tfidf.recomendacion_tf_idf(movie_id)

        if 'poster_path_full' in recommended_movies.columns:
            lista_poster = list(recommended_movies['poster_path_full'].head(5))
            lista_originalTitle = list(recommended_movies['title'].head(5))
            lista_tconst = list(recommended_movies['imdb_id'].head(5))
            lista_averageRating = list(round(recommended_movies['rating'], 2).head(5))
            ver_poster.view_poster(lista_poster,lista_originalTitle,lista_tconst,lista_averageRating)
            # vp.view_poster(lista_poster, lista_originalTitle, lista_tconst, lista_averageRating)

elif menu_id == "Community": #
    df_final=ddbb.df_final()
    df_final = df_final.drop_duplicates(subset='title', keep='first')
    col1, col2 = st.columns(2)
    with col1:
        ver_poster.title_poster_genre('','Fans of this movie also enjoyed these!')

        # st.subheader("Fans of this movie also enjoyed these!")

    with col2:
        movie_titles = df_final['title'].tolist()
        title='Matrix, The'
        default_index = movie_titles.index(title) if title in movie_titles else 0
        selected_title = st.selectbox("Select a movie you like: Connect with other movie enthusiasts and get personalized recommendations", movie_titles, index=default_index)

    if selected_title:
        movie_id = df_final[df_final['title'] == selected_title]['movieId'].values[0]
        recommended_movies = sim.recomendacion_jaccard(movie_id)

        if 'poster_path_full' in recommended_movies.columns:
            lista_poster = list(recommended_movies['poster_path_full'].head(5))
            lista_originalTitle = list(recommended_movies['title'].head(5))
            lista_tconst = list(recommended_movies['imdb_id'].head(5))
            lista_averageRating = list(round(recommended_movies['rating'], 2).head(5))
            # vp.view_poster(lista_poster, lista_originalTitle, lista_tconst, lista_averageRating)
            ver_poster.view_poster(lista_poster,lista_originalTitle,lista_tconst,lista_averageRating)


elif menu_id == "New Releases":
    st.title("New Releases")
    st.write("The latest movies to hit the screens")

elif menu_id == "Big fans":
    # st.title('Top picks for our biggest fans: ')
    df_final=ddbb.df_final()
    # movies = df_final.groupby('userId')['rating'].count().reset_index().sort_values(by='rating', ascending=False)
    # movies_count_user=list(movies.userId)
    # usuario = st.selectbox('Search and select a user', movies_count_user)
    movies = df_final.groupby('userId')['rating'].count().reset_index().sort_values(by='rating', ascending=False)
    # user_rating_counts = dict(zip(movies.userId, zip(movies.rating, movies.genres)))
    # user_options = [f"Usuario {userId} - voted movies: {count} - genres: {genres}" for userId, (count, genres) in user_rating_counts.items()]
    user_rating_counts = dict(zip(movies.userId, movies.rating))
    user_options = [f"Usuario {userId} - voted movies: {count}" for userId, count in user_rating_counts.items()]
    col1,col2=st.columns(2)
    with col1:
        st.subheader('Top picks for our biggest fans: ')

    with col2:
        col1,col2=st.columns(2)
        with col1:

            selected_user_option = st.selectbox('', user_options,label_visibility="collapsed")
            selected_user_id = int(selected_user_option.split()[1])    

            user_movies = df_final[df_final['userId'] == selected_user_id]
            selected_movie_genres = user_movies['genre_set']
            # selected_genres = set().union(*selected_movie_genres)
            all_genres = [genre for genre_set in selected_movie_genres for genre in genre_set]
            genre_counts = Counter(all_genres)
            df_genres = pd.DataFrame.from_dict(genre_counts, orient='index', columns=['Count']).reset_index()
            df_genres.rename(columns={'index': 'Genre'}, inplace=True)
            df_genres=df_genres.nlargest(10,'Count')
            user_genres_counts = dict(zip(df_genres.Genre, df_genres.Count))
            user_options_genre = [f"{Genre} - Count: {Count}" for Genre, Count in user_genres_counts.items()]

        with col2:
            with st.expander("View Top 10 Genres chosen by him user"):
                st.write(df_genres.to_html(index=False), unsafe_allow_html=True)
    recommended_movies = sim_knn.recomendacion_knn(selected_user_id)
    if 'poster_path_full' in recommended_movies.columns:
            lista_poster = list(recommended_movies['poster_path_full'].head(5))
            lista_originalTitle = list(recommended_movies['title'].head(5))
            lista_tconst = list(recommended_movies['imdb_id'].head(5))
            lista_averageRating = list(round(recommended_movies['rating'], 2).head(5))
            # vp.view_poster(lista_poster, lista_originalTitle, lista_tconst, lista_averageRating)
            ver_poster.view_poster(lista_poster,lista_originalTitle,lista_tconst,lista_averageRating)

elif menu_id == "Just for you":
    tdz.title_poster('', 'Movie recommendations just for you!')
    # st.title('Movie recommendations just for you!')
    # df_final=ddbb.df_final()
    # movies = df_final.groupby('userId')['rating'].count().reset_index().sort_values(by='rating', ascending=False)
    # movies_count_user=list(movies.userId)
    # usuario = st.selectbox('Search and select a user', movies_count_user)
    recommended_movies = sim_knn.recomendacion_knn(777)

    if 'poster_path_full' in recommended_movies.columns:
            lista_poster = list(recommended_movies['poster_path_full'].head(5))
            lista_originalTitle = list(recommended_movies['title'].head(5))
            lista_tconst = list(recommended_movies['imdb_id'].head(5))
            lista_averageRating = list(round(recommended_movies['rating'], 2).head(5))
            # vp.view_poster(lista_poster, lista_originalTitle, lista_tconst, lista_averageRating)
            ver_poster.view_poster(lista_poster,lista_originalTitle,lista_tconst,lista_averageRating)


elif menu_id == "Login":
    st.title("Login")
    st.write("Please log in to access personalized recommendations")

else:
    ver_poster.title_poster_genre(menu_id,'Genre')
    df_genre = df_movies[df_movies['genres'] == menu_id].sort_values(by='rating', ascending=False)
    lista_poster = list(df_genre['poster_path_full'].head(5))
    lista_originalTitle = list(df_genre['title'].head(5))
    lista_tconst = list(df_genre['imdb_id'].head(5))
    lista_averageRating = list(round(df_genre['rating'],1).head(5))
    # vp.view_poster(lista_poster,lista_originalTitle,lista_tconst,lista_averageRating)
    ver_poster.view_poster(lista_poster,lista_originalTitle,lista_tconst,lista_averageRating)

# cloud.imagen_cloud(df,'poster_path')
placeholder = st.empty()