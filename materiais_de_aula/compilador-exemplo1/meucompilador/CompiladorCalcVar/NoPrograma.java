package CompiladorCalcVar;

import java.util.List;

public class NoPrograma extends No {
    private List<No> nos;

    public NoPrograma(List<No> nos) {
        this.nos = nos;
    }

    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        for (No no : nos) {
            builder.append(no.toString()).append("\n");
        }
        return builder.toString();
    }

    public void mostrarNos() {
        System.out.println(toString());
    }
}
