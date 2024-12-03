from Scanner import Scanner

with open("main.in", 'r') as SourceCode:
    scanner = Scanner(file=SourceCode)
    scanner.run() # logs the process in terminal


with open("SymbolTable.out", 'w') as st:
    msg = ''
    msg += "Symbol Table: "
    for k, v in scanner.st.types.items():
        msg += '\n'
        msg += f"{k:<8} {v}"
    
    st.write(msg)

with open("Tokens.out", 'w') as st:
    msg = ''
    msg += "Tokens: "
    for token in scanner.tokens:
        msg += '\n'
        msg += str(token)
    
    st.write(msg)



