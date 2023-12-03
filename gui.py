import tkinter as tk
from tkinter import ttk
import mysql.connector
import tkinter.messagebox as messagebox

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="5789",
    database="db_project"
)
cursor = conn.cursor()

filter_settings = {
    'categories': set(),
    'rating': [],
    'year': [],
    'ott': []
}

max_row = 10

def filter_by_rating(rating):
    toggle_button_color(rating_button[rating])
    filter_settings['rating'] = [rating for rating in rating_names if rating_button[rating].cget('bg') == 'black']

def filter_by_year(year):
    toggle_button_color(year_button[year])
    filter_settings['year'] = [year for year in year_buttons if year_button[year].cget('bg') == 'black']

def filter_by_ott(ott_service):
    toggle_button_color(ott_button[ott_service])
    filter_settings['ott'] = [service for service in ott_list if ott_button[service].cget('bg') == 'black']

def toggle_button_color(button):
    current_bg = button.cget('bg')
    button.config(bg=button.cget('fg'), fg=current_bg)

def generate_recommendations(limit=max_row):
    global filter_settings

    where_conditions = []

    if filter_settings['rating']:
        where_conditions.append(f"m.rating IN ({','.join(map(repr, filter_settings['rating']))})")

    if filter_settings['year']:
        year_ranges = {
            '1900s': (1971, 1999),
            '2000s': (2000, 2009),
            '2010s': (2010, 2019),
            '2020s': (2020, 2029),
        }
        year_conditions = []
        for year_category in filter_settings['year']:
            start_year, end_year = year_ranges.get(year_category, (0, 0))
            year_conditions.append(f"m.release_year BETWEEN {start_year} AND {end_year}")
        where_conditions.append("(" + " OR ".join(year_conditions) + ")")

    if filter_settings['ott']:
        where_conditions.append(f"ott_service.ott_service IN ({','.join(map(repr, filter_settings['ott']))})")

    where_clause = " AND ".join(where_conditions)
    where_clause = f"WHERE {where_clause}" if where_clause else ""

    sql_query = f"""
        SELECT DISTINCT m.movie_id, m.title,
                        GROUP_CONCAT(DISTINCT director.director_name SEPARATOR ', ') AS directors,
                        GROUP_CONCAT(DISTINCT actor.actor_name SEPARATOR ', ') AS actors,
                        GROUP_CONCAT(DISTINCT genre.genre_name SEPARATOR ', ') AS genres,
                        m.release_year, m.rating, m.duration, ott_service.ott_service
                        
        FROM movies m
        LEFT JOIN direct ON m.movie_id = direct.movie_id
        LEFT JOIN director ON direct.director_id = director.director_id
        LEFT JOIN cast ON m.movie_id = cast.movie_id
        LEFT JOIN actor ON cast.actor_id = actor.actor_id
        LEFT JOIN ott_service ON m.ott_id = ott_service.ott_id
        LEFT JOIN movies_genre ON m.movie_id = movies_genre.movie_id
        LEFT JOIN genre ON movies_genre.genre_id = genre.genre_id
        {where_clause}
        GROUP BY m.movie_id
        ORDER BY RAND()  -- Random order
        LIMIT {limit}
    """

    cursor.execute(sql_query)
    result = cursor.fetchall()

    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)

    for row in result:
        result_text.config(state=tk.NORMAL)

        result_text.insert(tk.END, f"Title: {row[1]}\n"
                                f"Directors: {row[2]}\n"
                                f"Actors: {row[3]}\n"
                                f"Genres: {row[4]}\n"
                                f"Release Year: {row[5]}\n"
                                f"Rating: {row[6]}\n"
                                f"Duration: {row[7]} minutes\n"
                                f"OTT Service: {row[8]}\n")

        detail_button = tk.Button(result_text, text="Detail", command=lambda mid=row[0]: open_detail_window(mid))
        result_text.window_create(tk.END, window=detail_button)
        result_text.insert(tk.END, "\n\n")

    result_text.config(state=tk.DISABLED)

def search_movies(limit=max_row):
    global filter_settings
    search_query = search_var.get().strip()
    selected_categories_list = list(filter_settings['categories'])
    selected_rating = filter_settings['rating']
    selected_year = filter_settings['year']
    selected_ott = filter_settings['ott']

    if not selected_categories_list:
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Please select category first.")
        result_text.config(state=tk.DISABLED)
        return

    sql_query = """
        SELECT DISTINCT m.movie_id, m.title,
                        GROUP_CONCAT(DISTINCT director.director_name SEPARATOR ', ') AS directors,
                        GROUP_CONCAT(DISTINCT actor.actor_name SEPARATOR ', ') AS actors,
                        GROUP_CONCAT(DISTINCT genre.genre_name SEPARATOR ', ') AS genres,
                        m.release_year, m.rating, m.duration, ott_service.ott_service
        FROM movies m
        LEFT JOIN direct ON m.movie_id = direct.movie_id
        LEFT JOIN director ON direct.director_id = director.director_id
        LEFT JOIN cast ON m.movie_id = cast.movie_id
        LEFT JOIN actor ON cast.actor_id = actor.actor_id
        LEFT JOIN movies_genre ON m.movie_id = movies_genre.movie_id
        LEFT JOIN genre ON movies_genre.genre_id = genre.genre_id
        LEFT JOIN ott_service ON m.ott_id = ott_service.ott_id
        WHERE 
    """

    conditions = []

    if 'Movie' in selected_categories_list:
        conditions.append(f"m.title LIKE '%{search_query}%'")

    if 'Director' in selected_categories_list:
        conditions.append(f"director.director_name LIKE '%{search_query}%'")

    if 'Actor' in selected_categories_list:
        conditions.append(f"actor.actor_name LIKE '%{search_query}%'")

    if 'Genre' in selected_categories_list:
        conditions.append(f"genre.genre_name LIKE '%{search_query}%'")

    if selected_rating:
        conditions.append(f"m.rating IN ({','.join(map(repr, selected_rating))})")

    if selected_year:
        year_ranges = {
            '1900s': (1971, 1999),
            '2000s': (2000, 2009),
            '2010s': (2010, 2019),
            '2020s': (2020, 2029),
        }
        year_conditions = []
        for year_category in selected_year:
            start_year, end_year = year_ranges.get(year_category, (0, 0))
            year_conditions.append(f"m.release_year BETWEEN {start_year} AND {end_year}")
        conditions.append("(" + " OR ".join(year_conditions) + ")")

    if selected_ott:
        conditions.append(f"ott_service.ott_service IN ({','.join(map(repr, selected_ott))})")

    sql_query += " AND ".join(conditions) + f" GROUP BY m.movie_id LIMIT {limit}"

    cursor.execute(sql_query)
    result = cursor.fetchall()

    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)

    for row in result:
        result_text.config(state=tk.NORMAL)

        result_text.insert(tk.END, f"Title: {row[1]}\n"
                                   f"Directors: {row[2]}\n"
                                   f"Actors: {row[3]}\n"
                                   f"Genres: {row[4]}\n"
                                   f"Release Year: {row[5]}\n"
                                   f"Rating: {row[6]}\n"
                                   f"Duration: {row[7]} minutes\n"
                                   f"OTT Service: {row[8]}\n")

        detail_button = tk.Button(result_text, text="Detail", command=lambda mid=row[0]: open_detail_window(mid))
        result_text.window_create(tk.END, window=detail_button)
        result_text.insert(tk.END, "\n\n")

    result_text.config(state=tk.DISABLED)

def clear_search():
    search_var.set("")
    result_text.config(state=tk.NORMAL)
    generate_recommendations()
    result_text.config(state=tk.DISABLED)

def open_detail_window(movie_id):
    query = """
        SELECT m.title,
                GROUP_CONCAT(DISTINCT director.director_name) AS directors,
                GROUP_CONCAT(DISTINCT actor.actor_name SEPARATOR ', ') AS actors,
                GROUP_CONCAT(DISTINCT genre.genre_name SEPARATOR ', ') AS genres,
                m.release_year, m.rating, m.duration, ott_service.ott_service,
                m.last_update, m.description
        FROM movies m
        LEFT JOIN direct ON m.movie_id = direct.movie_id
        LEFT JOIN director ON direct.director_id = director.director_id
        LEFT JOIN cast ON m.movie_id = cast.movie_id
        LEFT JOIN actor ON cast.actor_id = actor.actor_id
        LEFT JOIN movies_genre ON m.movie_id = movies_genre.movie_id
        LEFT JOIN genre ON movies_genre.genre_id = genre.genre_id
        LEFT JOIN ott_service ON m.ott_id = ott_service.ott_id
        WHERE m.movie_id = %s
        GROUP BY m.movie_id
    """

    cursor.execute(query, (movie_id,))
    movie_details = cursor.fetchone()

    detail_window = tk.Toplevel(root)
    detail_window.title(f"Details for Movie ID: {movie_id}")
    detail_window.configure(bg='white')

    detail_text = tk.Text(detail_window, font=('Input Mono', 12, 'bold'), bg='white', fg='black')
    detail_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    detail_text.insert(tk.END, f"Title: {movie_details[0]}\n\n"
                               f"Directors: {movie_details[1]}\n\n"
                               f"Actors: {movie_details[2]}\n\n"
                               f"Genres: {movie_details[3]}\n\n"
                               f"Release Year: {movie_details[4]}\n\n"
                               f"Rating: {movie_details[5]}\n\n"
                               f"Duration: {movie_details[6]} minutes\n\n"
                               f"OTT: {movie_details[7]}\n\n"
                               f"Last Update: {'no info' if str(movie_details[8]) == '1970-01-01' else movie_details[8]}\n\n"
                               f"Description: {movie_details[9]}")
    detail_text.config(state=tk.DISABLED)

def open_category_window():
    global filter_settings
    category_window = tk.Toplevel(root)
    category_window.title("Select Categories")
    category_window.bind('<Control-BackSpace>', lambda event: category_window.destroy())

    def toggle_category(category):
        if category in filter_settings['categories']:
            filter_settings['categories'].remove(category)
            category_buttons[category].config(bg='white', fg='black')
        else:
            filter_settings['categories'].add(category)
            category_buttons[category].config(bg='black', fg='white')

    def reset_categories():
        filter_settings['categories'] = set()
        category_button.config(text='Category')

    reset_categories()

    category_button_names = ['Movie', 'Director', 'Actor', 'Genre']
    category_buttons = {}

    for category_name in category_button_names:
        category_buttons[category_name] = tk.Button(
            category_window, text=category_name,
            command=lambda category=category_name: toggle_category(category),
            width=15, height=2,
            bg='white', fg='black', bd=3, relief=tk.RAISED,
            font=('Input Mono', 10, 'bold')
        )
        category_buttons[category_name].pack(pady=5)

    def select_categories():
        if not filter_settings['categories']:
            category_button.config(text='Category')
        else:
            category_button.config(text='\n'.join(filter_settings['categories']))
        category_window.destroy()

    select_button = tk.Button(
        category_window, text="Select",
        command=select_categories,
        width=15, height=2,
        bg='white', fg='black', bd=3, relief=tk.RAISED,
        font=('Input Mono', 10, 'bold')
    )
    select_button.pack(side=tk.RIGHT, padx=10, pady=10)

def open_title_window():
    title_window = tk.Toplevel(root)
    title_window.title("Details")
    title_window.bind('<Control-BackSpace>', lambda event: title_window.destroy())

    text_label = tk.Label(title_window, text="HAND-MOVIE\n\nMade by Group 2\nGaeun Seo, Imafuku Kokoro, Kyunam Park", font=('Input Mono', 12, 'bold'))
    text_label.pack(padx=20, pady=20)

def open_rating_window(rating=None):
    rating_window = tk.Toplevel(root)
    rating_window.title(f"About Ratings")
    rating_window.bind('<Control-BackSpace>', lambda event: rating_window.destroy())

    text_label = tk.Label(rating_window, font=('Input Mono', 12, 'bold'), text=f"G(General Audiences)\nAll ages admitted.\nNothing that would offend parents for viewing by children.\n\nPG(Parental Guidance Suggested)\nSome material may not be suitable for children.\nParents urged to give \'parental guidance\'.\nMay contain some material parents might not like for their young children.\n\nPG-13(Parental Strongly Cautioned)\nSome material may be inappropriate for children under 13.\nParents are urged to be cautious.\nSome material may be inappropriate for pre-teenagers.\n\nR(Restricted)\nUnder 17 requires accompanying parent or adult guardian.\nContains some adult material.\nParents are urged to learn more about the film before taking their young children with them.\n\nNC-17(Adults Only)\nNo one 17 and under admitted.\nClearly adult.\nChildren are not admitted.")
    text_label.pack(padx=20, pady=20)

root = tk.Tk()
root.title("HAND-MOVIE")
root.configure(bg='black')
root.geometry("850x650")

title_frame = tk.Frame(root, bg='black')
title_frame.pack(pady=10)

title_label = tk.Label(title_frame, text="HAND-MOVIE", font=('Input Mono', 22, 'bold'), bg='#F2DB83', fg='black')
title_label.pack()
title_label.bind('<Button-1>', lambda event: open_title_window())
root.bind('<Control-e>', lambda event: open_title_window())

ttk.Separator(title_frame, orient=tk.HORIZONTAL).pack(fill='x', pady=7)

category_button = tk.Button(
    title_frame, text="Category", bg='#F2DB83', fg='black', bd=3, relief=tk.RAISED,
    font=('Input Mono', 12, 'bold'), command=open_category_window
)
category_button.pack(side=tk.LEFT)
root.bind('<Control-y>', lambda event: category_button.invoke())

search_var = tk.StringVar()
search_entry = tk.Entry(title_frame, textvariable=search_var, width=30, font=('Input Mono', 14, 'bold'))
search_entry.pack(side=tk.LEFT, padx=10)
search_entry.focus_set()
search_entry.bind('<Return>', lambda event=None: search_movies())

search_button = tk.Button(
    title_frame, text="Search", bg='white', fg='black', bd=3, relief=tk.RAISED,
    font=('Input Mono', 12, 'bold'), command=search_movies
)
search_button.pack(side=tk.LEFT)

clear_button = tk.Button(
    title_frame, text="Clear", bg='white', fg='black', bd=3, relief=tk.RAISED,
    font=('Input Mono', 12, 'bold'), command=clear_search
)
clear_button.pack(side=tk.RIGHT, padx=10)
root.bind('<Control-BackSpace>', lambda event: clear_button.invoke())

left_frame = tk.Frame(root, bg='black', relief=tk.RAISED)
left_frame.config(highlightbackground='white', highlightthickness=2)
left_frame.pack(side=tk.LEFT, padx=20)

rating_frame = tk.Frame(left_frame, bg='black', padx=15)
rating_frame.pack()

rating_label = tk.Label(rating_frame, text="Rating", font=('Input Mono', 12, 'bold'), bg='#F2DB83', fg='black')
rating_label.pack(pady = 3)
rating_label.bind('<Button-1>', open_rating_window)
root.bind('<Control-g>', lambda event: open_rating_window())

rating_names = ['G', 'PG', 'PG-13', 'R', 'NC-17']
max_rating_width = 12

rating_button = {}
for rating in rating_names:
    rating_button[rating] = tk.Button(rating_frame, text=rating, width=max_rating_width, 
                                      command=lambda rating=rating: filter_by_rating(rating),
                                      bg='white', fg='black', bd=3, relief=tk.RAISED, font=('Input Mono', 10, 'bold'))
    rating_button[rating].pack()
root.bind('<Control-F1>', lambda event: toggle_button_color(rating_button['G']))
root.bind('<Control-F2>', lambda event: toggle_button_color(rating_button['PG']))
root.bind('<Control-F3>', lambda event: toggle_button_color(rating_button['PG-13']))
root.bind('<Control-F4>', lambda event: toggle_button_color(rating_button['R']))
root.bind('<Control-F5>', lambda event: toggle_button_color(rating_button['NC-17']))

ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill='x', pady=5)

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
root.bind('<Control-F6>', lambda event: toggle_button_color(year_button['1900s']))
root.bind('<Control-F7>', lambda event: toggle_button_color(year_button['2000s']))
root.bind('<Control-F8>', lambda event: toggle_button_color(year_button['2010s']))
root.bind('<Control-F9>', lambda event: toggle_button_color(year_button['2020s']))

ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill='x', pady=5)

ott_frame = tk.Frame(left_frame, bg='black', padx=15)
ott_frame.pack()
ott_label = tk.Label(ott_frame, text="OTT", font=('Input Mono', 12, 'bold'), bg='black', fg='white')
ott_label.pack()

ott_list = ['netflix', 'amazon_prime', 'hulu', 'disney_plus']
max_ott_width = 12

ott_button = {}
for service in ott_list:
    ott_button[service] = tk.Button(ott_frame, text=service, width=max_ott_width, 
                                    command=lambda service=service: filter_by_ott(service),
                                    bg='white', fg='black', bd=3, relief=tk.RAISED, font=('Input Mono', 10, 'bold'))
    ott_button[service].pack()
root.bind('<Control-9>', lambda event: toggle_button_color(ott_button['Netflix']))
root.bind('<Control-0>', lambda event: toggle_button_color(ott_button['Amazon Prime']))
root.bind('<Control-minus>', lambda event: toggle_button_color(ott_button['Hulu']))
root.bind('<Control-=>', lambda event: toggle_button_color(ott_button['Disney+']))

right_frame = tk.Frame(root, bg='black')
right_frame.pack(side=tk.RIGHT, padx=10, expand=True, fill=tk.BOTH)

result_label = tk.Label(right_frame, text="Search and Recommendation Results", font=('Input Mono', 14, 'bold'), bg='black', fg='white')
result_label.pack(fill=tk.X)

result_text = tk.Text(right_frame, font=('Input Mono', 10, 'bold'))
result_text.pack(expand=True, fill=tk.BOTH, padx=10, pady=30)
result_text.config(state=tk.DISABLED)

generate_recommendations()

root.mainloop()