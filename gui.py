import tkinter as tk
from tkinter import ttk
import mysql.connector
import random

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="5789",
    database="db_project"  # Change to your database name
)
cursor = conn.cursor()

def filter_by_rating(rating):
    toggle_button_color(rating_button[rating])

def filter_by_year(year):
    toggle_button_color(year_button[year])

def filter_by_ott(ott_service):
    toggle_button_color(ott_button[ott_service])

def toggle_button_color(button):
    current_bg = button.cget('bg')
    button.config(bg=button.cget('fg'), fg=current_bg)

def execute_query_and_display_results(query, label_text):
    result_label.config(text=label_text)
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)

    cursor.execute(query)
    results = cursor.fetchall()

    if results:
        for result in results:
            display_result(result)
    else:
        result_text.insert(tk.END, "No results found.")

    result_text.config(state=tk.DISABLED)

def search_autocomplete(event):
    query = search_var.get().strip()

    if query:
        search_query = f"SELECT m.title, GROUP_CONCAT(DISTINCT d.director_name) AS director_names, " \
                       f"GROUP_CONCAT(DISTINCT a.actor_name) AS actor_names, " \
                       f"GROUP_CONCAT(DISTINCT g.genre_name) AS genre_names, " \
                       f"GROUP_CONCAT(DISTINCT c.country_name) AS country_names, " \
                       f"m.rating, GROUP_CONCAT(DISTINCT o.ott_service) AS ott_names, " \
                       f"m.release_year " \
                       f"FROM movies m " \
                       f"LEFT JOIN direct dr ON m.movie_id = dr.movie_id " \
                       f"LEFT JOIN director d ON dr.director_id = d.director_id " \
                       f"LEFT JOIN cast ca ON m.movie_id = ca.movie_id " \
                       f"LEFT JOIN actor a ON ca.actor_id = a.actor_id " \
                       f"LEFT JOIN movies_genre mg ON m.movie_id = mg.movie_id " \
                       f"LEFT JOIN genre g ON mg.genre_id = g.genre_id " \
                       f"LEFT JOIN movies_country mc ON m.movie_id = mc.movie_id " \
                       f"LEFT JOIN country c ON mc.country_id = c.country_id " \
                       f"LEFT JOIN ott_service o ON m.movie_id = o.movie_id " \
                       f"WHERE m.title LIKE '%{query}%' OR " \
                       f"d.director_name LIKE '%{query}%' OR " \
                       f"a.actor_name LIKE '%{query}%' OR " \
                       f"g.genre_name LIKE '%{query}%'" \
                       f"GROUP BY m.title, m.rating, m.release_year "
        execute_query_and_display_results(search_query, "Search Results")
    else:
        fetch_recommendations()

def fetch_recommendations():
    recommendation_query = f"SELECT m.title, GROUP_CONCAT(DISTINCT d.director_name) AS director_names, " \
                           f"GROUP_CONCAT(DISTINCT a.actor_name) AS actor_names, " \
                           f"GROUP_CONCAT(DISTINCT g.genre_name) AS genre_names, " \
                           f"GROUP_CONCAT(DISTINCT c.country_name) AS country_names, " \
                           f"m.rating, GROUP_CONCAT(DISTINCT o.ott_service) AS ott_names, " \
                           f"m.release_year " \
                           f"FROM movies m " \
                           f"JOIN direct dr ON m.movie_id = dr.movie_id " \
                           f"JOIN director d ON dr.director_id = d.director_id " \
                           f"JOIN cast ca ON m.movie_id = ca.movie_id " \
                           f"JOIN actor a ON ca.actor_id = a.actor_id " \
                           f"JOIN movies_genre mg ON m.movie_id = mg.movie_id " \
                           f"JOIN genre g ON mg.genre_id = g.genre_id " \
                           f"JOIN movies_country mc ON m.movie_id = mc.movie_id " \
                           f"JOIN country c ON mc.country_id = c.country_id " \
                           f"JOIN ott_service o ON m.movie_id = o.movie_id " \
                           f"GROUP BY m.title, m.rating, m.release_year "
    execute_query_and_display_results(recommendation_query, "Recommended Movies")

def display_result(result):
    movie_title, director_names, actor_names, genre_names, country_names, rating, ott_names, release_year = result
    actors_list = actor_names.split(',')[:3]
    directors_list = director_names.split(',')[:3]
    genres_list = genre_names.split(',')[:3]
    countries_list = country_names.split(',')[:3]

    result_text.insert(tk.END, f"Movie Title: {movie_title}\n"
                               f"Directors: {', '.join(directors_list)}\n"
                               f"Actors: {', '.join(actors_list)}\n"
                               f"Genres: {', '.join(genres_list)}\n"
                               f"Countries: {', '.join(countries_list)}\n"
                               f"Rating: {rating}\n"
                               f"OTT Services: {ott_names}\n"
                               f"Release Year: {release_year}\n\n")

    result_text.config(state=tk.DISABLED)

def randomize_recommendation():
    global all_recommendations

    if all_recommendations:
        execute_query_and_display_results(random.choice(all_recommendations), "Random Recommendation")

def open_title_window():
    title_window = tk.Toplevel(root)
    title_window.title("Details")
    
    text_label = tk.Label(title_window, text="HAND-MOVIE\n\nMade by Group 2\nGaeun Seo, Imafuku Kokoro, Kyunam Park", font=('Input Mono', 12, 'bold'))
    text_label.pack(padx=20, pady=20)

def open_rating_window(rating):
    rating_window = tk.Toplevel(root)
    rating_window.title(f"About Ratings")
    
    text_label = tk.Label(rating_window, font=('Input Mono', 12, 'bold'), text=f"G(General Audiences)\nAll ages admitted.\nNothing that would offend parents for viewing by children.\n\nPG(Parental Guidance Suggested)\nSome material may not be suitable for children.\nParents urged to give \'parental guidance\'.\nMay contain some material parents might not like for their young children.\n\nPG-13(Parental Strongly Cautioned)\nSome material may be inappropriate for children under 13.\nParents are urged to be cautious.\nSome material may be inappropriate for pre-teenagers.\n\nR(Restricted)\nUnder 17 requires accompanying parent or adult guardian.\nContains some adult material.\nParents are urged to learn more about the film before taking their young children with them.\n\nNC-17(Adults Only)\nNo one 17 and under admitted.\nClearly adult.\nChildren are not admitted.")
    text_label.pack(padx=20, pady=20)

root = tk.Tk()
root.title("HAND-MOVIE")
root.configure(bg='black')

# Set the base size of the window
root.geometry("850x650")

# Title, Search Bar, and Search Button Frame
title_frame = tk.Frame(root, bg='black')
title_frame.pack(pady=10)

# Title
title_label = tk.Label(title_frame, text="HAND-MOVIE", font=('Input Mono', 22, 'bold'), bg='#F2DB83', fg='black')
title_label.pack()
title_label.bind('<Button-1>', lambda event: open_title_window())

ttk.Separator(title_frame, orient=tk.HORIZONTAL).pack(fill='x', pady=7)

# Searching Bar
search_var = tk.StringVar()
search_entry = tk.Entry(title_frame, textvariable=search_var, width=30, font=('Input Mono', 14, 'bold'))
search_entry.pack(side=tk.LEFT)
search_entry.bind('<KeyRelease>', search_autocomplete)

# Search Button
search_button = tk.Button(title_frame, text="Search", bg='white', fg='black', bd=3, relief=tk.RAISED, font=('Input Mono', 12, 'bold'))
search_button.pack(side=tk.LEFT, padx=(10, 0))

# Left Side
left_frame = tk.Frame(root, bg='black', relief=tk.RAISED)
left_frame.config(highlightbackground='white', highlightthickness=2)
left_frame.pack(side=tk.LEFT, padx=20)

# Rating Box
rating_frame = tk.Frame(left_frame, bg='black', padx=15)
rating_frame.pack()

rating_label = tk.Label(rating_frame, text="Rating", font=('Input Mono', 12, 'bold'), bg='#F2DB83', fg='black')
rating_label.pack(pady = 3)
rating_label.bind('<Button-1>', open_rating_window)

rating_names = ['G', 'PG', 'PG-13', 'NC-17']
max_rating_width = 12

rating_button = {}
for rating in rating_names:
    rating_button[rating] = tk.Button(rating_frame, text=rating, width=max_rating_width, 
                                      command=lambda rating=rating: filter_by_rating(rating),
                                      bg='white', fg='black', bd=3, relief=tk.RAISED, font=('Input Mono', 10, 'bold'))  # Decrease the font size
    rating_button[rating].pack()

ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill='x', pady=5)

# Release Year Box
release_frame = tk.Frame(left_frame, bg='black', padx=15)
release_frame.pack()
release_label = tk.Label(release_frame, text="Release Year", font=('Input Mono', 12, 'bold'), bg='black', fg='white')
release_label.pack()

year_buttons = ['1900s', '2000s', '2010s', '2020s']
max_year_width = 12

year_button = {}
for year in year_buttons:
    year_button[year] = tk.Button(release_frame, text=year, width=max_year_width, 
                                  command=lambda year=year: filter_by_year(year),
                                  bg='white', fg='black', bd=3, relief=tk.RAISED, font=('Input Mono', 10, 'bold'))
    year_button[year].pack()

ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill='x', pady=5)

# OTT Box
ott_frame = tk.Frame(left_frame, bg='black', padx=15)
ott_frame.pack()
ott_label = tk.Label(ott_frame, text="OTT", font=('Input Mono', 12, 'bold'), bg='black', fg='white')
ott_label.pack()

ott_list = ['Netflix', 'Amazon Prime', 'Hulu', 'Disney+']
max_ott_width = 12

ott_button = {}
for service in ott_list:
    ott_button[service] = tk.Button(ott_frame, text=service, width=max_ott_width, 
                                    command=lambda service=service: filter_by_ott(service),
                                    bg='white', fg='black', bd=3, relief=tk.RAISED, font=('Input Mono', 10, 'bold'))
    ott_button[service].pack()

# Right Side
right_frame = tk.Frame(root, bg='black')
right_frame.pack(side=tk.RIGHT, padx=10, expand=True, fill=tk.BOTH)

# Result Box
result_label = tk.Label(right_frame, text="Recommendation for You", font=('Input Mono', 14, 'bold'), bg='black', fg='white')
result_label.pack(fill=tk.X)

result_text = tk.Text(right_frame, font=('Input Mono', 14, 'bold'))
result_text.pack(expand=True, fill=tk.BOTH, padx = 10, pady=30)
result_text.config(state=tk.DISABLED)

fetch_recommendations()

root.mainloop()