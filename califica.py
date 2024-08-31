import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating
import requests
import ddbb

# @st.cache_data(ttl=300)
# def fetchdetails(movieId):
#     url = f"https://api.themoviedb.org/3/movie/{movieId}?api_key=58326d7b9a8255025616c1b9a8340a44&language=en-US"
#     data = requests.get(url).json()
#     title = data.get('title')
#     description = data.get('overview')
#     poster_path = data.get('poster_path')
#     release_date = data.get('release_date')
#     genres = [genre['name'] for genre in data.get('genres', [])]
#     rating = data.get('vote_average')
#     poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
#     return {
#         'movieId': movieId,
#         'title': title,
#         'description': description,
#         'poster_url': poster_url,
#         'release_date': release_date,
#         'genres': genres,
#         'rating': rating
#     }


# columnas de df_final: ['userId', 'movieId', 'rating', 'timestamp', 'title', 'genres', 'genre_set', 'year']
df=ddbb.df_final()
df_poster=ddbb.load_df_poster()
df=df.merge(df_poster, on='movieId', how='left')
print(df.head())
def dicc(movieId):
    df=df[df['movieId']==movieId]
    return {
        'movieId': df.movieId,
        'title': df.title,
        'poster_url': df.poster_path,
        'release_date': df.year,
        'genres': df.genres,
        'rating': df.rating
    }




def calificar(df_details):
    calificaciones = []

    for index, row in df_details.iterrows():
        st.image(row['poster_path'], width=150, caption=row['title'])
        st.write(f"**Año:** {row['year'][:4]}")
        st.write(f"**Géneros:** {', '.join(row['genres'])}")
        st.write(f"**Ranking:** {row['rating']}")
        
        # Calificación con estrellas
        rating = st_star_rating(f"Califica {row['title']}", maxValue=5, defaultValue=0, key=f"rating_{row['movieId']}")
        calificaciones.append({'movieId': row['movieId'], 'title': row['title'], 'rating': rating})

    df_calificaciones = pd.DataFrame(calificaciones)
    
    return df_calificaciones

def crear_dataframe_con_detalles(movie_ids):
    movie_details = []
    for movieId in movie_ids:
        details = dicc(movieId)
      #   details = fetchdetails(movieId)
        if details['title'] and details['year']:
            movie_details.append(details)
    
    df_details = pd.DataFrame(movie_details)
    return df_details

movie_ids = [1,3]  # IDs de ejemplo
df_details= crear_dataframe_con_detalles(movie_ids)
st.write(df_details.head())
df_calificaciones=calificar(df_details)
st.write("tus calificaciones", df_calificaciones)