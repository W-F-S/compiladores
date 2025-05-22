package meucompilador;

import java.util.List;
import java.util.Stack;

public class MaquinaVirtual {
    public int executar(List<String> codigo) {
        Stack<Integer> pilha = new Stack<>();

        for (String instrucao : codigo) {
            if (instrucao.startsWith("PUSH")) {
                int valor = Integer.parseInt(instrucao.split(" ")[1]);
                pilha.push(valor);
            } else {
                int b = pilha.pop();
                int a = pilha.pop();
                switch (instrucao) {
                    case "ADD": pilha.push(a + b); break;
                    case "SUB": pilha.push(a - b); break;
                    case "MUL": pilha.push(a * b); break;
                    case "DIV": pilha.push(a / b); break;
                }
            }
        }
        return pilha.pop();
    }
}
