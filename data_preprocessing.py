import pandas as pd
import numpy as np
from tqdm import tqdm
import ast

# get csv file to dataframe
amazon_movies = pd.read_csv("./raw_data/amazon_prime_titles.csv")
disney_movies = pd.read_csv("./raw_data/disney_plus_titles.csv")
netflix_movies = pd.read_csv("./raw_data/netflix_titles.csv")
hulu_movies = pd.read_csv("./raw_data/hulu_titles.csv")

# add ott_service column
netflix_movies['ott_service'] = 'netflix'
amazon_movies['ott_service'] = 'amazon'
disney_movies['ott_service'] = 'disney'
hulu_movies['ott_service'] = 'hulu'

# concat 3 ott dataframes
movies = pd.concat([netflix_movies, disney_movies, amazon_movies, hulu_movies],ignore_index=True)
movies = movies[movies['type']=='Movie']
movies = movies.reset_index(drop=True)
movies['show_id'] = movies.index

# drop unusing columns
processed_movies = movies.drop(columns=['type', 'cast', 'country', 'listed_in','ott_service', 'description'])

# for ott table
ott_service = movies[['show_id', 'ott_service']]

# for cast table
cast_movies = movies.dropna(subset=['cast'], how='any', axis=0)
cast_lst = []
for idx, row in cast_movies.iterrows():
    for cast in row['cast'].split(","):
        if cast.strip() not in ['', '1', '3']:
            cast_lst.append([row['show_id'], cast.strip()])
cast = pd.DataFrame(cast_lst, columns=['movie_id', 'cast'])
cast.to_csv('./data/cast.csv')

# for genre table
genre_movies = movies.dropna(subset=['listed_in'], how='any', axis=0)
genre_lst = []
for idx, row in genre_movies.iterrows():
    for genre in row['listed_in'].split(","):
        genre_lst.append([row['show_id'], genre.strip()])
genre = pd.DataFrame(genre_lst, columns=['movie_id', 'genre'])
        
# for country table
country_movies = movies.dropna(subset=['country'], how='any', axis=0)
country_lst = []
for idx, row in country_movies.iterrows():
    for country in row['country'].split(","):
        country_lst.append([row['show_id'], country.strip()])
country = pd.DataFrame(country_lst, columns=['movie_id', 'country'])

# save dataframes to csv file
processed_movies.to_csv('./data/movies.csv')
cast.to_csv('./data/cast.csv')
ott_service.to_csv('./data/ott_service.csv')
genre.to_csv('./data/genre.csv')
country.to_csv('./data/country.csv')