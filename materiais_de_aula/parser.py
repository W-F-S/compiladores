# Variáveis globais
tokens = []  # Lista de tokens, ex.: ["2", "+", "3", "*", "4"]
pos = 0      # Posição atual

# Função para pegar o próximo token
def lookahead():
    if pos < len(tokens):
        return tokens[pos]
    return None

# Função para avançar o ponteiro
def consume(expected):
    if lookahead() == expected:
        global pos
        pos += 1
        return True
    raise Exception(f"Erro: esperado '{expected}', encontrado '{lookahead()}'")

# Regra E → T + E | T - E | T
def E():
    T()
    while lookahead() in ["+", "-"]:  # Suporte para + e -
        op = lookahead()
        consume(op)
        T()

# Regra T → F * T | F / T | F
def T():
    F()
    while lookahead() in ["*", "/"]:  # Suporte para * e /
        op = lookahead()
        consume(op)
        F()

# Regra F → num | ( E ) | id
def F():
    if lookahead() == "(":
        consume("(")
        E()
        consume(")")
    elif lookahead() in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        consume(lookahead())  # Consome o número
    elif lookahead() in ["x", "y", "z"]:  # Suporte para variáveis (ex.: x, y, z)
        consume(lookahead())  # Consome a variável
    else:
        raise Exception(f"Erro em F: esperado 'num', 'id' ou '(', encontrado '{lookahead()}'")

# Função principal
def parse(input_tokens):
    global tokens, pos
    tokens = input_tokens
    pos = 0
    E()
    if lookahead() is None:
        print("Análise concluída com sucesso!")
    else:
        raise Exception("Erro: entrada não consumida completamente")

# Testes com os desafios
test_cases = [
    ["5", "-", "2", "+", "3"],         # Teste com - e +
    ["2", "*", "(", "3", "+", "4", ")"],  # Teste com * e parênteses
    ["x", "+", "2", "*", "y"],         # Teste com variáveis
    ["6", "/", "2", "+", "3"],         # Teste com /
    ["7", "*", "4", "/", "8"],
    ["7", "*", "/", "8"],
    ["7", "*", "4", "8"],
]

for test in test_cases:
    print(f"\nTestando: {' '.join(test)}")
    try:
        parse(test)
    except Exception as e:
        print(e)