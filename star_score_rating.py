import pandas as pd
import streamlit as st
from streamlit_star_rating import st_star_rating
import os
import ddbb
import datetime

df = ddbb.df_final()
df_poster = ddbb.load_df_poster()
df = df.merge(df_poster, on='movieId', how='left')
df_file = "user_ratings.csv"

def rate_with_stars(movie_ids):
      global df_ratings  # Declare df_ratings as global

      if os.path.exists(df_file):
         df_ratings = pd.read_csv(df_file)
      else:
         df_ratings = pd.DataFrame(columns=["userId", "movieId", "title", "rating"])

      # User input for userId
      # userId = st.number_input("Enter your user ID", min_value=df.userId.max()+1, step=1)
      userId=777

      st.write("""<h2 style="text-align: center;padding:0px">How many stars for this film, people?</h2>""", unsafe_allow_html=True)
      if userId in df["userId"].unique() or userId in df_ratings["userId"].unique():
         def calificar(df_details, userId):
            calificaciones = []
            for index, row in df_details.iterrows():
                  # st.image(row['poster_path_full'], width=150)
                  rating = st_star_rating("", maxValue=5, defaultValue=0, key=f"rating_{row['movieId']}",customCSS = "div {background-color: red;display: flex;justify-content: center;height: 4.5rem;padding-top: 3px;width: 100%}, h3 {display: none}, #root > div > ul {display: flex;justify-content: center;}")
                  if rating > 0:
                     # calificaciones.append({'userId': userId, 'movieId': row['movieId'], 'title': row['title'], 'rating': rating})
                                     calificaciones.append({
                    'userId': userId, 
                    'movieId': row['movieId'], 
                    'title': row['title'], 
                    'rating': rating,
                    'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
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

         df_details = crear_dataframe_con_detalles([movie_ids])
         calificar(df_details, userId)

         df_ratings.to_csv(df_file, index=False)