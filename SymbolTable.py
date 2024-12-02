class SymbolTable:
    def __init__(self):
        self.types: dict[str, set] = {
            "var":set({}), # Variable
            "func":set({"print", "input"}), # Function
            "class":set({}), # Class (including data types)
            "kw":set({"while", "for", "if", "else", "elif", "repeat", "until", "class", "func"}), # Key Words
            "opr":set({'+', '-', '*', '/', '=', '==', '>', '>=', '<', '<=', 'inc', 'dec', 'div'}), # Operator
            "num":set({}), # Numeric
            "str":set({}), # String Literal
            "del":set({'{', '}', '[', ']', '(', ')', ';'}) # Delimiter
        }

    
    
