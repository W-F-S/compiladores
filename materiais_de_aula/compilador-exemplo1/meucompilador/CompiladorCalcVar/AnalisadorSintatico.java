package CompiladorCalcVar;

import java.util.List;
import java.util.ArrayList;

public class AnalisadorSintatico {
    private List<Token> tokens;
    private int posicao;
    private Token tokenAtual;
    private List<No> comandos;

    public AnalisadorSintatico(List<Token> tokens) {
        this.tokens = tokens;
        this.posicao = 0;
        this.tokenAtual = tokens.get(posicao);
    }

    private void avancar() {
        System.out.println(tokenAtual);
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
        }else if(token.tipo == TipoToken.IDENTIFICADOR){
            boolean encontrado = false;
            for (No no : comandos) {  //iterando sobre cada comando para ver se a variavel já foi definida
                System.out.println(no);
            }
            if (!encontrado) {
                throw new RuntimeException("Identificador não declarado: " + token.valor);
            }
            avancar();

        }
        throw new RuntimeException("Erro de sintaxe");
    }

    private No expressao() {
        No no = fator();
        while (tokenAtual.tipo == TipoToken.MAIS || tokenAtual.tipo == TipoToken.MENOS || tokenAtual.tipo == TipoToken.MULTIPLICA || tokenAtual.tipo == TipoToken.DIVIDE) {
            Token operador = tokenAtual;
            avancar();
            no = new NoOperadorBinario(no, operador, fator());
        }
        return no;

    }

    private No declaracao() {
        Token tipoToken;
        if (tokenAtual.tipo == TipoToken.INTEIRO) {
            tipoToken = tokenAtual;
            avancar();
        } else {
            throw new RuntimeException("Esperado o tipo 'int'. Encontrado: " + tokenAtual);
        }

        // ver se o próximo token é um identificador
        Token tokenVariavel;
        if (tokenAtual.tipo == TipoToken.IDENTIFICADOR) {
            tokenVariavel = tokenAtual;
            avancar();
        } else {
            throw new RuntimeException("Esperado identificador após o tipo. Encontrado: " + tokenAtual);
        }

        if (tokenAtual.tipo == TipoToken.DECLARACAO) {
            avancar();
        } else {
            throw new RuntimeException("Esperado '=' após o identificador. Encontrado: " + tokenAtual);
        }

        // expressão após o '='
        No expressao = expressao();


        if (tokenAtual.tipo == TipoToken.PONTO_VIRGULA) {
            avancar();
        } else {
            throw new RuntimeException("Esperado ';' ao final da declaração. Encontrado: " + tokenAtual);
        }

        return new NoIdentificador(tipoToken, tokenVariavel, expressao);
    }

    public NoPrograma programa() {
        comandos = new ArrayList<>();

        while (tokenAtual != null && tokenAtual.tipo != TipoToken.EOF && tokenAtual.tipo != TipoToken.PONTO_VIRGULA) {
            System.out.println("Token atual: " + tokenAtual);

            // MUDAR PARA DEFINICAO E NAO DECLARACAO
            if (tokenAtual.tipo == TipoToken.DECLARACAO) {
                System.out.println("Token DECLARACAO encontrado. Chamando método declaracao()...");
                No noDeclaracao = declaracao();
                System.out.println("Declaração processada: " + noDeclaracao);
                comandos.add(noDeclaracao);
            } else if (tokenAtual.tipo == TipoToken.IDENTIFICADOR){
                System.out.println("Token IDENTIFICADOR encontrado. Decidindo ação para identificador...");

            } else {
                System.out.println("Tratando o token como expressão. Chamando método expressao()...");
            }
            avancar();
        }

        System.out.println("Fim da análise do programa. Nós coletados:");
        for (No no : comandos) {
            System.out.println(no);
        }

        return new NoPrograma(comandos);
    }
}
