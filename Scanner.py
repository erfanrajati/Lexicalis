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
        self.tokens = []


    def scan_word(self, word: str) -> tuple[str, str]: # might raise a KeyError or ValueError
        # see if the word was already found
        for key in self.st.types.keys():
            if word.strip() in self.st.types[key]:
                result = (word, key)
                
                # Add the new token to Symbol Table and Token list
                self.tokens.append(result) 
                self.st.types[result[1]].add(result[0])
                
                # Log
                print(f"Token found: {result}")
                return result

        # if the word wasn't already found
        forward = word[0]
        if forward == '$': # Variabale
            result = variable_diagram.scan(word)

        elif forward in self.char_cat.uppercase_chars: # Class names
            result = class_diagram.scan(word)

        elif forward in self.char_cat.digits: # Numberic
            try:
                result = integer_diagram.scan(word)
            except:
                result = float_diagram.scan(word)
            
        elif forward == '"': # String literal
            result = string_diagram.scan(word)

        # Add the new token to Symbol Table and Token list
        self.tokens.append(result) 
        self.st.types[result[1]].add(result[0])
        
        # Log
        print(f"Token found: {result}")
        return result
    

    def scan_group(self, group: str) -> list[tuple[str, str]]:
        group += '#' # acts like 'other', not considered by any State Diagram
        results = []
        first, forward = 0, 0
        while first < len(group) and group != '#': 
            if group[first] in self.st.types['del']:
                # to buffer the potential delimiter
                target = group[first]
                temp = self.scan_word(target)
                results.append(temp)
                # print(group, target) # Debug
                group = group[1:]


            elif group and group[first] in self.st.types['opr']:
                # to buffer the entire operator token
                forward += 1
                while (group[forward] in self.st.types['opr']) and (group[forward] != '#'): 
                    forward += 1
                else: # backtrack
                    target = group[:forward]
                    temp = self.scan_word(target)
                    results.append(temp)
                    group = group[forward:]

            elif group and (group[first] in self.char_cat.non_special | set({'$'})):
                # to buffer the entire variable token.
                forward += 1
                while (group[forward] in self.char_cat.non_special | set({'.'})) and (group[forward] != '#'):
                    forward += 1
                    # print(group, forward) # Debug
                else: # backtrack
                    target = group[:forward] # from first to one before forward
                    temp = self.scan_word(target)
                    results.append(temp)
                    group = group[forward:]

            elif group and group[first] == '"':
                # to buffer the entire string token
                forward += 1
                while group[forward] in self.char_cat.all_chars - '"': 
                    forward += 1
                else: # no backtrack
                    target = group[first:forward+1]
                    temp = self.scan_word(target)
                    results.append(temp)
                    group = group[:first] + group[forward:]
            else:
                raise KeyError(group[:-1])
            
            forward = first
                    
        return results


    # COMPLETED
    def tokenize(self, word: str) -> list[tuple[str, str]]:
    # def tokenize(self, word: str, file_out) -> list[tuple[str, str]]:
        '''Might raise Key or Value errors'''
        
        # see if the word was a single token:
        try:
            results = [self.scan_word(word)] 
            # must return a list if it's a token since the return value of this function is later treated as a list
        
        # if it's not a single token
        except UnboundLocalError:
            try: 
                results = self.scan_group(group=word)
            except UnboundLocalError:
                raise UnboundLocalError("Token not recognized") # change error massage for readability
        except KeyError:
            results = self.scan_group(group=word)
            
        return results


    def split(self, line: str) -> tuple[list[str], bool]:
        '''
        Splits the input line of code by space. 
        But leaves the strings whole as the should be.
        Returns the a tuple containing the list of words and 
        error status that shows if the strings where all closed. (False means not Closed)
        '''
        line = line.replace('"', ' " ')
        words = line.split()
        string_stat = True
        while True:
            begin, end = 0, 0
            for i in range(len(words)):
                if words[i] == '"' and begin:
                    end = i
                    break

                if words[i] == '"':
                    begin = i
                     
            print(begin, end)
            if begin and end:
                cat = '"' + ' '.join(s for s in words[begin+1:end]) + '"'
                print(cat)
                words = words[:begin] + [cat] + words[end+1:]

            elif begin:
                words = words[:begin]
                string_stat = False
                break

            else: # No string is left
                break
        
        return (words, string_stat)



    def run(self):
    # def run(self, file_out):
    
        for i, line in self.lines.items():
            line = line.replace('"', ' " ')

            print(f"\n\nScanning line: {i}")
            print("    -->", line)
            
            words = self.split(line)
            if words[1] == False: # Means some string was opened and not closed
                print(f"Error detected at line {i}")
                print("    --> String was opened but not closed.")

            words = words[0] # to just consider the main part from here on
            
            # Tokenize each wrod and handle exceptions.
            for word in words:
                try:
                    print(f"\nWorking on: {word}")
                    self.tokenize(word)
                except KeyError as e:
                    print(f"Error detected at line {i}\n    --> {e}")
                except ValueError as e:
                    print(f"Error detected at line {i}\n    --> {e}: {word}")
                except UnboundLocalError as e:
                    print(f"Error detected at line {i}\n    --> {e}: {word}")




# Debug

code = "[ 123.234]]] for[INT+] $I] \"hello my name is erfan\" 123+456 $Gsd!d"
# code = "[=<]"

st = SymbolTable()

scanner = Scanner(code, st=st)
scanner.run()

print("\n\nSymbol Table: ")
for k, v in scanner.st.types.items():
    print(k, v)

print("\n\nTokens: ")
for t in scanner.tokens:
    print(t)


