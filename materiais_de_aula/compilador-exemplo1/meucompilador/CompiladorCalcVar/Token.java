package CompiladorCalcVar;

public class Token {
    public TipoToken tipo;
    public String valor;
    public int valorInt;


    public Token(TipoToken tipo, String valor) {
        this.tipo = tipo;
        this.valor = valor;
    }

    public Token(TipoToken tipo, int valor) {
        this.tipo = tipo;
        this.valorInt = valor;
    }

    public Token(TipoToken tipo) {
        this(tipo, null);
    }

    @Override
    public String toString() {
        if ((valor == null || valor.isEmpty()) && tipo == TipoToken.INTEIRO) {
            return tipo + ":" + valorInt;
        }
        if (valor != null && !valor.isEmpty()) {
            return tipo + ":" + valor;
        }
        return tipo.toString();
    }
}
