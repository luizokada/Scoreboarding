import sys
import re


def lerArq(Lines):
    operacoes = []
    operacoes1 = []
    for i in range(len(Lines)):
        operacoes.append(Lines[i].split(' ', 1))
        operacoes[i][1] = operacoes[i][1].split(',')
    print(operacoes)
    return operacoes


def read_operands(operacoes):
    registradores = []
    for j in range(len(operacoes)):
        for i in range(len(operacoes[j][1])):
            if operacoes[j][0] != "ld":
                operacoes[j][1][i] = re.sub('[^0-9]', '', operacoes[j][1][i])
                registradores.append(re.sub('[^0-9]', '', operacoes[j][1][i]))
            else:
                operacoes[j][1][0] = re.sub('[^0-9]', '', operacoes[j][1][0])
                operacoes[j][1][1] = operacoes[j][1][1].removeprefix(' (')
                operacoes[j][1][1] = operacoes[j][1][1].removesuffix('rb')
                operacoes[j][1][1] = operacoes[j][1][1].removesuffix(')')
    return operacoes


def execution():
    return


def write_results(nome_arq, operacoes):
    nome_arq.split('.')
    saida = nome_arq[1]
    saida = saida+'.out'
    arquivo = open(saida, 'w')
    print(operacoes)


def main():
    registradores = [0]*13
    nome_arq = sys.argv[1]
    arquivo = open(nome_arq, 'r')
    Lines = arquivo.readlines()
    operacoes = lerArq(Lines)
    operacoes = read_operands(operacoes)
    write_results(nome_arq, operacoes)
    return 0


if __name__ == "__main__":
    main()
