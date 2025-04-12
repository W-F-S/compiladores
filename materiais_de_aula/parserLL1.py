# Tabela LL(1) como dicionário: (não-terminal, terminal) -> produção
tabela = {
    ('E', 'id'): ['T', "E'"],
    ('E', '('): ['T', "E'"],
    ("E'", '+'): ['+', 'T', "E'"],
    ("E'", ')'): ['ε'],
    ("E'", '$'): ['ε'],
    ('T', 'id'): ['F', "T'"],
    ('T', '('): ['F', "T'"],
    ("T'", '+'): ['ε'],
    ("T'", '*'): ['*', 'F', "T'"],
    ("T'", ')'): ['ε'],
    ("T'", '$'): ['ε'],
    ('F', 'id'): ['id'],
    ('F', '('): ['(', 'E', ')']
}

# Função para verificar se um símbolo é não-terminal
def eh_nao_terminal(simbolo):
    return simbolo in ['E', "E'", 'T', "T'", 'F']

# Função do parser LL(1)
def parser_ll1(entrada):
    pilha = ['$', 'E']  # Pilha inicial com símbolo inicial 'E' e fim '$'
    entrada = entrada + ['$']  # Adiciona '$' ao final da entrada
    i = 0  # Índice da entrada
    lookahead = entrada[i]

    print(f"{'Pilha':<20} {'Entrada':<20} {'Ação':<20}")
    print("-" * 60)

    while pilha:
        topo = pilha[-1]  # Topo da pilha
        estado = f"{' '.join(pilha):<20} {' '.join(entrada[i:]):<20}"

        if not eh_nao_terminal(topo):  # Terminal ou '$'
            if topo == lookahead:
                pilha.pop()  # Match
                i += 1
                # Verifica se ainda há elementos na entrada antes de atualizar lookahead
                if i < len(entrada):
                    lookahead = entrada[i]
                else:
                    break  # Sai do loop se a entrada foi totalmente consumida
                print(f"{estado}Match {topo}")
            else:
                return f"Erro: token inesperado '{lookahead}'"
        else:  # Não-terminal
            chave = (topo, lookahead)
            if chave in tabela:
                producao = tabela[chave]
                pilha.pop()  # Remove o não-terminal
                if producao != ['ε']:  # Se não for epsilon, empilha a produção
                    pilha.extend(reversed(producao))
                print(f"{estado}{topo} → {' '.join(producao)}")
            else:
                return f"Erro: nenhuma produção para {topo} com lookahead {lookahead}"

    if i == len(entrada) and not pilha:
        return "Entrada aceita"
    return "Erro: entrada incompleta ou inválida"

# Teste da implementação
entrada = ['id', '+', 'id', '*', 'id']
resultado = parser_ll1(entrada)
print("\nResultado:", resultado)