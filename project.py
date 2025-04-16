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

    def setup_favorites_tab(self):
        tab = self.tabs["Favorites"]
        self.favorite_id = self.labeled_entry(tab, "Favorite ID", 50, 50)
        self.fav_user_id = self.labeled_entry(tab, "User ID", 50, 90)
        self.fav_song_id = self.labeled_entry(tab, "Song ID", 50, 130)
        self.colored_button(tab, "Add Favorite", self.add_favorite, 600, 80)
        self.colored_button(tab, "View Favorites", self.view_favorites, 600, 130)
        self.favorite_output = tk.Text(tab, height=15, width=100)
        self.favorite_output.place(x=50, y=200)

    def setup_queries_tab(self):
        tab = self.tabs["Queries"]
        self.colored_button(tab, "Users and Favorites", self.query_users_favorites, 50, 50)
        self.colored_button(tab, "Artists and Songs", self.query_artists_songs, 250, 50)
        self.colored_button(tab, "Songs with Details", self.query_song_details, 450, 50)
        self.query_output = tk.Text(tab, height=30, width=130)
        self.query_output.place(x=50, y=100)

    def add_user(self):
        try:
            self.cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)",
                                (self.user_id.get(), self.user_name.get(), self.user_fname.get(),
                                 self.user_lname.get(), self.user_email.get()))
            self.conn.commit()
            self.clear_entries([self.user_id, self.user_name, self.user_fname, self.user_lname, self.user_email])
            messagebox.showinfo("Success", "User added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_users(self):
        self.cursor.execute("SELECT * FROM users")
        rows = self.cursor.fetchall()
        self.user_output.delete("1.0", tk.END)
        for row in rows:
            self.user_output.insert(tk.END, f"{row}\n")

    def add_song(self):
        try:
            self.cursor.execute("INSERT INTO songs VALUES (?, ?, ?, ?, ?, ?)",
                                (self.song_id.get(), self.song_title.get(), self.song_album_id.get(),
                                 self.song_artist_id.get(), self.song_genre_id.get(), self.song_sales.get()))
            self.conn.commit()
            self.clear_entries([self.song_id, self.song_title, self.song_album_id,
                                self.song_artist_id, self.song_genre_id, self.song_sales])
            messagebox.showinfo("Success", "Song added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_songs(self):
        self.cursor.execute("SELECT * FROM songs")
        rows = self.cursor.fetchall()
        self.song_output.delete("1.0", tk.END)
        for row in rows:
            self.song_output.insert(tk.END, f"{row}\n")

    def add_artist(self):
        try:
            self.cursor.execute("INSERT INTO artists VALUES (?, ?, ?, ?, ?)",
                                (self.artist_id.get(), self.artist_name.get(), self.artist_country.get(),
                                 self.artist_grammys.get(), self.artist_social.get()))
            self.conn.commit()
            self.clear_entries([self.artist_id, self.artist_name, self.artist_country,
                                self.artist_grammys, self.artist_social])
            messagebox.showinfo("Success", "Artist added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_artists(self):
        self.cursor.execute("SELECT * FROM artists")
        rows = self.cursor.fetchall()
        self.artist_output.delete("1.0", tk.END)
        for row in rows:
            self.artist_output.insert(tk.END, f"{row}\n")

    def add_genre(self):
        try:
            self.cursor.execute("INSERT INTO genres VALUES (?, ?)",
                                (self.genre_id.get(), self.genre_name.get()))
            self.conn.commit()
            self.clear_entries([self.genre_id, self.genre_name])
            messagebox.showinfo("Success", "Genre added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_genres(self):
        self.cursor.execute("SELECT * FROM genres")
        rows = self.cursor.fetchall()
        self.genre_output.delete("1.0", tk.END)
        for row in rows:
            self.genre_output.insert(tk.END, f"{row}\n")

    def add_album(self):
        try:
            self.cursor.execute("INSERT INTO albums VALUES (?, ?, ?)",
                                (self.album_id.get(), self.album_name.get(), self.album_year.get()))
            self.conn.commit()
            self.clear_entries([self.album_id, self.album_name, self.album_year])
            messagebox.showinfo("Success", "Album added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_albums(self):
        self.cursor.execute("SELECT * FROM albums")
        rows = self.cursor.fetchall()
        self.album_output.delete("1.0", tk.END)
        for row in rows:
            self.album_output.insert(tk.END, f"{row}\n")

    def add_favorite(self):
        try:
            self.cursor.execute("INSERT INTO favorites VALUES (?, ?, ?)",
                                (self.favorite_id.get(), self.fav_user_id.get(), self.fav_song_id.get()))
            self.conn.commit()
            self.clear_entries([self.favorite_id, self.fav_user_id, self.fav_song_id])
            messagebox.showinfo("Success", "Favorite added successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_favorites(self):
        self.cursor.execute("SELECT * FROM favorites")
        rows = self.cursor.fetchall()
        self.favorite_output.delete("1.0", tk.END)
        for row in rows:
            self.favorite_output.insert(tk.END, f"{row}\n")

    def query_users_favorites(self):
        try:
            self.cursor.execute('''SELECT u.username, s.title FROM users u
                                   JOIN favorites f ON u.user_id = f.user_id
                                   JOIN songs s ON f.song_id = s.song_id''')
            rows = self.cursor.fetchall()
            self.query_output.delete("1.0", tk.END)
            for row in rows:
                self.query_output.insert(tk.END, f"User: {row[0]} | Song: {row[1]}\n")
        except Exception as e:
            messagebox.showerror("Query Error", str(e))

    def query_artists_songs(self):
        try:
            self.cursor.execute('''SELECT a.artist_name, s.title FROM artists a
                                   JOIN songs s ON a.artist_id = s.artist_id''')
            rows = self.cursor.fetchall()
            self.query_output.delete("1.0", tk.END)
            for row in rows:
                self.query_output.insert(tk.END, f"Artist: {row[0]} | Song: {row[1]}\n")
        except Exception as e:
            messagebox.showerror("Query Error", str(e))

    def query_song_details(self):
        try:
            self.cursor.execute('''SELECT s.title, g.genre_name, a.artist_name FROM songs s
                                   JOIN genres g ON s.genre_id = g.genre_id
                                   JOIN artists a ON s.artist_id = a.artist_id''')
            rows = self.cursor.fetchall()
            self.query_output.delete("1.0", tk.END)
            for row in rows:
                self.query_output.insert(tk.END, f"Song: {row[0]} | Genre: {row[1]} | Artist: {row[2]}\n")
        except Exception as e:
            messagebox.showerror("Query Error", str(e))

if __name__ == '__main__':
    root = tk.Tk()
    app = MusicApp(root)
    root.mainloop()
