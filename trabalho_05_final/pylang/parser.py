import ply.yacc as yacc
from .lexer import tokens, lexer

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
)

def p_program(p):
    '''program : statements'''
    p[0] = p[1]

def p_statements(p):
    '''statements : statements statement
                 | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : expression SEMICOLON
                | assignment SEMICOLON
                | conditional
                | loop
                | function_declaration
                | return_statement SEMICOLON
                | print_statement SEMICOLON
                | input_statement SEMICOLON
                | block'''
    p[0] = p[1]

def p_expression(p):
    '''expression : expression PLUS expression
                 | expression MINUS expression
                 | expression TIMES expression
                 | expression DIVIDE expression
                 | expression MODULO expression
                 | expression EQ expression
                 | expression NEQ expression
                 | expression LT expression
                 | expression LE expression
                 | expression GT expression
                 | expression GE expression
                 | expression AND expression
                 | expression OR expression
                 | NOT expression
                 | LPAREN expression RPAREN
                 | value'''
    # Lógica de construção da árvore sintática
    if len(p) == 4:
        if p[1] == '(':
            p[0] = p[2]
        else:
            p[0] = (p[2], p[1], p[3])  # (operador, lado esquerdo, lado direito)
    elif len(p) == 3:
        p[0] = (p[1], p[2])  # Operador unário (NOT)
    else:
        p[0] = p[1]  # value

def p_conditional(p):
    '''conditional : IF LPAREN expression RPAREN statement
                  | IF LPAREN expression RPAREN statement ELSE statement'''
    if len(p) == 6:  # if without else
        p[0] = ('if', p[3], p[5])
    else:  # if with else (len == 8)
        p[0] = ('if-else', p[3], p[5], p[7])


def p_return_statement(p):
    '''return_statement : RETURN expression
                       | RETURN'''
    if len(p) == 3:  # Return with value
        p[0] = ('return', p[2])
    else:  # Empty return
        p[0] = ('return', None)

def p_print_statement(p):
    '''print_statement : PRINT LPAREN expression RPAREN'''
    p[0] = ('print', p[3])

def p_input_statement(p):
    '''input_statement : INPUT LPAREN STRING RPAREN
                      | INPUT LPAREN RPAREN'''
    if len(p) == 5:
        p[0] = ('input', p[3])
    else:
        p[0] = ('input', '')

def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN statement'''
    p[0] = ('while', p[3], p[5])  # (condição, corpo)

def p_value(p):
    '''value : NUMBER
             | STRING
             | ID
             | boolean
             | function_call'''
    p[0] = ('value', p[1])

def p_boolean(p):
    '''boolean : TRUE
              | FALSE'''
    p[0] = ('boolean', p[1] == 'verdadeiro')  # Converts to Python bool

def p_arg_list(p):
    '''arg_list : arg_list COMMA expression
               | expression
               | empty'''
    if len(p) == 4:  # Multiple arguments
        p[0] = p[1] + [p[3]]
    elif len(p) == 2:  # Single argument or empty
        p[0] = [p[1]] if p[1] is not None else []

def p_empty(p):
    'empty :'
    p[0] = None

def p_assignment(p):
    '''assignment : ID ASSIGN expression'''
    p[0] = ('assign', p[1], p[3])

def p_loop(p):
    '''loop : WHILE LPAREN expression RPAREN statement
            | FOR LPAREN assignment SEMICOLON expression SEMICOLON assignment RPAREN statement'''
    if p[1] == 'enquanto':
        p[0] = ('while', p[3], p[5])
    else:
        p[0] = ('for', p[3], p[5], p[7], p[9])

def p_function_declaration(p):
    '''function_declaration : FUNCTION ID LPAREN params RPAREN block'''
    p[0] = ('function', p[2], p[4], p[6])

def p_params(p):
    '''params : param_list
              | empty'''
    p[0] = p[1] if len(p) > 1 else []

def p_param_list(p):
    '''param_list : param_list COMMA ID
                 | ID'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_function_call(p):
    '''function_call : ID LPAREN arg_list RPAREN'''
    p[0] = ('function-call', p[1], p[3])

def p_block(p):
    '''block : LBRACE statements RBRACE'''
    p[0] = ('block', p[2])

def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p}'")
    else:
        print("Erro de sintaxe no final do arquivo")

parser = yacc.yacc()

