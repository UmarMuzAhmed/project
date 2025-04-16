import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

class MusicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Database GUI")
        self.root.geometry("1200x850")

        self.db_connection()
        self.create_tables()
        self.setup_tabs()

    def db_connection(self):
        self.conn = sqlite3.connect("music.db")
        self.cursor = self.conn.cursor()

    def create_tables(self):
        try:
            self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                fname TEXT NOT NULL,
                lname TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS artists (
                artist_id INTEGER PRIMARY KEY,
                artist_name TEXT NOT NULL,
                country_of_origin TEXT,
                grammys_won INTEGER DEFAULT 0,
                social_media TEXT
            );
            CREATE TABLE IF NOT EXISTS genres (
                genre_id INTEGER PRIMARY KEY,
                genre_name TEXT NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS albums (
                album_id INTEGER PRIMARY KEY,
                album_name TEXT NOT NULL,
                release_year INTEGER
            );
            CREATE TABLE IF NOT EXISTS songs (
                song_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                album_id INTEGER,
                artist_id INTEGER,
                genre_id INTEGER,
                sales INTEGER DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS favorites (
                favorite_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                song_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (song_id) REFERENCES songs(song_id)
            );
            """)
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

if __name__ == '__main__':
    root = tk.Tk()
    app = MusicApp(root)
    root.mainloop()
