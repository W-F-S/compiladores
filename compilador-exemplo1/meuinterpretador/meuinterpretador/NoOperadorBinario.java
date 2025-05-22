package meuinterpretador;

public class NoOperadorBinario extends No {
    public No esquerda;
    public Token operador;
    public No direita;

    public NoOperadorBinario(No esquerda, Token operador, No direita) {
        this.esquerda = esquerda;
        this.operador = operador;
        this.direita = direita;
    }

    @Override
    public String toString() {
        return "(" + esquerda.toString() + " " + operador.tipo + " " + direita.toString() + ")";
    }
}
