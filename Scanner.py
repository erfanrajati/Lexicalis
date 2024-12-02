from SymbolTable import SymbolTable
from Ascii import cc
from StateDiagram import *

class Scanner:
    # main initializer, uses file input
    # def __init__(self, file, s_table:SymbolTable, charCat=cc):
    #     lines = file.readlines()
    #     l: list[str] = len(lines)
    #     self.lines = dict(zip(range(l), lines))
    #     self.st = s_table
    #     self.cc = charCat

    # Debug initialized, uses string input
    def __init__(self, inputString, s_table:SymbolTable, charCat=cc):
        lines = [inputString]
        l: list[str] = len(lines)
        self.lines = dict(zip(range(l), lines))
        self.st = s_table
        self.cc = charCat


    def scan_word(self, word) -> tuple[str, str]: # might raise a KeyError
        forward = word[0]
        if forward == '$': # Variabale
             result = variable_diagram.scan(word)

        if forward in self.cc.digits: # Numberic
            pass
            
        if forward == '"': # String literal
            pass
    
        return result
    

    def tokenize(self, word: str) -> tuple[str, str]:
        # handle multi token words here...

        # see if the word was already found
        for key in self.st.types.keys():
            if word.strip() in self.st.types[key]:
                return (word, "kw")
            
        # if the token wasn't already found
        result = self.scan_word(word) # returns a tuple like: (word, type) / might raise KeyError or ValueError
        self.st.types[result[1]].add(result[0]) # add the token to the Symbol Table
        return result


    def run(self):
        for i, line in self.lines.items():
            words = line.split()
            for word in words:
                # To catch the exception raised in StateDiagram.scan()
                try:
                    result = self.tokenize(word)
                except KeyError as e:
                    print(f"Error detected at line {i}:\n{e}")
                except ValueError as e:
                    print(f"Error detected at line {i}:\n{e}")
                else:
                    # Debug
                    print(result)
                    # Fill a file with the result.



# Debug

st = SymbolTable()
scanner = Scanner("$Fpeat", s_table=st)
scanner.run()


