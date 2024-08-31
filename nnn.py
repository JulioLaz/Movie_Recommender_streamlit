import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating
import os
import ddbb

df = ddbb.df_final()
df_poster = ddbb.load_df_poster()
df = df.merge(df_poster, on='movieId', how='left')
df_file = "user_ratings.csv"

if os.path.exists(df_file):
    df_ratings = pd.read_csv(df_file)
else:
    df_ratings = pd.DataFrame(columns=["userId", "movieId", "title", "rating"])

# User input for userId
userId = st.number_input("Enter your user ID", min_value=df.userId.max()+1, step=1)
st.write("The current user ID is", int(userId))


movie_titles = df['title'].unique().tolist()
title='Titanic'
default_index = movie_titles.index(title) if title in movie_titles else 0
selected_title = st.selectbox("Select a movie you like: Connect with other movie enthusiasts and get personalized recommendations", movie_titles, index=default_index)

if selected_title:
        movie_ids = df[df['title'] == selected_title]['movieId'].values[0]

if userId in df["userId"].unique() or userId in df_ratings["userId"].unique():
    def calificar(df_details, userId):
        calificaciones = []
        for index, row in df_details.iterrows():
            # st.image(row['poster_path_full'], width=150)
            rating = st_star_rating("", maxValue=5, defaultValue=0, key=f"rating_{row['movieId']}")
            if rating > 0:
                calificaciones.append({'userId': userId, 'movieId': row['movieId'], 'title': row['title'], 'rating': rating})
        
        if calificaciones:
            new_df_ratings = pd.DataFrame(calificaciones)
            global df_ratings
            df_ratings = pd.concat([df_ratings, new_df_ratings], ignore_index=True)

    # Function to extract movie details by movieId
    def dicc(movieId):
        global df
        movie_data = df[df['movieId'] == movieId]
        if movie_data.empty:
            return None
        return {
            'movieId': movie_data.movieId.iloc[0],
            'title': movie_data.title.iloc[0],
            'poster_path_full': movie_data.poster_path_full.iloc[0],
            'year': movie_data.year.iloc[0],
            'genres': movie_data.genres.iloc[0],
            'rating': movie_data.rating.iloc[0]
        }

    # Function to create a DataFrame with movie details
    def crear_dataframe_con_detalles(movie_ids):
        movie_details = []
        for movieId in movie_ids:
            details = dicc(movieId)
            if details:
                movie_details.append(details)
        
        df_details = pd.DataFrame(movie_details)
        return df_details

    # Example movie IDs
    # movie_ids = [1, 3]  # Replace with actual movie IDs
    df_details = crear_dataframe_con_detalles([movie_ids])
    calificar(df_details, userId)

    # Save updated DataFrame back to the CSV file
    df_ratings.to_csv(df_file, index=False)

    # st.write(f"Your ratings have been saved with userId {userId}")
