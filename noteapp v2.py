import sys
import tkinter as tk
import tkinter.scrolledtext as tkst
import datetime
import sqlite3
import os

# check if the database exists
if os.path.exists("notes.db"):
    # if it exists, connect to it
    conn = sqlite3.connect("notes.db")
else:
    # if it doesn't exist, create it and connect to it
    conn = sqlite3.connect("notes.db")

    # create a table to store the notes
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY,
            date TEXT,
            time DATETIME,
            note TEXT
        )
    """)

# define the main window
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Note Manager")
        self.resizable(True, True)
        self.geometry("500x500")

        # configure the rows and columns in the grid to be proportional to the size of the parent widget
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=10)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=3)
        self.grid_columnconfigure(3, weight=1)

        # create the widgets
        self.add_note_label = tk.Label(self, text="Enter a note:")
        self.add_note_textbox = tkst.ScrolledText(self)
        self.add_note_button = tk.Button(self, text="Add Note", command=self.add_note)
        self.view_notes_label = tk.Label(self, text="Enter a date to view notes for:")
        self.view_notes_date = tk.StringVar()
        self.view_notes_date.set(datetime.date.today().strftime("%d-%m-%Y"))
        self.view_notes_entry = tk.Entry(self, textvariable=self.view_notes_date)
        self.view_notes_button = tk.Button(self, text="View Notes", command=self.view_notes)
        self.notes_list = tk.Listbox(self)

        # create the layout
        self.add_note_label.grid(row=0, column=0, sticky="W")
        self.add_note_textbox.grid(row=1, column=0, columnspan=3, rowspan=3, sticky="W")
        self.add_note_button.grid(row=1, column=3, sticky="W")
        self.view_notes_label.grid(row=4, column=0, sticky="W")
        self.view_notes_entry.grid(row=4, column=1, columnspan=2, sticky="W")
        self.view_notes_button.grid(row=4, column=3, sticky="W")
        self.notes_list.config(width=100)
        self.notes_list.grid(row=5, column=0, columnspan=4, sticky="W")


    # add a note to the database
    def add_note(self):
        # get the current date and time
        date = datetime.date.today().strftime("%d-%m-%Y")
        time = datetime.datetime.now()

        # get the note from the text box
        note = self.add_note_textbox.get('1.0', tk.END)

        # insert the note and time into the database
        conn.execute("""
            INSERT INTO notes (date, time, note)
            VALUES (?, ?, ?)
        """, (date, time, note))

        # commit the changes to the database
        conn.commit()

        # clear the text box
        self.add_note_textbox.delete('1.0', tk.END)

    # view notes for a specific date
    def view_notes(self):
        # get the selected date
        date = self.view_notes_date.get()  # <-- Call the get method to get the value of the StringVar

        # get the notes and times for the selected date from the database
        cursor = conn.execute("""
            SELECT time, note
            FROM notes
            WHERE date = ?
        """, (date,))

        # clear the notes list
        self.notes_list.delete(0, tk.END)

        # add the notes and times to the notes list
        for row in cursor:
            self.notes_list.insert(tk.END, f"{row[0]}: {row[1]}")

# create and show the main window
app = MainWindow()
app.mainloop()

