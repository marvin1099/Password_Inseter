#!/usr/bin/env python

import tkinter as tk
from tkinter import messagebox, ttk
import sys

def main():
    root = tk.Tk()
    style = tk.ttk.Style()
    style.theme_use('default')
    #root.withdraw()
    root.title("Password filler input tester ")
    root.geometry("400x250")

    # This is the password that is expected
    correct_password = "test123"

    def verify_password():
        entered_password = password_entry.get()
        if entered_password == correct_password:
            messagebox.showinfo("Success", "Password Correct!")
            sys.exit()
        else:
            messagebox.showerror("Error", "Incorrect Password")

    # Create the main UI components
    label = tk.Label(root, text="Please autofill the password\nThe correct one is test123")
    label.pack(pady=20)

    password_entry = tk.Entry(root, show='*', width=30)
    password_entry.pack(pady=10)

    submit_button = tk.Button(root, text="Submit", command=verify_password)
    submit_button.pack(pady=20)

    # Bind Enter key to the submit button
    root.bind('<Return>', lambda event: submit_button.invoke())

    # Automatically focus on the password entry box
    password_entry.focus_set()

    root.mainloop()

if __name__ == "__main__":
    main()
