# Password Integrity Checker – Version 3.0
#### Overview:

The Password Integrity Checker is a Python Tkinter desktop application that evaluates the security of a user-entered password. It checks whether the password has ever appeared in known data breaches using the Have I Been Pwned (HIBP) API and displays a real-time strength meter with clear visual feedback.

The program focuses on usability, responsiveness, and security, combining GUI design with API integration, cryptographic hashing, and multithreading.

---

## Features

### Breach Checking (Have I Been Pwned API)
The program hashes the password using SHA-1 and queries the HIBP API using the k-anonymous model to determine if the password has ever been exposed in a data breach.
- Exception handling for network errors, timeouts, and unexpected responses

### Real-time Strength Meter
Updates live as the user types:
- Strength score updates (0–7 scale)
- Color-coded strength bar updates visually
- Strength label updates dynamically
- Clears automatically when input is empty

### Animated Loading Bar
When checking a password, a short animation simulates processing while the API call runs in a separate thread so the GUI never freezes.
- Clears automatically when input is empty

### Password Visibility Toggle
Users can toggle visibility between hidden (`*`) and plaintext.

### Keyboard Shortcuts
- **Enter** → Check password  
- **Escape** → Clear input  
- Real-time strength updates on every keystroke  

### Password Improvement Suggestions  
The program analyzes password weaknesses and provides context-aware suggestions
- “Use at least 12 characters”
- “Add uppercase letters”
- “Add symbols like ! @ # $ %”
- “Make it even longer for extra strength”

### GUI Design
The UI is fully built with Tkinter:
- Clean, compact layout
- Dynamic strength bar
- Loading animation bar
- Popup dialogs for breach warnings or safety confirmation

### Automated Tests
`test-project` includes tests for:
- SHA-1 hashing
- Strength evaluation
- Strength naming
- Edge cases and consistency

---

## Project Structure

```
├── project.py           # Main GUI application
├── test_project.py      # Automated tests
├── README.md            # Documentation
└── requirements.txt     # Dependencies
```

---

### How it works
1. User enters a password
2. Strength meter updates in real time
3. When checking:
    - Password is hashed (SHA-1)
    - First 5 hash characters are sent to the HIBP API
    - Response is scanned locally for matching suffix
4. GUI displays breach count, strength, and suggestions

---

## How to Run

```
pip install -r requirements.txt
python project.py
```

---

## Core Technologies
- Python 3
- Tkinter (GUI)
- Requests (API calls)
- Threading (non-blocking UI)
- Hashlib (SHA-1 hashing)
- PyTest (unit testing)

---

## Final Thoughts

This project pushed me to combine:
- GUI development
- API requests
- Multithreading
- Cryptographic hashing
- Exception handling
- Automated testing

I learned how to design a full software application from idea → design → implementation → testing → documentation.
