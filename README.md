# Password Integrity Checker – GUI Version 2.0

#### Description:
The Password Integrity Checker is a Tkinter-based Python GUI application that evaluates the strength and security of a user-entered password. It checks whether the password has appeared in known data breaches using the Have I Been Pwned (HIBP) API and evaluates password strength based on length and character variety.  

---

## Features

### Breach Checking (Have I Been Pwned API)
- The program hashes the password using SHA-1 and queries the HIBP API using the k-anonymous model to check if the password has ever been exposed.
- Displays the number of breaches found for the entered password in the GUI.
- Handles API errors gracefully with pop-up dialogs.

### Password Strength Evaluation
- Evaluates passwords as **Weak**, **Medium**, or **Strong** based on:
  - Length
  - Use of lowercase letters
  - Use of uppercase letters
  - Use of digits
  - Use of symbols

### Graphical User Interface
- Password input box with hidden characters (`*`)
- Buttons for **Check Password** and **Clear Input**
- Real-time display of breach count and password strength in a single area
- User-friendly pop-ups for errors and warnings

---

## File Overview

### `project.py`
- Contains all top-level functions and GUI logic:
  - `hash_password_sha1()` – hash password and split prefix/suffix for API
  - `query_hibp_api()` – query HIBP API for breach data
  - `get_password_breach_count()` – count password appearances in breaches
  - `evaluate_password_strength()` – determine password strength
  - `check_password()` – GUI button function to evaluate and display results
  - `clear_input()` – resets input and result display
- `main()` launches the Tkinter GUI interface

### `requirements.txt`
- Lists required external libraries (`requests`).

---

## How to Run

```
pip install -r requirements.txt
python project.py
```

## Design Decisions

- SHA-1 + K-Anonymity
- Only the first five characters of the hash are sent to HIBP for privacy.
- GUI Interface
- Improves user experience compared to CLI.
- Integrated display of breach count and password strength.
- Strength Evaluation
- Simple, clear scoring system for immediate feedback on password safety.
- Error Handling
- Uses pop-ups instead of console messages for better UX.