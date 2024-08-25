import pandas as pd
from sklearn.neighbors import NearestNeighbors
import ddbb
import numpy as np

def recomendacion_knn(user_input):
    df_final = ddbb.df_final()
    df_ratings= ddbb.load_df_ratings()
    
    n_recommendations=10
    if isinstance(user_input, int):
        print('Existing user')
        df_agg = df_final.groupby(['userId', 'movieId'])['rating'].mean().reset_index()
        print(df_agg.userId.max())
        ratings_matrix = df_agg.pivot(index='userId', columns='movieId', values='rating')
        avg_ratings = ratings_matrix.mean(axis=1, skipna=True)
        ratings_matrix_normalized = ratings_matrix.sub(avg_ratings, axis=0).fillna(0)
        knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
        knn_model.fit(ratings_matrix_normalized.values)
        idx = ratings_matrix_normalized.index.get_loc(user_input)
        distances, indices = knn_model.kneighbors(ratings_matrix_normalized.iloc[idx].values.reshape(1, -1), n_neighbors=n_recommendations + 1)
    else:
        print('New user')
        new_user_ratings = pd.DataFrame({
            'userId': [df_agg['userId'].max() + 1] * 2,
            'movieId': user_input.index,
            'rating': user_input.values})
        df_agg = pd.concat([df_agg, new_user_ratings], ignore_index=True)
        ratings_matrix = df_agg.pivot(index='userId', columns='movieId', values='rating')
        avg_ratings = ratings_matrix.mean(axis=1, skipna=True)
        ratings_matrix_normalized = ratings_matrix.sub(avg_ratings, axis=0).fillna(0)
        knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
        knn_model.fit(ratings_matrix_normalized.values)
        idx = ratings_matrix_normalized.index.get_loc(df_agg.userId.max())

    distances, indices = knn_model.kneighbors(ratings_matrix_normalized.iloc[idx].values.reshape(1, -1), n_neighbors=n_recommendations + 1)
    distances = distances.flatten()[1:]
    indices = indices.flatten()[1:]

    similar_users = ratings_matrix_normalized.iloc[indices]
    mean_ratings = similar_users.T.dot(distances) / np.sum(distances)
    df_mean_ratings = pd.DataFrame(mean_ratings, index=ratings_matrix_normalized.columns, columns=['mean_rating'])
    df_mean_ratings = df_mean_ratings.dropna()

    if isinstance(user_input, int):
        movies_seen = df_final[df_final['userId']==user_input].index
    else:
        movies_seen = df_agg[df_agg['userId'] == df_agg['userId'].max()]['movieId']
    df_mean_ratings = df_mean_ratings[~df_mean_ratings.index.isin(movies_seen)]

    df_mean_ratings = df_mean_ratings.sort_values('mean_rating', ascending=False)
    recommended_movies = pd.merge(df_mean_ratings, df_final[['movieId', 'title', 'genres','year']], left_index=True, right_on='movieId')
    recommended_movies.drop_duplicates(subset=['movieId'], inplace=True)
    columnas=['movieId', 'title', 'genres','mean_rating','year']
    recommended_movies=recommended_movies[columnas].head(n_recommendations)

    df_average_ratings=df_ratings.groupby('movieId')['rating'].mean().reset_index()
    df_poster_knn = pd.merge(recommended_movies, df_average_ratings, on='movieId', how='left')
    return df_poster_knn

print(recomendacion_knn(15))