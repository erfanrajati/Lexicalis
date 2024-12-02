from Ascii import char_cat # char_cat is an Object from CharCat class

class StateDiagram:
    def __init__(self, *args:tuple[tuple, str], token_type, char_cat=char_cat):
        self.products = dict()
        self.token_type = token_type
        self.char_cat = char_cat # Character Categories e.g. Lower, Upper, etc.
        for pair in args:
            self.products[pair[0]] = pair[1]

    def scan(self, word) -> tuple[str, str]:
        state = '0'
        for char in word:
            c = ''
            if char in self.char_cat.lowercase_chars:
                c = 'L'
            elif char in self.char_cat.uppercase_chars:
                c = 'U'
            elif char in self.char_cat.digits:
                c = 'D'
            else:
                c = char

            state = self.products[(state, c)] 
            # if no KeyError was raised, the token is accepted
        if state == 'A':
            return (word, self.token_type)
        else:
            raise ValueError("Token did not reach acceptance state.")

      
variable_diagram = StateDiagram(
    (('0', '$'), '1'),
    (('1', 'U'), 'A'),
    (('A', 'U'), 'A'),
    (('A', 'L'), 'A'),
    (('A', 'D'), 'A'),
    token_type="var"
)

integer_diagram = StateDiagram(
    (('0', 'D'), 'A'),
    (('A', 'D'), 'A'),
    token_type="num"
)

float_diagram = StateDiagram(
    (('0', 'D'), '1'),
    (('1', 'D'), '1'),
    (('1', '.'), '2'),
    (('2', 'D'), 'A'),
    (('A', 'D'), 'A'),
    token_type="num" 
    # Scalability: change this to float and add a float key to symbol table for more flexible syntactic analyzer
)

class_diagram = StateDiagram(
    (('0', 'U'), 'A'),
    (('A', 'U'), 'A'),
    token_type="class"
)

string_diagram = StateDiagram(
    (('0', '"'), '1'),
    *(
        (('1', char), '1') 
        for char in char_cat.all_chars if char != '"'
    ),
    (('1', '"'), 'A'),
    token_type="str"
)

# Debug
# print(variable_diagram.scan("$FDfsodn"))
# variable_diagram.scan("$F11fd")
# variable_diagram.scan("$FDfs#fdpj")

# print(float_diagram.scan("12.21"))
# print(class_diagram.scan("FDHW"))
# print(string_diagram.scan("\"helloooefhe\""))

