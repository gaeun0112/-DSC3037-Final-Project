import csv
import mysql.connector
from datetime import datetime


# Use this code only first you create your database
mydb = mysql.connector.connect(
    host = "localhost",
    user= "root",
    passwd = "5789"  
)
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS db_project")

def connectDB(db_use):
    mydb = mysql.connector.connect(
        host = "localhost",
        user= "root",
        passwd = "5789",
        database = db_use
    )
    mycursor = mydb.cursor(prepared=True)
    return mydb, mycursor

mydb, myCursor = connectDB("db_project")


# movies table
myCursor.execute("CREATE TABLE IF NOT EXISTS movies(movie_id INT PRIMARY KEY, title VARCHAR(255), last_update DATE, release_year SMALLINT, rating VARCHAR(255), duration SMALLINT, ott_id SMALLINT, description TEXT)")
with open('./DSC3037_23_2_RDBMS/for_use/movies.csv', encoding='UTF-8') as csvfile:
    movies_data = csv.reader(csvfile)
    header = next(movies_data)  # Skip header
    for data in movies_data:
        last_update = datetime.strptime(data[3], '%Y%m%d').date()
        myCursor.execute("INSERT INTO movies(movie_id, title, last_update, release_year, rating, duration, ott_id, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (int(data[1]), data[2], last_update, int(data[4]), data[5], int(data[6]), int(data[7]), data[8]))
mydb.commit()


# ott_service table
myCursor.execute("CREATE TABLE IF NOT EXISTS ott_service (ott_id INT PRIMARY KEY, ott_service VARCHAR(255), last_update DATE, FOREIGN KEY (ott_id) REFERENCES movies(ott_id))")

with open('./DSC3037_23_2_RDBMS/for_use/ott_service.csv', encoding='UTF-8') as csvfile:
    ott_data = csv.reader(csvfile)
    header = next(ott_data)  # Skip header
    for data in ott_data:
        last_update = datetime.strptime(data[3], '%Y%m%d').date()
        myCursor.execute("INSERT INTO ott_service (ott_id, ott_service, last_update) VALUES (%s, %s, %s)", (int(data[1]), data[2], last_update))
mydb.commit()


# director table
myCursor.execute("CREATE TABLE IF NOT EXISTS director (director_id INT PRIMARY KEY, director_name VARCHAR(255), last_update DATE)")

with open('./DSC3037_23_2_RDBMS/for_use/director.csv', encoding='UTF-8') as csvfile:
    director_data = csv.reader(csvfile)
    header = next(director_data)  # Skip header
    for data in director_data:
        last_update = datetime.strptime(data[3], '%Y%m%d').date()
        myCursor.execute("INSERT INTO director (director_id, director_name, last_update) VALUES (%s, %s, %s)", (int(data[1]), data[2], last_update))
mydb.commit()


# direct table
myCursor.execute("CREATE TABLE IF NOT EXISTS direct (movie_id INT, director_id INT, last_update DATE, PRIMARY KEY (movie_id, director_id), FOREIGN KEY (movie_id) REFERENCES movies(movie_id), FOREIGN KEY (director_id) REFERENCES director(director_id))")

with open('./DSC3037_23_2_RDBMS/for_use/direct.csv', encoding='UTF-8') as csvfile:
    director_data = csv.reader(csvfile)
    header = next(director_data)  # Skip header
    for data in director_data:
        last_update = datetime.strptime(data[3], '%Y%m%d').date()
        myCursor.execute("INSERT INTO direct (movie_id, director_id, last_update) VALUES (%s, %s, %s)", (int(data[1]), int(data[2]), last_update))
mydb.commit()


# actor table
myCursor.execute("CREATE TABLE IF NOT EXISTS actor (actor_id INT PRIMARY KEY, actor_name VARCHAR(255), last_update DATE)")

with open('./DSC3037_23_2_RDBMS/for_use/actor.csv', encoding='UTF-8') as csvfile:
    actor_data = csv.reader(csvfile)
    header = next(actor_data)  # Skip header
    for data in actor_data:
        last_update = datetime.strptime(data[3], '%Y%m%d').date()
        myCursor.execute("INSERT INTO actor (actor_id, actor_name, last_update) VALUES (%s, %s, %s)", (int(data[1]), data[2], last_update))
mydb.commit()


# cast table
myCursor.execute("CREATE TABLE IF NOT EXISTS cast (movie_id INT, actor_id INT, last_update DATE, PRIMARY KEY (movie_id, actor_id), FOREIGN KEY (movie_id) REFERENCES movies(movie_id), FOREIGN KEY (actor_id) REFERENCES actor(actor_id))")

with open('./DSC3037_23_2_RDBMS/for_use/cast.csv', encoding='UTF-8') as csvfile:
    cast_data = csv.reader(csvfile)
    header = next(cast_data)  # Skip header
    for data in cast_data:
        last_update = datetime.strptime(data[3], '%Y%m%d').date()
        myCursor.execute("INSERT INTO cast (movie_id, actor_id, last_update) VALUES (%s, %s, %s)", (int(data[1]), int(data[2]), last_update))
mydb.commit()


# genre table
myCursor.execute("CREATE TABLE IF NOT EXISTS genre (genre_id INT PRIMARY KEY, genre_name VARCHAR(255), last_update DATE)")

with open('./DSC3037_23_2_RDBMS/for_use/genre.csv', encoding='UTF-8') as csvfile:
    genre_data = csv.reader(csvfile)
    header = next(genre_data)  # Skip header
    for data in genre_data:
        last_update = datetime.strptime(data[3], '%Y%m%d').date()
        myCursor.execute("INSERT INTO genre (genre_id, genre_name, last_update) VALUES (%s, %s, %s)", (int(data[1]), data[2], last_update))
mydb.commit()


# movies_genre table
myCursor.execute("CREATE TABLE IF NOT EXISTS movies_genre (movie_id INT, genre_id INT, last_update DATE, PRIMARY KEY (movie_id, genre_id), FOREIGN KEY (movie_id) REFERENCES movies(movie_id), FOREIGN KEY (genre_id) REFERENCES genre(genre_id))")

with open('./DSC3037_23_2_RDBMS/for_use/movies_genre.csv', encoding='UTF-8') as csvfile:
    movies_genre_data = csv.reader(csvfile)
    header = next(movies_genre_data)  # Skip header
    for data in movies_genre_data:
        last_update = datetime.strptime(data[3], '%Y%m%d').date()
        myCursor.execute("INSERT INTO movies_genre (movie_id, genre_id, last_update) VALUES (%s, %s, %s)", (int(data[1]), int(data[2]), last_update))
mydb.commit()  


# country table
myCursor.execute("CREATE TABLE IF NOT EXISTS country (country_id INT PRIMARY KEY, country_name VARCHAR(255), last_update DATE)")

with open('./DSC3037_23_2_RDBMS/for_use/country.csv', encoding='UTF-8') as csvfile:
    country_data = csv.reader(csvfile)
    header = next(country_data)  # Skip header
    for data in country_data:
        last_update = datetime.strptime(data[3], '%Y%m%d').date()
        myCursor.execute("INSERT INTO country (country_id, country_name, last_update) VALUES (%s, %s, %s)", (int(data[1]), data[2], last_update))
mydb.commit()


# movies_country table
myCursor.execute("CREATE TABLE IF NOT EXISTS movies_country (movie_id INT, country_id INT, last_update DATE, PRIMARY KEY (movie_id, country_id), FOREIGN KEY (movie_id) REFERENCES movies(movie_id), FOREIGN KEY (country_id) REFERENCES country(country_id))")

with open('./DSC3037_23_2_RDBMS/for_use/movies_genre.csv', encoding='UTF-8') as csvfile:
    movies_country_data = csv.reader(csvfile)
    header = next(movies_country_data)  # Skip header
    for data in movies_country_data:
        last_update = datetime.strptime(data[3], '%Y%m%d').date()
        myCursor.execute("INSERT INTO movies_country (movie_id, country_id, last_update) VALUES (%s, %s, %s)", (int(data[1]), int(data[2]), last_update))
mydb.commit()