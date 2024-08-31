import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating
import ddbb

df = ddbb.df_final()
df_poster = ddbb.load_df_poster()
df = df.merge(df_poster, on='movieId', how='left')

def calificar(df_details):
      calificaciones = []
      for index, row in df_details.iterrows():
         st.image(row['poster_path_full'], width=150)
         rating = st_star_rating("", maxValue=5, defaultValue=0, key=f"rating_{row['movieId']}")
         calificaciones.append({'movieId': row['movieId'], 'title': row['title'], 'rating': rating})
      df_calificaciones = pd.DataFrame(calificaciones)
      return df_calificaciones


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
         movie_details.append(details)
    
    df_details = pd.DataFrame(movie_details)
    return df_details

movie_ids = [1, 3]  # IDs de ejemplo
df_details = crear_dataframe_con_detalles(movie_ids)
df_calificaciones = calificar(df_details)
st.write("tus calificaciones", df_calificaciones)