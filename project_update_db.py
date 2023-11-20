import csv
import mysql.connector

# USe this code only first you create your database
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

csv_data = csv.reader(open('./data/movies.csv', encoding='UTF-8'))
header = next(csv_data)

myCursor.execute("CREATE TABLE movies(movie_id INT PRIMARY KEY, title VARCHAR(255), director VARCHAR(4000), date_added VARCHAR(255), release_year INT, rating VARCHAR(255), duration VARCHAR(255))")
for data in csv_data:
    data = data[1:-1]
    myCursor.execute("INSERT INTO movies (movie_id, title, director, date_added, release_year, rating, duration) VALUES (%s, %s, %s, %s, %s, %s, %s)", data)
mydb.commit()



ott_data = csv.reader(open('./data/ott_service.csv', encoding='UTF-8'))
ott_header = next(ott_data)

myCursor.execute("CREATE TABLE ott_service(movie_id INT PRIMARY KEY, ott_service VARCHAR(255), FOREIGN KEY (movie_id) REFERENCES movies(movie_id))")
for data in ott_data:
    data = data[1:]
    myCursor.execute("INSERT INTO ott_service (movie_id, ott_service) VALUES (%s, %s)", data)
mydb.commit()

genre_data = csv.reader(open('./data/genre.csv', encoding='UTF-8'))
genre_header = next(genre_data)

myCursor.execute("CREATE TABLE genre(genre_id INT PRIMARY KEY, movie_id INT, genre VARCHAR(255), FOREIGN KEY (movie_id) REFERENCES movies(movie_id))")
for data in genre_data:
    #data = data[1:]
    myCursor.execute("INSERT INTO genre (genre_id, movie_id, genre) VALUES (%s, %s, %s)", data)
mydb.commit()


country_data = csv.reader(open('./data/country.csv', encoding='UTF-8'))
country_header = next(country_data)

myCursor.execute("CREATE TABLE country(country_id INT PRIMARY KEY,movie_id INT, country VARCHAR(255), FOREIGN KEY (movie_id) REFERENCES movies(movie_id))")
for data in country_data:
    #data = data[1:]
    myCursor.execute("INSERT INTO country(country_id, movie_id, country) VALUES (%s, %s, %s)", data)
mydb.commit()