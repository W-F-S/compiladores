class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.current_return = None


    def evaluate_expression(self, expr):
        # DEBUG (opcional)
        print(f"\n[DEBUG] Avaliando: {expr} | Variáveis: {self.variables}")


        if expr is None:
            print("Expressão None")


        if isinstance(expr, (int, float, str)) and not isinstance(expr, tuple):
            if isinstance(expr, str) and expr in self.variables:
                return self.variables[expr]
            return expr

        # Caso 2: Expressão é uma operação (tupla)
        elif isinstance(expr, tuple):
            # Operações binárias (+, -, >, etc)
            if len(expr) == 3:
                op, left, right = expr
                left_val = self.evaluate_expression(left)
                right_val = self.evaluate_expression(right)

                # Verificação de tipos
                if None in (left_val, right_val):
                    raise ValueError(f"Operandos não podem ser None: {left_val} {op} {right_val}")

                # Operações matemáticas
                if op == '+': return left_val + right_val
                elif op == '-': return left_val - right_val
                elif op == '*': return left_val * right_val
                elif op == '/': return left_val / right_val
                # Operações de comparação
                elif op == '>': return left_val > right_val
                elif op == '<': return left_val < right_val
                elif op == '>=': return left_val >= right_val
                elif op == '<=': return left_val <= right_val
                elif op == '==': return left_val == right_val
                elif op == '!=': return left_val != right_val
                # Operações lógicas
                elif op == 'AND': return left_val and right_val
                elif op == 'OR': return left_val or right_val

            # Operador unário NOT
            elif len(expr) == 2 and expr[0] == 'NOT':
                val = self.evaluate_expression(expr[1])
                return not val



    def interpret(self, node):
        """Interpreta um nó da árvore sintática"""
        if node is None:
            return None

        # Nó do tipo programa (lista de statements)
        if isinstance(node, list):
            for statement in node:
                self.interpret(statement)
            return

        # Atribuição de variável
        if node[0] == 'assign':
            var_name = node[1]
            value = self.interpret(node[2])
            self.variables[var_name] = value
            return value

        # Expressões matemáticas
        elif node[0] in ('+', '-', '*', '/', '%'):
            left = self.interpret(node[1])
            right = self.interpret(node[2])

            if node[0] == '+': return left + right
            elif node[0] == '-': return left - right
            elif node[0] == '*': return left * right
            elif node[0] == '/': return left / right
            elif node[0] == '%': return left % right

        # Expressões lógicas
        elif node[0] in ('==', '!=', '<', '<=', '>', '>=', 'AND', 'OR'):
            left = self.interpret(node[1])
            right = self.interpret(node[2])

            if node[0] == '==': return left == right
            elif node[0] == '!=': return left != right
            elif node[0] == '<': return left < right
            elif node[0] == '<=': return left <= right
            elif node[0] == '>': return left > right
            elif node[0] == '>=': return left >= right
            elif node[0] == 'AND': return left and right
            elif node[0] == 'OR': return left or right

        # Operador NOT
        elif node[0] == 'NOT':
            return not self.interpret(node[1])

        # Estrutura condicional IF
        elif node[0] == 'if':
            condition = self.interpret(node[1])
            if condition:
                return self.interpret(node[2])


        elif node[0] == 'if-else':
            condition = self.interpret(node[1])
            if condition:
                return self.interpret(node[2])
            else:
                return self.interpret(node[3])


        elif node[0] == 'while':
            condition, body = node[1], node[2]

            while True:
                condition_result = self.evaluate_expression(condition)
                if condition_result is None:
                    print("Aviso: Condição do 'enquanto' retornou None")
                    break
                if not condition_result:
                    break
                self.interpret(body)

        # Loop FOR
        elif node[0] == 'for':
            self.interpret(node[1])  # Inicialização
            while self.interpret(node[2]):  # Condição
                result = self.interpret(node[4])  # Corpo
                if result is not None:
                    return result
                self.interpret(node[3])  # Incremento

        # Bloco de código
        elif node[0] == 'block':
            for statement in node[1]:
                result = self.interpret(statement)
                if result is not None:
                    return result

        # Declaração de função
        elif node[0] == 'function-decl':
            func_name = node[1]
            params = node[2]
            body = node[3]
            self.functions[func_name] = (params, body)

        # Chamada de função
        elif node[0] == 'function-call':
            func_name = node[1]
            args = node[2]

            if func_name in self.functions:
                params, body = self.functions[func_name]

                # Salva o estado atual
                old_vars = self.variables.copy()

                # Cria novo escopo
                self.variables = {}

                # Passa os parâmetros
                for param, arg in zip(params, args):
                    self.variables[param] = self.interpret(arg)

                # Executa a função
                result = None
                try:
                    self.interpret(body)
                except Exception as e:
                    if str(e) == 'return':
                        result = self.current_return

                # Restaura o escopo anterior
                self.variables = old_vars

                return result
            else:
                raise Exception(f"Função '{func_name}' não definida")

        # Comando RETURN
        elif node[0] == 'return':
            self.current_return = self.interpret(node[1])
            raise Exception('return')  # Usado para sair da função

        # Comando PRINT
        elif node[0] == 'print':
            value = self.interpret(node[1])
            print(value)

        # Comando INPUT
        elif node[0] == 'input':
            prompt = node[1] if len(node) > 1 else ""
            return input(prompt)

        # Valores literais
        elif node[0] == 'value':
            if isinstance(node[1], str) and node[1] in self.variables:
                return self.variables[node[1]]
            return node[1]


        elif node[0] == 'boolean':
            return node[1]

        elif isinstance(node, str):
            if node in self.variables:
                return self.variables[node]
            raise Exception(f"Variável '{node}' não definida")

        # Números e strings diretamente
        elif isinstance(node, (int, float, str)):
            return node

        else:
            raise Exception(f"Tipo de nó desconhecido: {node}")
