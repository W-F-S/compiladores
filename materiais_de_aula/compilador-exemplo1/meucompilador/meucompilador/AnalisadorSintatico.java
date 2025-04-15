package meucompilador;

import java.util.List;
import java.util.ArrayList;

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
        }else if(token.tipo == TipoToken.ATRIBUICAO){

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

    private No identificador(){
        No no = termo();
        while (tokenAtual.tipo == TipoToken.IDENTIFICADOR) {
            Token operador = tokenAtual;
            avancar();
            no = new NoIdentificador(no, operador, termo());
        }
        return no;
    }

    private No declaracao() {

        No no = termo();
        while (tokenAtual.tipo == TipoToken.MAIS || tokenAtual.tipo == TipoToken.MENOS) {
            Token operador = tokenAtual;
            avancar();
            no = new NoOperadorBinario(no, operador, termo());
        }
        return no;
        /**
        // Consome o token de tipo (ex: "int")
        Token tipoToken = consumir(TipoToken.INTEIRO, "Esperado o tipo 'int'");
        // Consome o token do identificador
        Token idToken = consumir(TipoToken.IDENTIFICADOR, "Esperado identificador após o tipo");
        // Consome o operador de atribuição '='
        consumir(TipoToken.ATRIBUICAO, "Esperado '=' após o identificador");
        // Lê a expressão (por exemplo, um número ou uma operação)
        No expressao = expressao();
        // Consome o ponto e vírgula ';'
        consumir(TipoToken.PONTO_VIRGULA, "Esperado ';' ao final da declaração");

        return new NoDeclaracao(tipoToken, idToken, expressao);
        */
    }


        // Dentro da classe AnalisadorSintatico
    private Token consumir(TipoToken tipoEsperado, String mensagemErro) {
        if (tokenAtual.tipo == tipoEsperado) {
            Token token = tokenAtual;
            avancar();
            return token;
        }
        throw new RuntimeException(mensagemErro + ". Encontrado: " + tokenAtual);
    }


    public No analisar() {
        return expressao();
    }

    public NoPrograma programa() {
        List<No> comandos = new ArrayList<>();

        System.out.println("Iniciando análise do programa...");

        // Processa todos os tokens até encontrar o EOF
        while (tokenAtual != null && tokenAtual.tipo != TipoToken.EOF) {
            System.out.println("Token atual: " + tokenAtual);

            // Decide qual comando ler com base no token atual
            if (tokenAtual.tipo == TipoToken.ATRIBUICAO) {
                System.out.println("Token ATRIBUICAO encontrado. Chamando método declaracao()...");
                No noDeclaracao = declaracao();
                System.out.println("Declaração processada: " + noDeclaracao);
                comandos.add(noDeclaracao);
            } else if (tokenAtual.tipo == TipoToken.IDENTIFICADOR{
                System.out.println("Token IDENTIFICADOR encontrado. Decidindo ação para identificador...");
                // Aqui, conforme o design da sua linguagem, você pode tratar o IDENTIFICADOR
                // como parte de uma expressão ou de outra construção; por enquanto, vamos tratá-lo como expressão.
                No noExpressao = expressao();
                System.out.println("Expressão processada: " + noExpressao);
                comandos.add(noExpressao);
            } else {
                System.out.println("Tratando o token como expressão. Chamando método expressao()...");
                No noExpressao = expressao();
                System.out.println("Expressão processada: " + noExpressao);
                comandos.add(noExpressao);
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
