class SymbolTable:
    def __init__(self):
        self.types = {
            "var":{}, # Variable
            "func":{"print", "input"}, # Function
            "class":{}, # Class (including data types)
            "kw":{"while", "for", "if", "else", "elif", "repeat", "until", "class", "func"}, # Key Words
            "opr":{'+', '-', '*', '/', '=', '==', '>=', '<=', 'inc', 'dec', 'div'}, # Operator
            "num":{}, # Numeric
            "str":{}, # String Literal
            "del":{'{', '}', '[', ']', '(', ')', ';'} # Delimiter
        }

    
    
