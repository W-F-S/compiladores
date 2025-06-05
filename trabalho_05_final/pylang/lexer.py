import ply.lex as lex

reserved = {
    'se': 'IF',
    'senao': 'ELSE',
    'enquanto': 'WHILE',
    'para': 'FOR',
    'funcao': 'FUNCTION',
    'retorne': 'RETURN',
    'verdadeiro': 'TRUE',
    'falso': 'FALSE',
    'escreva': 'PRINT',
    'leia': 'INPUT',
    'e': 'AND',
    'ou': 'OR',
    'nao': 'NOT'
}

tokens = [
    'NUMBER', 'STRING', 'ID',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE',
    'ASSIGN', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE',
    'COMMA', 'SEMICOLON'
] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_EQ = r'=='
t_NEQ = r'!='
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_ASSIGN = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'

t_ignore = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+\.?\d*'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Erro léxico: Caractere ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
