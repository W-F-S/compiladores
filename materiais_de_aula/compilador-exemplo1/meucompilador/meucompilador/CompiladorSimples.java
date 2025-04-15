package meucompilador;

import java.util.List;

public class CompiladorSimples {
    public static void main(String[] args) {
        String entrada = "int i = 30;";
        System.out.println("Expressão de entrada: " + entrada);

        AnalisadorLexico lexer = new AnalisadorLexico(entrada);
        List<Token> tokens = lexer.obterTokens();
        //System.out.println(tokens);



        AnalisadorSintatico parser = new AnalisadorSintatico(tokens);
        No ast = parser.programa();

        /**
        GeradorCodigo gerador = new GeradorCodigo();
        gerador.gerar(ast);
        List<String> codigo = gerador.getInstrucoes();
        System.out.println("Código Gerado: " + codigo);

        MaquinaVirtual maquina = new MaquinaVirtual();
        int resultado = maquina.executar(codigo);
        System.out.println("Resultado da execução: " + resultado);
        */
    }
}
