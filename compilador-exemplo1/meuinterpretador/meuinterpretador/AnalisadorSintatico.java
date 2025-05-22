package meuinterpretador;

import java.util.List;

public class AnalisadorSintatico {
    private List<Token> tokens;
    private int posicao;
    private Token tokenAtual;

    public AnalisadorSintatico(List<Token> tokens) {
        this.tokens = tokens;
        this.posicao = 0;
        this.tokenAtual = tokens.get(posicao);
    }

    private void avancar() {
        posicao++;
        tokenAtual = (posicao < tokens.size()) ? tokens.get(posicao) : null;
    }

    private No fator() {
        Token token = tokenAtual;
        if (token.tipo == TipoToken.INTEIRO) {
            avancar();
            return new NoNumero(token);
        } else if (token.tipo == TipoToken.ABRE_PARENTESES) {
            avancar();
            No no = expressao();
            if (tokenAtual.tipo != TipoToken.FECHA_PARENTESES) {
                throw new RuntimeException("Erro de sintaxe: esperado ')'");
            }
            avancar();
            return no;
        }
        throw new RuntimeException("Erro de sintaxe");
    }

    private No termo() {
        No no = fator();
        while (tokenAtual.tipo == TipoToken.MULTIPLICA || tokenAtual.tipo == TipoToken.DIVIDE) {
            Token operador = tokenAtual;
            avancar();
            no = new NoOperadorBinario(no, operador, fator());
        }
        return no;
    }

    private No expressao() {
        No no = termo();
        while (tokenAtual.tipo == TipoToken.MAIS || tokenAtual.tipo == TipoToken.MENOS) {
            Token operador = tokenAtual;
            avancar();
            no = new NoOperadorBinario(no, operador, termo());
        }
        return no;
    }

    public No analisar() {
        return expressao();
    }
}
