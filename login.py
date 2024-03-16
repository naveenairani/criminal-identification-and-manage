import tkinter as tk
from tkinter import messagebox
import pymysql

import subprocess

def execute_home_py(login_root):
    import subprocess
    subprocess.Popen(["python", "home.py", "--login-root", str(login_root)])  


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
            # Call the function to execute home.py
            execute_home_py(root)
            # Destroy the login window
            root.destroy()

        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    except pymysql.Error as err:
        messagebox.showerror("Error", "Database connection error: {}".format(err))

# Add the function to execute home.py
 # Replace "python" with the appropriate command to execute Python scripts on your system

def open_warning_page(message):
    warning_window = tk.Toplevel(root)
    warning_window.title("Warning")

    warning_label = tk.Label(warning_window, text=message)
    warning_label.pack()

def open_warning_page(message):
    warning_window = tk.Toplevel(root)
    warning_window.title("Warning")

    warning_label = tk.Label(warning_window, text=message)
    warning_label.pack()

def open_warning_page(message):
    warning_window = tk.Toplevel()
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
        admin_code = admin_code_entry.get()  # Get the admin code

        # Validate admin code
        if not admin_code:
            open_warning_page("Please enter the admin code or user credentials!.")
            return

        # Validate the admin code value
        if admin_code != "admin123":  # Change "admin123" to your desired admin code
            open_warning_page("Invalid Admin Code")
            return

        # Check if any field is empty
        if not all([name, dob, email, username, password]):
            open_warning_page("Please fill in all fields.")
            return

        # Connect to MySQL database
        try:
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="@Naveen69",
                database="criminaldb"
            )
            cursor = conn.cursor()

            # Check if username already exists
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            if cursor.fetchone():
                open_warning_page("Username already exists. Please choose a different username.")
                return

            # Insert new user into the database
            query = "INSERT INTO users (name, dob, email, username, password) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (name, dob, email, username, password))
            conn.commit()
            messagebox.showinfo("Registration Successful", "You have been successfully registered!")

        except pymysql.Error as err:
            messagebox.showerror("Error", "Database connection error: {}".format(err))

    # Create registration window
    registration_window = tk.Toplevel(root)
    registration_window.title("Registration")

    # Create labels and entry widgets for registration
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

    # Create register button
    register_button = tk.Button(registration_window, text="Register", command=register)
    register_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="we")

# Main window (login window)
root = tk.Tk()
root.geometry("1500x900+200+100")
root.title("Login")

# Calculate the center coordinates of the window
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
position_right = int(root.winfo_screenwidth()/2 - window_width/2)
position_down = int(root.winfo_screenheight()/2 - window_height/2)

# Set the window to be centered on the screen
root.geometry("+{}+{}".format(position_right, position_down))

# Create a frame for the login section
login_frame = tk.Frame(root, bd=3,bg="#F5F4F4", relief=tk.RAISED, width=420, height=220)  # Adjust width and height as needed
login_frame.place(relx=0.5, rely=0.4, anchor="center")

# Create login labels and entry widgets inside the login frame
username_label = tk.Label(login_frame, text="Username:")
username_label.place(relx=0.3, rely=0.3, anchor="center")
username_entry = tk.Entry(login_frame)
username_entry.place(relx=0.62, rely=0.3, anchor="center")

password_label = tk.Label(login_frame, text="Password  :")
password_label.place(relx=0.3, rely=0.45, anchor="center")
password_entry = tk.Entry(login_frame, show="*")
password_entry.place(relx=0.62, rely=0.45, anchor="center")

# Create login button inside the login frame
login_button = tk.Button(login_frame, text="Login", command=lambda: login(username_entry.get(), password_entry.get()),
                         padx=10, pady=5, bg="blue", fg="#00C1FF", width=20)  # Adjust the width as needed
login_button.place(relx=0.5, rely=0.65, anchor="center")

# Create registration button inside the login frame
register_button = tk.Button(login_frame, text="Register", command=register_user, padx=10, pady=5, bg="green", fg="#00DF39", width=20)  # Adjust the width as needed
register_button.place(relx=0.5, rely=0.85, anchor="center")

# Configure login frame properties
login_frame.configure(bg="white")
root.mainloop()