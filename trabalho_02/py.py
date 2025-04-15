from collections import deque

# Definição da tabela LL(1)
tabela_LL1 = {
    ("S", "if"): ["if", "E", "then", "S", "else", "S"],
    ("S", "a"): ["a"],
    ("E", "b"): ["b"],
    ("E", "c"): ["c"]
}

# Função do parser LL(1)
def parser_LL1(entrada):
    entrada.append("$")  # Adiciona o símbolo de fim de entrada
    index = 0  # Índice para lookahead

    # Pilha inicial com símbolo inicial e fim de entrada
    pilha = deque(["$", "S"])

    print(f"{'Pilha':<30}{'Entrada':<30}{'Ação'}")
    print("="*80)

    while pilha:
        topo = pilha.pop()  # Remove o topo da pilha
        lookahead = entrada[index]  # Primeiro símbolo da entrada

        # Impressão dos estados da pilha e da entrada
        print(f"{' '.join(pilha):<30}{' '.join(entrada[index:]):<30}", end="")

        if topo == lookahead:
            # Correspondência entre terminal e entrada → Avança na entrada
            index += 1
            print(f"Match '{lookahead}'")
        elif (topo, lookahead) in tabela_LL1:
            # Substitui o topo pela produção correspondente na tabela
            producao = tabela_LL1[(topo, lookahead)]
            print(f"Usa regra {topo} → {' '.join(producao)}")
            pilha.extend(reversed(producao))  # Empilha a produção em ordem reversa
        else:
            # Erro sintático se não houver regra na tabela
            print(f"Erro sintático! '{lookahead}' inesperado.")
            return False

    #verificando se pilha vazia
    if index == len(entrada):
        print("\nentrada aceita")
    else:
        print("\nentrada não consumida.")

    return True

#le a entrada imput do compilador
def parser(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    tokens = conteudo.split()
    return tokens

if __name__ == "__main__":
    nome_arquivo = "e.txt"
    teste = parser(nome_arquivo)
    parser_LL1(teste)
