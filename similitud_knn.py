import pandas as pd
from sklearn.neighbors import NearestNeighbors
import ddbb
import numpy as np

def recomendacion_knn(user_input):
    df_final = ddbb.df_final()
    df_movies = ddbb.load_df_movies()
    # df_ratings= ddbb.load_df_ratings()
    df_ratings= ddbb.df_concat()
    # df_ratings=df_ratings[['userId','movieId','rating']]
    df_poster=ddbb.load_df_poster()
    # new_user=ddbb.new_user_rate()['userId'].unique()[0]
    # max_user=ddbb.load_df_ratings()['userId'].max()
    # print(new_user)
    
    # df_agg = df_final.groupby(['userId', 'movieId'])['rating'].mean().reset_index()
    # df_agg = df_ratings
    n_recommendations=5
    # if new_user <= user_input:
    if isinstance(user_input, int):
        print('Existing user')
        # print(df_ratings.userId.max())
        ratings_matrix = df_ratings.pivot(index='userId', columns='movieId', values='rating')
        avg_ratings = ratings_matrix.mean(axis=1, skipna=True)
        ratings_matrix_normalized = ratings_matrix.sub(avg_ratings, axis=0).fillna(0)
        knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
        knn_model.fit(ratings_matrix_normalized.values)
        idx = ratings_matrix_normalized.index.get_loc(user_input)
        distances, indices = knn_model.kneighbors(ratings_matrix_normalized.iloc[idx].values.reshape(1, -1), n_neighbors=n_recommendations + 1)
    else:
        print('New user')
        new_user_ratings = pd.DataFrame({
            'userId': [df_ratings['userId'].max() + 1] * len(user_input),  # Match length to user_input
            # 'userId': [df_agg['userId'].max() + 1] * 2,
            'movieId': user_input.index,
            'rating': user_input.values})
        
        new_df_movies = new_user_ratings.merge(df_movies, on='movieId', how='left')
        selected_movie_genres = new_df_movies[new_df_movies['movieId'].isin(user_input.index)]['genre_set']
        selected_genres = set().union(*selected_movie_genres)
      #   print(selected_genres)
        df_final_filtered = df_final[df_final['genre_set'].apply(lambda x: bool(selected_genres & x))]
        # df_final_filtered=df_final_filtered.copy()
        df_final_filtered.drop_duplicates(subset=['movieId'], inplace=True)

        df_agg = df_final_filtered.groupby(['userId', 'movieId'])['rating'].mean().reset_index()
        df_agg_final = pd.concat([df_agg, new_user_ratings], ignore_index=True)
        ratings_matrix = df_agg_final.pivot(index='userId', columns='movieId', values='rating')
        avg_ratings = ratings_matrix.mean(axis=1, skipna=True)
        ratings_matrix_normalized = ratings_matrix.sub(avg_ratings, axis=0).fillna(0)
        knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
        knn_model.fit(ratings_matrix_normalized.values)
        idx = ratings_matrix_normalized.index.get_loc(df_agg_final.userId.max())

    max_neighbors = min(n_recommendations + 1, len(ratings_matrix_normalized))
    if max_neighbors >= 5:
      distances, indices = knn_model.kneighbors(ratings_matrix_normalized.iloc[idx].values.reshape(1, -1), n_neighbors=max_neighbors)
    else:
        df_agg = df_final.groupby(['userId', 'movieId'])['rating'].mean().reset_index()
        df_agg_final = pd.concat([df_agg, new_user_ratings], ignore_index=True)
        ratings_matrix = df_agg_final.pivot(index='userId', columns='movieId', values='rating')
        avg_ratings = ratings_matrix.mean(axis=1, skipna=True)
        ratings_matrix_normalized = ratings_matrix.sub(avg_ratings, axis=0).fillna(0)
        knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
        knn_model.fit(ratings_matrix_normalized.values)
        idx = ratings_matrix_normalized.index.get_loc(df_agg_final.userId.max())      
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
        movies_seen = df_agg_final[df_agg_final['userId'] == df_agg_final['userId'].max()]['movieId']
    df_mean_ratings = df_mean_ratings[~df_mean_ratings.index.isin(movies_seen)]

    df_mean_ratings = df_mean_ratings.sort_values('mean_rating', ascending=False)
    recommended_movies = pd.merge(df_mean_ratings, df_final[['movieId', 'title', 'genres','year']], left_index=True, right_on='movieId')
    recommended_movies.drop_duplicates(subset=['movieId'], inplace=True)
    columnas=['movieId', 'title', 'genres','mean_rating','year']
    recommended_movies=recommended_movies[columnas].head(n_recommendations)

    df_average_ratings=df_ratings.groupby('movieId')['rating'].mean().reset_index()
    df_poster_knn = pd.merge(recommended_movies, df_average_ratings, on='movieId', how='left')
    df_poster_knn_final = pd.merge(df_poster_knn, df_poster, on='movieId', how='left')

    return df_poster_knn_final

# print(recomendacion_knn(15))

# import pandas as pd
# from sklearn.neighbors import NearestNeighbors
# import ddbb
# import numpy as np

# def prepare_ratings_matrix(df_agg, user_ratings=None):
#     if user_ratings is not None:
#         df_agg = pd.concat([df_agg, user_ratings], ignore_index=True)
#     ratings_matrix = df_agg.pivot(index='userId', columns='movieId', values='rating')
#     avg_ratings = ratings_matrix.mean(axis=1, skipna=True)
#     return ratings_matrix.sub(avg_ratings, axis=0).fillna(0)

# def get_recommendations(ratings_matrix_normalized, user_id, n_recommendations):
#     knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
#     knn_model.fit(ratings_matrix_normalized.values)
#     idx = ratings_matrix_normalized.index.get_loc(user_id)
#     distances, indices = knn_model.kneighbors(ratings_matrix_normalized.iloc[idx].values.reshape(1, -1), n_neighbors=n_recommendations + 1)
#     return distances.flatten()[1:], indices.flatten()[1:]

# def recomendacion_knn(user_input):
#     df_final = ddbb.df_final()
#     df_movies = ddbb.load_df_movies()
#     df_ratings = ddbb.load_df_ratings()
#     df_poster = ddbb.load_df_poster()
    
#     df_agg = df_final.groupby(['userId', 'movieId'])['rating'].mean().reset_index()
#     n_recommendations = 5

#     if not isinstance(user_input, int):
#         new_user_id = df_agg['userId'].max() + 1
#         user_ratings = pd.DataFrame({
#             'userId': [new_user_id] * len(user_input),
#             'movieId': user_input.index,
#             'rating': user_input.values
#         })
#         df_agg = pd.concat([df_agg, user_ratings], ignore_index=True)
#         user_input = new_user_id

#     ratings_matrix_normalized = prepare_ratings_matrix(df_agg)
#     distances, indices = get_recommendations(ratings_matrix_normalized, user_input, n_recommendations)

#     similar_users = ratings_matrix_normalized.iloc[indices]
#     mean_ratings = similar_users.T.dot(distances) / np.sum(distances)
#     df_mean_ratings = pd.DataFrame(mean_ratings, index=ratings_matrix_normalized.columns, columns=['mean_rating']).dropna()

#     movies_seen = df_agg[df_agg['userId'] == user_input]['movieId']
#     df_mean_ratings = df_mean_ratings[~df_mean_ratings.index.isin(movies_seen)]
#     df_mean_ratings = df_mean_ratings.sort_values('mean_rating', ascending=False)

#     recommended_movies = pd.merge(df_mean_ratings, df_final[['movieId', 'title', 'genres', 'year']], left_index=True, right_on='movieId')
#     recommended_movies = recommended_movies[['movieId', 'title', 'genres', 'mean_rating', 'year']].drop_duplicates(subset=['movieId']).head(n_recommendations)

#     df_average_ratings = df_ratings.groupby('movieId')['rating'].mean().reset_index()
#     df_poster_knn = pd.merge(recommended_movies, df_average_ratings, on='movieId', how='left')
#     df_poster_knn_final = pd.merge(df_poster_knn, df_poster, on='movieId', how='left')

#     return df_poster_knn_final