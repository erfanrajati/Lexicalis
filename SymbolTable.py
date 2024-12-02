class SymbolTable:
    def __init__(self):
        self.types = {
            "var":[], # Variable
            "func":["print", "input"], # Function
            "cls":[], # Class (including data types)
            "kw":[], # Key Words
            "opr":[], # Operator
            "num":[], # Numeric
            "str":[], # String Literal
            "del":[] # Delimiter
        }

    
