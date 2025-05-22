package CompiladorCalcVar;

import java.util.ArrayList;
import java.util.List;

/**
modificar o codigo para suportar ler palavras declaradas
*/

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



    /**
     *Lê a declaracao de uma variavel
     */
    private Token palavra(){
        StringBuilder palavra = new StringBuilder();
        // Enquanto o caractere atual for uma letra ou talvez um dígito (para casos de identificadores alfanuméricos)
        while (caractereAtual != null && (Character.isLetter(caractereAtual) || Character.isDigit(caractereAtual))) {
            palavra.append(caractereAtual);
            avancar();
        }
        String lexema = palavra.toString();

        // Verifica se o lexema é uma palavra-chave (por exemplo, "int")
        if ("int".equals(lexema)) {
            return new Token(TipoToken.INTEIRO, lexema);  // você precisará definir esse tipo em seu enum TipoToken
        }
        // Se não for, trata como identificador
        return new Token(TipoToken.IDENTIFICADOR, lexema);  // ajuste o construtor para receber Strings se necessário
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

            if (Character.isLetter(caractereAtual)){
                tokens.add(palavra());
                continue;
            }


            switch (caractereAtual) {
                case '+': tokens.add(new Token(TipoToken.MAIS)); break;
                case '-': tokens.add(new Token(TipoToken.MENOS)); break;
                case '*': tokens.add(new Token(TipoToken.MULTIPLICA)); break;
                case '/': tokens.add(new Token(TipoToken.DIVIDE)); break;
                case '(': tokens.add(new Token(TipoToken.ABRE_PARENTESES)); break;
                case ')': tokens.add(new Token(TipoToken.FECHA_PARENTESES)); break;
                case '=': tokens.add(new Token(TipoToken.DECLARACAO)); break;
                case ';': tokens.add(new Token(TipoToken.PONTO_VIRGULA)); break;

                default: throw new RuntimeException("Caractere inválido: " + caractereAtual);
            }
            avancar();
        }
        tokens.add(new Token(TipoToken.EOF));
        return tokens;
    }
}
