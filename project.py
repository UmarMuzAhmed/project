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

    def setup_tabs(self):
        self.tab_control = ttk.Notebook(self.root)
        self.tabs = {}
        tab_names = ["Users", "Songs", "Artists", "Genres", "Albums", "Favorites", "Queries"]

        for i, name in enumerate(tab_names):
            frame = tk.Frame(self.tab_control)
            self.tabs[name] = frame
            self.tab_control.add(frame, text=name)
            self.set_background_image(frame, f"{i+1}.jpg")

        self.tab_control.pack(expand=1, fill="both")

        self.setup_users_tab()
        self.setup_songs_tab()
        self.setup_artists_tab()
        self.setup_genres_tab()
        self.setup_albums_tab()
        self.setup_favorites_tab()
        self.setup_queries_tab()

    def set_background_image(self, frame, image_path):
        image = Image.open(image_path).resize((1200, 850))
        bg_photo = ImageTk.PhotoImage(image)
        bg_label = tk.Label(frame, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def labeled_entry(self, parent, label_text, x, y, width=30):
        label = tk.Label(parent, text=label_text, font=("Arial", 12), bg="#dff0f7")
        label.place(x=x, y=y)
        entry = tk.Entry(parent, width=width, font=("Arial", 12))
        entry.place(x=x+180, y=y)
        return entry

    def colored_button(self, parent, text, command, x, y):
        button = tk.Button(parent, text=text, command=command, font=("Helvetica", 11, "bold"),
                           bg="#004080", fg="white", activebackground="#0059b3",
                           bd=0, relief="raised", padx=10, pady=5)
        button.place(x=x, y=y, width=160, height=40)
        return button

    def setup_users_tab(self):
        tab = self.tabs["Users"]
        self.user_id = self.labeled_entry(tab, "User ID", 50, 50)
        self.user_name = self.labeled_entry(tab, "Username", 50, 90)
        self.user_fname = self.labeled_entry(tab, "First Name", 50, 130)
        self.user_lname = self.labeled_entry(tab, "Last Name", 50, 170)
        self.user_email = self.labeled_entry(tab, "Email", 50, 210)
        self.colored_button(tab, "Add User", self.add_user, 600, 130)
        self.colored_button(tab, "View Users", self.view_users, 600, 180)
        self.user_output = tk.Text(tab, height=15, width=100)
        self.user_output.place(x=50, y=300)

    def setup_songs_tab(self):
        tab = self.tabs["Songs"]
        self.song_id = self.labeled_entry(tab, "Song ID", 50, 50)
        self.song_title = self.labeled_entry(tab, "Title", 50, 90)
        self.song_album_id = self.labeled_entry(tab, "Album ID", 50, 130)
        self.song_artist_id = self.labeled_entry(tab, "Artist ID", 50, 170)
        self.song_genre_id = self.labeled_entry(tab, "Genre ID", 50, 210)
        self.song_sales = self.labeled_entry(tab, "Sales", 50, 250)
        self.colored_button(tab, "Add Song", self.add_song, 600, 150)
        self.colored_button(tab, "View Songs", self.view_songs, 600, 200)
        self.song_output = tk.Text(tab, height=15, width=100)
        self.song_output.place(x=50, y=320)

    def setup_artists_tab(self):
        tab = self.tabs["Artists"]
        self.artist_id = self.labeled_entry(tab, "Artist ID", 50, 50)
        self.artist_name = self.labeled_entry(tab, "Name", 50, 90)
        self.artist_country = self.labeled_entry(tab, "Country", 50, 130)
        self.artist_grammys = self.labeled_entry(tab, "Grammys Won", 50, 170)
        self.artist_social = self.labeled_entry(tab, "Social Media", 50, 210)
        self.colored_button(tab, "Add Artist", self.add_artist, 600, 150)
        self.colored_button(tab, "View Artists", self.view_artists, 600, 200)
        self.artist_output = tk.Text(tab, height=15, width=100)
        self.artist_output.place(x=50, y=300)

    def setup_genres_tab(self):
        tab = self.tabs["Genres"]
        self.genre_id = self.labeled_entry(tab, "Genre ID", 50, 50)
        self.genre_name = self.labeled_entry(tab, "Genre Name", 50, 90)
        self.colored_button(tab, "Add Genre", self.add_genre, 600, 60)
        self.colored_button(tab, "View Genres", self.view_genres, 600, 110)
        self.genre_output = tk.Text(tab, height=15, width=100)
        self.genre_output.place(x=50, y=160)

    def setup_albums_tab(self):
        tab = self.tabs["Albums"]
        self.album_id = self.labeled_entry(tab, "Album ID", 50, 50)
        self.album_name = self.labeled_entry(tab, "Album Name", 50, 90)
        self.album_year = self.labeled_entry(tab, "Release Year", 50, 130)
        self.colored_button(tab, "Add Album", self.add_album, 600, 70)
        self.colored_button(tab, "View Albums", self.view_albums, 600, 120)
        self.album_output = tk.Text(tab, height=15, width=100)
        self.album_output.place(x=50, y=200)

    
if __name__ == '__main__':
    root = tk.Tk()
    app = MusicApp(root)
    root.mainloop()
