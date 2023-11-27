import csv
import mysql.connector

# Use this code only first you create your database
# mydb = mysql.connector.connect(
#     host = "localhost",
#     user= "root",
#     passwd = "8812"  
# )
    
# mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE db_project")

def connectDB(db_use):
    mydb = mysql.connector.connect(
        host = "localhost",
        user= "root",
        passwd = "8812",
        database = db_use
    )
    
    mycursor = mydb.cursor(prepared=True)
    return mydb, mycursor

mydb, myCursor = connectDB("db_project")


# movies table
csv_data = csv.reader(open('./data/movies.csv', encoding='UTF-8'))
header = next(csv_data)

myCursor.execute("CREATE TABLE movies(movie_id INT PRIMARY KEY, title VARCHAR(255), director VARCHAR(4000), date_added VARCHAR(255), release_year INT, rating VARCHAR(255), duration VARCHAR(255))")
for data in csv_data:
    data = data[1:]
    myCursor.execute("INSERT INTO movies (movie_id, title, director, date_added, release_year, rating, duration) VALUES (%s, %s, %s, %s, %s, %s, %s)", data)
mydb.commit()


# ott_service table
ott_data = csv.reader(open('./data/ott_service.csv', encoding='UTF-8'))
ott_header = next(ott_data)

myCursor.execute("CREATE TABLE ott_service(movie_id INT PRIMARY KEY, ott_service VARCHAR(255), FOREIGN KEY (movie_id) REFERENCES movies(movie_id))")
for data in ott_data:
    data = data[1:]
    myCursor.execute("INSERT INTO ott_service (movie_id, ott_service) VALUES (%s, %s)", data)
mydb.commit()


# genre table
genre_data = csv.reader(open('./data/genre.csv', encoding='UTF-8'))
genre_header = next(genre_data)

myCursor.execute("CREATE TABLE genre(id INT PRIMARY KEY, movie_id INT, genre VARCHAR(255), FOREIGN KEY (movie_id) REFERENCES movies(movie_id))")
for data in genre_data:
    #data = data[1:]
    myCursor.execute("INSERT INTO genre (id, movie_id, genre) VALUES (%s, %s, %s)", data)
mydb.commit()


# country table
country_data = csv.reader(open('./data/country.csv', encoding='UTF-8'))
country_header = next(country_data)

myCursor.execute("CREATE TABLE country(id INT PRIMARY KEY,movie_id INT, country VARCHAR(255), FOREIGN KEY (movie_id) REFERENCES movies(movie_id))")
for data in country_data:
    #data = data[1:]
    myCursor.execute("INSERT INTO country(id, movie_id, country) VALUES (%s, %s, %s)", data)
mydb.commit()


# actor table
actor_data = csv.reader(open('./data/cast.csv', encoding='UTF-8'))
actor_header = next(actor_data)

myCursor.execute("CREATE TABLE actor(id INT PRIMARY KEY,movie_id INT, actor VARCHAR(255), FOREIGN KEY (movie_id) REFERENCES movies(movie_id))")
for data in actor_data:
    #data = data[1:]
    myCursor.execute("INSERT INTO actor(id, movie_id, actor) VALUES (%s, %s, %s)", data)
mydb.commit()

