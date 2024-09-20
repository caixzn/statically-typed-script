class TokenType:
    LET = 'LET'
    IDENTIFIER = 'IDENTIFIER'
    COLON = 'COLON'
    TYPE = 'TYPE'
    EQUALS = 'EQUALS'
    SEMICOLON = 'SEMICOLON'
    WHILE = 'WHILE'
    IF = 'IF'
    ELSE = 'ELSE'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    INT_LITERAL = 'INT_LITERAL'
    FLOAT_LITERAL = 'FLOAT_LITERAL'
    BOOL_LITERAL = 'BOOL_LITERAL'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'
    LESS_THAN = 'LESS_THAN'
    GREATER_THAN = 'GREATER_THAN'
    EQUAL_EQUAL = 'EQUAL_EQUAL'
    NOT_EQUAL = 'NOT_EQUAL'
    EOF = 'EOF'
    OR = 'OR'
    AND = 'AND'
    LESS_EQUAL = 'LESS_EQUAL'
    GREATER_EQUAL = 'GREATER_EQUAL'
    NOT = 'NOT'
    BREAK = 'BREAK'
    PRINT = 'PRINT'

class Token:
    def __init__(self, type: str, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', line={self.line}, column={self.column})"

class Lexer:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.position = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> list[Token]:
        tokens = []
        while self.position < len(self.source_code):
            tokens.extend(self.get_next_token())
        tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return tokens

    def get_next_token(self) -> list[Token]:
        char = self.source_code[self.position]

        if char.isspace():
            self.consume_whitespace()
            return []

        if char == '/' and self.peek() == '/':
            self.consume_comment()
            return []

        if char.isalpha() or char == '_':
            return [self.consume_identifier()]

        if char.isdigit():
            return [self.consume_number()]

        if char == '"':
            return [self.consume_string()]

        return [self.consume_symbol()]

    def consume_whitespace(self):
        while self.position < len(self.source_code) and self.source_code[self.position].isspace():
            if self.source_code[self.position] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.position += 1

    def consume_comment(self):
        while self.position < len(self.source_code) and self.source_code[self.position] != '\n':
            self.position += 1

    def consume_identifier(self) -> Token:
        start = self.position
        start_column = self.column
        while self.position < len(self.source_code) and (self.source_code[self.position].isalnum() or self.source_code[self.position] == '_'):
            self.position += 1
            self.column += 1
        value = self.source_code[start:self.position]
        
        if value in ['let', 'while', 'break', 'if', 'else', 'print', 'true', 'false']:
            token_type = value.upper()
            if value in ['true', 'false']:
                token_type = TokenType.BOOL_LITERAL
        elif value in ['int', 'float', 'bool']:
            token_type = TokenType.TYPE
        else:
            token_type = TokenType.IDENTIFIER

        return Token(token_type, value, self.line, start_column)

    def consume_number(self) -> Token:
        start = self.position
        start_column = self.column
        is_float = False
        while self.position < len(self.source_code) and (self.source_code[self.position].isdigit() or self.source_code[self.position] == '.'):
            if self.source_code[self.position] == '.':
                if is_float:
                    raise ValueError(f"Invalid number format at line {self.line}, column {self.column}")
                is_float = True
            self.position += 1
            self.column += 1
        value = self.source_code[start:self.position]
        token_type = TokenType.FLOAT_LITERAL if is_float else TokenType.INT_LITERAL
        return Token(token_type, value, self.line, start_column)

    def consume_string(self) -> Token:
        start = self.position
        start_column = self.column
        self.position += 1  # Skip opening quote
        self.column += 1
        while self.position < len(self.source_code) and self.source_code[self.position] != '"':
            if self.source_code[self.position] == '\n':
                raise ValueError(f"Unterminated string at line {self.line}")
            self.position += 1
            self.column += 1
        if self.position == len(self.source_code):
            raise ValueError(f"Unterminated string at line {self.line}")
        self.position += 1  # Skip closing quote
        self.column += 1
        value = self.source_code[start:self.position]
        return Token(TokenType.STRING_LITERAL, value, self.line, start_column)

    def consume_symbol(self) -> Token:
        char = self.source_code[self.position]
        self.position += 1
        column = self.column
        self.column += 1

        if char == ':':
            return Token(TokenType.COLON, char, self.line, column)
        elif char == '=':
            if self.position < len(self.source_code) and self.source_code[self.position] == '=':
                self.position += 1
                self.column += 1
                return Token(TokenType.EQUAL_EQUAL, '==', self.line, column)
            return Token(TokenType.EQUALS, char, self.line, column)
        elif char == ';':
            return Token(TokenType.SEMICOLON, char, self.line, column)
        elif char == '(':
            return Token(TokenType.LPAREN, char, self.line, column)
        elif char == ')':
            return Token(TokenType.RPAREN, char, self.line, column)
        elif char == '{':
            return Token(TokenType.LBRACE, char, self.line, column)
        elif char == '}':
            return Token(TokenType.RBRACE, char, self.line, column)
        elif char == '+':
            return Token(TokenType.PLUS, char, self.line, column)
        elif char == '-':
            return Token(TokenType.MINUS, char, self.line, column)
        elif char == '*':
            return Token(TokenType.MULTIPLY, char, self.line, column)
        elif char == '/':
            return Token(TokenType.DIVIDE, char, self.line, column)
        elif char == '<':
            if self.position < len(self.source_code) and self.source_code[self.position] == '=':
                self.position += 1
                self.column += 1
                return Token(TokenType.LESS_EQUAL, '<=', self.line, column)
            return Token(TokenType.LESS_THAN, char, self.line, column)
        elif char == '>':
            if self.position < len(self.source_code) and self.source_code[self.position] == '=':
                self.position += 1
                self.column += 1
                return Token(TokenType.GREATER_EQUAL, '>=', self.line, column)
            return Token(TokenType.GREATER_THAN, char, self.line, column)
        elif char == '!':
            if self.position < len(self.source_code) and self.source_code[self.position] == '=':
                self.position += 1
                self.column += 1
                return Token(TokenType.NOT_EQUAL, '!=', self.line, column)
            return Token(TokenType.NOT, char, self.line, column)
        elif char == '|' and self.position < len(self.source_code) and self.source_code[self.position] == '|':
            self.position += 1
            self.column += 1
            return Token(TokenType.OR, '||', self.line, column)
        elif char == '&' and self.position < len(self.source_code) and self.source_code[self.position] == '&':
            self.position += 1
            self.column += 1
            return Token(TokenType.AND, '&&', self.line, column)
        else:
            raise ValueError(f"Unexpected character '{char}' at line {self.line}, column {column}")

    def peek(self) -> str:
        if self.position + 1 < len(self.source_code):
            return self.source_code[self.position + 1]
        return ''
