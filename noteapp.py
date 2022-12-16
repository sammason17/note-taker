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

while True:
    # get the current date and time
    date = datetime.date.today()
    time = datetime.datetime.now()

    # prompt the user for a note
    note = input("Enter a note: ")

    # insert the note and time into the database
    conn.execute("""
        INSERT INTO notes (date, time, note)
        VALUES (?, ?, ?)
    """, (date, time, note))

    # commit the changes to the database
    conn.commit()

    # prompt the user to see if they want to add another note
    another = input("Add another note? (Y/N) ")
    if another.lower() == "n":
        break

# prompt the user for a date to view notes for
view_date = input("Enter a date to view notes for (YYYY-MM-DD): ")

# get the notes and times for the specified date from the database
cursor = conn.execute("""
    SELECT time, note
    FROM notes
    WHERE date = ?
""", (view_date,))

# print the notes and times for the specified date
for row in cursor:
    print(f"{row[0]}: {row[1]}")

# close the connection to the database
conn.close()

