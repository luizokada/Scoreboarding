import sys
import re


def lerArq(Lines):
    operacoes = []
    operacoes1 = []
    for i in range(len(Lines)):
        operacoes1.append(Lines[i].split())
        operacoes.append((operacoes1[i][0], operacoes1[i][1].split(",")))
        #operacoes[i][1] = re.sub('[^0-9]', '', operacoes[i][1])
    return operacoes


def lerOperandos(operacoes):
    registradores = []
    for j in range(len(operacoes)):
        for i in range(len(operacoes[j][1])):
            operacoes[j][1][i] = re.sub('[^0-9]', '', operacoes[j][1][i])
            registradores.append(re.sub('[^0-9]', '', operacoes[j][1][i]))
    return operacoes


def main():
    nome_arq = sys.argv[1]
    arquivo = open(nome_arq, 'r')
    Lines = arquivo.readlines()
    linha = []
    operacoes = lerArq(Lines)
    lerOperandos(operacoes)
    return 0


if __name__ == "__main__":
    main()
