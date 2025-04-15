package meucompilador;

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

    /*
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
            for (No no : comandos) {  // 'tokens' é a lista de tokens armazenada no seu analisador sintático
                System.out.println(no);
            }
            if (!encontrado) {
                throw new RuntimeException("Identificador não declarado: " + token.valor);
            }
            avancar();
                public NoIdentificador(No tipo, Token identificador) {

            return new NoIdentificador(, token);
        }
        throw new RuntimeException("Erro de sintaxe");
    }

    */

    private No expressao() {
        No no;
        while (tokenAtual.tipo == TipoToken.MAIS || tokenAtual.tipo == TipoToken.MENOS || tokenAtual.tipo == TipoToken.MULTIPLICA || tokenAtual.tipo == TipoToken.DIVIDE) {
            Token operador = tokenAtual;
            avancar();
            no = new NoOperadorBinario(no, operador, termo());
        }
        return no;

    }

    /*
    private No identificador(){
        No no = termo();
        while (tokenAtual.tipo == TipoToken.IDENTIFICADOR) {
            Token operador = tokenAtual;
            avancar();
            no = new NoIdentificador(no, operador, termo());
        }
        return no;
    }
    */

    private No declaracao() {
        // Verifica se o token atual é o tipo (ex: "int")
        Token tipoToken;
        if (tokenAtual.tipo == TipoToken.INTEIRO) {
            tipoToken = tokenAtual;
            avancar();
        } else {
            throw new RuntimeException("Esperado o tipo 'int'. Encontrado: " + tokenAtual);
        }

        // Verifica se o próximo token é um identificador
        Token tokenVariavel;
        if (tokenAtual.tipo == TipoToken.IDENTIFICADOR) {
            tokenVariavel = tokenAtual;
            avancar();
        } else {
            throw new RuntimeException("Esperado identificador após o tipo. Encontrado: " + tokenAtual);
        }

        // Verifica se o próximo token é '=' (atribuição)
        if (tokenAtual.tipo == TipoToken.DECLARACAO) { // ou TipoToken.ATRIBUICAO, se for o nome correto
            avancar();
        } else {
            throw new RuntimeException("Esperado '=' após o identificador. Encontrado: " + tokenAtual);
        }

        // Lê a expressão após o '='
        No expressao = expressao();

        // Verifica se há ponto e vírgula
        if (tokenAtual.tipo == TipoToken.PONTO_VIRGULA) {
            avancar();
        } else {
            throw new RuntimeException("Esperado ';' ao final da declaração. Encontrado: " + tokenAtual);
        }

        return new NoIdentificador(tipoToken, tokenVariavel, expressao);
    }

    public NoPrograma programa() {
        comandos = new ArrayList<>();

        System.out.println("Iniciando análise do programa...");

        // Processa todos os tokens até encontrar o EOF
        while (tokenAtual != null && tokenAtual.tipo != TipoToken.EOF) {
            System.out.println("Token atual: " + tokenAtual);

            // MUDAR PARA DEFINICAO E NAO DECLARACAO
            if (tokenAtual.tipo == TipoToken.DECLARACAO) {
                System.out.println("Token DECLARACAO encontrado. Chamando método declaracao()...");
                No noDeclaracao = declaracao();
                System.out.println("Declaração processada: " + noDeclaracao);
                comandos.add(noDeclaracao);
            } else if (tokenAtual.tipo == TipoToken.IDENTIFICADOR){
                System.out.println("Token IDENTIFICADOR encontrado. Decidindo ação para identificador...");

                //comandos.add(noExpressao);
            } else {
                System.out.println("Tratando o token como expressão. Chamando método expressao()...");
                //No noExpressao = expressao();
                //System.out.println("Expressão processada: " + noExpressao);
                //comandos.add(noExpressao);
                // Opcional: se houver um PONTO_VIRGULA, você pode consumi-lo aqui
            }
        }

        System.out.println("Fim da análise do programa. Nós coletados:");
        for (No no : comandos) {
            System.out.println(no);
        }

        return new NoPrograma(comandos);
    }


}
