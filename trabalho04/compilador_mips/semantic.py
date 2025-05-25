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
                self.analyze_function(node)

    def analyze_function(self, node):
        _, name, params, body, ret_expr = node
        function_scope = set()

        # Add parameters to function scope
        for param_type, param_name in params:
            if param_name in function_scope:
                raise Exception(f"Duplicate parameter name: {param_name}")
            function_scope.add(param_name)

        # Analyze function body
        for stmt in body:
            if stmt[0] == 'declare':
                var_name = stmt[1]
                if var_name in function_scope:
                    raise Exception(f"Duplicate variable: {var_name}")
                function_scope.add(var_name)
            elif stmt[0] == 'assign':
                var_name = stmt[1]
                if var_name not in function_scope:
                    raise Exception(f"Undeclared variable: {var_name}")
                self.check_expr(stmt[2], function_scope)
            elif stmt[0] == 'print':
                var_name = stmt[1]
                if var_name not in function_scope:
                    raise Exception(f"Undeclared variable: {var_name}")

        # Check return expression
        self.check_expr(ret_expr, function_scope)

    def check_expr(self, expr, symbol_table=None):
        symbol_table = symbol_table or self.symbol_table
        if expr[0] in ('PLUS', 'MINUS'):
            self.check_expr(expr[1], symbol_table)
            self.check_expr(expr[2], symbol_table)
        elif expr[0] == 'var':
            if expr[1] not in symbol_table:
                raise Exception(f"Undeclared variable: {expr[1]}")

