
import re

# LEXER SIMPLES E ROBUSTO
tokens_regras = [
    ('INT', r'int\b'),
    ('ID', r'[a-zA-Z_]\w*'),
    ('NUMBER', r'\d+'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('EQUALS', r'='),
    ('SEMICOLON', r';'),
    ('SKIP', r'[ \t\n]+'),
]

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

def lexer(input):
    tokens = []
    pos = 0
    while pos < len(input):
        match = None
        for token_type, pattern in tokens_regras:
            regex = re.compile(pattern)
            match = regex.match(input, pos)
            if match:
                if token_type != 'SKIP':
                    tokens.append(Token(token_type, match.group()))
                pos = match.end()
                break
        if not match:
            raise Exception(f'Token inválido: {input[pos]}')
    tokens.append(Token('$', '$'))
    return tokens

# PARSER LL(1) ROBUSTO COM ANÁLISE SEMÂNTICA
class ParserLL1:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.symbols = {}
        self.stack = ['$', 'programa']

        self.tab = {
            ('programa', 'INT'): ['stmt_list'],
            ('programa', 'ID'): ['stmt_list'],
            ('programa', '$'): ['stmt_list'],

            ('stmt_list', 'INT'): ['stmt', 'stmt_list'],
            ('stmt_list', 'ID'): ['stmt', 'stmt_list'],
            ('stmt_list', '$'): [],

            ('stmt', 'INT'): ['INT', 'ID', 'SEMICOLON'],
            ('stmt', 'ID'): ['ID', 'EQUALS', 'expr', 'SEMICOLON'],

            ('expr', 'ID'): ['term', 'expr_tail'],
            ('expr', 'NUMBER'): ['term', 'expr_tail'],

            ('expr_tail', 'PLUS'): ['PLUS', 'term', 'expr_tail'],
            ('expr_tail', 'MINUS'): ['MINUS', 'term', 'expr_tail'],
            ('expr_tail', 'SEMICOLON'): [],

            ('term', 'ID'): ['ID'],
            ('term', 'NUMBER'): ['NUMBER'],
        }

    def token_atual(self):
        return self.tokens[self.pos]

    def match(self, esperado):
        atual = self.token_atual()
        if atual.type == esperado:
            self.pos += 1
            return atual
        raise Exception(f'Erro sintático: Esperado {esperado}, obteve {atual.type}')

    def parse(self):
        while self.stack:
            topo = self.stack.pop()
            token = self.token_atual()

            if topo in ('INT', 'ID', 'NUMBER', 'PLUS', 'MINUS', 'EQUALS', 'SEMICOLON', '$'):
                self.match(topo)

            elif (topo, token.type) in self.tab:
                prod = self.tab[(topo, token.type)]
                for s in reversed(prod):
                    self.stack.append(s)

                if prod == ['INT', 'ID', 'SEMICOLON']:
                    var_token = self.tokens[self.pos + 1]  # pos atual é INT, próximo é ID
                    var_nome = var_token.value
                    if var_nome in self.symbols:
                        raise Exception(f'Erro semântico: variável "{var_nome}" já declarada.')
                    self.symbols[var_nome] = 'int'

                if prod == ['ID', 'EQUALS', 'expr', 'SEMICOLON']:
                    var_nome = token.value
                    if var_nome not in self.symbols:
                        raise Exception(f'Erro semântico: variável "{var_nome}" não declarada.')

                if prod == ['ID']:
                    var_nome = token.value
                    if var_nome not in self.symbols:
                        raise Exception(f'Erro semântico: variável "{var_nome}" não declarada.')

            else:
                raise Exception(f'Erro sintático inesperado: {topo} com token {token.type}')

        return self.symbols

if __name__ == "__main__":
    codigo = """
        int x;
        int y;
        x = 10;
        y = x + 20;
    """
    tokens = lexer(codigo)
    parser = ParserLL1(tokens)
    simbolos = parser.parse()
    print("Análise concluída com sucesso.")
    print("Tabela de símbolos:", simbolos)
