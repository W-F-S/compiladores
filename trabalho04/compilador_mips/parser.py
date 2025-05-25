from lexer import Lexer

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.ast = []

    def match(self, expected):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == expected:
            self.pos += 1
        else:
            raise Exception(f"Erro sintático: esperado {expected}")

    def parse(self):
        while self.pos < len(self.tokens):
            if self.tokens[self.pos][0] == 'INT':
                self.parse_declaration()
            elif self.tokens[self.pos][0] == 'ID':
                self.parse_assignment()
            elif self.tokens[self.pos][0] == 'PRINT':
                self.parse_print()
            elif self.tokens[self.pos][0] == 'FUNCTION':
                self.parse_function()
            else:
                raise Exception("erro parser, comando desconhecido")
        return self.ast

    def parse_declaration(self):
        self.match('INT')
        var_name = self.tokens[self.pos][1]
        self.match('ID')
        self.match('SEMICOLON')
        self.ast.append(('declare', var_name))

    def parse_assignment(self):
        var_name = self.tokens[self.pos][1]
        self.match('ID')
        self.match('EQUALS')
        expr = self.parse_expression()
        self.match('SEMICOLON')
        self.ast.append(('assign', var_name, expr))

    def parse_print(self):
        self.match('PRINT')
        var_name = self.tokens[self.pos][1]
        self.match('ID')
        self.match('SEMICOLON')
        self.ast.append(('print', var_name))


    def parse_function(self):
        self.match('FUNCTION')
        func_name = self.tokens[self.pos][1]
        self.match('ID')
        self.match('LPAREN')

        # Parse parameters
        params = []
        if self.tokens[self.pos][0] != 'RPAREN':
            while True:
                param_type = self.tokens[self.pos][0]  # Should be 'INT' or other type
                self.match(param_type)
                param_name = self.tokens[self.pos][1]
                self.match('ID')
                params.append((param_type, param_name))

                if self.tokens[self.pos][0] == 'COMMA':
                    self.match('COMMA')
                else:
                    break

        self.match('RPAREN')
        self.match('LBRACE')

        # Parse function body
        body = []
        while self.tokens[self.pos][0] != 'RBRACE':
            if self.tokens[self.pos][0] == 'INT':
                body.append(self.parse_declaration())
            elif self.tokens[self.pos][0] == 'ID':
                body.append(self.parse_assignment())
            elif self.tokens[self.pos][0] == 'PRINT':
                body.append(self.parse_print())
            elif self.tokens[self.pos][0] == 'RETURN':
                break

        # Parse return statement
        self.match('RETURN')
        ret_expr = self.parse_expression()
        self.match('SEMICOLON')
        self.match('RBRACE')

        self.ast.append(('function', func_name, params, body, ret_expr))

    def parse_expression(self):
        term = self.parse_term()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ('PLUS', 'MINUS'):
            op = self.tokens[self.pos][0]
            self.pos += 1
            next_term = self.parse_term()
            term = (op, term, next_term)
        return term

    def parse_term(self):
        if self.tokens[self.pos][0] == 'NUMBER':
            val = int(self.tokens[self.pos][1])
            self.pos += 1
            return ('num', val)
        elif self.tokens[self.pos][0] == 'ID':
            var_name = self.tokens[self.pos][1]
            self.pos += 1
            return ('var', var_name)
        else:
            raise Exception("Erro sintático: termo inválido")
