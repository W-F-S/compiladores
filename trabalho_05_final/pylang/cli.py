import sys
from .parser import parser
from .interpreter import Interpreter

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = f.read()
        result = parser.parse(data)
        interpreter = Interpreter()
        interpreter.interpret(result)
    else:
        print("Modo interativo (Ctrl+D para sair)")
        interpreter = Interpreter()
        while True:
            try:
                s = input('pylang> ')
                if not s.endswith(';'):
                    s += ';'
                result = parser.parse(s)
                interpreter.interpret(result)
            except EOFError:
                break
            except Exception as e:
                print(f"Erro: {e}")

if __name__ == '__main__':
    main()
