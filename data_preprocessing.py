import pandas as pd
import numpy as np
from tqdm import tqdm
import ast

# get csv file to dataframe
amazon_movies = pd.read_csv("./data/amazon_prime_titles.csv")
amazon_info = pd.read_csv("./data/amazon prime movies.csv")
disney_movies = pd.read_csv("./data/disney_plus_titles.csv")
disney_info = pd.read_csv("./data/DisneyMoviesDataset.csv")
netflix_movies = pd.read_csv("./data/netflix_titles.csv")
netflix_info = pd.read_csv("./data/netflix-rotten-tomatoes-metacritic-imdb.csv")
# add imdb movies dataset : https://www.kaggle.com/datasets/ashpalsingh1525/imdb-movies-dataset
imdb_info = pd.read_csv("./data/imdb_movies.csv")\
    

# process disney_info language column
disney_info_lang = disney_info.dropna(subset=['Language'], how='any', axis=0)
for i, row in disney_info_lang.iterrows():
    text = row['Language']
    if text[0] == '[':
        return_txt = ""
        for txt in ast.literal_eval(text):
            return_txt+=txt + ", "
        disney_info.loc[i, 'Language'] = return_txt[:-2]
        

# add ott_service column
netflix_movies['ott_service'] = 'netflix'
amazon_movies['ott_service'] = 'amazon'
disney_movies['ott_service'] = 'disney'


# some preprocesses for data : matchin ()_movies dataframes and ()_info dataframes
# working for adding 'IMDB_score' column and 'language' column
def info_df_preprocess(df, info_df, title_column, language_column, imdb_column):
    info_df[title_column] = info_df[title_column].str.lower()  
    df['IMDB_score'] = None
    df['language'] = None

    for idx, row in tqdm(df.iterrows()):
        title_lower = row['title'].lower()

        if title_lower in info_df[title_column].values:
            info_row = info_df[info_df[title_column] == title_lower].iloc[0]
            df.loc[idx, 'IMDB_score'] = info_row[imdb_column]
            df.loc[idx, 'language'] = info_row[language_column]
            

    return df

netflix_movies = info_df_preprocess(netflix_movies, netflix_info, 'Title','Languages', 'IMDb Score')
amazon_movies = info_df_preprocess(amazon_movies, amazon_info, "Movie Name", "Language", "IMDb Rating")
disney_movies = info_df_preprocess(disney_movies, disney_info, "title", "Language", "imdb")


# concat 3 ott dataframes
movies = pd.concat([netflix_movies, disney_movies, amazon_movies],ignore_index=True)
movies = movies[movies['type']=='Movie']
movies = movies.reset_index(drop=True)
movies['show_id'] = movies.index


# To reduce "null" data in "imdb_score" column and "language" column, get additional data from imdb_info
imdb_info["names"] = imdb_info["names"].str.lower()
for idx, row in tqdm(movies.iterrows()):
    title_lower = row['title'].lower()

    if title_lower in imdb_info["names"].values:
        info_row = imdb_info[imdb_info['names'] == title_lower].iloc[0]
        movies.loc[idx, 'IMDB_score'] = info_row['score']/10
        movies.loc[idx, 'language'] = info_row["orig_lang"]


# drop unusing columns
processed_movies = movies.drop(columns=['type', 'cast', 'country', 'listed_in','ott_service', 'language', 'description', 'IMDB_score'])

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

# for language table
language_movies = movies.dropna(subset=['language'], how='any', axis=0)
language_lst = []
for idx, row in language_movies.iterrows():
    for language in row['language'].split(","):
        language_lst.append([row['show_id'], language.strip()])
language = pd.DataFrame(language_lst, columns=['movie_id', 'language'])

# for imdb_score table
imdb_movies = movies.dropna(subset=['IMDB_score'], how='any', axis=0)
imdb_lst = []
for idx, row in imdb_movies.iterrows():
    imdb_lst.append([row['show_id'],row['IMDB_score']])
imdb = pd.DataFrame(imdb_lst, columns=['movie_id', 'imdb_score'])


# save dataframes to csv file
processed_movies.to_csv('./data/movies.csv')
cast.to_csv('./data/cast.csv')
ott_service.to_csv('./data/ott_service.csv')
genre.to_csv('./data/genre.csv')
country.to_csv('./data/country.csv')
language.to_csv('./data/language.csv')
imdb.to_csv('./data/imdb.csv')