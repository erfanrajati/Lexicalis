from Ascii import cc # cc is an Object from CharCat class

class StateDiagram:
    def __init__(self, *args:tuple[tuple, str], cc=cc):
        self.products = dict()
        self.cc = cc # Character Categories e.g. Lower, Upper, etc.
        for pair in args:
            self.products[pair[0]] = pair[1]

    def scan(self, word):
        state = '0'
        for char in word:
            c = ''
            if char in self.cc.lowercase_chars:
                c = 'L'
            elif char in self.cc.uppercase_chars:
                c = 'U'
            elif char in self.cc.digits:
                c = 'D'
            else:
                c = char

            state = self.products[(state, c)] 
            # if no KeyError was raised, the token is accepted
        if state == 'A':
            return (word, "var")
        else:
            raise ValueError("Token did not reach acceptance state.")

        
variable_diagram = StateDiagram(
    (('0', '$'), '1'),
    (('1', 'U'), 'A'),
    (('A', 'U'), 'A'),
    (('A', 'L'), 'A'),
    (('A', 'D'), 'A'),
)

integer_diagram = StateDiagram(
    (('0', 'D'), 'A'),
    (('A', 'D'), 'A'),
)

float_diagram = StateDiagram(
    (('0', 'D'), '1'),
    (('1', 'D'), '1'),
    (('1', '.'), '2'),
    (('2', 'D'), 'A'),
    (('A', 'D'), 'A'),
)

# Debug
variable_diagram.scan("$FDfsodn")
variable_diagram.scan("$F11fd")
variable_diagram.scan("$FDfs#fdpj")

