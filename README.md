# Password Inseter

A password-protected program launcher & auto-filler. On first run you set a master password, choose a target program (e.g. SAM), and save the config. Every subsequent run asks for that password before launching the program and typing the password into it — if you enter nothing, it just exits.

## How it works

- The password is salted (64 random alphanumeric chars) and hashed with **SHA-512** before storage — cracking the stored hash is not feasible.
- The config (hash, salt, program path, args, wait time) is saved in a `password-filler.conf` INI file next to the script.
- On login, `pyautogui` types the password into the target program and presses Enter.

## Usage

```bash
python password-filler.py          # GUI mode (default)
python password-filler.py --cli    # Terminal-only mode
python password-filler.py --tk-theme clam  # Change tkinter theme
```

**First run:** You will be guided through setting a password, selecting the target program (with optional arguments), configuring a startup delay, and choosing whether to wait for the program to exit.

**Subsequent runs:** Enter the correct password to launch the program and auto-fill the password field.

## Background

This was made for **SAM - Steam Account Manager** ([github.com/rex706/SAM](https://github.com/rex706/SAM)). SAM would show two error messages when given the wrong or no password. This tool avoids that entirely by handling password verification itself — the target program only ever receives the correct password.

## Dependencies

```
pip install pyautogui psutil
```

- `pyautogui` — types the password into the target window
- `psutil` — checks if the target process started successfully
- `tkinter` — ships with Python, used for the GUI dialogs

## Testing

`input-tester.py` is a simple GUI that expects the password `test123`. Use it to verify that `password-filler.py` correctly auto-fills the password field.

```bash
python password-filler.py           # then select input-tester.py as the target program
```

## Downloads

Pre-compiled binaries for Linux and Windows are available, or grab the Python file if you have the requirements:

- [Codeberg Releases](https://codeberg.org/marvin1099/Password_Inseter/releases) (primary)
- [GitHub Releases](https://github.com/marvin1099/Password_Inseter/releases) (backup)

## Tutorial Video

<video src="samco.mp4" controls></video>
