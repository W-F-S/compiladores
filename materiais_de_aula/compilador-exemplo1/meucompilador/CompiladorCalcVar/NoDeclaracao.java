package CompiladorCalcVar;

public class NoDeclaracao extends No {
    public Token tipo;            // esperando INTEIRO
    public Token identificador;   // Nome da variável
    public No expressao;          // Nó que representa a expressão atribuída (ex: NoNumero, NoOperadorBinario, etc.)

    public NoDeclaracao(Token tipo, Token identificador, No expressao) {
        this.tipo = tipo;
        this.identificador = identificador;
        this.expressao = expressao;
    }

    @Override
    public String toString() {
        // Exemplo de representação: "(int i = expressao)"
        return "(" + tipo.toString() + " " + identificador.toString() + " = " + expressao.toString() + ")";
    }
}
