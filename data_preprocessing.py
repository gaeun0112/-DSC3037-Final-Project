import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime as dt
import re


# get csv file to dataframe
amazon_movies = pd.read_csv("./DSC3037_23_2_RDBMS/raw_data/amazon_prime_titles.csv")
disney_movies = pd.read_csv("./DSC3037_23_2_RDBMS/raw_data/disney_plus_titles.csv")
hulu_movies = pd.read_csv("./DSC3037_23_2_RDBMS/raw_data/hulu_titles.csv")
netflix_movies = pd.read_csv("./DSC3037_23_2_RDBMS/raw_data/netflix_titles.csv")


# add ott_service column before merging
amazon_movies['ott_id'] = 1
disney_movies['ott_id'] = 2
hulu_movies['ott_id'] = 3
netflix_movies['ott_id'] = 4


# concat 3 ott dataframes
movies = pd.concat([netflix_movies,disney_movies,amazon_movies,hulu_movies], ignore_index=True)
movies = movies[movies['type']=='Movie'] # this is movie program
movies = movies.reset_index(drop=True)


# pre-processing
movies = movies.rename(columns={'show_id': 'movie_id'})
movies.movie_id = pd.to_numeric(movies.index + 1)
movies = movies.rename(columns={'date_added': 'last_update'})
movies.last_update = movies.last_update.fillna('January 1, 1970')
movies.last_update = pd.to_datetime(movies.last_update).dt.strftime('%Y%m%d')
movies.last_update = pd.to_numeric(movies.last_update)
movies = movies.fillna('no info')
movies.duration = pd.to_numeric(movies.duration.apply(lambda x: '000' if x == 'no info' else x.replace(' min', '')))
movies.release_year = movies.release_year.apply(lambda x: '0000' if x == 'no info' else x)
movies.rating = movies.rating.apply(lambda x: x.replace('TV-MA', 'R').replace('16+', 'R').replace('TV-14', 'PG-13').replace('ALL', 'G').replace('18+', 'NC-17').replace('13+', 'PG').replace('TV-G', 'G').replace('7+', 'G').replace('TV-Y', 'G').replace('G7', 'G').replace('G-FV', 'G').replace('TV-PG', 'PG').replace('TV-Y', 'G').replace('TV-Y7', 'G'))
movies.rating = movies.rating.apply(lambda x: 'no info' if x not in ['R', 'PG-13', 'PG', 'G', 'NC-17'] else x)


# for ott table
ott_service = pd.DataFrame({
    'ott_id': [1, 2, 3, 4],
    'ott_service': ['amazon_prime','netflix','hulu','disney_plus'],
    'last_update':[movies['last_update'].max()]*4                      
    })


# for director table
tmp = pd.melt(movies.director.str.split(', ', expand=True).reset_index(), id_vars='index', var_name='tmp', value_name='director_name')
tmp = tmp.drop(columns=['tmp']).rename(columns={'index':'movie_id'}).dropna()
tmp.director_name = tmp.director_name.apply(lambda x: x.lower().replace('_',' ').lstrip().replace('.','. ').replace('  ',' ').replace(' director','').replace('knigjht','knight').replace('knioght','knight'))
tmp.director_name = tmp.director_name.apply(lambda x: 'no info' if 'validcapi' in x or 'test' in x else x)
tmp.director_name = tmp.director_name.apply(lambda x: 'alex winter' if 'director alex winter' in x else x)
tmp.director_name = tmp.director_name.apply(lambda x: 'gigi saul guerrero' if 'director gigi saul guerrero' in x else x)
tmp.director_name = tmp.director_name.apply(lambda x: 'jennifer kent' if 'director jennifer kent' in x else x)
tmp.director_name = tmp.director_name.apply(lambda x: 'kids 1st tv' if 'kids 1st tv' in x else x)
tmp.director_name = tmp.director_name.apply(lambda x: 'no info' if '1' == x else x)
tmp = tmp.drop_duplicates(subset=['movie_id', 'director_name'], keep='first')
tmp.movie_id+=1
tmp = pd.merge(tmp, movies[['movie_id','last_update']], on='movie_id', how='left')
director_tmp = pd.Series(sorted(list(set(tmp.director_name))))
director = pd.DataFrame({'director_id':director_tmp.index+1,'director_name':director_tmp,'last_update':[movies.last_update.max()]*len(director_tmp)})


# for direct table
direct = pd.merge(tmp, director[['director_id','director_name']], on='director_name')
direct = direct.sort_values(by=['movie_id']).reset_index(drop=True).drop(columns=['director_name'])
direct = direct[['movie_id','director_id','last_update']]


# for actor table
ban_list = ['','1','2','3','A','Test Actor 1','Test Actor 2','Test Actor1 US']
tmp = pd.melt(movies.cast.str.split(', ', expand=True).reset_index(), id_vars='index', var_name='tmp', value_name='actor_name')
tmp = tmp.drop(columns=['tmp']).rename(columns={'index':'movie_id'}).dropna()
tmp.actor_name = tmp.actor_name.apply(lambda x: 'no info' if x in ban_list else x.lower().replace('\'', ' ').replace('\"', ' ').lstrip().replace('  ',' '))
tmp.actor_name = tmp.actor_name.apply(lambda x: 'samantha bond' if 'samantha bond' in x else x)
tmp = tmp.drop_duplicates(subset=['movie_id', 'actor_name'], keep='first')
tmp.movie_id+=1
tmp = pd.merge(tmp, movies[['movie_id','last_update']], on='movie_id', how='left')
actor_tmp = pd.Series(sorted(list(set(tmp.actor_name))))
actor = pd.DataFrame({'actor_id':actor_tmp.index+1,'actor_name':actor_tmp,'last_update':[movies.last_update.max()]*len(actor_tmp)})


# for cast table
cast = pd.merge(tmp, actor[['actor_id','actor_name']], on='actor_name')
cast = cast.sort_values(by=['movie_id']).reset_index(drop=True).drop(columns=['actor_name'])
cast = cast[['movie_id','actor_id','last_update']]


# for genre table
tmp = pd.melt(movies.listed_in.str.split(', ', expand=True).reset_index(), id_vars='index', var_name='tmp', value_name='genre_name')
tmp = tmp.drop(columns=['tmp']).rename(columns={'index':'movie_id'}).dropna()
tmp.genre_name = tmp.genre_name.apply(lambda x: x.lower().lstrip().replace(' features','').replace(' film','').replace(' movies','').replace('anime','animation').replace('/',' and ').replace('-',' and ').replace('and','&').replace('classics','classic').replace('comedies','comedy').replace('dramas','drama').replace('documentaries','documentary').replace('romantic','romance').replace('and culture','culture'))
tmp = tmp.drop_duplicates(subset=['movie_id', 'genre_name'], keep='first')
tmp.movie_id+=1
tmp = pd.merge(tmp, movies[['movie_id','last_update']], on='movie_id', how='left')
genre_tmp = pd.Series(sorted(list(set(tmp.genre_name))))
genre = pd.DataFrame({'genre_id':genre_tmp.index+1, 'genre_name':genre_tmp, 'last_update':[movies.last_update.max()]*len(genre_tmp)})


# for movies_genre table
movies_genre = pd.merge(tmp, genre[['genre_id','genre_name']], on='genre_name')
movies_genre = movies_genre.sort_values(by=['movie_id']).reset_index(drop=True).drop(columns=['genre_name'])
movies_genre = movies_genre[['movie_id','genre_id','last_update']]


# country table
tmp = pd.melt(movies.country.str.split(', ', expand=True).reset_index(), id_vars='index', var_name='tmp', value_name='country_name')
tmp = tmp.drop(columns=['tmp']).rename(columns={'index':'movie_id'}).dropna().drop_duplicates(subset=['movie_id', 'country_name'], keep='first')
tmp.movie_id+=1
tmp = pd.merge(tmp, movies[['movie_id','last_update']], on='movie_id', how='left')
tmp.country_name = tmp.country_name.apply(lambda x: 'no info' if len(x) < 3 else x.replace(',',''))
country_tmp = pd.Series(sorted(list(set(tmp.country_name))))
country = pd.DataFrame({'country_id':country_tmp.index+1, 'country_name':country_tmp, 'last_update':[movies.last_update.max()]*len(country_tmp)})


# for movies_country table
movies_country = pd.merge(tmp, country[['country_id','country_name']], on='country_name')
movies_country = movies_country.sort_values(by=['movie_id']).reset_index(drop=True).drop(columns=['country_name'])
movies_country = movies_country[['movie_id','country_id','last_update']]


# drop unusing columns
processed_movies = movies.drop(columns=['type','director','cast','country','listed_in'])
processed_movies = processed_movies[['movie_id','title','last_update','release_year','rating','duration','ott_id','description']]

# save dataframes to csv file
processed_movies.to_csv('./DSC3037_23_2_RDBMS/for_use/movies.csv')
ott_service.to_csv('./DSC3037_23_2_RDBMS/for_use/ott_service.csv')
director.to_csv('./DSC3037_23_2_RDBMS/for_use/director.csv')
direct.to_csv('./DSC3037_23_2_RDBMS/for_use/direct.csv')
actor.to_csv('./DSC3037_23_2_RDBMS/for_use/actor.csv')
cast.to_csv('./DSC3037_23_2_RDBMS/for_use/cast.csv')
genre.to_csv('./DSC3037_23_2_RDBMS/for_use/genre.csv')
movies_genre.to_csv('./DSC3037_23_2_RDBMS/for_use/movies_genre.csv')
country.to_csv('./DSC3037_23_2_RDBMS/for_use/country.csv')
movies_country.to_csv('./DSC3037_23_2_RDBMS/for_use/movies_country.csv')