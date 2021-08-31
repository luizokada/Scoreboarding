from io import StringIO
from os import write
import sys
import re
from typing import List, Tuple


class UnidadeFuncionalStatus:
    def __init__(self) -> None:
        self.busy = False
        self.op = ''
        self.fi = ''
        self.fj = ''
        self.fk = ''
        self.qj = ''
        self.qk = ''
        self.rj = False
        self.rk = False
        self.pc = -1
        pass

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

    def setrk(self, rk):
        self.rk = rk

    def setOP(self, op):
        self.op = op

    def getOP(self):
        return self.op

    def setqj(self, qj):
        self.qj = qj

    def getqj(self):
        return self.qj

    def setqk(self, qk):
        self.qk = qk

    def getqk(self):
        return self.qk

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

    def getpc(self):
        return self.fj

    def setpc(self, fk):
        self.fk = fk


class operacoesStatus:
    def __init__(self) -> None:
        self.op = ''
        self.fi = ''
        self.fj = ''
        self.fk = ''
        self.issue = -1
        self.leitura = -1
        self.execucaoi = -1
        self.execucaof = -1
        self.escrita = -1

    def setOP(self, OP):
        self.op = OP

    def getOP(self):
        return self.op

    def setfi(self, fi):
        self.fi = fi

    def getfi(self):
        return self.fi

    def setfj(self, fj):
        self.fj = fj

    def getfj(self):
        return self.fj

    def setfk(self, fk):
        self.fk = fk

    def getfk(self):
        return self.fk

    def setIssue(self, issue):
        self.issue = issue

    def getIssue(self):
        return self.issue

    def setLeitura(self, leitura):
        self.leitura = leitura

    def getLeitura(self):
        return self.leitura

    def setExecucaoi(self, execucaoi):
        self.execucaoi = execucaoi

    def getExecucaoi(self):
        return self.execucaoi

    def setExecucaof(self, execucaof):
        self.execucaof = execucaof

    def getExecucaof(self):
        return self.execucaof

    def getEscrita(self):
        return self.escrita

    def setEscrita(self, escrita):
        self.escrita = escrita

    def printatributo(self):
        print(self.op)
        print(self.fi)
        print(self.fj)
        print(self.fk)
        pass


def isWAW(UnidadeFuncionais, operacoes, pc):
    return


def isRAW():
    return


def isWAR():
    return


'''
unidadeFuncionais[0]=Intenger
unidadeFuncionais[1]=Mult1
unidadeFuncionais[2]=Mult2
unidadeFuncionais[3]=add
unidadeFuncionais[4]=Divide
registradoresStatus[0]....[11]=r0....r12
registradoresStatus[12]=rb
'''


def issue(operacoes: List[operacoesStatus], unidadesFuncionais: List[UnidadeFuncionalStatus], registradores: List[str], pc: int, clock: int):
    if not isWAW(unidadesFuncionais, operacoes, pc):
        if operacoes[pc].getOP() == 'ld':
            if not unidadesFuncionais[0].isBusy():
                unidadesFuncionais[0].setOP(operacoes[pc].getOP())
                unidadesFuncionais[0].setfi(operacoes[pc].getfi())
                unidadesFuncionais[0].setfj(operacoes[pc].getfj())
                unidadesFuncionais[0].setfk(operacoes[pc].getfk())
                unidadesFuncionais[0].setqj('')
                registradores[int(
                    re.sub('[^0-9]', '', operacoes[pc].getfi()))] = 'Integer'

                if operacoes[pc].getfk() == 'rb':
                    unidadesFuncionais[0].setqk('')
                else:
                    registradores[int(
                        re.sub('[^0-9]', '', operacoes[pc].getfi()))] = 'Integer'
                    unidadesFuncionais[0].setqk(
                        registradores[int(re.sub('[^0-9]', '', operacoes[pc].getfk()))])
                if unidadesFuncionais[0].getqk() == '':
                    unidadesFuncionais[0].setrk(True)
                else:
                    unidadesFuncionais[0].setfk(False)
                unidadesFuncionais[0].setBusy(True)
                operacoes[pc].setIssue(clock)
                return pc+1
            else:
                return pc
    else:
        return pc


def read_operands(operacoes: List[operacoesStatus], unidadesFuncionais: List[UnidadeFuncionalStatus], registradores: List[str], clock: int):
    for i in range(len(unidadesFuncionais)):
        if unidadesFuncionais[i].isBusy() and operacoes[].getIssue != -1:
            if not isRAW():

    return operacoes


def execution():
    return


def writeResults():
    return


def scoreboarding(operacoes):
    pc = 0
    clock = 1
    registradoresStatus = ['']*13
    unidadesFuncionais = [UnidadeFuncionalStatus() for i in range(5)]
    while pc < len(operacoes):
        pc = issue(operacoes, unidadesFuncionais,
                   registradoresStatus, pc, clock)
        print(unidadesFuncionais[0].getfi())
        read_operands()
        execution()
        write()
        clock = +1
    return


def setOPs(Lines) -> List[operacoesStatus]:
    statusop = [operacoesStatus() for i in range(len(Lines))]
    for i in range(len(Lines)):
        aux = operacoesStatus()
        statusop[i].setOP(Lines[i][0])
        statusop[i].setfi(Lines[i][1][0])
        statusop[i].setfj(Lines[i][1][1])
        statusop[i].setfk(Lines[i][1][2])
    return statusop


def lerArq(nome_arq):
    statusop = []
    arquivo = open(nome_arq, 'r')
    Lines = arquivo.read().splitlines()
    for i in range(len(Lines)):
        Lines[i] = Lines[i].split(' ', 1)
        Lines[i][1] = Lines[i][1].split(',')
        if Lines[i][0] == 'ld':
            aux = Lines[i][1][1]
            aux = aux.split(')')
            aux[0] = aux[0].replace('(', '')
            Lines[i][1][1] = aux[0]
            Lines[i][1].append(aux[1])
    statusop = setOPs(Lines)
    return statusop


def writestatus(nome_arq):
    nome_arq = nome_arq.split('.')
    saida = nome_arq[0]
    saida = saida+'.out'
    arquivo = open(saida, 'w')


def main():
    operacoes = lerArq(sys.argv[1])
    scoreboarding(operacoes)
    writestatus(sys.argv[1])
    return 0


if __name__ == "__main__":
    main()
