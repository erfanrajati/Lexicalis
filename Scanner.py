from SymbolTable import SymbolTable
import string


class Scanner:
    def __init__(self, file, s_table:SymbolTable):
        lines = file.readlines()
        l = len(lines)
        self.lines = dict(zip(range(l), lines))
        self.st = s_table


class CharCat:
    def __init__(self):
        self.lowercase_chars = set(string.ascii_lowercase)  # 'a' to 'z'
        self.uppercase_chars = set(string.ascii_uppercase)  # 'A' to 'Z'
        self.digits = set(string.digits)                    # '0' to '9'