package meuinterpretador;

public class Token {
    public TipoToken tipo;
    public Integer valor;

    public Token(TipoToken tipo, Integer valor) {
        this.tipo = tipo;
        this.valor = valor;
    }

    public Token(TipoToken tipo) {
        this(tipo, null);
    }

    @Override
    public String toString() {
        return (valor != null) ? tipo + ":" + valor : tipo.toString();
    }
}
