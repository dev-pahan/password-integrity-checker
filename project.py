### CLI Version ###
# Version 1.0
# -------------------------------------------------------
# Features: Password breach check via HIBP API, Password strength evaluation
# -------------------------------------------------------

import hashlib
import requests
import time
import sys
import string

# ------------------------
# Logic Functions
# ------------------------

# CLI loading animation to enhance UX and mimic "progress"
def display_loading(message, duration=1.5):
    print(message, end="")
    for _ in range(int(duration / 0.3)):
        for dot in ". .. ...".split():
            sys.stdout.write(f"\r{message}{dot} ")
            sys.stdout.flush()
            time.sleep(0.3)
    print("\r", end="")

# Hash a password using SHA1 and return prefix & suffix for HIBP k-anonymity
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

# Display the results for a given password
def display_results(password, breach_count, strength):
    if breach_count:
        print(f"⚠️  Exposed {breach_count} times! Consider changing it.\nStrength: {strength}")
    else:
        print(f"✅  Not found in known breaches.\nStrength: {strength}")

# ------------------------
# Main CLI Application
# ------------------------

def main():
    print("=== Password Integrity Checker ===\n")
    
    while True:
        password = input("Enter a password to check (or type 'exit' to quit): ").strip()
        
        if password.lower() == "exit":
            print("\nExiting Password Integrity Checker. Stay safe!")
            break

        if not password:
            print("Input Error: Please enter a password.\n")
            continue

        display_loading("Checking HIBP API")
        breach_count = get_password_breach_count(password)
        strength = evaluate_password_strength(password)
        display_results(password, breach_count, strength)
        print()


if __name__ == "__main__":
    main()