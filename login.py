import tkinter as tk
from tkinter import messagebox
import pymysql
import subprocess

def execute_home_py():
    subprocess.Popen(["python", "home.py"])

def login(username, password):
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="@Naveen69",
            database="criminaldb"
        )
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Login Successful", "Welcome, " + username)
            execute_home_py()
            root.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    except pymysql.Error as err:
        messagebox.showerror("Error", "Database connection error: {}".format(err))

def open_warning_page(message):
    warning_window = tk.Toplevel(root)
    warning_window.title("Warning")
    warning_label = tk.Label(warning_window, text=message)
    warning_label.pack()

def register_user():
    def register():
        name = name_entry.get()
        dob = dob_entry.get()
        email = email_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        admin_code = admin_code_entry.get()

        if not admin_code:
            open_warning_page("Please enter the admin code or user credentials!")
            return

        if admin_code != "admin123":
            open_warning_page("Invalid Admin Code")
            return

        if not all([name, dob, email, username, password]):
            open_warning_page("Please fill in all fields.")
            return

        try:
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="@Naveen69",
                database="criminaldb"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            if cursor.fetchone():
                open_warning_page("Username already exists. Please choose a different username.")
                return

            query = "INSERT INTO users (name, dob, email, username, password) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (name, dob, email, username, password))
            conn.commit()
            messagebox.showinfo("Registration Successful", "You have been successfully registered!")
            registration_window.destroy()

        except pymysql.Error as err:
            messagebox.showerror("Error", "Database connection error: {}".format(err))

    registration_window = tk.Toplevel(root)
    registration_window.title("Registration")

    name_label = tk.Label(registration_window, text="Name:")
    name_label.grid(row=0, column=0, padx=10, pady=5)
    name_entry = tk.Entry(registration_window)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    dob_label = tk.Label(registration_window, text="Date of Birth:")
    dob_label.grid(row=1, column=0, padx=10, pady=5)
    dob_entry = tk.Entry(registration_window)
    dob_entry.grid(row=1, column=1, padx=10, pady=5)

    email_label = tk.Label(registration_window, text="Email:")
    email_label.grid(row=2, column=0, padx=10, pady=5)
    email_entry = tk.Entry(registration_window)
    email_entry.grid(row=2, column=1, padx=10, pady=5)

    username_label = tk.Label(registration_window, text="Username:")
    username_label.grid(row=3, column=0, padx=10, pady=5)
    username_entry = tk.Entry(registration_window)
    username_entry.grid(row=3, column=1, padx=10, pady=5)

    password_label = tk.Label(registration_window, text="Password:")
    password_label.grid(row=4, column=0, padx=10, pady=5)
    password_entry = tk.Entry(registration_window, show="*")
    password_entry.grid(row=4, column=1, padx=10, pady=5)

    admin_code_label = tk.Label(registration_window, text="Admin Code:")
    admin_code_label.grid(row=5, column=0, padx=10, pady=5)
    admin_code_entry = tk.Entry(registration_window, show="*")
    admin_code_entry.grid(row=5, column=1, padx=10, pady=5)

    register_button = tk.Button(registration_window, text="Register", command=register)
    register_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="we")

root = tk.Tk()
root.geometry("1500x900+200+100")
root.title("Login")

window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
position_right = int(root.winfo_screenwidth()/2 - window_width/2)
position_down = int(root.winfo_screenheight()/2 - window_height/2)
root.geometry("+{}+{}".format(position_right, position_down))

login_frame = tk.Frame(root, bd=3, bg="#F5F4F4", relief=tk.RAISED, width=420, height=220)
login_frame.place(relx=0.5, rely=0.4, anchor="center")

username_label = tk.Label(login_frame, text="Username:")
username_label.place(relx=0.3, rely=0.3, anchor="center")
username_entry = tk.Entry(login_frame)
username_entry.place(relx=0.62, rely=0.3, anchor="center")

password_label = tk.Label(login_frame, text="Password  :")
password_label.place(relx=0.3, rely=0.45, anchor="center")
password_entry = tk.Entry(login_frame, show="*")
password_entry.place(relx=0.62, rely=0.45, anchor="center")

login_button = tk.Button(login_frame, text="Login", command=lambda: login(username_entry.get(), password_entry.get()),
                         padx=10, pady=5, bg="blue", fg="#00C1FF", width=20)
login_button.place(relx=0.5, rely=0.65, anchor="center")

register_button = tk.Button(login_frame, text="Register", command=register_user, padx=10, pady=5, bg="green", fg="#00DF39", width=20)
register_button.place(relx=0.5, rely=0.85, anchor="center")

login_frame.configure(bg="white")
root.mainloop()
