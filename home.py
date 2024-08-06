#home.py
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import threading
import shutil
from facerec import *
from register import *
from dbHandler import *
import sys
active_page = 0
thread_event = None
left_frame = None
right_frame = None
heading = None
webcam = None
img_label = None
img_read = None
img_list = []
slide_caption = None
slide_control_panel = None
current_slide = -1



root = tk.Tk()
root.geometry("1500x900+200+100")  
root.attributes('-fullscreen', True)  

pages = []
for i in range(5): 
    pages.append(tk.Frame(root, bg="#202d42"))
    pages[i].pack(side="top", fill="both", expand=True)
    pages[i].place(x=0, y=0, relwidth=1, relheight=1)
    
thread_event = threading.Event()
webcam = cv2.VideoCapture(0) 


def close_login_root():
    login_root_id = int(sys.argv[sys.argv.index("--login-root") + 1])
    login_root = tk.Tk()  # Create a Tk object
    login_root.withdraw()  # Withdraw the Tkinter root window of login.py
    login_root.wm_attributes("-topmost", True)  # Ensure the window is on top
    login_root.overrideredirect(True)  # Remove the window decorations
    login_root.after(0, lambda: login_root.destroy())

# Your home.py code here

# Call the function to close the root window of login.py




def goBack():
    global active_page, thread_event, webcam
    active_page -= 1 
    if active_page == 3 and webcam is not None:
        webcam.release()

    if active_page == 2:
        for widget in right_frame.winfo_children():
            widget.destroy()

    if active_page == 4:
        for widget in content.winfo_children():
            widget.destroy()

    pages[active_page].lift()




def basicPageSetup(pageNo):
    global left_frame, right_frame, heading
    back_img = tk.PhotoImage(file="back.png")
    back_button = tk.Button(pages[pageNo], image=back_img, bg="#202d42", bd=0, highlightthickness=0,activebackground="#202d42", command=goBack)
    back_button.image = back_img
    back_button.place(x=10, y=10)
    heading = tk.Label(pages[pageNo], fg="white", bg="#202d42", font="Arial 20 bold", pady=17)
    heading.pack()
    content = tk.Frame(pages[pageNo], bg="#202d42", pady=20)
    content.pack(expand="true", fill="both")
    left_frame = tk.Frame(content, bg="#202d42")
    left_frame.grid(row=0, column=0, sticky="nsew")
    right_frame = tk.LabelFrame(content, text="Detected Criminals", bg="#202d42", font="Arial 20 bold", bd=4,foreground="#2ea3ef", labelanchor="n")
    right_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
    content.grid_columnconfigure(0, weight=1, uniform="group1")
    content.grid_columnconfigure(1, weight=1, uniform="group1")
    content.grid_rowconfigure(0, weight=1)


def calculate_img_size(frame):
    img_size = (frame.shape[0] + frame.shape[1]) // 2  # Example calculation
    if img_size <= 0:
        print(f"Invalid img_size value detected: {img_size}. Setting to default value of 100.")
        img_size = 100
    return img_size


def showImage(frame, img_size):
    print(f"frame shape: {frame.shape if frame is not None else 'None'}, img_size: {img_size}")
    if frame is None or frame.size == 0:
        raise ValueError("Invalid frame size")
    if img_size <= 0:
        raise ValueError("img_size must be a positive integer")
    img = cv2.resize(frame, (img_size, img_size))
    # Further processing

    global img_label, left_frame
    img = cv2.resize(frame, (img_size, img_size))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    if (img_label == None):
        img_label = tk.Label(left_frame, image=img, bg="#202d42")
        img_label.image = img
        img_label.pack(padx=20)
    else:
        img_label.configure(image=img)
        img_label.image = img


def getNewSlide(control):
    global img_list, current_slide
    if len(img_list) > 1:
        if control == "prev":
            current_slide = (current_slide - 1) % len(img_list)
        else:
            current_slide = (current_slide + 1) % len(img_list)
        img_size = left_frame.winfo_height() - 200
        showImage(img_list[current_slide], img_size)
        slide_caption.configure(text="Image {} of {}".format(current_slide + 1, len(img_list)))


def selectMultiImage(opt_menu, menu_var):
    global img_list, current_slide, slide_caption, slide_control_panel
    filetype = [("images", "*.jpg *.jpeg *.png")]
    path_list = filedialog.askopenfilenames(title="Choose least 5 images", filetypes=filetype)
    if len(path_list) < 5:
        messagebox.showerror("Error", "Choose least 5 images.")
    else:
        img_list = []
        current_slide = -1
        # Resetting slide control panel
        if slide_control_panel is not None:
            slide_control_panel.destroy()
        # Creating Image list
        for path in path_list:
            img_list.append(cv2.imread(path))
        # Creating choices for profile pic menu
        menu_var.set("")
        opt_menu['menu'].delete(0, 'end')
        for i in range(len(img_list)):
            ch = "Image " + str(i + 1)
            opt_menu['menu'].add_command(label=ch, command=tk._setit(menu_var, ch))
            menu_var.set("Image 1")
        # Creating slideshow of images
        img_size = left_frame.winfo_height() - 200
        current_slide += 1
        showImage(img_list[current_slide], img_size)

        slide_control_panel = tk.Frame(left_frame, bg="#202d42", pady=10)
        slide_control_panel.pack()

        back_img = tk.PhotoImage(file="previous.png")
        next_img = tk.PhotoImage(file="next.png")

        prev_slide = tk.Button(slide_control_panel, image=back_img, bg="#202d42", bd=0, highlightthickness=0,activebackground="#202d42", command=lambda: getNewSlide("prev"))
        prev_slide.image = back_img
        prev_slide.grid(row=0, column=0, padx=60)

        slide_caption = tk.Label(slide_control_panel, text="Image 1 of {}".format(len(img_list)), fg="#ff9800",bg="#202d42", font="Arial 15 bold")
        slide_caption.grid(row=0, column=1)

        next_slide = tk.Button(slide_control_panel, image=next_img, bg="#202d42", bd=0, highlightthickness=0,activebackground="#202d42", command=lambda: getNewSlide("next"))
        next_slide.image = next_img
        next_slide.grid(row=0, column=2, padx=60)


def register(entries, required, menu_var):
    global img_list

    # Checking if no image selected
    if len(img_list) == 0:
        messagebox.showerror("Error", "Select Images first.")
        return

    # Fetching data from entries
    entry_data = {}
    for i, entry in enumerate(entries):
        val = entry[1].get()

        if len(val) == 0 and required[i] == 1:
            messagebox.showerror("Field Error", "Required field missing :\n\n%s" % (entry[0]))
            return
        else:
            entry_data[entry[0]] = val.lower()

    # Setting Directory
    path = os.path.join('face_samples', "temp_criminal")
    if not os.path.isdir(path):
        os.mkdir(path)

    no_face = []
    for i, img in enumerate(img_list):
        # Storing Images in directory
        id = registerCriminal(img, path, i + 1)
        if (id != None):
            no_face.append(id)

    # check if any image doesn't contain face
    if len(no_face) > 0:
        no_face_st = ""
        for i in no_face:
            no_face_st += "Image " + str(i) + ", "
        messagebox.showerror("Registration Error", "Registration failed!\n\nFollowing images doesn't contain","face or Face is too small:\n\n%s" % (no_face_st))
        shutil.rmtree(path, ignore_errors=True)
    else:
        # Storing data in database
        rowId = insertData(entry_data)

        if (rowId > 0):
            messagebox.showinfo("Success", "Criminal Registered Successfully.")
            shutil.move(path, os.path.join('face_samples', entry_data["Name"]))

            # save profile pic
            profile_img_num = int(menu_var.get().split(' ')[1]) - 1
            if not os.path.isdir("profile_pics"):
                os.mkdir("profile_pics")
            cv2.imwrite("profile_pics/criminal %d.png" % rowId, img_list[profile_img_num])

            goBack()
        else:
            shutil.rmtree(path, ignore_errors=True)
            messagebox.showerror("Database Error", "Some error occurred while storing data.")


## update scrollregion when all widgets are in canvas
def on_configure(event, canvas, win):
    canvas.configure(scrollregion=canvas.bbox('all'))
    canvas.itemconfig(win, width=event.width)


## Register Page ##
def getPage1():
    global active_page, left_frame, right_frame, heading, img_label
    active_page = 1
    img_label = None
    opt_menu = None
    menu_var = tk.StringVar(root)
    pages[1].lift()

    basicPageSetup(1)
    heading.configure(text="Register Criminal")
    right_frame.configure(text="Enter Details")

    btn_grid = tk.Frame(left_frame, bg="#202d42")
    btn_grid.pack()

    tk.Button(btn_grid, text="Select Images", command=lambda: selectMultiImage(opt_menu, menu_var),font="Arial 15 bold", bg="#2196f3",fg="white", pady=10, bd=0, highlightthickness=0, activebackground="#091428",activeforeground="white").grid(row=0, column=0, padx=25, pady=25)

    # Creating Scrollable Frame
    canvas = tk.Canvas(right_frame, bg="#202d42", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand="true", padx=30)
    scrollbar = tk.Scrollbar(right_frame, command=canvas.yview, width=20, troughcolor="#202d42", bd=0,activebackground="#00bcd4", bg="#2196f3", relief="raised")
    scrollbar.pack(side="left", fill="y")

    scroll_frame = tk.Frame(canvas, bg="#202d42", pady=20)
    scroll_win = canvas.create_window((0, 0), window=scroll_frame, anchor='nw')

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda event, win=scroll_win: on_configure(event, canvas, win))

    tk.Label(scroll_frame, text="* Required Fields", bg="#202d42", fg="yellow", font="Arial 13 bold").pack()
    # Adding Input Fields
    input_fields = ("Name", "Father's Name", "Mother's Name", "Gender", "DOB(yyyy-mm-dd)", "Blood Group","Identification Mark", "Nationality", "Religion", "Crimes Done", "Profile Image")
    ip_len = len(input_fields)
    required = [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0]

    entries = []
    for i, field in enumerate(input_fields):
        row = tk.Frame(scroll_frame, bg="#202d42")
        row.pack(side="top", fill="x", pady=15)

        label = tk.Text(row, width=20, height=1, bg="#202d42", fg="#ffffff", font="Arial 13", highlightthickness=0,
                        bd=0)
        label.insert("insert", field)
        label.pack(side="left")

        if (required[i] == 1):
            label.tag_configure("star", foreground="yellow", font="Arial 13 bold")
            label.insert("end", "  *", "star")
        label.configure(state="disabled")

        if (i != ip_len - 1):
            ent = tk.Entry(row, font="Arial 13", selectbackground="#90ceff")
            ent.pack(side="right", expand="true", fill="x", padx=10)
            entries.append((field, ent))
        else:
            menu_var.set("Image 1")
            choices = ["Image 1"]
            opt_menu = tk.OptionMenu(row, menu_var, *choices)
            opt_menu.pack(side="right", fill="x", expand="true", padx=10)
            opt_menu.configure(font="Arial 13", bg="#2196f3", fg="white", bd=0, highlightthickness=0,
                               activebackground="#90ceff")
            menu = opt_menu.nametowidget(opt_menu.menuname)
            menu.configure(font="Arial 13", bg="white", activebackground="#90ceff", bd=0)

    tk.Button(scroll_frame, text="Register", command=lambda: register(entries, required, menu_var),
              font="Arial 15 bold",
              bg="#2196f3", fg="white", pady=10, padx=30, bd=0, highlightthickness=0, activebackground="#091428",
              activeforeground="white").pack(pady=25)


def showCriminalProfile(name):
    top = tk.Toplevel(bg="#202d42")
    top.title("Criminal Profile")
    top.geometry("1500x900+%d+%d" % (root.winfo_x() + 10, root.winfo_y() + 10))

    tk.Label(top, text="Criminal Profile", fg="white", bg="#202d42", font="Arial 20 bold", pady=10).pack()
    
    (id, crim_data) = retrieveData(name)

    if id is not None:
        path = os.path.join("profile_pics", "criminal %d.png" % id)
        profile_img = cv2.imread(path)

        profile_img = cv2.resize(profile_img, (500, 500))
        img = cv2.cvtColor(profile_img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        img_label = tk.Label(top, image=img, bg="#202d42")
        img_label.image = img
        img_label.pack()

        info_frame = tk.Frame(top, bg="#202d42")
        info_frame.pack()

        for i, (field, value) in enumerate(crim_data.items()):
            tk.Label(info_frame, text=field.capitalize(), pady=15, fg="yellow", font="Arial 15 bold", bg="#202d42").grid(row=i,
                                                                                                              column=0,
                                                                                                              sticky='w')
            tk.Label(info_frame, text=":", fg="yellow", padx=50, font="Arial 15 bold", bg="#202d42").grid(row=i,
                                                                                                          column=1)
            val = "---" if (value == "") else value
            tk.Label(info_frame, text=val.capitalize(), fg="white", font="Arial 15", bg="#202d42").grid(row=i, column=2,
                                                                                                        sticky='w')
    else:
        tk.Label(top, text="Criminal ID not found!", fg="red", font="Arial 15 bold", bg="#202d42").pack()



def startRecognition():
    global img_read, img_label

    if (img_label == None):
        messagebox.showerror("Error", "No image selected. ")
        return

    crims_found_labels = []
    for wid in right_frame.winfo_children():
        wid.destroy()

    frame = cv2.flip(img_read, 1, 0)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face_coords = detect_faces(gray_frame)

    if (len(face_coords) == 0):
        messagebox.showerror("Error", "Image doesn't contain any face or face is too small.")
    else:
        (model, names) = train_model()
        print('Training Successful. Detecting Faces')
        (frame, recognized) = recognize_face(model, frame, gray_frame, face_coords, names)

        img_size = left_frame.winfo_height() - 40
        frame = cv2.flip(frame, 1, 0)
        showImage(frame, img_size)

        if (len(recognized) == 0):
            messagebox.showerror("Error", "No criminal recognized.")
            return

        for i, crim in enumerate(recognized):
            crims_found_labels.append(tk.Label(right_frame, text=crim[0], bg="orange",font="Arial 15 bold", pady=20))
            crims_found_labels[i].pack(fill="x", padx=20, pady=10)
            crims_found_labels[i].bind("<Button-1>", lambda e, name=crim[0]: showCriminalProfile(name))


def selectImage():
    global left_frame, img_label, img_read
    for wid in right_frame.winfo_children():
        wid.destroy()

    filetype = [("images", "*.jpg *.jpeg *.png")]
    path = filedialog.askopenfilename(title="Choose a image", filetypes=filetype)

    if (len(path) > 0):
        img_read = cv2.imread(path)

        img_size = left_frame.winfo_height() - 40
        showImage(img_read, img_size)


## Detection Page ##
def getPage2():
    global active_page, left_frame, right_frame, img_label, heading
    img_label = None
    active_page = 2
    pages[2].lift()

    basicPageSetup(2)
    heading.configure(text="Detect Criminal")
    right_frame.configure(text="Detected Criminals")

    btn_grid = tk.Frame(left_frame, bg="#202d42")
    btn_grid.pack()

    tk.Button(btn_grid, text="Select Image", command=selectImage, font="Arial 15 bold", padx=20, bg="#2196f3",fg="white", pady=10, bd=0, highlightthickness=0, activebackground="#091428",activeforeground="white").grid(row=0, column=0, padx=25, pady=25)
    tk.Button(btn_grid, text="Recognize", command=startRecognition, font="Arial 15 bold", padx=20, bg="#2196f3",fg="white", pady=10, bd=0, highlightthickness=0, activebackground="#091428",activeforeground="white").grid(row=0, column=1, padx=25, pady=25)


def videoLoop(model, names):
    global thread_event, left_frame, webcam, img_label
    webcam = cv2.VideoCapture(0)
    old_recognized = []
    crims_found_labels = []
    img_label = None

    try:
        while not thread_event.is_set():
            # Loop until the camera is working
            while (True):
                # Put the image from the webcam into 'frame'
                (return_val, frame) = webcam.read()
                if (return_val == True):
                    break
                else:
                    print("Failed to open webcam. Trying again...")

            # Flip the image (optional)
            frame = cv2.flip(frame, 1, 0)
            # Convert frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect Faces
            face_coords = detect_faces(gray_frame)
            (frame, recognized) = recognize_face(model, frame, gray_frame, face_coords, names)

            # Recognize Faces
            recog_names = [item[0] for item in recognized]
            if (recog_names != old_recognized):
                for wid in right_frame.winfo_children():
                    wid.destroy()
                del (crims_found_labels[:])

                for i, crim in enumerate(recognized):
                    crims_found_labels.append(tk.Label(right_frame, text=crim[0], bg="orange",font="Arial 15 bold", pady=20))
                    crims_found_labels[i].pack(fill="x", padx=20, pady=10)
                    crims_found_labels[i].bind("<Button-1>", lambda e, name=crim[0]: showCriminalProfile(name))

                old_recognized = recog_names

            # Display Video stream
            img_size = min(left_frame.winfo_width(), left_frame.winfo_height()) - 20

            showImage(frame, img_size)

    except RuntimeError:
        print("[INFO]Caught Runtime Error")
    except tk.TclError:
        print("[INFO]Caught Tcl Error")



## Import the functions from dbHandler
from dbHandler import fetchAllData, updateData, deleteData



def deleteRecord(id, window):
    try:
        # Convert the ID to an integer
        id = int(id)
        if deleteData(id):
            messagebox.showinfo("Success", "Criminal record deleted successfully.", parent=window)
        else:
            # If deleteData function returns False, it means record deletion failed
            messagebox.showerror("Error", "Failed to delete criminal record.", parent=window)
    except ValueError:
        messagebox.showerror("Error", "Invalid ID. Please enter a valid ID.", parent=window)




def updateRecord(id, entries, parent_window):
    print("Updating record with ID:", id)  # Add this line for debugging
    print("Entries:", entries)  # Add this line for debugging
    try:
        if not any(entries.values()):  # Check if any data is provided
            messagebox.showwarning("Warning", "No data provided for update.", parent=parent_window)
        else:
            # Call the updateData function from dbHandler
            updateData(id, entries)
            messagebox.showinfo("Success", "Criminal record updated successfully.", parent=parent_window)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}", parent=parent_window)



## video surveillance Page ##
def getPage3():
    global active_page, left_frame, right_frame, thread_event, webcam, heading
    active_page = 3
    pages[3].lift()
    basicPageSetup(3)
    heading.configure(text="Video Surveillance")
    right_frame.configure(text="Detected Criminals")
    left_frame.configure(pady=40)
    (model, names) = train_model()
    print('Training Successful. Detecting Faces')
    thread_event = threading.Event()
    thread = threading.Thread(target=videoLoop, args=(model, names))
    thread.start()

def getPage4(window):
    global selected_id
    selected_id = None
    basicPageSetup(4)
    heading.configure(text="Manage Criminals", fg="white", bg="#202d42", font=("Arial", 20, "bold"))
    right_frame.configure(text="Detected Criminals", bg="#202d42", fg="white", font=("Arial", 14, "bold"))
    left_frame.configure(pady=40, bg="#202d42")
    content = tk.Frame(window, bg="#202d42")
    content.pack(side="left", padx=20, pady=20, fill="both", expand=True)
    form_frame = tk.Frame(content, bg="#202d42")
    form_frame.pack(side="left", padx=20, pady=20, fill="both", expand=True)
    record_frame = tk.Frame(content, bg="#202d42")
    record_frame.pack(side="right", padx=20, pady=20, fill="both", expand=True)
    form_title_label = tk.Label(form_frame, text="Criminal Information", bg="#202d42", fg="white", font=("Arial", 16, "bold"))
    form_title_label.pack(pady=(10, 10))
    form_fields = ["Name", "Father's Name", "Mother's Name", "Gender", "DOB", "Blood Group", "Identification Mark", "Nationality", "Religion", "Crimes Done"]
    form_entries = {}
    for field in form_fields:
        field_label = tk.Label(form_frame, text=field, bg="#202d42", fg="white", font=("Arial", 12))
        field_label.pack(anchor="w", pady=(5, 0))
        entry = tk.Entry(form_frame, font=("Arial", 12))
        entry.pack(fill="x", padx=5)
        form_entries[field] = entry
    id_label = tk.Label(form_frame, text="Enter ID:", bg="#202d42", fg="white", font=("Arial", 12))
    id_label.pack(anchor="w", pady=(10, 0))
    id_entry = tk.Entry(form_frame, font=("Arial", 12))
    id_entry.pack(fill="x", padx=5)
    update_button = tk.Button(form_frame, text="Update", command=lambda: updateRecord(id_entry.get(), {field: entry.get() for field, entry in form_entries.items()}, manage_criminal_window), font=("Arial", 10), bg="#2196f3", fg="white", pady=5)
    update_button.pack(side="top", pady=(10, 5))

    delete_button = tk.Button(form_frame, text="Delete", command=lambda: deleteRecord(id_entry.get(), manage_criminal_window), font=("Arial", 10), bg="red", fg="white", pady=5, width=7)
    delete_button.pack(side="top")

    criminal_records = fetchAllData()
    scrollbar = tk.Scrollbar(record_frame)
    scrollbar.pack(side="right", fill="y")
    record_listbox = tk.Listbox(record_frame, yscrollcommand=scrollbar.set, font=("Arial", 12))
    record_listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=record_listbox.yview)

    if criminal_records:
        for record in criminal_records:
            record_info = f"ID: {record['id']} | Name: {record['name']} | Father's Name: {record['father_name']} | Mother's Name: {record['mother_name']} | Gender: {record['gender']} | DOB(yyyy-mm-dd): {record['dob']} | Blood Group: {record['blood_group']} | Identification Mark: {record.get('identification_mark', '---')} | Nationality: {record['nationality']} | Religion: {record['religion']} | Crimes Done: {record['crimes_done']}"
            record_listbox.insert(tk.END, record_info)
    
            record_listbox.bind("<ButtonRelease-1>", lambda event, id=record['id']: on_record_select(id))

    else:
        no_records_label = tk.Label(record_frame, text="No criminal records found.", bg="#202d42", fg="white", font=("Arial", 12))
        no_records_label.pack(fill="both", expand=True)

    def backToMainPage():
        window.destroy()
        root.deiconify()  

    back_button = tk.Button(content, text="Back", command=backToMainPage, font=("Arial", 14, "bold"), bg="#2196f3", fg="white", pady=10)
    back_button.pack(side="bottom", pady=(20, 0))




def on_record_select(record_id):
    global selected_id
    selected_id = record_id


def openManageCriminalWindow():
    global manage_criminal_window
    manage_criminal_window = tk.Toplevel(root)
    manage_criminal_window.attributes('-fullscreen', True)  # Maximize the window
    getPage4(manage_criminal_window)

def exitTheWindow():
    root.destroy()

from policelist import fetchPoliceList

from policelist import fetchPoliceList  # Import the fetchPoliceList function

def show_police_details(event):
    # Get the index of the selected item
    index = listbox.curselection()[0]
    # Get the details of the selected police officer
    selected_police = police_list[index]
    
    # Create a new window to display details
    details_window = tk.Toplevel(police_window)
    details_window.title("Police Officer Details")
    
    # Display complete details in labels
    labels = [
        ("Name:", selected_police['name']),
        ("Rank:", selected_police['rank']),
        ("Badge Number:", selected_police['badge_number']),
        ("Contact Information:", selected_police['contact_information']),
        ("Department:", selected_police['department']),
        ("Hire Date:", selected_police['hire_date']),
        ("Shift:", selected_police['shift']),
        ("Salary:", selected_police['salary']),
        ("Designation:", selected_police['designation'])
    ]
    
    for label_text, value in labels:
        label = tk.Label(details_window, text=label_text, font=("Arial", 12, "bold"))
        label.grid(sticky="w", padx=10, pady=5)
        value_label = tk.Label(details_window, text=value, font=("Arial", 12))
        value_label.grid(row=labels.index((label_text, value)), column=1, sticky="w", padx=10, pady=5)

def police_page(root=None):
    if root is None:
        root = tk.Tk()

    # Function to display police list page
    global police_list
    police_list = fetchPoliceList()

    # Create a new window for police list
    global police_window
    police_window = tk.Toplevel(root)
    police_window.attributes('-fullscreen', True)  # Set the window to fullscreen
    police_window.title("Police List")

    # Create a frame for the title and listbox
    title_frame = tk.Frame(police_window, bg="#202d42")
    title_frame.pack(fill='x')

    # Title label
    title_label = tk.Label(title_frame, text="List of Police Officers", fg="white", bg="#202d42", font=("Arial", 20, "bold"))
    title_label.pack(pady=10)

    # Create a frame for the listbox
    frame = tk.Frame(police_window)
    frame.pack(expand=True, fill='both')

    # Display the police list in a listbox with numbers
    global listbox
    listbox = tk.Listbox(frame, width=100, height=30, font=("Arial", 12, "bold"))
    for i, police in enumerate(police_list, start=1):
        listbox.insert(tk.END, f"{i}. {police['name']} - {police['rank']}")
    listbox.pack(side='left', expand=True, fill='both', padx=10, pady=10)

    # Bind double-click event to show details
    listbox.bind("<Double-Button-1>", show_police_details)

    # Add a "Go Back" button
    back_button = tk.Button(frame, text="Go Back", command=police_window.destroy, bg="#ff5733", fg="white", font=("Arial", 12, "bold"))
    back_button.pack(side='right', pady=10, padx=10)

    root.mainloop()





######################################## Home Page ####################################
tk.Label(pages[0], text="Criminal Identification System", fg="white", bg="#202d42", font="Arial 35 bold", pady=10).pack()

logo = tk.PhotoImage(file="logo.png")
tk.Label(pages[0], image=logo, bg="#202d42").pack()

btn_frame = tk.Frame(pages[0], bg="#202d42", pady=10)
btn_frame.pack()

buttons = [
    ("Register Criminal", getPage1),
    ("Detect Criminal", getPage2),
    ("Video Surveillance", getPage3),
    ("Manage Criminal", openManageCriminalWindow),
    ("Police List", lambda: police_page(root)),
    ("Log-Out", exitTheWindow)
]

button_width = 20
button_height = 2

# Loop through the buttons list and create buttons for each entry
for text, command in buttons:
    button = tk.Button(btn_frame, text=text, command=command, width=button_width, height=button_height, font=("Arial", 12, "bold"))
    if text == "Log-Out":
        button.configure(bg="red", activebackground="#FF5733")  # Change color of the last button to red
    else:
        button.configure(bg="#2196f3", activebackground="#091428")  # Set default color for other buttons
    button.pack(pady=5, padx=10)  # Adjust padding as needed

pages[0].lift()
root.mainloop()
close_login_root()