import streamlit as st
import populares as pop
import ddbb
import view_posters as vp
import menu
import styles
import similitud as sim
import similitud_tfidf as sim_tfidf
import similitud_knn as sim_knn
import pandas as pd
# st.set_page_config(page_title="movie recomendation", page_icon='🎦', layout="wide")

# df = data.data_genre_explode()
df_movies = ddbb.df_merge_movies_ratings()

styles.styles_main()

menu_data,over_theme,menu_id=menu.menu()

if menu_id == "Home":
    st.title("Welcome to Movie Recommendations")
    st.write("Discover your next favorite movie!")

elif menu_id == "Genres":
    st.title("Movie Genres")
    st.write("Explore movies by genre")


elif menu_id == "Most Populars":
    df=pop.recomendacion_populares()
    lista_poster = list(df['poster_path_full'].head(5))
    lista_originalTitle = list(df['title'].head(5))
    lista_tconst = list(df['imdb_id'].head(5))
    lista_averageRating = list(round(df['mean_rating'],1).head(5))
    vp.view_poster(lista_poster,lista_originalTitle,lista_tconst,lista_averageRating)

elif menu_id == "Top Rated":
    df_final=ddbb.df_final()
    df_final = df_final.drop_duplicates(subset='title', keep='first')
    st.title("Community")

    movie_titles = df_final['title'].tolist()
    title='Matrix, The'
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
            vp.view_poster(lista_poster, lista_originalTitle, lista_tconst, lista_averageRating)

elif menu_id == "Community": #
    df_final=ddbb.df_final()
    df_final = df_final.drop_duplicates(subset='title', keep='first')
    st.title("Community")

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
            vp.view_poster(lista_poster, lista_originalTitle, lista_tconst, lista_averageRating)

elif menu_id == "New Releases":
    # st.title("New Releases")
    # st.write("The latest movies to hit the screens")
    st.title('Movie Recommendation System')

    df_final=ddbb.df_final()
    movies = df_final[['movieId', 'title']].drop_duplicates()
    selected_movie_title = st.selectbox('Search and select a movie to rate', movies['title'])
    selected_movie_id = int(movies[movies['title'] == selected_movie_title]['movieId'].values[0])

    rating = st.slider(f"Rate {selected_movie_title}", 1, 5, 3)
    user_ratings = {selected_movie_id: rating}

    st.write("Your Ratings:", user_ratings)
    usuario = pd.Series(user_ratings)
    print(usuario)
    if st.button('Get Recommendations'):
        recommendations = sim_knn.recomendacion_knn(usuario)
        st.write(recommendations)    

    recommended_movies = sim_knn.recomendacion_knn(usuario)

    if 'poster_path_full' in recommended_movies.columns:
            lista_poster = list(recommended_movies['poster_path_full'].head(5))
            lista_originalTitle = list(recommended_movies['title'].head(5))
            lista_tconst = list(recommended_movies['imdb_id'].head(5))
            lista_averageRating = list(round(recommended_movies['rating'], 2).head(5))
            vp.view_poster(lista_poster, lista_originalTitle, lista_tconst, lista_averageRating)


elif menu_id == "Login":
    st.title("Login")
    st.write("Please log in to access personalized recommendations")

else:
    vp.title_poster_genre(menu_id)
    df_genre = df_movies[df_movies['genres'] == menu_id].sort_values(by='rating', ascending=False)
    lista_poster = list(df_genre['poster_path_full'].head(5))
    lista_originalTitle = list(df_genre['title'].head(5))
    lista_tconst = list(df_genre['imdb_id'].head(5))
    lista_averageRating = list(round(df_genre['rating'],1).head(5))
    vp.view_poster(lista_poster,lista_originalTitle,lista_tconst,lista_averageRating)

# cloud.imagen_cloud(df,'poster_path')
placeholder = st.empty()