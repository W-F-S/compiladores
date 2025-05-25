class CodeGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.code = []
        self.var_map = {}

    def generate(self):
        self.code.append(".data")
        # Global variables
        for node in self.ast:
            if node[0] == 'declare':
                var = node[1]
                self.var_map[var] = f"var_{var}"
                self.code.append(f"{self.var_map[var]}: .word 0")

        self.code.append(".text\n.globl main\nmain:")

        # Generate code for main program
        for node in self.ast:
            if node[0] == 'assign':
                self.gen_assign(node[1], node[2])
            elif node[0] == 'print':
                self.gen_print(node[1])
            elif node[0] == 'function':
                self.gen_function(node)

        self.code.append("li $v0, 10\nsyscall")
        return "\n".join(self.code)

    def gen_function(self, node):
        _, name, params, body, ret_expr = node

        # Function prologue
        self.code.append(f"{name}:")
        self.code.append("addi $sp, $sp, -8")  # Make space for $ra and $fp
        self.code.append("sw $ra, 4($sp)")    # Save return address
        self.code.append("sw $fp, 0($sp)")    # Save frame pointer
        self.code.append("move $fp, $sp")     # Set new frame pointer

        # Allocate space for parameters and local variables
        stack_offset = 8  # Start after $ra and $fp
        local_vars = {}

        # Process parameters (passed in $a0, $a1, etc.)
        for i, (param_type, param_name) in enumerate(params):
            if i < 4:  # MIPS first 4 args in $a0-$a3
                self.code.append(f"sw $a{i}, {stack_offset}($fp)")
            else:
                # Additional args would be on stack above $fp
                pass
            local_vars[param_name] = stack_offset
            stack_offset += 4

        # Process local declarations
        for stmt in body:
            if stmt[0] == 'declare':
                var_name = stmt[1]
                local_vars[var_name] = stack_offset
                stack_offset += 4
                self.code.append(f"addi $sp, $sp, -4")  # Allocate space

        # Generate function body
        for stmt in body:
            if stmt[0] == 'assign':
                var_name = stmt[1]
                self.gen_expr(stmt[2])
                self.code.append(f"sw $t0, {local_vars[var_name]}($fp)")
            elif stmt[0] == 'print':
                var_name = stmt[1]
                self.code.append(f"lw $a0, {local_vars[var_name]}($fp)")
                self.code.append("li $v0, 1\nsyscall")

        # Generate return expression
        self.gen_expr(ret_expr)
        self.code.append("move $v0, $t0")  # Return value in $v0

        # Function epilogue
        self.code.append("move $sp, $fp")  # Restore stack pointer
        self.code.append("lw $ra, 4($sp)") # Restore return address
        self.code.append("lw $fp, 0($sp)") # Restore frame pointer
        self.code.append("addi $sp, $sp, 8") # Restore stack
        self.code.append("jr $ra")         # Return


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
