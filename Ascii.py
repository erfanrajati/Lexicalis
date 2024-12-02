import string

class CharCat:
    def __init__(self):
        self.lowercase_chars = set(string.ascii_lowercase)  # 'a' to 'z'
        self.uppercase_chars = set(string.ascii_uppercase)  # 'A' to 'Z'
        self.digits = set(string.digits)                    # '0' to '9'
        self.non_special = self.digits | self.lowercase_chars | self.uppercase_chars
        self.all_chars = set(string.printable)

char_cat = CharCat()