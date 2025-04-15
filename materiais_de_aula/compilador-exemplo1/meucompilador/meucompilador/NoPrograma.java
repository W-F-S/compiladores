package meucompilador;

import java.util.List;

public class NoPrograma extends No {
    private List<No> nos;

    public NoPrograma(List<No> nos) {
        this.nos = nos;
    }

    // Método para retornar uma representação textual de todos os nós do programa
    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        for (No no : nos) {
            builder.append(no.toString()).append("\n");
        }
        return builder.toString();
    }

    // Método auxiliar para exibir os nós, se desejar imprimir diretamente
    public void mostrarNos() {
        System.out.println(toString());
    }
}
