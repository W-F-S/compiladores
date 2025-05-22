class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.code = []
        self.var_map = {}

    def generate(self):
        self.code.append(".data")
        for node in self.ast:
            if node[0] == 'declare':
                var = node[1]
                self.var_map[var] = f"var_{var}"
                self.code.append(f"{self.var_map[var]}: .word 0")
        self.code.append(".text\n.globl main\nmain:")
        for node in self.ast:
            if node[0] == 'assign':
                self.gen_assign(node[1], node[2])
            elif node[0] == 'print':
                self.gen_print(node[1])
            elif node[0] == 'function':
                _, name, args, body, ret_expr = node
                self.code.append(f"{name}:")
                for stmt in body:
                    if stmt[0] == 'assign':
                        self.gen_assign(stmt[1], stmt[2])
                    elif stmt[0] == 'print':
                        self.gen_print(stmt[1])
                self.gen_expr(ret_expr)
                self.code.append("move $v0, $t0")
                self.code.append("jr $ra")
        self.code.append("li $v0, 10\nsyscall")
        return "\n".join(self.code)


    def gen_assign(self, var, expr):
        self.gen_expr(expr)
        self.code.append(f"sw $t0, {self.var_map[var]}")

    def gen_print(self, var):
        self.code.append(f"lw $a0, {self.var_map[var]}")
        self.code.append("li $v0, 1\nsyscall")

    def gen_expr(self, expr):
        if expr[0] == 'num':
            self.code.append(f"li $t0, {expr[1]}")
        elif expr[0] == 'var':
            self.code.append(f"lw $t0, {self.var_map[expr[1]]}")
        elif expr[0] in ('PLUS', 'MINUS'):
            self.gen_expr(expr[1])
            self.code.append("sw $t0, 0($sp)\naddi $sp, $sp, -4")
            self.gen_expr(expr[2])
            self.code.append("addi $sp, $sp, 4\nlw $t1, 0($sp)")
            op = 'add' if expr[0] == 'PLUS' else 'sub'
            self.code.append(f"{op} $t0, $t1, $t0")
