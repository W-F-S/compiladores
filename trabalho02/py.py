from collections import deque

# Definição da tabela LL(1) como um dicionário (chave: (não-terminal, terminal))
tabela_LL1 = {
    ("S", "if"): ["if", "E", "then", "S", "else", "S"],
    ("S", "a"): ["a"],
    ("E", "b"): ["b"],
    ("E", "c"): ["c"]
}

# Função para verificar se um símbolo é terminal
def eh_terminal(simbolo):
    return simbolo in ["if", "then", "else", "a", "b", "c", "$"]

# Função do parser LL(1)
def parser_LL1(entrada):
    # Adiciona $ ao final da entrada
    entrada.append("$")
    index = 0  # Índice da entrada (lookahead)

    # Pilha inicial
    pilha = deque(["$", "S"])

    print(f"{'Pilha':<30}{'Entrada':<30}{'Ação'}")
    print("="*80)

    while pilha:
        topo = pilha.pop()  # Remove o topo da pilha
        lookahead = entrada[index]  # Primeiro símbolo da entrada

        print(f"{' '.join(pilha):<30}{' '.join(entrada[index:]):<30}", end="")

        if topo == lookahead:
            # Correspondência entre terminal e entrada → Avança na entrada
            index += 1
            print(f"Match '{lookahead}'")
        elif (topo, lookahead) in tabela_LL1:
            # Substitui topo por produção correspondente na tabela
            producao = tabela_LL1[(topo, lookahead)]
            print(f"Usa regra {topo} → {' '.join(producao)}")
            pilha.extend(reversed(producao))  # Empilha a produção em ordem reversa
        else:
            # Erro sintático se não houver regra na tabela
            print(f"Erro sintático! '{lookahead}' inesperado.")
            return False

    # Se pilha vazia e entrada consumida corretamente, a análise é válida
    if index == len(entrada):
        print("\nEntrada aceita! 🎉")
        return True
    else:
        print("\nErro: entrada não consumida completamente.")
        return False

# Testando com a entrada "if b then a else a $"
entrada_teste = ["if", "b", "then", "a", "else", "a"]
parser_LL1(entrada_teste)
