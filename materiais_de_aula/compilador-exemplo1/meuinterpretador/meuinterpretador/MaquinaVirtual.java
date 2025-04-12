package meuinterpretador;

public class MaquinaVirtual {
    public int executar(No no) {
        if (no instanceof NoNumero) {
            return ((NoNumero) no).valor;
        } else if (no instanceof NoOperadorBinario) {
            NoOperadorBinario binario = (NoOperadorBinario) no;
            int esquerda = executar(binario.esquerda);
            int direita = executar(binario.direita);
            switch (binario.operador.tipo) {
                case MAIS: return esquerda + direita;
                case MENOS: return esquerda - direita;
                case MULTIPLICA: return esquerda * direita;
                case DIVIDE: return esquerda / direita;
            }
        }
        throw new RuntimeException("Erro de execução");
    }
}
