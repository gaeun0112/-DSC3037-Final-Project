import pandas as pd

amazon_movies = pd.read_csv("./data/amazon_prime_titles.csv")
amazon_info = pd.read_csv("./data/amazon prime movies.csv")
disney_movies = pd.read_csv("./data/disney_plus_titles.csv")
disney_info = pd.read_csv("./data/DisneyMoviesDataset.csv")
netflix_movies = pd.read_csv("./data/netflix_titles.csv")
netflix_info = pd.read_csv("./data/netflix-rotten-tomatoes-metacritic-imdb.csv")


# add ott_service column
netflix_movies['ott_service'] = 'netflix'
amazon_movies['ott_service'] = 'amazon'
disney_movies['ott_service'] = 'disney'

movies = pd.concat([netflix_movies, disney_movies, amazon_movies],ignore_index=True)
movies = movies[movies['type']=='Movie']
movies = movies.reset_index(drop=True)
movies['show_id'] = movies.index

processed_movies = movies.drop(columns=['type', 'cast', 'country', 'listed_in', 'ott_service'])

# for ott table
ott_service = movies[['show_id', 'ott_service']]

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



processed_movies.to_csv('./data/movies.csv')
ott_service.to_csv('./data/ott_service.csv')
genre.to_csv('./data/genre.csv')
country.to_csv('./data/country.csv')