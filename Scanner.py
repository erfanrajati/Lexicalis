from SymbolTable import SymbolTable

class Scanner:
    def __init__(self, file, s_table:SymbolTable, charCat):
        lines = file.readlines()
        l: list[str] = len(lines)
        self.lines = dict(zip(range(l), lines))
        self.st = s_table
        self.cc = charCat

    def scan(self, word):
        forward = word[0]
        if forward == '$': # Variabale
            pass

        if forward in self.cc.digits: # Numberic
            pass
            
        if forward == '"': # String literal
            pass
    
    def tokenize(self, word: str):
        for key in self.st.types.keys():
            if word.strip() in self.st.types[key]:
                return (word, "kw")
        
        # if the token wasn't already found
        return self.scan(word)


    def split(self):
        for line in self.lines:
            words = line.split()
            for word in words:
                self.tokenize(word)




