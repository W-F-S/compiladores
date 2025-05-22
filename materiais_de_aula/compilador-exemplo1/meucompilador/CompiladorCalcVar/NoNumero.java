package CompiladorCalcVar;

public class NoNumero extends No {
    public int valor;

    public NoNumero(Token token) {
        this.valor = (token.valorInt);
    }

    @Override
    public String toString() {
        return Integer.toString(valor);
    }
}
