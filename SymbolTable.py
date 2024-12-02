class SymbolTable:
    def __init__(self):
        self.types = {
            "var":[], # Variable
            "func":["print", "input"], # Function
            "cls":["INT", "FLOAT", "STR", "BOOL"], # Class
            "opr":[], # Operator
            "num":[], # Numeric
            "str":[], # String Literal
            "del":[] # Delimiter
        }

    
