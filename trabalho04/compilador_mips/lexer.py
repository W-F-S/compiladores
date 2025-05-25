import re

TOKENS = [
    ('INT', r'int'),
    ('PRINT', r'print'),
    ('NUMBER', r'\d+'),
    ('ID', r'[a-zA-Z_]\w*'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('EQUALS', r'='),
    ('SEMICOLON', r';'),
    ('WHITESPACE', r'[ \t\n]+'),
    ('UNKNOWN', r'.'),
    ('FUNCTION', r'function'),
    ('RETURN', r'return'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('COMMA', r',')
]

class Lexer:
    def __init__(self, code):
        self.tokens = []
        self.code = code

    def tokenize(self):
        pos = 0
        while pos < len(self.code):
            match = None
            for token_type, token_regex in TOKENS:
                regex = re.compile(token_regex)
                match = regex.match(self.code, pos)
                if match:
                    if token_type != 'WHITESPACE':
                        token_value = match.group(0)
                        self.tokens.append((token_type, token_value))
                    pos = match.end(0)
                    break
            if not match:
                raise Exception(f'erro lexer, símbolo desconhecido {self.code[pos]}')
        return self.tokens
