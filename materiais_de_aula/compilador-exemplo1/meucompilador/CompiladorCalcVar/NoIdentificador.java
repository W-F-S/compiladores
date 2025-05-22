package CompiladorCalcVar;

public class NoIdentificador extends No {
    public Token tipo;
    public Token identificador;
    public No expressao;

    public NoIdentificador(Token tipo, Token identificador, No expressao) {
        this.tipo = tipo;
        this.identificador = identificador;
        this.expressao = expressao;

    }

    @Override
    public String toString() {
        return "()";
    }
}
