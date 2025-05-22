class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = set()

    def analyze(self):
        for node in self.ast:
            if node[0] == 'declare':
                if node[1] in self.symbol_table:
                    raise Exception(f"Erro semântico: variável '{node[1]}' já declarada")
                self.symbol_table.add(node[1])
            elif node[0] == 'assign':
                if node[1] not in self.symbol_table:
                    raise Exception(f"Erro semântico: variável '{node[1]}' não declarada")
                self.check_expr(node[2])
            elif node[0] == 'print':
                if node[1] not in self.symbol_table:
                    raise Exception(f"Erro semântico: variável '{node[1]}' não declarada")
            elif node[0] == 'function':
                _, name, args, body, ret_expr = node
                local_symbols = set(args)
                for stmt in body:
                    if stmt[0] == 'declare':
                        if stmt[1] in local_symbols:
                            raise Exception(f"Erro semântico: variável '{stmt[1]}' já declarada")
                        local_symbols.add(stmt[1])
                    elif stmt[0] == 'assign':
                        if stmt[1] not in local_symbols:
                            raise Exception(f"Erro semântico: variável '{stmt[1]}' não declarada")
                        self.check_expr(stmt[2], local_symbols)
                    elif stmt[0] == 'print':
                        if stmt[1] not in local_symbols:
                            raise Exception(f"Erro semântico: variável '{stmt[1]}' não declarada")
                self.check_expr(ret_expr, local_symbols)


    def check_expr(self, expr):
        if expr[0] in ('PLUS', 'MINUS'):
            self.check_expr(expr[1])
            self.check_expr(expr[2])
        elif expr[0] == 'var' and expr[1] not in self.symbol_table:
            raise Exception(f"Erro semântico: variável '{expr[1]}' não declarada")
