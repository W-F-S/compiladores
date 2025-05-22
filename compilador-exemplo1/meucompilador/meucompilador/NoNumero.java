package meucompilador;

public class NoNumero extends No {
    public int valor;

    public NoNumero(Token token) {
        this.valor = token.valor;
    }

    @Override
    public String toString() {
        return Integer.toString(valor);
    }
}
