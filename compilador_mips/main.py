from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from codegen import CodeGenerator

code = open("exemplo.txt").read()

lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

semantic = SemanticAnalyzer(ast)
semantic.analyze()

generator = CodeGenerator(ast)
mips_code = generator.generate()

with open("saida.asm", "w") as f:
    f.write(mips_code)