import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
import pyperclip

class VaultX:
    def __init__(self, root):
        self.root = root
        self.root.title("VaultX Password Manager")
        self.root.geometry("600x400")
        self.connection = sqlite3.connect("vaultx.db")
        self.cursor = self.connection.cursor()
        self.setup_database()
        self.show_welcome_screen()

    def setup_database(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)
        self.connection.commit()

    def show_welcome_screen(self):
        self.clear_screen()
        self.welcome_frame = tk.Frame(self.root, bg="lightblue")
        self.welcome_frame.pack(fill="both", expand=True)

        welcome_label = tk.Label(self.welcome_frame, text="VaultX", font=("Arial", 32, "bold"), bg="lightblue", fg="darkblue")
        welcome_label.pack(pady=50)

        signup_button = tk.Button(self.welcome_frame, text="Sign Up", font=("Arial", 14), command=self.show_signup_screen)
        signup_button.pack(pady=10)

        login_button = tk.Button(self.welcome_frame, text="Log In", font=("Arial", 14), command=self.show_login_screen)
        login_button.pack(pady=10)

    def show_signup_screen(self):
        self.clear_screen()
        self.signup_frame = tk.Frame(self.root, bg="lightyellow")
        self.signup_frame.pack(fill="both", expand=True)

        tk.Label(self.signup_frame, text="Sign Up", font=("Arial", 20, "bold"), bg="lightyellow").pack(pady=10)

        tk.Label(self.signup_frame, text="Username:", bg="lightyellow").pack(pady=5)
        self.signup_username_entry = tk.Entry(self.signup_frame)
        self.signup_username_entry.pack(pady=5)

        tk.Label(self.signup_frame, text="Password:", bg="lightyellow").pack(pady=5)
        self.signup_password_entry = tk.Entry(self.signup_frame, show="*")
        self.signup_password_entry.pack(pady=5)

        signup_button = tk.Button(self.signup_frame, text="Create Account", command=self.signup)
        signup_button.pack(pady=10)

        back_button = tk.Button(self.signup_frame, text="Back", command=self.show_welcome_screen)
        back_button.pack(pady=5)

    def show_login_screen(self):
        self.clear_screen()
        self.login_frame = tk.Frame(self.root, bg="lightgreen")
        self.login_frame.pack(fill="both", expand=True)

        tk.Label(self.login_frame, text="Log In", font=("Arial", 20, "bold"), bg="lightgreen").pack(pady=10)

        tk.Label(self.login_frame, text="Username:", bg="lightgreen").pack(pady=5)
        self.login_username_entry = tk.Entry(self.login_frame)
        self.login_username_entry.pack(pady=5)

        tk.Label(self.login_frame, text="Password:", bg="lightgreen").pack(pady=5)
        self.login_password_entry = tk.Entry(self.login_frame, show="*")
        self.login_password_entry.pack(pady=5)

        login_button = tk.Button(self.login_frame, text="Log In", command=self.login)
        login_button.pack(pady=10)

        back_button = tk.Button(self.login_frame, text="Back", command=self.show_welcome_screen)
        back_button.pack(pady=5)

    def signup(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        if username and password:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            try:
                self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
                self.connection.commit()
                messagebox.showinfo("Success", "Account created successfully!")
                self.show_login_screen()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def login(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()
        if username and password:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            self.cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, hashed_password))
            user = self.cursor.fetchone()
            if user:
                self.user_id = user[0]
                self.show_password_manager()
            else:
                messagebox.showerror("Error", "Invalid credentials.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def show_password_manager(self):
        self.clear_screen()
        self.manager_frame = tk.Frame(self.root, bg="white")
        self.manager_frame.pack(fill="both", expand=True)

        tk.Label(self.manager_frame, text="Password Manager", font=("Arial", 20, "bold"), bg="white").pack(pady=10)

        add_frame = ttk.LabelFrame(self.manager_frame, text="Add Password", labelanchor="n")
        add_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(add_frame, text="Website:").grid(row=0, column=0, padx=5, pady=5)
        self.website_entry = tk.Entry(add_frame)
        self.website_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_frame, text="Username:").grid(row=1, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(add_frame)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(add_frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(add_frame, text="Add", command=self.add_password).grid(row=3, columnspan=2, pady=10)

        view_frame = ttk.LabelFrame(self.manager_frame, text="View Passwords", labelanchor="n")
        view_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(view_frame, text="Website:").grid(row=0, column=0, padx=5, pady=5)
        self.view_website_entry = tk.Entry(view_frame)
        self.view_website_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(view_frame, text="Username:").grid(row=1, column=0, padx=5, pady=5)
        self.view_username_entry = tk.Entry(view_frame)
        self.view_username_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(view_frame, text="View Password", command=self.view_password).grid(row=2, columnspan=2, pady=10)

    def add_password(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        if website and username and password:
            self.cursor.execute("INSERT INTO passwords (website, username, password, user_id) VALUES (?, ?, ?, ?)",
                                (website, username, password, self.user_id))
            self.connection.commit()
            messagebox.showinfo("Success", "Password added successfully!")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def view_password(self):
        website = self.view_website_entry.get()
        username = self.view_username_entry.get()
        if website and username:
            self.cursor.execute("SELECT password FROM passwords WHERE website=? AND username=? AND user_id=?",
                                (website, username, self.user_id))
            result = self.cursor.fetchone()
            if result:
                password = result[0]
                password_window = tk.Toplevel(self.root)
                password_window.title("Password Viewer")
                password_window.geometry("300x200")

                tk.Label(password_window, text="Password:").pack(pady=10)
                password_entry = tk.Entry(password_window, show="*")
                password_entry.insert(0, password)
                password_entry.pack(pady=5)

                def toggle_password_visibility():
                    if password_entry.cget("show") == "*":
                        password_entry.config(show="")
                    else:
                        password_entry.config(show="*")

                eye_button = tk.Button(password_window, text="👁", command=toggle_password_visibility)
                eye_button.pack(pady=5)

                copy_button = tk.Button(password_window, text="Copy", command=lambda: pyperclip.copy(password))
                copy_button.pack(pady=5)
            else:
                messagebox.showerror("Error", "No password found for this website and username.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
if __name__ == "__main__":
    root = tk.Tk()
    app = VaultX(root)
    root.mainloop()
