import sys
import re
from typing import List

'''
Nome: Luiz Fernando Okada
RA:107247
Trabalho 1 Arquitetura de Organização de computadores
'''

'''
Classe que representa os status das unidade funcionais
'''


class UnidadeFuncionalStatus:
    def __init__(self) -> None:
        self.nome = ''
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

    def setNome(self, nome):
        self.nome = nome

    def getNome(self):
        return self.nome

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

    def getfk(self):
        return self.fk

    def setfk(self, fk):
        self.fk = fk

    def getpc(self):
        return self.pc

    def setpc(self, pc):
        self.pc = pc

    def reset(self):
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


'''
Classe que representa os status das instruçoes
'''


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
        self.finalizada = False

    def isFinalizada(self):
        return self.finalizada

    def setFinalizada(self, finalizada):
        self.finalizada = finalizada

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
registradoresStatus[0]....[12]=r0....r12
registradoresStatus[13]=rb
'''


def issue(operacao: operacoesStatus, unidadesFuncionais: List[UnidadeFuncionalStatus], registradores: List[str], pc: int, clock: int, statusOPs: List[operacoesStatus]):
    if not isWAW(unidadesFuncionais, operacao, pc):
        if operacao.getOP() == 'ld':
            UF = 0
        elif operacao.getOP() == 'multd':
            if not unidadesFuncionais[1].isBusy():
                UF = 1
            else:
                UF = 2
        elif operacao.getOP() == 'addd' or operacao.getOP() == 'subd':
            UF = 3
        elif operacao.getOP() == 'divd':
            UF = 4
        else:
            return pc
        if not unidadesFuncionais[UF].isBusy():
            unidadesFuncionais[UF].setOP(operacao.getOP())
            unidadesFuncionais[UF].setfi(operacao.getfi())
            unidadesFuncionais[UF].setfk(operacao.getfk())
            unidadesFuncionais[UF].setpc(pc)
            registradores[int(
                re.sub('[^0-9]', '', operacao.getfi()))] = unidadesFuncionais[UF].getNome()
            try:
                int(operacao.getfj())
                unidadesFuncionais[UF].setqj('')
                unidadesFuncionais[UF].setfj('')
                if operacao.getfk() == 'rb':
                    unidadesFuncionais[UF].setqk(registradores[13])
                else:
                    unidadesFuncionais[UF].setqk(
                        registradores[int(re.sub('[^0-9]', '', operacao.getfk()))])
            except ValueError:
                unidadesFuncionais[UF].setfj(operacao.getfj())
                unidadesFuncionais[UF].setqk(
                    registradores[int(re.sub('[^0-9]', '', operacao.getfk()))])
                unidadesFuncionais[UF].setqj(
                    registradores[int(re.sub('[^0-9]', '', operacao.getfj()))])
            unidadesFuncionais[UF].setBusy(True)
            statusOPs.append(operacao)
            statusOPs[pc].setIssue(clock)
            return pc+1
        else:
            return pc


def read_operands(operacoes: List[operacoesStatus], unidadesFuncionais: List[UnidadeFuncionalStatus],  clock: int):
    for i in range(len(unidadesFuncionais)):
        if unidadesFuncionais[i].isBusy():
            if unidadesFuncionais[i].isrj() and unidadesFuncionais[i].isrk():
                if operacoes[unidadesFuncionais[i].getpc()].getIssue() < clock and operacoes[unidadesFuncionais[i].getpc()].getLeitura() == -1:
                    operacoes[unidadesFuncionais[i].getpc()].setLeitura(clock)
    return


def execution(operacoes: List[operacoesStatus], unidadesFuncionais: List[UnidadeFuncionalStatus], clock: int):
    for i in range(len(unidadesFuncionais)):
        if unidadesFuncionais[i].isBusy():
            if operacoes[unidadesFuncionais[i].getpc()].getLeitura() < clock and operacoes[unidadesFuncionais[i].getpc()].getLeitura() != -1 and operacoes[unidadesFuncionais[i].getpc()].getExecucaof() == -1:
                if operacoes[unidadesFuncionais[i].getpc()].getExecucaoi() == -1:
                    operacoes[unidadesFuncionais[i].getpc()
                              ].setExecucaoi(clock)
                if unidadesFuncionais[i].getOP() == 'ld':
                    operacoes[unidadesFuncionais[i].getpc()
                              ].setExecucaof(clock)
                elif unidadesFuncionais[i].getOP() == 'addd' or unidadesFuncionais[i].getOP() == 'subd':
                    if clock - operacoes[unidadesFuncionais[i].getpc()].getExecucaoi() == 1:
                        operacoes[unidadesFuncionais[i].getpc()
                                  ].setExecucaof(clock)
                elif unidadesFuncionais[i].getOP() == 'multd':
                    if clock - operacoes[unidadesFuncionais[i].getpc()].getExecucaoi() == 9:
                        operacoes[unidadesFuncionais[i].getpc()
                                  ].setExecucaof(clock)
                elif unidadesFuncionais[i].getOP() == 'divd':
                    if clock - operacoes[unidadesFuncionais[i].getpc()].getExecucaoi() == 39:
                        operacoes[unidadesFuncionais[i].getpc()
                                  ].setExecucaof(clock)
    return


def writeResults(unidadesFuncionais: List[UnidadeFuncionalStatus], operacoes: List[operacoesStatus], registradores: List[str], clock: int):
    if not isWAR():
        for i in range(len(unidadesFuncionais)):
            if unidadesFuncionais[i].isBusy():
                if operacoes[unidadesFuncionais[i].getpc()].getExecucaof() != -1 and operacoes[unidadesFuncionais[i].getpc()].getExecucaof() < clock:
                    operacoes[unidadesFuncionais[i].getpc()].setEscrita(clock)
                    operacoes[unidadesFuncionais[i].getpc()
                              ].setFinalizada(True)
    return


def canRead(unidadesFuncionais: List[UnidadeFuncionalStatus], operacoes: List[operacoesStatus], registradores: List[str]):
    for i in range(len(unidadesFuncionais)):
        if unidadesFuncionais[i].isBusy():
            if unidadesFuncionais[i].getfk() == 'rb':
                unidadesFuncionais[i].setqk(registradores[13])
            else:
                unidadesFuncionais[i].setqk(
                    registradores[int(re.sub('[^0-9]', '',  unidadesFuncionais[i].getfk()))])
            if unidadesFuncionais[i].getfj() == '':
                unidadesFuncionais[i].setqk('')
            else:
                unidadesFuncionais[i].setqj(
                    registradores[int(re.sub('[^0-9]', '',  unidadesFuncionais[i].getfj()))])

            if unidadesFuncionais[i].getqj() == '' and operacoes[unidadesFuncionais[i].getpc()].getLeitura() == -1:
                unidadesFuncionais[i].setrj(True)
            else:
                unidadesFuncionais[i].setrj(False)
            if unidadesFuncionais[i].getqk() == '' and operacoes[unidadesFuncionais[i].getpc()].getLeitura() == -1:
                unidadesFuncionais[i].setrk(True)
            else:
                unidadesFuncionais[i].setrk(False)
    return


def canExecute(unidadesFuncionais: List[UnidadeFuncionalStatus], operacoes: List[operacoesStatus]):
    for i in range(len(unidadesFuncionais)):
        if unidadesFuncionais[i].isBusy():
            if operacoes[unidadesFuncionais[i].getpc()].getLeitura() != -1 and operacoes[unidadesFuncionais[i].getpc()].getExecucaoi() == -1:
                unidadesFuncionais[i].setrj(False)
                unidadesFuncionais[i].setrk(False)
    return


def isVazio(unidadesFuncionais: List[UnidadeFuncionalStatus], memoria, pc: int) -> bool:
    if pc < len(memoria)-1:
        return True
    for i in range(len(unidadesFuncionais)):
        if unidadesFuncionais[i].isBusy():
            return True
    return False


def scoreboarding(operacoes):
    pc = 0
    clock = 1
    registradoresStatus = ['']*14
    unidadesFuncionais = [UnidadeFuncionalStatus() for _ in range(5)]
    unidadesFuncionais[0].setNome('Integer')
    unidadesFuncionais[1].setNome('Mult1')
    unidadesFuncionais[2].setNome('Mult2')
    unidadesFuncionais[3].setNome('Add')
    unidadesFuncionais[4].setNome('Divide')
    while isVazio(unidadesFuncionais, operacoes, pc):
        pc = issue(operacoes, unidadesFuncionais,
                   registradoresStatus, pc, clock)
        canRead(unidadesFuncionais, operacoes, registradoresStatus)
        read_operands(operacoes, unidadesFuncionais, clock)
        canExecute(unidadesFuncionais, operacoes)
        execution(operacoes, unidadesFuncionais, clock)
        writeResults(unidadesFuncionais, operacoes, registradoresStatus, clock)
        clock = clock + 1
    return


def buscaOp(Lines, pc) -> List[operacoesStatus]:
    statusop = operacoesStatus()
    if pc < len(Lines):
        statusop.setOP(Lines[pc][0])
        statusop.setfi(Lines[pc][1][0])
        statusop.setfj(Lines[pc][1][1])
        statusop.setfk(Lines[pc][1][2])
    return statusop


def lerArq(nome_arq):
    try:
        arquivo = open(nome_arq, 'r')
        memoria = arquivo.read().splitlines()
        for i in range(len(memoria)):
            memoria[i] = memoria[i].split(' ', 1)
            memoria[i][1] = memoria[i][1].split(',')
            if memoria[i][0] == 'ld':
                aux = memoria[i][1][1]
                aux = aux.split(')')
                aux[0] = aux[0].replace('(', '')
                memoria[i][1][1] = aux[0]
                memoria[i][1].append(aux[1])
        return memoria
    except FileNotFoundError:
        print("O arquivo nao existe tente executar novamente")
        exit()


def writestatus(nome_arq):
    nome_arq = nome_arq.split('.')
    saida = nome_arq[0]
    saida = saida+'.out'
    arquivo = open(saida, 'w')


def pipeline(memoria):
    pc = 0
    clock = 1
    regBusca = operacoesStatus()
    registradoresStatus = ['']*14
    unidadesFuncionais = [UnidadeFuncionalStatus() for _ in range(5)]
    statusOP = []
    unidadesFuncionais[0].setNome('Integer')
    unidadesFuncionais[1].setNome('Mult1')
    unidadesFuncionais[2].setNome('Mult2')
    unidadesFuncionais[3].setNome('Add')
    unidadesFuncionais[4].setNome('Divide')
    regBusca = buscaOp(memoria, pc)
    clock = clock+1
    pc = issue(regBusca, unidadesFuncionais,
               registradoresStatus, pc, clock, statusOP)
    buscaOp(memoria, pc)
    clock = clock+1
    canRead(unidadesFuncionais, statusOP, registradoresStatus)
    read_operands(statusOP, unidadesFuncionais, clock)
    pc = issue(regBusca, unidadesFuncionais,
               registradoresStatus, pc, clock, statusOP)
    regBusca = buscaOp(memoria, pc)
    clock = clock+1
    canExecute(unidadesFuncionais, statusOP)
    execution(statusOP, unidadesFuncionais, clock)
    canRead(unidadesFuncionais, statusOP, registradoresStatus)
    read_operands(statusOP, unidadesFuncionais, clock)
    pc = issue(regBusca, unidadesFuncionais,
               registradoresStatus, pc, clock, statusOP)
    regBusca = buscaOp(memoria, pc)
    while isVazio(unidadesFuncionais, memoria, pc):
        clock = clock+1
        writeResults(unidadesFuncionais, statusOP, registradoresStatus, clock)
        canExecute(unidadesFuncionais, statusOP)
        execution(statusOP, unidadesFuncionais, clock)
        canRead(unidadesFuncionais, statusOP, registradoresStatus)
        read_operands(statusOP, unidadesFuncionais, clock)
        pc = issue(regBusca, unidadesFuncionais,
                   registradoresStatus, pc, clock, statusOP)
        regBusca = buscaOp(memoria, pc)
        for i in range(len(unidadesFuncionais)):
            if unidadesFuncionais[i].isBusy():
                if statusOP[unidadesFuncionais[i].getpc()].getEscrita() != -1:
                    registradoresStatus[int(
                        re.sub('[^0-9]', '', statusOP[unidadesFuncionais[i].getpc()].getfi()))] = ''
                    unidadesFuncionais[i].reset()

    return


def main():
    memoria = lerArq(sys.argv[1])
    pipeline(memoria)
    # scoreboarding(operacoes)
    writestatus(sys.argv[1])
    return 0


if __name__ == "__main__":
    main()
