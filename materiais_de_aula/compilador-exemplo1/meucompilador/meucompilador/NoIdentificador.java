package meucompilador;

public class NoIdentificador extends No {
    public No tipo;
    public Token identificador;

    public NoIdentificador(No tipo, Token identificador) {
        this.tipo = tipo;
        this.identifiador = identificador;
    }

    @Override
    public String toString() {
        return "()";
    }
}
