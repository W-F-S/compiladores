import ply.lex as lex
import ply.yacc as yacc
import math

# --- Ambiente de execução ---
variables = {}
functions = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'sqrt': math.sqrt,
    'log': math.log10,
    'ln': math.log,
    'exp': math.exp,
    'abs': abs,
    'round': round
}

# --- Análise Léxica (Lex) ---

tokens = (
    'INTEGER',
    'FLOAT',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'POWER',
    'LPAREN',
    'RPAREN',
    'EQUALS',
    'IDENTIFIER',
    'COMMENT_SINGLE',
    'COMMENT_MULTI'
)

# Operadores
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_POWER   = r'\^'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# Identificadores
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = 'IDENTIFIER'
    return t

# Números
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Comentários
def t_COMMENT_SINGLE(t):
    r'//.*'
    pass  # Ignora comentários de linha

def t_COMMENT_MULTI(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')  # Atualiza contador de linhas
    pass  # Ignora comentários multi-linha

# Controle de linhas e espaços
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Tratamento de erros léxicos
def t_error(t):
    print(f"caractere inválido '{t.value[0]}', linha {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir o lexer
lexer = lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
    ('right', 'POWER'),
)

def p_expression_binop(p):
    p[0] = (p[2], p[1], p[3])

def p_expression_uminus(p):
    p[0] = ('neg', p[2])

def p_expression_group(p):
    p[0] = p[2]

def p_expression_number(p):
    p[0] = p[1]

def p_expression_identifier(p):
    if p[1] in variables:
        p[0] = variables[p[1]]
    else:
        print(f"Variável não definida: '{p[1]}'")
        p[0] = 0

def p_expression_function(p):
    if p[1] in functions:
        p[0] = ('call', p[1], p[3])
    else:
        print(f"Função não definida: '{p[1]}'")
        p[0] = 0

def p_assignment(p):
    'expression : IDENTIFIER EQUALS expression'
    variables[p[1]] = p[3]
    p[0] = ('=', p[1], p[3])

# Tratamento de erros com recuperação
def p_error(p):
    if p:
        print(f"Erro de sintaxe - Token: {p}")
        print(f"Detalhes: type='{p.type}', value='{p.value}', lineno={p.lineno}, lexpos={p.lexpos}")

        if p.type in ('PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER'):
            print("Operador duplicado ou operando faltante")
        elif p.type == 'LPAREN':
            print("Parêntese não fechado")
        elif p.type == 'RPAREN':
            print("Parêntese não aberto")
        else:
            print("Expressão inválida")
    else:
        print("Erro no final da entrada")

# Construir o parser
parser = yacc.yacc()

# --- Funções para AST ---
def build_ast(expr):
    if isinstance(expr, tuple):
        return (expr[0], build_ast(expr[1]), build_ast(expr[2]))
    elif isinstance(expr, list):
        return [build_ast(e) for e in expr]
    else:
        return expr

def print_ast(ast, level=0):
    if isinstance(ast, tuple):
        print('  ' * level + '(' + str(ast[0]))
        print_ast(ast[1], level+1)
        print_ast(ast[2], level+1)
        print('  ' * level + ')')
    else:
        print('  ' * level + str(ast))

# --- Avaliador de expressões ---
def evaluate(node):
    if isinstance(node, (int, float)):
        return node

    if isinstance(node, str):
        return variables.get(node, 0)

    if isinstance(node, tuple):
        if node[0] == '=':
            variables[node[1]] = evaluate(node[2])
            return variables[node[1]]
        elif node[0] == 'call':
            func = functions.get(node[1])
            if func:
                arg = evaluate(node[2])
                return func(arg)
            else:
                print(f"Função não definida: {node[1]}")
                return 0
        elif node[0] == 'neg':
            return -evaluate(node[1])
        else:
            left = evaluate(node[1])
            right = evaluate(node[2])

            if node[0] == '+': return left + right
            elif node[0] == '-': return left - right
            elif node[0] == '*': return left * right
            elif node[0] == '/': return left / right
            elif node[0] == '^': return left ** right

    return 0

def process_file(input_file):
    with open(input_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('//'):
                continue

            result = parser.parse(line)
            ast = build_ast(result)
            value = evaluate(result)

            print(f"\nLinha {line_num}: {line}")
            print("AST:")
            print_ast(ast)
            print(f"Resultado: {value}")

if __name__ == '__main__':
    import sys
    input_file = sys.argv[1]
    process_file(input_file)
