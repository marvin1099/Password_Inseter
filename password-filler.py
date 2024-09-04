#!/usr/bin/env python

import hashlib
import argparse
import pyautogui
import random
import psutil
import subprocess
import time
import sys
from getpass import getpass
import os
import configparser
import shlex

# Conditional import of tkinter
if '--cli' not in sys.argv:
    import tkinter as tk
    from tkinter import simpledialog, messagebox, filedialog


# Function to get the directory where the script is located
def get_script():
    if getattr(sys, 'frozen', False):  # Check if running as a frozen executable (e.g., PyInstaller)
        return os.path.abspath(sys.executable)
    else:
        return os.path.abspath(__file__)

scriptfile = get_script()
scriptdir = os.path.dirname(scriptfile)
scriptname, scriptext = os.path.splitext(os.path.basename(scriptfile))

INI_FILE = os.path.join(scriptdir, scriptname + ".conf")

class Interface:
    def __init__(self, cli=False, theme='default'):
        self.cli = cli
        if not cli:
            self.root = tk.Tk()
            style = tk.ttk.Style()
            style.theme_use(theme)
            self.root.withdraw()

    def prompt_password(self, title="SamBox", prompt="Enter Password:", hide=True):
        if self.cli:
            if hide:
                return getpass(f"{prompt} ")
            else:
                return input(f"{prompt} ")
        else:
            result = simpledialog.askstring(title, prompt, show='*' if hide else None)
            if result is None:
                sys.exit()
            return result

    def prompt_input(self, title="SamBox", prompt="Input:", hide=False):
        if self.cli:
            return input(f"{prompt} ")
        else:
            if hide:
                return simpledialog.askstring(title, prompt, show='*')
            else:
                return simpledialog.askstring(title, prompt)

    def show_message(self, title, message):
        if self.cli:
            print(f"{title}: {message}")
        else:
            messagebox.showinfo(title, message)

    def show_error(self, title, message):
        if self.cli:
            print(f"{title}: {message}")
        else:
            messagebox.showerror(title, message)

    def select_file(self, title="Select Program"):
        if self.cli:
            while True:
                file_path = input("Enter the path to the program to run: ").strip()
                if os.path.isfile(file_path):
                    return file_path
                else:
                    print("No selection. Please enter a valid file path.")
        else:
            file_path = filedialog.askopenfilename(title=title)
            if not file_path:
                self.show_error("Wrong", "No selection. Please select a file.")
                return ""
            return file_path

def compute_hash(password, salt):
    return hashlib.sha512(str(password+salt).encode('utf-8')).hexdigest()

def write_ini_file(hash_value, salt, program_path, args='', wait=2, waitexit=True):
    config = configparser.ConfigParser()
    config['Settings'] = {
        'hash': hash_value,
        'salt': salt,
        'program': program_path,
        'args': args,
        'wait': wait,
        'waitexit': waitexit
    }
    with open(INI_FILE, 'w', encoding='utf-8') as configfile:
        config.write(configfile)

def read_ini_file():
    config = configparser.ConfigParser()
    config.read(INI_FILE, encoding='utf-8')
    if 'Settings' not in config:
        raise ValueError("ini file is missing 'Settings' section.")
    settings = config['Settings']
    hash_value = settings.get('hash')
    salt = settings.get('salt')
    program_path = settings.get('program')
    args = settings.get('args', '')
    wait = settings.get('wait', 2)
    waitexit = settings.get('waitexit', True)
    if not hash_value or not program_path:
        raise ValueError("ini file is missing required fields.")
    return hash_value, salt, program_path, args, wait, waitexit

def setup(interface):
    while True:
        password1 = interface.prompt_password(prompt="Set Password:", hide=True)
        password2 = interface.prompt_password(prompt="Repeat Password:", hide=True)

        if password1 != password2:
            interface.show_error("Wrong", "Passwords don't match. Try again.")
            continue

        if not password1:
            interface.show_error("Wrong", "Empty password. Try again.")
            continue

        # Select program
        program_path = interface.select_file(title="Select Program")
        if not program_path:
            interface.show_error("Wrong", "No selection. Please select a file.")
            continue

        if not os.path.isfile(program_path):
            interface.show_error("Wrong", "Selected file is invalid. Please select a valid file.")
            continue

        # Prompt for arguments
        if interface.cli:
            args = input("Enter command-line arguments (optional): ").strip()
        else:
            args = simpledialog.askstring("SamBox", "Enter command-line arguments (optional): ")
            if args is None:
                args = ''

        # Promt for program wait time
        wait = interface.prompt_input(prompt="Set program wait time")
        try:
            wait = float(wait)
        except Exception as e:
            wait = 2.0

        # Promt it to wait for finish of program
        waitexit = interface.prompt_input(prompt="Wait for the end of the program (y/n)")
        if not waitexit or (waitexit and ("y" in waitexit or "t" in waitexit or "1" in waitexit)):
            waitexit = True
        else:
            waitexit = False

        ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        chars=[]
        for i in range(64):
            chars.append(random.choice(ALPHABET))
        salt="".join(chars)

        # Compute hash
        hash_value = compute_hash(password1, salt)

        # Write ini file
        try:
            write_ini_file(hash_value, salt, program_path, args, wait, waitexit)
            interface.show_message("Success", "Setup completed successfully.")
            break
        except Exception as e:
            interface.show_error("Error", f"Failed to write ini file: {e}")
            continue

def login(interface):
    while True:
        password = interface.prompt_password(title="SamBox", prompt="Enter Password:", hide=True)
        if password == "":
            sys.exit()

        try:
            stored_hash, salt, program_path, args, wait, waitexit = read_ini_file()
        except Exception as e:
            interface.show_error("Error", f"Failed to read ini file: {e}")
            sys.exit(1)

        input_hash = compute_hash(password, salt)

        if input_hash == stored_hash:
            # Run the program and send the password
            run_program_and_send_password(program_path, args, wait, waitexit, password, interface)
            sys.exit()
        else:
            interface.show_error("Wrong", "Wrong Password. Try again.")

def run_program_and_send_password(program_path, args, wait, waitexit, password, interface):
    try:
        program_path = os.path.abspath(program_path)
        print(program_path)
        if args:
            args_list = shlex.split(args)
            process = subprocess.Popen([program_path] + args_list, shell=False)
        else:
            process = subprocess.Popen([program_path], shell=False)
    except Exception as e:
        interface.show_error("Error", f"Failed to start the program: {e}")
        return

    # Wait for the program to initialize
    try:
        wait = float(wait)
    except Exception as e:
        wait = 2.0
    time.sleep(wait)  # Adjust as needed based on program startup time

    # Optionally, check if the process is running
    if not psutil.pid_exists(process.pid):
        print("The program might not have started successfully. Trying anyway.")

    # Send the password and press Enter
    try:
        pyautogui.typewrite(password, interval=0.05)
        pyautogui.press('enter')
    except Exception as e:
        interface.show_error("Error", f"Failed to send password to the program: {e}")

    if waitexit and not (isinstance(waitexit,str) and waitexit.lower() == "false"):
        print("\nWaiting for exit of started program...\n")
        process.wait()

def main():
    parser = argparse.ArgumentParser(description="SamBox Program")
    parser.add_argument('--cli', action='store_true', help='Use CLI mode')
    if not getattr(sys, 'frozen', False):
        parser.add_argument('--tk-theme', dest="tk_theme", help='Set name of the tk theme to use')
    args = parser.parse_args()

    try:
        tkt = args.tk_theme
    except Exception as e:
        tkt = 'default'

    interface = Interface(cli=args.cli,theme=tkt)

    if not os.path.isfile(INI_FILE):
        # Setup phase
        setup(interface)

    # Authentication phase
    login(interface)

if __name__ == '__main__':
    main()
