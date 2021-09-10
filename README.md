# ARQIITrabI
Escalonamento Dinâmico
Simulador de Scoreboarding
Para esta tarefa você deve implementar um simulador de Scoreboarding.

Especificação

a) Instruções
ld d, (offset)rb
muld d, o1, o2
divd d, o1, o2
subd d, o1, o2
addd d, o1, o2
d = registrador destino
offset = deslocamento (inteiro – positivo ou negativo)
b = registrador base
o1 = registrador do operando 1
o2 = registrador do operando 2
rb = registrador base (usado apenas na instrução ld)
Registradores: r1 … r12 e rb

b) Latência da instruções

ld → 1 ciclo

muld → 10 ciclos

divd → 40 ciclos

subd → 2 ciclos

addd → 2 ciclos

c) Execução
O simulador não irá executar efetivamente o código. Ele irá apenas simular a gerência das
dependências, como realizado nos exercícios resolvidos durante a aula.

d) Saída
A cada ciclo de clock, o simular deve apresentar: (1) a tabela Status das Instruções, (2) a tabela
Status das Unidades Funcionais, (3) Status dos Registradores. Ou seja, a saída do simulador é como
a folha resposta para Scoreboarding. A saída deve ser um arquivo de log.

e) Entrada do Simulador
A entrada é um arquivo texto contendo o programa a ser simulado. Exemplo:
ld r1, (12)rb
ld r3, (16)rb
addd r4, r2, r1
subd r5, r4, r2

f) O Simulador
- O código do simulador deverá refletir na íntegra a estratégia Scoreboarding. Para tal fim, o código
deverá implementar na íntegra o Scoreboard Bookkeeping. Desta forma, é esperado que o
simulador tenha os seguintes módulos (funções): issue, read_operands, execution, write_results.

g) A Implementação
- Pode ser utilizada qualquer linguagem de programação.
- A entrada deve seguir estritamente o padrão do Item e.
- A saída deve ser um arquivo texto.

h) Parâmetros de Execução
- A execução do simulador deve ser da seguinte forma:
./scoreboarding <arquivo de entrada>
- O arquivo de entrada deve ter o padrão: <nome>.asm.
- O arquivo de saída deve ter o padrão: <nome>.out.
- Exemplo:
./scoreboarding exe1.asm → irá gerar exe1.out

 i) Ambiente de Execução
- Os trabalhos devem executar em um ambiente Linux, ambiente Windows não é aceito
