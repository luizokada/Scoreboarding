import sys
import re
from typing import List, Tuple


class UnidadeFuncional:
    def __init__(self) -> None:
        self.busy = False
        self.op = ''
        self.fi = -1
        self.fj = -1
        self.fk = -1
        self.qj = ''
        self.qk = ''
        self.rj = False
        self.rk = False

    def isBusy(self) -> bool:
        return self.busy

    def setBusy(self, busy):
        self.busy = busy

    def isrj(self) -> bool:
        return self.rj

    def setrj(self, rj):
        self.rj = rj

    def isrk(self) -> bool:
        return self.rk

    def setrj(self, rk):
        self.rk = rk

    def setOP(self, OP):
        self.op = OP

    def getOP(self):
        return self.op

    def setfi(self, fi):
        self.fi = fi

    def getfi(self):
        return self.op

    def setfj(self, fj):
        self.fj = fj

    def getfj(self):
        return self.fj

    def setfk(self, fk):
        self.fk = fk

    def getOP(self):
        return self.op

    def setqj(self, qj):
        self.qj = qj

    def getqj(self):
        return self.qj

    def setqk(self, qk):
        self.qk = qk

    def getqj(self):
        return self.qk
    pass


def lerArq(nome_arq):
    operacoes = []
    arquivo = open(nome_arq, 'r')
    Lines = arquivo.read().splitlines()
    for i in range(len(Lines)):
        operacoes.append(Lines[i].split(' ', 1))
        operacoes[i][1] = operacoes[i][1].split(',')
        if operacoes[i][0] == 'ld':
            aux = operacoes[i][1][1]
            aux = aux.split(')')
            aux[0].removeprefix('(')
            print(aux)
            operacoes[i][1] = aux
    print(operacoes)
    return operacoes


def read_operands(operacoes):
    return operacoes


def execution():
    return


def write_results(nome_arq, operacoes):
    nome_arq.split('.')
    saida = nome_arq[1]
    saida = saida+'.out'
    arquivo = open(saida, 'w')


def main():
    operacoes = lerArq(sys.argv[1])
    write_results(sys.argv[1], operacoes)
    return 0


if __name__ == "__main__":
    main()
