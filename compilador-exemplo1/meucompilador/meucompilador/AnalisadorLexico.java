package meucompilador;

import java.util.ArrayList;
import java.util.List;

public class AnalisadorLexico {
    private String texto;
    private int posicao;
    private Character caractereAtual;

    public AnalisadorLexico(String texto) {
        this.texto = texto;
        this.posicao = 0;
        this.caractereAtual = (texto.length() > 0) ? texto.charAt(0) : null;
    }

    private void avancar() {
        posicao++;
        caractereAtual = (posicao < texto.length()) ? texto.charAt(posicao) : null;
    }

    private void ignorarEspacos() {
        while (caractereAtual != null && Character.isWhitespace(caractereAtual)) {
            avancar();
        }
    }

    private Token numero() {
        StringBuilder numStr = new StringBuilder();
        while (caractereAtual != null && Character.isDigit(caractereAtual)) {
            numStr.append(caractereAtual);
            avancar();
        }
        return new Token(TipoToken.INTEIRO, Integer.parseInt(numStr.toString()));
    }

    public List<Token> obterTokens() {
        List<Token> tokens = new ArrayList<>();
        while (caractereAtual != null) {
            if (Character.isWhitespace(caractereAtual)) {
                ignorarEspacos();
                continue;
            }
            if (Character.isDigit(caractereAtual)) {
                tokens.add(numero());
                continue;
            }
            switch (caractereAtual) {
                case '+': tokens.add(new Token(TipoToken.MAIS)); break;
                case '-': tokens.add(new Token(TipoToken.MENOS)); break;
                case '*': tokens.add(new Token(TipoToken.MULTIPLICA)); break;
                case '/': tokens.add(new Token(TipoToken.DIVIDE)); break;
                case '(': tokens.add(new Token(TipoToken.ABRE_PARENTESES)); break;
                case ')': tokens.add(new Token(TipoToken.FECHA_PARENTESES)); break;
                default: throw new RuntimeException("Caractere inválido: " + caractereAtual);
            }
            avancar();
        }
        tokens.add(new Token(TipoToken.EOF));
        return tokens;
    }
}
