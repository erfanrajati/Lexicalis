import SymbolTable
from Ascii import char_cat
from StateDiagram import *

class Scanner:
    def __init__(self, file, st=SymbolTable.st, char_cat=char_cat):
        '''main initializer, uses file input'''
        self.st = st
        self.char_cat = char_cat
        self.lines: list[str] = file.readlines()
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
                
                # Add the new token to Token list
                self.tokens.append(result) 
                
                # Log
                # print(f"Token found: {result}")
                return result

        # if the word wasn't already found
        first = word[0]
        if first == '$': # Variabale
            result = variable_diagram.scan(word)

        elif first in self.char_cat.uppercase_chars: # Class names
            result = class_diagram.scan(word)

        elif first in self.char_cat.digits: # Numberic
            try:
                result = integer_diagram.scan(word)
            except:
                result = float_diagram.scan(word)
            
        elif first == '"': # String literal
            result = string_diagram.scan(word)

        # Add the new token to Symbol Table and Token list
        self.tokens.append(result) 
        self.st.types[result[1]].add(result[0])
        
        # Log
        # print(f"Token found: {result}")
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

            elif group[first] in self.st.types['opr']:
                # Buffer the entire operator token
                forward += 1
                while (group[forward] in self.st.types['opr']) and (group[forward] != '#'): 
                    forward += 1
                else: 
                    target = group[:forward] # backtrack
                    temp = self.scan_word(target)
                    results.append(temp)
                    group = group[forward:]

            elif (group[first] in self.char_cat.non_special | set({'$'})):
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

            elif group[first] == '"': # Can't happen now, because of the new split method!
                pass
            #     # Buffer the entire string token
            #     forward += 1
            #     while group[forward] in self.char_cat.all_chars - '"': 
            #         forward += 1
            #     else: 
            #         target = group[first:forward+1] # no backtrack
            #         temp = self.scan_word(target)
            #         results.append(temp)
            #         group = group[forward:]
            
            else:
                raise KeyError(group[:-1]) # Show which part was causing the error (Except #)
            
            # Bring back forward after each operation
            forward = first 
                    
        return results


    def tokenize(self, word: str) -> list[tuple[str, str]]:
        '''
        Runs in the background.
        Gets a word (single or multi token) and returns the tokens inside that word.
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


    def split(self, line: str) -> list[str]:
        '''
        Splits the input line of code by space. 
        But leaves the strings whole as the should be.
        Returns the a tuple containing the list of words and 
        error status that shows if the strings where all closed. (False means not Closed)
        '''
        line = line.replace('"', ' " ')
        words = line.split()
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
                print(f"Error detected")
                print("    --> String was opened but not closed.")
                return words
            
            else: # No string is left
                break
        return words


    def run(self):
        '''Tokenizes the given file.'''   
        for i, line in enumerate(self.lines):
            line = line.replace('"', ' " ')
            print("-----------------------")
            print(f"Scanning line: {i+1}")
            print("    --> ", line.strip(), '\n')
            words = self.split(line)
            
            # Tokenize each wrod and handle exceptions.
            for word in words:
                try:
                    # Log
                    # print(f"\nWorking on: {word}")
                    self.tokenize(word)
                except KeyError as e:
                    print(f"Error detected\n    --> {e}")
                except ValueError as e:
                    print(f"Error detected\n    --> {e}: {word}")
                except UnboundLocalError as e:
                    print(f"Error detected\n    --> {e}: {word}")




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


