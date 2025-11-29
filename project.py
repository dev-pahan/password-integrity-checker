## GUI Update ## 
# Version 3.0
# -------------------------------------------------------
# New Features & Upgrades From GUI v2:
# - Threading added to avoid GUI freezing during API calls
# - Animated loading bar for better progress feedback
# - Completely redesigned strength scoring system (0–7)
# - Color-changing strength meter bar added (live updates)
# - Added password show/hide toggle
# - Enter key triggers check, Escape key clears everything
# - Improved popup messages for breached / safe passwords
# - Strength label updates live while typing
# - Password improvement suggestions
# - Bug fix: UI freezing resolved with async thread calls
# - Bug fix: Strength meter now resets properly on clear
# -------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import requests
import string
import threading
import time

# ------------------------
# Password Logic Functions
# ------------------------

# Hash a password using SHA1 and return prefix & suffix
def hash_password_sha1(password):
    try:
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        return sha1_hash[:5], sha1_hash[5:]
    except Exception as e:
        raise RuntimeError(f"Error hashing password: {e}")

# Query Have I Been Pwned API for a given SHA1 prefix
def query_hibp_api(prefix):
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        response = requests.get(url, timeout=10)  # set a timeout
        response.raise_for_status()
        return response.text
    except requests.Timeout:
        raise RuntimeError("Request timed out. Check your internet connection.")
    except requests.ConnectionError:
        raise RuntimeError("Network error occurred. Unable to connect to HIBP API.")
    except requests.HTTPError as e:
        raise RuntimeError(f"HTTP error occurred: {e.response.status_code}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error querying HIBP API: {e}")

# Get the number of times a password appears in breaches
def get_password_breach_count(password):
    try:
        prefix, suffix = hash_password_sha1(password)
        response = query_hibp_api(prefix)
        for line in response.splitlines():
            if ":" not in line:
                continue
            hash_suffix, count = line.split(":")
            if hash_suffix == suffix:
                return int(count)
        return 0
    except ValueError:
        raise RuntimeError("Error parsing response from HIBP API.")
    except Exception as e:
        raise RuntimeError(f"Failed to check password breach count: {e}")

# Strength evaluation using a scoring system
def evaluate_password_strength(password):
    score = 0
    length = len(password)
    if length >= 8: score += 1
    if length >= 12: score += 1
    if length >= 16: score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1
    if length >= 12 and score >= 5: score += 1
    return min(score, 7)

# Convert score to text label
def get_strength_name(score):
    if score <= 2:
        return "Very Weak"
    elif score == 3:
        return "Weak"
    elif score == 4:
        return "Moderate"
    elif score == 5:
        return "Strong"
    else:
        return "Very Strong"
    
# Create improvement suggestions based on password weaknesses
def get_improvement_suggestions(password):
    suggestions = []
    length = len(password)

    if length < 12:
        suggestions.append("Use at least 12 characters")
    if not any(c.islower() for c in password):
        suggestions.append("Add lowercase letters")
    if not any(c.isupper() for c in password):
        suggestions.append("Add uppercase letters")
    if not any(c.isdigit() for c in password):
        suggestions.append("Include numbers")
    if not any(c in string.punctuation for c in password):
        suggestions.append("Add symbols (e.g., ! @ # $ %)")
    if not suggestions:
        return "Your password is strong - great job!"

    return "Suggestions:\n- " + "\n- ".join(suggestions)

# ------------------------
# GUI Functions
# ------------------------

# Async thread so UI does not freeze during HIBP API call
def start_check_thread():
    threading.Thread(target=check_password, daemon=True).start()

# Loading bar animation 
def animate_loading_bar():
    for i in range(351):
        canvas_loading.coords(loading_rect, 0, 0, i, 20)
        root.update_idletasks()
        time.sleep(0.005)

# Main password checking flow
def check_password():
    password = password_entry.get().strip()
    if not password:
        messagebox.showwarning("Input Error", "Please enter a password.")
        return

    analyzing_label.config(text="Analyzing HIBP Database...")
    root.update_idletasks()

    animate_loading_bar()

    try:
        breach_count = get_password_breach_count(password)
        strength_score = evaluate_password_strength(password)
        strength_name = get_strength_name(strength_score)
        suggestions = get_improvement_suggestions(password)

        if breach_count > 0:
            analyzing_label.config(
                text=f"⚠️ This password appeared in breaches {breach_count} times!\n"
                    f"Strength: {strength_name}\n\n{suggestions}"
            )
            messagebox.showerror(
                "Password Breached!",
                f"⚠️ This password has appeared in breaches {breach_count} times!\n"
                f"Strength: {strength_name}\n\n{suggestions}"
            )
        else:
            analyzing_label.config(
                text=f"✔️ Not found in known breaches.\n"
                    f"Strength: {strength_name}\n\n{suggestions}"
            )
            messagebox.showinfo(
                "Safe Password",
                f"✔️ This password was NOT found in any known breaches.\n"
                f"Strength: {strength_name}\n\n{suggestions}"
            )

    except Exception as e:
        analyzing_label.config(text="")
        messagebox.showerror("Error", f"An error occurred: {e}")

# Live-updating strength bar
def update_strength_bar(event=None):
    password = password_entry.get()
    
    if not password:
        strength_label.config(text="Strength")
        analyzing_label.config(text="")
        canvas_strength_bar.coords(bar_rect, 0, 0, 0, 20)
        canvas_loading.coords(loading_rect, 0, 0, 0, 20)
        return

    score = evaluate_password_strength(password)
    strength_label.config(text=get_strength_name(score))

    max_width = 300
    width = int((score / 7) * max_width)

    color = (
        "#ff4d4d" if score <= 2 else
        "#ffa64d" if score == 3 else
        "#ffff4d" if score == 4 else
        "#80ff80" if score == 5 else
        "#00cc44"
    )

    canvas_strength_bar.coords(bar_rect, 0, 0, width, 20)
    canvas_strength_bar.itemconfig(bar_rect, fill=color)


# Password visibility toggle
def toggle_password_visibility():
    if password_entry.cget("show") == "":
        password_entry.config(show="*")
        show_hide_button.config(text="👁")
    else:
        password_entry.config(show="")
        show_hide_button.config(text="🙈")

# Clear function resets everything including bars
def clear_input():
    password_entry.delete(0, tk.END)
    canvas_strength_bar.coords(bar_rect, 0,0,0,20)
    strength_label.config(text="Strength")
    canvas_loading.coords(loading_rect, 0, 0, 0, 20)
    analyzing_label.config(text="")


# ------------------------
# Main GUI Application
# ------------------------

def main():
    global root, password_entry, show_hide_button, strength_label, analyzing_label
    global canvas_strength_bar, bar_rect, canvas_loading, loading_rect, result_text

    # Create main application window
    root = tk.Tk()
    root.title("Password Integrity Checker")
    root.resizable(False, False)

    # Desired window size
    window_width = 450
    window_height = 580

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate x and y coordinates to center the window
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)

    # Set the geometry to center the window
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Custom Tkinter style
    style = ttk.Style()
    style.configure("Blue.Horizontal.TProgressbar", troughcolor="#e0e0e0", background="#0078d7", thickness=15)
    style.configure("Poppins.TButton", font=("Poppins", 10, "bold"))

    # Main Frame that holds title, entry box, strength bar
    main_frame = ttk.Frame(root)
    main_frame.pack(pady=20)

    # Title text displayed above password entry
    title_label = ttk.Label(main_frame, text="Enter Password", font=("Poppins", 12, "bold"))
    title_label.pack()

    # Frame for password entry + visibility toggle button
    entry_frame = ttk.Frame(main_frame)
    entry_frame.pack(pady=5)

    # Frame for password entry + visibility toggle button
    entry_frame = ttk.Frame(main_frame)
    entry_frame.pack(pady=5)

    # Sub-frame to hold Entry and Button side by side
    input_frame = ttk.Frame(entry_frame)
    input_frame.pack()

    # Password input box
    password_entry = ttk.Entry(input_frame, width=30, show="*")
    password_entry.pack(side="left", padx=(0,5), ipady=3)  # ipady adjusts vertical padding

    # Toggle visibility button (shows/hides password)
    show_hide_button = ttk.Button(input_frame, text="👁", width=4, command=toggle_password_visibility)
    show_hide_button.pack(side="left", ipady=3)
    
    # Event bindings:
    password_entry.bind("<KeyRelease>", update_strength_bar)
    password_entry.bind("<Return>", lambda event: start_check_thread())

    root.bind("<Escape>", lambda event: clear_input())

    # Label above the dynamic strength bar
    strength_label = ttk.Label(main_frame, text="Strength", font=("Poppins", 10, "bold"))
    strength_label.pack(pady=(10, 3))

    # Canvas that visually represents password strength bar
    canvas_strength_bar = tk.Canvas(main_frame, width=300, height=20, bg="#e0e0e0", highlightthickness=0)
    canvas_strength_bar.pack()

    # Rectangle inside the canvas — width + color updates dynamically based on strength score
    bar_rect = canvas_strength_bar.create_rectangle(0, 0, 0, 20, fill="#00cc44", outline="", width=0)

    # Button Row (Check Password + Clear buttons)
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=15)

    ttk.Button(button_frame, text="Check Password", command=start_check_thread, style="Poppins.TButton", padding=(20, 5)).grid(row=0, column=0, padx=10,)
    ttk.Button(button_frame, text="Clear", command=clear_input, style="Poppins.TButton", padding=(0, 5)).grid(row=0, column=1, padx=10)

    # Loading bar animation canvas
    canvas_loading = tk.Canvas(root, width=350, height=20, bg="#e0e0e0", highlightthickness=0)
    canvas_loading.pack(pady=10)
    
    # Rectangle that visually grows during loading animation
    loading_rect = canvas_loading.create_rectangle(0, 0, 0, 20, fill="#0078d7", outline="", width=0)

    # Label to show analyzing status AND results
    analyzing_label = ttk.Label(root, text="", font=("Poppins", 12, "bold"), foreground="#0078d7", wraplength=400, justify="center")
    analyzing_label.pack(pady=(5, 10))

    # Start Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
