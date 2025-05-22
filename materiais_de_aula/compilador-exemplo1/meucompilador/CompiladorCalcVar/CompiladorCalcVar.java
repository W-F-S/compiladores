package CompiladorCalcVar;

import java.util.List;

public class CompiladorCalcVar {
    public static void main(String[] args) {
        String entrada = "int i = 1 + 30;";
        System.out.println("Expressão de entrada: " + entrada);

        AnalisadorLexico lexer = new AnalisadorLexico(entrada);
        List<Token> tokens = lexer.obterTokens();
        System.out.println(tokens);

        AnalisadorSintatico parser = new AnalisadorSintatico(tokens);
        No ast = parser.programa();
    }
}
