from SymbolTable import SymbolTable
from Ascii import char_cat
from StateDiagram import *

class Scanner:
    # def __init__(self, file, s_table:SymbolTable, char_cat=char_cat):
    #     '''main initializer, uses file input'''
    #     lines = file.readlines()
    #     l: list[str] = len(lines)
    #     self.lines = dict(zip(range(l), lines))
    #     self.st = s_table
    #     self.char_cat = char_cat

    def __init__(self, inputString, st:SymbolTable, char_cat=char_cat):
        '''Debug initializer, uses string input'''
        self.st = st
        self.char_cat = char_cat

        # Add space before and after each delimiter
        # c = 0
        # while c < len(inputString)-1:
        #     if inputString[c] in self.st.types['del']:
        #         inputString = inputString[:c] + ' ' + inputString[c] + ' ' + inputString[c+1:]
        #         c+=2
        #         continue
        #     c+=1
        
        lines = [inputString]
        l: list[str] = len(lines)
        self.lines = dict(zip(range(l), lines))



    def scan_word(self, word: str) -> tuple[str, str]: # might raise a KeyError or ValueError
        # see if the word was already found
        for key in self.st.types.keys():
            if word.strip() in self.st.types[key]:
                return (word, key)

        # if the word wasn't already found
        forward = word[0]
        if forward == '$': # Variabale
             result = variable_diagram.scan(word)

        if forward in self.char_cat.digits: # Numberic
            pass
            
        if forward == '"': # String literal
            pass
    
        return result
    

    def scan_group(self, group: str) -> list[tuple[str, str]]:
        results = []
        first, forward = 0, 0
        while first < len(group):
            if group[first] in self.st.types['del']:
                # to buffer the potential delimiter
                target = group[first]
                group = group[first] + group[first+1:]

            if first in self.st.types['opr']:
                # to buffer the entire operator token
                forward += 1
                while group[first:forward] in self.st.types['opr']: 
                    forward += 1
                else: # backtrack
                    target = group[first:forward]

            if first == '$' or first in self.char_cat.non_special:
                # to buffer the entire variable token.
                forward += 1
                while group[forward] in self.char_cat.non_special and forward < len(group): 
                    forward += 1
                else: # backtrack
                    target = group[first:forward] # from first to one before forward

            if first == '"':
                # to buffer the entire string token
                forward += 1
                while group[forward] in self.char_cat.all_chars - '"': 
                    forward += 1
                else: # no backtrack
                    target = group[first:forward+1]



            if target:
                results.append(self.scan_word(target))
            else:
                first += 1
                forward = first

    

    # COMPLETED
    def tokenize(self, word: str) -> list[tuple[str, str]]:
        '''Might raise Key or Value errors'''

        temp = set(word)
        if temp & self.st.types['del'] or temp & self.st.types['opr']:
            results = self.scan_group(group=word)
        else: # the word contains a single token here
            results = [self.scan_word(word)] 
        
        for r in results:
            self.st.types[r[1]].add(r[0]) # add the token to the Symbol Table
        return results


    def run(self):
        for i, line in self.lines.items():
            words = line.split() 
                # also splits inside the strings! musn't do that.
                # must concat all members from "* to *"
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
                    # or perhaps fill a file with the result.



# Debug

st = SymbolTable()
scanner = Scanner("$Fpeat {while} for [print()] { }", st=st)
scanner.run()


