from collections import deque
tabela = {
    ("S", "if"): ["if", "E", "then", "S", "else", "S"],
    ("S", "a"): ["a"],
    ("E", "b"): ["b"],
    ("E", "c"): ["c"]
}

def parser_LL1(entrada):
    entrada.append("$")
    index = 0

    pilha = deque(["$", "S"])

    print(f"{'Pilha':<30}{'Entrada':<30}{'Ação'}")
    print("="*80)

    while pilha:
        topo = pilha.pop()   # Remove o topo da pilha
        prox = entrada[index]  # Primeiro símbolo da entrada

        print(f"{' '.join(pilha):<30}{' '.join(entrada[index:]):<30}", end="")

        if topo == prox:
            index += 1
            print("proximo '{}'".format(prox))

        elif (topo, prox) in tabela:
            producao = tabela[(topo, prox)]
            print("regra {} -> {}".format(topo, " ".join(producao)))

            #empilhando tudo
            i = len(producao) - 1
            while i >= 0:
                pilha.append(producao[i])
                i -= 1
        else:
            print("erro com regra da tabela: '{}' pilha: {}".format(prox, " ".join(pilha)))
            return False

    if index == len(entrada):
        print("\nentrada aceita")
    else:
        print("\nentrada não consumida.")
    return True

def parser(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    tokens = conteudo.split()
    return tokens

if __name__ == "__main__":
    nome_arquivo = "e.txt"
    teste = parser(nome_arquivo)
    parser_LL1(teste)
