import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
import sqlite3
import random

def filter_by_rating(rating):
    toggle_button_color(rating_button[rating])

def filter_by_year(year):
    toggle_button_color(year_button[year])

def filter_by_ott(ott_service):
    toggle_button_color(ott_button[ott_service])

def toggle_button_color(button):
    current_bg = button.cget('bg')
    button.config(bg=button.cget('fg'), fg=current_bg)

def search_autocomplete(event):
    query = search_var.get().strip()

    if query:
        result_label.config(text="Searched Result")
    else:
        result_label.config(text="Recommendation for You")

root = tk.Tk()
root.title("HAND-list")
root.configure(bg='black')

# Set the base size of the window
root.geometry("600x650")  # Adjust the size as needed

# Database Connection
conn = sqlite3.connect('db_project.db')
cursor = conn.cursor()

# Title, Search Bar, and Search Button Frame
title_frame = tk.Frame(root, bg='black')
title_frame.pack(pady=10)

# Title and Horizontal Line
title_label = tk.Label(title_frame, text="HAND-list", font=('Helvetica', 16, 'bold'), bg='#F2DB83', fg='black')  # Set background to yellow
title_label.pack()
ttk.Separator(title_frame, orient=tk.HORIZONTAL).pack(fill='x', pady=7)

# Searching Bar
search_var = tk.StringVar()
search_entry = tk.Entry(title_frame, textvariable=search_var, width=30, font=('Helvetica', 14, 'bold'))
search_entry.pack(side=tk.LEFT)
search_entry.bind('<KeyRelease>', search_autocomplete)

# Update the command of the Search Button to use the search function
search_button = tk.Button(title_frame, text="Search", bg='white', fg='black', bd=3, relief=tk.RAISED, font=('Helvetica', 12, 'bold'))
search_button.pack(side=tk.LEFT, padx=(10, 0))

# Left Side
left_frame = tk.Frame(root, bg='black', relief=tk.RAISED)
left_frame.config(highlightbackground='white', highlightthickness=2)  # Add a border around the frame
left_frame.pack(side=tk.LEFT, padx=10)

# Rating Box
rating_frame = tk.Frame(left_frame, bg='black', padx=15)  # Reduce padx to narrow the space
rating_frame.pack()
rating_label = tk.Label(rating_frame, text="Rating", font=('Helvetica', 12, 'bold'), bg='black', fg='white')
rating_label.pack(pady = 3)

rating_names = ['G', 'PG', 'PG-13', 'NC-17']
max_rating_width = 12

rating_button = {}
for rating in rating_names:
    rating_button[rating] = tk.Button(rating_frame, text=rating, width=max_rating_width, 
                                      command=lambda rating=rating: filter_by_rating(rating),
                                      bg='white', fg='black', bd=3, relief=tk.RAISED, font=('Helvetica', 10, 'bold'))  # Decrease the font size
    rating_button[rating].pack()

# Add a horizontal line
ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill='x', pady=5)  # Reduce pady to narrow the space

# Release Year Box
release_frame = tk.Frame(left_frame, bg='black', padx=15)  # Reduce padx to narrow the space
release_frame.pack()
release_label = tk.Label(release_frame, text="Release Year", font=('Helvetica', 12, 'bold'), bg='black', fg='white')
release_label.pack()

year_buttons = ['1900s', '2000s', '2010s', '2020s']
max_year_width = 12

year_button = {}
for year in year_buttons:
    year_button[year] = tk.Button(release_frame, text=year, width=max_year_width, 
                                  command=lambda year=year: filter_by_year(year),
                                  bg='white', fg='black', bd=3, relief=tk.RAISED, font=('Helvetica', 10, 'bold'))  # Decrease the font size
    year_button[year].pack()

# Add another horizontal line
ttk.Separator(left_frame, orient=tk.HORIZONTAL).pack(fill='x', pady=5)  # Reduce pady to narrow the space

# OTT Box
ott_frame = tk.Frame(left_frame, bg='black', padx=15)  # Reduce padx to narrow the space
ott_frame.pack()
ott_label = tk.Label(ott_frame, text="OTT", font=('Helvetica', 12, 'bold'), bg='black', fg='white')
ott_label.pack()

ott_list = ['Netflix', 'Amazon Prime', 'Hulu', 'Disney+']
max_ott_width = 12

ott_button = {}
for service in ott_list:
    ott_button[service] = tk.Button(ott_frame, text=service, width=max_ott_width, 
                                    command=lambda service=service: filter_by_ott(service),
                                    bg='white', fg='black', bd=3, relief=tk.RAISED, font=('Helvetica', 10, 'bold'))  # Decrease the font size
    ott_button[service].pack()

# Right Side
right_frame = tk.Frame(root, bg='black')
right_frame.pack(side=tk.RIGHT, padx=50)

# Result Box
result_label = tk.Label(right_frame, text="Recommendation for You", font=('Helvetica', 14, 'bold'), bg='black', fg='white')
result_label.pack(pady=10)

# Result Box
result_text = tk.Text(right_frame, height=35, width=50)
result_text.pack()
result_text.config(state=tk.DISABLED)

root.mainloop()