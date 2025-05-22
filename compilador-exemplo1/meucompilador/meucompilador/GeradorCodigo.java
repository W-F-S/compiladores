package meucompilador;

import java.util.ArrayList;
import java.util.List;

public class GeradorCodigo {
    private List<String> instrucoes;

    public GeradorCodigo() {
        instrucoes = new ArrayList<>();
    }

    public void gerar(No no) {
        if (no instanceof NoNumero) {
            NoNumero numero = (NoNumero) no;
            instrucoes.add("PUSH " + numero.valor);
        } else if (no instanceof NoOperadorBinario) {
            NoOperadorBinario binario = (NoOperadorBinario) no;
            gerar(binario.esquerda);
            gerar(binario.direita);
            switch (binario.operador.tipo) {
                case MAIS: instrucoes.add("ADD"); break;
                case MENOS: instrucoes.add("SUB"); break;
                case MULTIPLICA: instrucoes.add("MUL"); break;
                case DIVIDE: instrucoes.add("DIV"); break;
            }
        }
    }

    public List<String> getInstrucoes() {
        return instrucoes;
    }
}
