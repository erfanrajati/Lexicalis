import string

class CharCat:
    def __init__(self):
        self.lowercase_chars = set(string.ascii_lowercase)  # 'a' to 'z'
        self.uppercase_chars = set(string.ascii_uppercase)  # 'A' to 'Z'
        self.digits = set(string.digits)                    # '0' to '9'

cc = CharCat()