package meucompilador;

import java.util.List;

public class CompiladorSimples {
    public static void main(String[] args) {
        String entrada = "7 * 30";
        System.out.println("Expressão de entrada: " + entrada);

        AnalisadorLexico lexer = new AnalisadorLexico(entrada);
        List<Token> tokens = lexer.obterTokens();

        AnalisadorSintatico parser = new AnalisadorSintatico(tokens);
        No ast = parser.analisar();

        GeradorCodigo gerador = new GeradorCodigo();
        gerador.gerar(ast);
        List<String> codigo = gerador.getInstrucoes();
        System.out.println("Código Gerado: " + codigo);

        MaquinaVirtual maquina = new MaquinaVirtual();
        int resultado = maquina.executar(codigo);
        System.out.println("Resultado da execução: " + resultado);
    }
}
