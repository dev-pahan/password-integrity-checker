### GUI Update ###
# Version 2.0
# -------------------------------------------------------
# New Features & Upgrades from v1 CLI:
# - Graphical User Interface using Tkinter
# - Clear input button added for improved UX
# - Error handling with pop-ups instead of terminal prints
# - Real-time result display in GUI
# - Password strength and breach results integrated into a single output
# - Bug fixes: consistent SHA1 hashing, better API error handling
# -------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import requests
import string

# ------------------------
# Password Logic Functions
# ------------------------

# Hash a password using SHA1 and return prefix & suffix
def hash_password_sha1(password):
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    return sha1_hash[:5], sha1_hash[5:]

# Query Have I Been Pwned API for a given SHA1 prefix
def query_hibp_api(prefix):
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f"Error fetching data from HIBP API: {response.status_code}")
    return response.text

# Get the number of times a password appears in breaches 
def get_password_breach_count(password):
    prefix, suffix = hash_password_sha1(password)
    response = query_hibp_api(prefix)
    for line in response.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return int(count)
    return 0

# Evaluate password strength based on length and character variety
def evaluate_password_strength(password):
    length = len(password)
    categories = sum([
        bool(set(password) & set(string.ascii_lowercase)),
        bool(set(password) & set(string.ascii_uppercase)),
        bool(set(password) & set(string.digits)),
        bool(set(password) & set(string.punctuation))
    ])
    if length >= 12 and categories >= 3:
        return "Strong"
    elif length >= 8 and categories >= 2:
        return "Medium"
    else:
        return "Weak"

# ------------------------
# GUI Functions
# ------------------------

# Check password on button click
def check_password():
    password = password_entry.get().strip()
    if not password:
        messagebox.showwarning("Input Error", "Please enter a password.")
        return

    try:
        breach_count = get_password_breach_count(password)
        strength = evaluate_password_strength(password)

        if breach_count:
            result_text.set(f"⚠️ Exposed {breach_count} times! Consider changing it.\nStrength: {strength}")
        else:
            result_text.set(f"✅ Not found in known breaches.\nStrength: {strength}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Clear input and result display
def clear_input():
    password_entry.delete(0, tk.END)
    result_text.set("")

# ------------------------
# Main GUI Application
# ------------------------

def main():
    global root, password_entry, result_text

    # Create main application window
    root = tk.Tk()
    root.title("Password Integrity Checker")
    root.geometry("400x200")
    root.resizable(False, False)

    # Password input
    ttk.Label(root, text="Enter Password:").pack(pady=(20, 5))
    password_entry = ttk.Entry(root, width=30, show="*")
    password_entry.pack()

    # Buttons
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)
    ttk.Button(button_frame, text="Check Password", command=check_password).grid(row=0, column=0, padx=5)
    ttk.Button(button_frame, text="Clear", command=clear_input).grid(row=0, column=1, padx=5)

    # Result display
    result_text = tk.StringVar()
    ttk.Label(root, textvariable=result_text, wraplength=350, justify="center").pack(pady=10)

    # Start Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
