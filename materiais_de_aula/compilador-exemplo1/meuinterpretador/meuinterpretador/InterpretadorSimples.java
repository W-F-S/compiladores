package meuinterpretador;

import java.util.List;

public class InterpretadorSimples {
    public static void main(String[] args) {
        String entrada = "3 + 4 * (2 - 1)";
        System.out.println("Expressão de entrada: " + entrada);

        AnalisadorLexico lexer = new AnalisadorLexico(entrada);
        List<Token> tokens = lexer.obterTokens();
        System.out.println("Tokens: " + tokens);

        AnalisadorSintatico parser = new AnalisadorSintatico(tokens);
        No ast = parser.analisar();
        System.out.println("Árvore Sintática: " + ast);

        MaquinaVirtual maquina = new MaquinaVirtual();
        int resultado = maquina.executar(ast);
        System.out.println("Resultado da execução: " + resultado);
    }
}
