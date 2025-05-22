import ply.lex as lex
import ply.yacc as yacc
from llvmlite import ir
import llvmlite.binding as llvm

# --- Análise Léxica ---

tokens = (
    'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN'
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NUMBER = r'\d+'

t_ignore = ' \t\n'

def t_error(t):
    print(f"Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

# --- Análise Sintática ---

class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        self.children = children if children is not None else []
        self.leaf = leaf

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = Node('binop', [p[1], p[3]], p[2])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = Node('number', leaf=p[1])

def p_expression_paren(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    print("Erro de sintaxe!")

parser = yacc.yacc()

# --- Geração de Código LLVM IR ---

class CodeGenerator:
    def __init__(self):
        self.module = ir.Module(name="expr")
        self.func_type = ir.FunctionType(ir.IntType(32), [])
        self.func = ir.Function(self.module, self.func_type, name="main")
        self.block = self.func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(self.block)

    def generate(self, node):
        if node.type == 'number':
            return ir.Constant(ir.IntType(32), int(node.leaf))
        elif node.type == 'binop':
            left = self.generate(node.children[0])
            right = self.generate(node.children[1])
            if node.leaf == '+':
                return self.builder.add(left, right, name="addtmp")
            elif node.leaf == '-':
                return self.builder.sub(left, right, name="subtmp")
            elif node.leaf == '*':
                return self.builder.mul(left, right, name="multmp")
            elif node.leaf == '/':
                return self.builder.sdiv(left, right, name="divtmp")
        raise Exception(f"Tipo de nó inválido: {node.type}")

    def finalize(self):
        # Retorna o resultado da expressão (armazenado em eax para NASM)
        result = self.generate(self.ast)
        self.builder.ret(result)
        return str(self.module)

    def set_ast(self, ast):
        self.ast = ast

# --- Função Principal ---

def compile_expression(expression):
    ast = parser.parse(expression)
    if ast:
        code_gen = CodeGenerator()
        code_gen.set_ast(ast)
        llvm_ir = code_gen.finalize()
        # Inicializa o LLVM
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        # Converte IR para assembly NASM
        target = llvm.Target.from_default_triple()
        target_machine = target.create_target_machine()
        mod = llvm.parse_assembly(llvm_ir)
        asm = target_machine.emit_assembly(mod)
        return asm
    return None

# Exemplo de uso
if __name__ == "__main__":
    expr ='''
        3 + 5 * (2 - 1) 
        4 * 5
        7 - 3
    '''
    asm_code = compile_expression(expr)
    if asm_code:
        print("Código Assembly NASM Gerado:")
        print(asm_code)
        with open("output.asm", "w") as f:
            f.write(asm_code)