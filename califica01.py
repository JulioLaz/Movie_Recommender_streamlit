import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating
import json
import os
import ddbb

df = ddbb.df_final()
df_poster = ddbb.load_df_poster()
df = df.merge(df_poster, on='movieId', how='left')

# Function to save ratings to a JSON file
def save_ratings_to_json(ratings, userId):
    json_file = "user_ratings.json"
    
    # Load existing data if the file exists
    if os.path.exists(json_file):
        with open(json_file, "r") as f:
            all_ratings = json.load(f)
    else:
        all_ratings = []

    # Update user ratings
    all_ratings.append({"userId": userId, "ratings": ratings})

    # Save back to JSON file
    with open(json_file, "w") as f:
        json.dump(all_ratings, f, indent=4)

# Function to calculate and collect ratings
def calificar(df_details, userId):
    calificaciones = []
    for index, row in df_details.iterrows():
        st.image(row['poster_path_full'], width=150)
        rating = st_star_rating("", maxValue=5, defaultValue=0, key=f"rating_{row['movieId']}")
        if rating > 0:
            calificaciones.append({'movieId': row['movieId'], 'title': row['title'], 'rating': rating})
    
    if calificaciones:
        save_ratings_to_json(calificaciones, userId)

def dicc(movieId):
    global df  # Declare df as global
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

def crear_dataframe_con_detalles(movie_ids):
    movie_details = []
    for movieId in movie_ids:
        details = dicc(movieId)
        if details:
            movie_details.append(details)
    
    df_details = pd.DataFrame(movie_details)
    return df_details

# Determine new userId
json_file = "user_ratings.json"
if os.path.exists(json_file):
    with open(json_file, "r") as f:
        all_ratings = json.load(f)
        max_userId = max(rating["userId"] for rating in all_ratings)
else:
    max_userId = 0

userId = max_userId + 1
userId = int(df["userId"].max()) + 1
st

# Example movie IDs
movie_ids = [1, 3]  # Replace with actual movie IDs
df_details = crear_dataframe_con_detalles(movie_ids)
calificar(df_details, userId)

st.write(f"Your ratings have been saved with userId {userId}")
