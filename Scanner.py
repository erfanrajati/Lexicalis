import SymbolTable
from Ascii import char_cat
from StateDiagram import *

class Scanner:
    def __init__(self, file, st = SymbolTable.st, char_cat=char_cat):
        '''main initializer, uses file input'''
        self.st = st
        self.char_cat = char_cat
        self.lines = file.readlines()
        self.tokens: list[tuple[str, str]] = []


    # def __init__(self, inputString, st=SymbolTable.st, char_cat=char_cat):
    #     '''Debug initializer, uses string input'''
    #     self.st = st
    #     self.char_cat = char_cat        
    #     self.lines = [inputString]
    #     self.tokens = []


    def scan_word(self, word: str) -> tuple[str, str]: 
        '''
        Runs in the background,
        Gets a word and returns if it's a token and its type.
        '''
        # see if the word was already found
        for key in self.st.types.keys():
            if word in self.st.types[key]:
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
        '''
        Runs in the background, scans groups of tokens. 
        Returns a list of tokens in that group
        '''
        group += '#' # acts like 'other', not evaluated by any State Diagram
        results = []
        first, forward = 0, 0
        while first < len(group) and group != '#': 
            if group[first] in self.st.types['del']:
                # Buffer the potential delimiter
                target = group[first]
                temp = self.scan_word(target)
                results.append(temp)
                # print(group, target) # Debug
                group = group[1:]

            elif group and group[first] in self.st.types['opr']:
                # Buffer the entire operator token
                forward += 1
                while (group[forward] in self.st.types['opr']) and (group[forward] != '#'): 
                    forward += 1
                else: 
                    target = group[:forward] # backtrack
                    temp = self.scan_word(target)
                    results.append(temp)
                    group = group[forward:]

            elif group and (group[first] in self.char_cat.non_special | set({'$'})):
                # Buffer the entire variable token.
                forward += 1
                while (group[forward] in self.char_cat.non_special | set({'.'})) and (group[forward] != '#'):
                    forward += 1
                    # print(group, forward) # Debug
                else: 
                    target = group[:forward] # backtrack
                    temp = self.scan_word(target)
                    results.append(temp)
                    group = group[forward:]

            elif group and group[first] == '"':
                # Buffer the entire string token
                forward += 1
                while group[forward] in self.char_cat.all_chars - '"': 
                    forward += 1
                else: 
                    target = group[first:forward+1] # no backtrack
                    temp = self.scan_word(target)
                    results.append(temp)
                    group = group[forward:]
            else:
                raise KeyError(group[:-1]) # Show which part was causing the error
            
            # Bring back forward after each operation
            forward = first 
                    
        return results


    def tokenize(self, word: str) -> list[tuple[str, str]]:
        '''
        Runs in the background
        Gets a word (single or multi token) and returns the token inside that word.
        '''
        
        # see if the word was a single token:
        try:
            results = [self.scan_word(word)] 

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
                     
            if begin and end:
                cat = '"' + ' '.join(s for s in words[begin+1:end]) + '"'
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
    
        for i, line in enumerate(self.lines):
            line = line.replace('"', ' " ')

            print(f"\n\nScanning line: {i+1}")
            print("    -->", line)
            
            words = self.split(line)
            if words[1] == False: # Means some string was opened and not closed
                print(f"Error detected at line {i+1}")
                print("    --> String was opened but not closed.")

            words = words[0] # to just consider the main part from here on
            
            # Tokenize each wrod and handle exceptions.
            for word in words:
                try:
                    print(f"\nWorking on: {word}")
                    self.tokenize(word)
                except KeyError as e:
                    print(f"Error detected at line {i+1}\n    --> {e}")
                except ValueError as e:
                    print(f"Error detected at line {i+1}\n    --> {e}: {word}")
                except UnboundLocalError as e:
                    print(f"Error detected at line {i+1}\n    --> {e}: {word}")




# Debug

# code = "[ 123.234]]] for[INT+] $I] \"hello my name is erfan\" 123+456 $Gsd!d"
# # code = "[=<]"


# scanner = Scanner(code)
# scanner.run()

# print("\n\nSymbol Table: ")
# for k, v in scanner.st.types.items():
#     print(k, v)

# print("\n\nTokens: ")
# for t in scanner.tokens:
#     print(t)


