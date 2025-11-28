# Password Integrity Checker – CLI Version 1.0

#### Description:
The Password Integrity Checker is a command-line (CLI) Python application that evaluates the strength and security of a user-entered password. It checks whether the password has appeared in known data breaches using the Have I Been Pwned (HIBP) API and evaluates password strength based on length and character variety.

---

## Features

### Breach Checking (Have I Been Pwned API)
- The program hashes the password using SHA-1 and queries the HIBP API using the k-anonymous model to check if the password has ever been exposed.
- Returns the number of breaches found for the entered password.

### Password Strength Evaluation
- Scores passwords as **Weak**, **Medium**, or **Strong** based on:
  - Length
  - Use of lowercase letters
  - Use of uppercase letters
  - Use of digits
  - Use of symbols

### User-Friendly CLI
- Loading animation to simulate processing while waiting for the API response.
- Clear messages for exposed passwords, safe passwords, or input errors.
- Exit option via typing `exit`.

---

## File Overview

### `project.py`
- Contains all top-level functions and `main()`:
  - `hash_password_sha1()` – hash password and split prefix/suffix for API
  - `query_hibp_api()` – query HIBP API for breach data
  - `get_password_breach_count()` – count password appearances in breaches
  - `evaluate_password_strength()` – determine password strength
  - `display_results()` – print breach and strength info
  - `display_loading()` – simple CLI loading animation
- `main()` launches the CLI interface

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
- CLI Loading Animation
- Enhances UX and mimics progress while API checks are performed.
- Strength Evaluation
- Simple, clear scoring system for immediate feedback on password safety.
