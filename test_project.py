from project import hash_password_sha1, evaluate_password_strength, get_strength_name

def test_hash_password_sha1():
    prefix, suffix = hash_password_sha1("password")
    assert len(prefix) == 5
    assert len(suffix) == 35

def test_evaluate_password_strength():
    assert evaluate_password_strength("abc") <= 2
    assert evaluate_password_strength("Password123!") >= 5
    assert evaluate_password_strength("SuperStrongPassword123!") == 7

def test_get_strength_name():
    assert get_strength_name(1) == "Very Weak"
    assert get_strength_name(4) == "Moderate"
    assert get_strength_name(7) == "Very Strong"

def test_hash_password_sha1_consistency():
    p1 = hash_password_sha1("Hello123")
    p2 = hash_password_sha1("Hello123")
    assert p1 == p2

def test_strength_empty_password():
    assert evaluate_password_strength("") == 0

def test_strength_very_strong():
    score = evaluate_password_strength("A!b2C3d4E5f6G7h8@")
    assert score >= 6

def test_get_strength_name_boundaries():
    assert get_strength_name(0) == "Very Weak"
    assert get_strength_name(1) == "Very Weak"
    assert get_strength_name(2) == "Very Weak"
    assert get_strength_name(3) == "Weak"
    assert get_strength_name(4) == "Moderate"
    assert get_strength_name(5) == "Strong"
    assert get_strength_name(6) == "Very Strong"
    assert get_strength_name(7) == "Very Strong"


