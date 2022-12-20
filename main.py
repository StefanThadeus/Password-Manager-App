from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD FINDER ------------------------------- #


def search_password():
    website = website_entry.get()

    if len(website) == 0:
        messagebox.showinfo(title="Oops!", message="Please make sure you entered the website name!")
        return

    try:
        with open("data.json", "r") as data_file:
            # read data (it is now a python dictionary stored inside "data" variable)
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error!", message="No data file found!")
    else:
        try:
            message = f"Email: {data[website]['email']}\nPassword: {data[website]['password']}"
            messagebox.showinfo(title=website, message=message)
        except KeyError:
            messagebox.showerror(title="Error!", message="Password for given website not found!")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)

    # enter the password into the clipboard
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website:
            {
                "email": email,
                "password": password
            }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops!", message="Please make sure you haven't left any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                # read old data (it is now a python dictionary stored inside "data" variable)
                data = json.load(data_file)
                # update old data with new
                data.update(new_data)
        except FileNotFoundError:
            data = new_data

        with open("data.json", "w") as data_file:
            # save updated data
            json.dump(data, data_file, indent=4)

        website_entry.delete(0, END)
        website_entry.focus()
        password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

# window setup
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# make a canvas (which allows to stack elements on top of each other)
canvas = Canvas(width=200, height=200, highlightthickness=0)

# add image to canvas
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)

# add canvas to grid
canvas.grid(column=1, row=0)

# labels
# anchor 'e' stands for east, which is right alignment
website_label = Label(text="Website:", anchor='e', justify=RIGHT, width=20)
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:", anchor='e', justify=RIGHT, width=20)
email_label.grid(row=2, column=0)
password_label = Label(text="Password:", anchor='e', justify=RIGHT, width=20)
password_label.grid(row=3, column=0)

# entries
website_entry = Entry(width=18)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=37)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "stefan@gmail.com")
password_entry = Entry(width=18)
password_entry.grid(row=3, column=1)

# buttons
search_password_button = Button(text="Search", width=15, command=search_password)
search_password_button.grid(row=1, column=2)
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=35, command=save)
add_button.grid(row=4, column=1, columnspan=2)

# maintain window until user closes app
window.mainloop()
