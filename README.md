

# Lexicalis

**Lexicalis** is a Python-based lexical analyzer designed to tokenize source code written in an imaginary programming language. The project is robust, flexible, and features detailed inline documentation to help users understand and extend its functionality. This documentation provides a structured guide to the design, functionality, and usage of Lexicalis.

---

## Features

- **Symbol Table:** Stores predefined tokens such as keywords, operators, and delimiters. and fills out with newly found tokens along the way.
- **State Diagrams:** Used to validate and classify tokens like variables, numbers, strings, and classes.
- **Comprehensive Error Handling:** Ensures invalid tokens are flagged appropriately.
- **Extendability:** Designed to support the addition of new token types and patterns.

---

## How It Works

The analyzer follows a structured flow, as depicted in the flowchart below:

1. **Source Input**: A source code string is provided.
2. **Line Splitting**: The source is split into lines and then into individual words (potential tokens).
3. **Word Scanning**: Each word can either be a single token or a group of tokens, which will be fed into `scan_word()` or `scan_group()` for any of those cases respectively.
3. **Token Validation**:
   - Each word is checked against the **Symbol Table (ST)** to see if it's already found.
   - If not found, the token is validated using **State Diagrams**.
4. **Accepted Tokens**: Valid tokens are categorized and stored in the symbol table.
5. **Error Reporting**: If a token cannot reach a valid acceptance state, an error is raised.

### Flowchart

For a visual representation, refer to the flowchart below:
```ascii art

                   +-------------------+
                   |    Source Code    |
                   +-------------------+
                            |
                            v
                   +-------------------+
                   |   Split to Lines  |
                   +-------------------+
                            |
                            v
                   +-------------------+
                   |  Split to Words   |
                   +-------------------+
                            |
                            v
                   +-------------------+
                   |  Tokenize Words   |
                   +-------------------+
                            |
         +------------------+------------------+
         |                                     |
 +------------------+                 +----------------------+
 |   Single Token   |                 |   Group of Tokens    |
 +------------------+                 +----------------------+
         |                                       |
         v                                       v
 +------------------+                 +----------------------+
 |   scan_word()    |  <------+       |     scan_group()     |
 +------------------+         |       +----------------------+
         |                    |                  |
         v                    |                  v
 +----------------------+     |     +-------------------------+
 |  Check Symbol Table  |     +---- | Split Group into Tokens |
 +----------------------+           +-------------------------+
         |               \                       
 +-----------------+      \           +-------------------+
 |  Found Already  |       \------->  |   Not Found Yet   |
 +-----------------+                  +-------------------+
         |                                     |
         v                                     v
    +------------+                  +-------------------+
    |    Done    | <--------------  |   State Diagram   |
    +------------+                  +-------------------+


```

## Code Overview

### 1. **Scanner Class**
The `Scanner` class orchestrates the tokenization process. It relies on the `SymbolTable` and `StateDiagram` classes to identify and validate tokens.

Key Methods:
- **`tokenize(source: str)`**:
  - Splits the source code into lines and words.
  - Passes each word through `scan_word` and `scan_group`.
- **`scan_word(word: str)`**:
  - Checks if the word exists in the Symbol Table.
  - If not found, delegates to State Diagram for validation.
- **`scan_group(group: list[str])`**:
  - Processes multi-character tokens, combining symbols into a valid group.

### 2. **SymbolTable Class**
The `SymbolTable` acts as a central repository for all token types. It maintains token sets like:
- **Keywords**: `while`, `for`, `if`, `else`
- **Operators**: `+`, `-`, `==`, `div`
- **Delimiters**: `{`, `}`, `;`

Users can add or modify tokens for customization.

### 3. **StateDiagram Class**
Implements finite automata to validate complex tokens. It defines a transition map (`products`) for each token type.

Example Diagrams:
- **Variable**: Recognizes identifiers starting with `$`.
- **Number**: Validates integers and floating-point numbers.
- **String**: Detects strings enclosed in quotes.

---

## Example Usage

Here’s a simple example demonstrating how to use Lexicalis:

```python
from Scanner import Scanner

source_code = """
    while x < 10 {
        print("Hello, world!")
    }
"""

scanner = Scanner()
tokens = scanner.tokenize(source_code)

for token_type, token_value in tokens:
    print(f"{token_type}: {token_value}")
```

Expected Output:
```
kw: while
var: x
opr: <
num: 10
del: {
func: print
str: "Hello, world!"
del: }
```

---

## Error Handling

Invalid tokens or unrecognized patterns raise a `ValueError` with descriptive messages, aiding debugging and error resolution.

Example:
```python
scanner.scan_word("$Invalid#Token") 
# Output: ValueError: Token did not reach acceptance state.
```

---

## Extending Lexicalis

1. **Adding New Tokens**:
   - Update the `SymbolTable` with the new token type and values.
2. **Custom State Diagrams**:
   - Create a new `StateDiagram` instance with the required transition map.

Example:
```python
custom_diagram = StateDiagram(
    (('0', 'C'), '1'),
    (('1', 'U'), 'A'),
    token_type="custom"
)
```

---

## Future Enhancements

- **Support for Multi-line Strings**.
- **Integration with Syntactic Analyzers**.
- **Interactive Visualizations of Tokenization**.

---

Feel free to reach out or contribute to Lexicalis.


