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
        self.rj = True
        self.rk = True
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
        return self.fi

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
    '''
    define os atributos do objeto como ele foi criado
    '''

    def reset(self):
        self.busy = False
        self.op = ''
        self.fi = ''
        self.fj = ''
        self.fk = ''
        self.qj = ''
        self.qk = ''
        self.rj = True
        self.rk = True
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
    '''
    Sets e gets dessa classe 
    '''

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
    '''
    Verifica se não existe operação
    '''

    def isVazio(self):
        if self.op == '':
            return True
        else:
            return False
        pass


'''
Verifica se existe o Hazzard WAW
'''


def isWAW(operacao: operacoesStatus, registradores: List[str]):
    if operacao.getfi() == 'rb':
        if registradores[13] == '':
            return False
        else:
            return True
    elif registradores[int(re.sub('[^0-9]', '', operacao.getfi()))] == '':
        return False
    else:
        return True


'''
Verifica se existe o Hazzard WAR
'''


def isWAR(unidadeFuncional: UnidadeFuncionalStatus, unidadesFuncionais: List[UnidadeFuncionalStatus], operacoes: List[operacoesStatus]):
    for i in range(len(unidadesFuncionais)):
        if unidadeFuncional.getfi() == unidadesFuncionais[i].getfj() or unidadeFuncional.getfi() == unidadesFuncionais[i].getfk():
            if operacoes[unidadesFuncionais[i].getpc()].getLeitura() == -1 and unidadesFuncionais[i].getpc() < unidadeFuncional.getpc():
                return True
    return False


'''
Funçao que emite uma operção 
'''


def issue(operacao: operacoesStatus, unidadesFuncionais: List[UnidadeFuncionalStatus], registradores: List[str], pc: int, clock: int, statusOPs: List[operacoesStatus]):
    if operacao.isVazio():
        return pc
    elif not isWAW(operacao, registradores):
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
    else:
        return pc


'''
Funçao que executa a leitura do operandos de um operação que esta em uma UF
'''


def read_operands(operacoes: List[operacoesStatus], unidadesFuncionais: List[UnidadeFuncionalStatus], registradores: List[str],  clock: int):
    canRead(unidadesFuncionais, operacoes, registradores)
    for i in range(len(unidadesFuncionais)):
        if unidadesFuncionais[i].isBusy():
            if unidadesFuncionais[i].isrj() and unidadesFuncionais[i].isrk():
                if operacoes[unidadesFuncionais[i].getpc()].getIssue() < clock and operacoes[unidadesFuncionais[i].getpc()].getLeitura() == -1:
                    operacoes[unidadesFuncionais[i].getpc()].setLeitura(clock)
    return


'''
Funçao que executa uma operação que esta em uma UF
'''


def execution(operacoes: List[operacoesStatus], unidadesFuncionais: List[UnidadeFuncionalStatus], clock: int):
    canExecute(unidadesFuncionais, operacoes)
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


'''
Funçao que escreve os resultados das operações
'''


def writeResults(unidadesFuncionais: List[UnidadeFuncionalStatus], operacoes: List[operacoesStatus], registradores: List[str], clock: int):
    for i in range(len(unidadesFuncionais)):
        if not isWAR(unidadesFuncionais[i], unidadesFuncionais, operacoes):
            if unidadesFuncionais[i].isBusy():
                if operacoes[unidadesFuncionais[i].getpc()].getExecucaof() != -1 and operacoes[unidadesFuncionais[i].getpc()].getExecucaof() < clock:
                    operacoes[unidadesFuncionais[i].getpc()].setEscrita(clock)
                    operacoes[unidadesFuncionais[i].getpc()
                              ].setFinalizada(True)
    return


'''
Retorna a UF que irá escrever no registrador
'''


def setUF(nome: str):
    if nome == 'Integer':
        UF = 0
    elif nome == 'Mult1':
        UF = 1
    elif nome == 'Mult2':
        UF = 2
    elif nome == 'Add':
        UF = 3
    elif nome == 'Divide':
        UF = 4
    else:
        UF = 5
    return UF


'''
Verifica o Hazzard RAW
Funçao que verifica se uma determina operação que está em uma UF pode começar a leitua

'''


def canRead(unidadesFuncionais: List[UnidadeFuncionalStatus], operacoes: List[operacoesStatus], registradores: List[str]):
    for i in range(len(unidadesFuncionais)):
        if unidadesFuncionais[i].isBusy() and operacoes[unidadesFuncionais[i].getpc()].getLeitura() == -1:
            if unidadesFuncionais[i].getfk() == 'rb':
                unidadesFuncionais[i].setqk(registradores[13])
            else:
                unidadesFuncionais[i].setqk(
                    registradores[int(re.sub('[^0-9]', '',  unidadesFuncionais[i].getfk()))])
            if unidadesFuncionais[i].getfj() == '':
                unidadesFuncionais[i].setqj('')
            else:
                unidadesFuncionais[i].setqj(
                    registradores[int(re.sub('[^0-9]', '',  unidadesFuncionais[i].getfj()))])
            if unidadesFuncionais[i].getfk() == 'rb':
                UFk = setUF(registradores[13])
            else:
                UFk = setUF(
                    registradores[int(re.sub('[^0-9]', '',  unidadesFuncionais[i].getfk()))])
            if unidadesFuncionais[i].getfj() == '':
                UFj = setUF('')
            else:
                UFj = setUF(
                    registradores[int(re.sub('[^0-9]', '',  unidadesFuncionais[i].getfj()))])
            if UFk == 5:
                unidadesFuncionais[i].setqk('')
            else:
                if operacoes[unidadesFuncionais[UFk].getpc()].getIssue() > operacoes[unidadesFuncionais[i].getpc()].getIssue():
                    unidadesFuncionais[i].setqk('')
            if UFj == 5:
                unidadesFuncionais[i].setqj('')
            else:
                if operacoes[unidadesFuncionais[UFj].getpc()].getIssue() > operacoes[unidadesFuncionais[i].getpc()].getIssue():
                    unidadesFuncionais[i].setqj('')
            if unidadesFuncionais[i].getqj() == '':
                unidadesFuncionais[i].setrj(True)
            else:
                unidadesFuncionais[i].setrj(False)
            if unidadesFuncionais[i].getqk() == '':
                unidadesFuncionais[i].setrk(True)
            else:
                unidadesFuncionais[i].setrk(False)
    return


'''
Funçao que verifica se uma determina operação que está em uma UF pode começar a execução
'''


def canExecute(unidadesFuncionais: List[UnidadeFuncionalStatus], operacoes: List[operacoesStatus]):
    for i in range(len(unidadesFuncionais)):
        if unidadesFuncionais[i].isBusy():
            if operacoes[unidadesFuncionais[i].getpc()].getLeitura() != -1 and operacoes[unidadesFuncionais[i].getpc()].getExecucaoi() == -1:
                unidadesFuncionais[i].setrj(False)
                unidadesFuncionais[i].setrk(False)
    return


'''
Verifica se o pipiline está vazio
'''


def isVazio(unidadesFuncionais: List[UnidadeFuncionalStatus], memoria, pc: int) -> bool:
    if pc < len(memoria):
        return True
    for i in range(len(unidadesFuncionais)):
        if unidadesFuncionais[i].isBusy():
            return True
    return False


'''
Fução que busca a operaç~o na memória 
É o estágio de busca do pipeline
'''


def buscaOp(Lines, pc) -> List[operacoesStatus]:
    statusop = operacoesStatus()
    if pc < len(Lines):
        statusop.setOP(Lines[pc][0])
        statusop.setfi(Lines[pc][1][0].strip())
        statusop.setfj(Lines[pc][1][1].strip())
        statusop.setfk(Lines[pc][1][2].strip())
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
        nome_arq = nome_arq.split('.')
        saida = nome_arq[0]
        saida = saida+'.out'
        arquivo = open(saida, 'w')
        return memoria
    except FileNotFoundError:
        print("O arquivo nao existe tente executar novamente")
        exit()


'''
Funçao responsável por escrever o arquivo de saida 
'''


def writestatus(nome_arq, unidadesFuncionais: List[UnidadeFuncionalStatus], operacoes: List[operacoesStatus], registradores: List[str], clock: int):
    nome_arq = nome_arq.split('.')
    saida = nome_arq[0]
    saida = saida+'.out'
    arquivo = open(saida, 'a')
    arquivo.writelines('Clock:'+str(clock)+'\n')
    arquivo.write('\t\t\tStatus operacoes\n')
    arquivo.write('\t\t\t     issue      |' +
                  'read\t|'+'Execution\t|'+'write\t|\n')

    for i in range(len(operacoes)):
        if operacoes[i].getOP() == 'ld':
            arquivo.write(operacoes[i].getOP()+'    |')
        else:
            if operacoes[i].getOP() == 'multd':
                arquivo.write(operacoes[i].getOP()+' |')
            else:
                arquivo.write(operacoes[i].getOP()+'  |')
        if abs(int(re.sub('[^0-9]', '', operacoes[i].getfi()))) > 9:
            arquivo.write(operacoes[i].getfi()+' |')
        else:
            arquivo.write(operacoes[i].getfi()+'  |')
        if abs(int(re.sub('[^0-9]', '', operacoes[i].getfj()))) > 9:
            arquivo.write(operacoes[i].getfj()+' |')
        else:
            arquivo.write(operacoes[i].getfj()+'  |')
        if operacoes[i].getfk() != 'rb':
            if abs(int(re.sub('[^0-9]', '', operacoes[i].getfk()))) > 9:
                arquivo.write(operacoes[i].getfk()+' |')
            else:
                arquivo.write(operacoes[i].getfk()+'  |')
        else:
            arquivo.write(operacoes[i].getfk()+'  |')
        if operacoes[i].getIssue() != -1:
            arquivo.write('\t\t'+str(operacoes[i].getIssue())+'\t|')
        else:
            arquivo.write('     ')
        if operacoes[i].getLeitura() != -1:
            arquivo.write(str(operacoes[i].getLeitura())+'\t|')
        else:
            arquivo.write('\t|')
        if operacoes[i].getExecucaoi() != -1:
            if operacoes[i].getExecucaof() != -1:
                arquivo.write(str(operacoes[i].getExecucaoi()) +
                              '-'+str(operacoes[i].getExecucaof())+'\t\t|')
            else:
                arquivo.write(str(operacoes[i].getExecucaoi()) +
                              ' - \t\t|')
        else:
            arquivo.write('\t\t|')
        if operacoes[i].getEscrita() != -1:
            arquivo.write(str(operacoes[i].getEscrita())+'\t|'+'\n')
        else:
            arquivo.write('\t|\n')
    arquivo.write('\n')
    arquivo.write(
        '------------------------Status Unidades Funcionais-------------------------\n')
    arquivo.write('   FU   |'+' Busy  |' +
                  'OP    |'+'Fi  |'+'Fj  |'+'Fk  |'+'Qj       |'+'Qk       |'+'Rj     |'+'Rk     |'+'\n')
    for i in range(len(unidadesFuncionais)):
        if i == 3:
            arquivo.write(unidadesFuncionais[i].getNome()+'  \t|')
        else:
            arquivo.write(unidadesFuncionais[i].getNome()+'\t|')
        if unidadesFuncionais[i].isBusy():
            arquivo.write(str(unidadesFuncionais[i].isBusy())+'\t|')
            if i == 1 or i == 2:
                arquivo.write(unidadesFuncionais[i].getOP()+' |')
            elif i == 0:
                arquivo.write(unidadesFuncionais[i].getOP()+'    |')
            else:
                arquivo.write(unidadesFuncionais[i].getOP()+'  |')
            if abs(int(re.sub('[^0-9]', '', unidadesFuncionais[i].getfi()))) > 9:
                arquivo.write(unidadesFuncionais[i].getfi()+' |')
            else:
                arquivo.write(unidadesFuncionais[i].getfi()+'  |')
            if unidadesFuncionais[i].getfj() == '':
                arquivo.write('\t |')
            else:
                if abs(int(re.sub('[^0-9]', '', unidadesFuncionais[i].getfj()))) > 9:
                    arquivo.write(unidadesFuncionais[i].getfj()+' |')
                else:
                    arquivo.write(unidadesFuncionais[i].getfj()+'  |')
            if unidadesFuncionais[i].getfk() != 'rb':
                if abs(int(re.sub('[^0-9]', '', unidadesFuncionais[i].getfk()))) > 9:
                    arquivo.write(unidadesFuncionais[i].getfk()+' |')
                else:
                    arquivo.write(unidadesFuncionais[i].getfk()+'  |')
            else:
                arquivo.write(unidadesFuncionais[i].getfk()+'  |')
            if unidadesFuncionais[i].getqj() == '':
                arquivo.write('         |')
            else:
                if unidadesFuncionais[i].getqj() == 'Integer':
                    arquivo.write(unidadesFuncionais[i].getqj()+'  |')
                elif unidadesFuncionais[i].getqj() == 'Divide':
                    arquivo.write(unidadesFuncionais[i].getqj()+'   |')
                elif unidadesFuncionais[i].getqj() == 'Mult1' or unidadesFuncionais[i].getqj() == 'Mult2':
                    arquivo.write(unidadesFuncionais[i].getqj()+'    |')
                elif unidadesFuncionais[i].getqj() == 'Add':
                    arquivo.write(unidadesFuncionais[i].getqj()+'      |')
            if unidadesFuncionais[i].getqk() == '':
                arquivo.write('         |')
            else:
                if unidadesFuncionais[i].getqk() == 'Integer':
                    arquivo.write(unidadesFuncionais[i].getqk()+'  |')
                elif unidadesFuncionais[i].getqk() == 'Divide':
                    arquivo.write(unidadesFuncionais[i].getqk()+'   |')
                elif unidadesFuncionais[i].getqk() == 'Mult1' or unidadesFuncionais[i].getqk() == 'Mult2':
                    arquivo.write(unidadesFuncionais[i].getqk()+'    |')
                elif unidadesFuncionais[i].getqk() == 'Add':
                    arquivo.write(unidadesFuncionais[i].getqk()+'      |')
            if unidadesFuncionais[i].isrj():
                arquivo.write(str(unidadesFuncionais[i].isrj())+'   |')
            else:
                arquivo.write(str(unidadesFuncionais[i].isrj())+'  |')
            if unidadesFuncionais[i].isrk():
                arquivo.write(str(unidadesFuncionais[i].isrk())+'   |\n')
            else:
                arquivo.write(str(unidadesFuncionais[i].isrk())+'  |\n')

        else:
            arquivo.write(str(unidadesFuncionais[i].isBusy())+'  |')
            arquivo.write('      |')
            arquivo.write('    |')
            arquivo.write('    |')
            arquivo.write('    |')
            arquivo.write('         |')
            arquivo.write('         |')
            arquivo.write('       |')
            arquivo.write('       |')
            arquivo.write('\n')

    arquivo.write('\n')
    arquivo.write(
        '----------------------------------------------Status Registradores--------------------------------------------------\n')
    arquivo.write(
        '    |R0     |R1     |R2     |R3     |R4     |R5     |R6     |R7     |R8     |R9     |R10    |R11    |R12    |RB     |\n')
    arquivo.write('UF  |')
    for i in range(len(registradores)):
        if registradores[i] == '':
            arquivo.write('       |')
        else:
            if registradores[i] == 'Mult1' or registradores[i] == 'Mult2':
                arquivo.write(registradores[i]+'  |')
            elif registradores[i] == 'Add':
                arquivo.write(registradores[i]+'    |')
            elif registradores[i] == 'Divide':
                arquivo.write(registradores[i]+' |')
            elif registradores[i] == 'Integer':
                arquivo.write(registradores[i]+'|')
    arquivo.write(
        '\n--------------------------------------------------------------------------------------------------------------------\n\n')
    return


'''
Funçao que representa o simulador do pipeline 
unidadeFuncionais[0] = Intenger
unidadeFuncionais[1] = Mult1
unidadeFuncionais[2] = Mult2
unidadeFuncionais[3] = add
unidadeFuncionais[4] = Divide
registradoresStatus[0]....[12] = r0....r12
registradoresStatus[13] = rb

'''


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
    writestatus(sys.argv[1], unidadesFuncionais,
                statusOP, registradoresStatus, clock)
    clock = clock+1
    pc = issue(regBusca, unidadesFuncionais,
               registradoresStatus, pc, clock, statusOP)
    regBusca = buscaOp(memoria, pc)
    writestatus(sys.argv[1], unidadesFuncionais,
                statusOP, registradoresStatus, clock)
    clock = clock+1
    read_operands(statusOP, unidadesFuncionais, registradoresStatus, clock)
    pc = issue(regBusca, unidadesFuncionais,
               registradoresStatus, pc, clock, statusOP)
    regBusca = buscaOp(memoria, pc)
    writestatus(sys.argv[1], unidadesFuncionais,
                statusOP, registradoresStatus, clock)
    clock = clock+1
    execution(statusOP, unidadesFuncionais, clock)
    read_operands(statusOP, unidadesFuncionais, registradoresStatus, clock)
    pc = issue(regBusca, unidadesFuncionais,
               registradoresStatus, pc, clock, statusOP)
    regBusca = buscaOp(memoria, pc)
    writestatus(sys.argv[1], unidadesFuncionais,
                statusOP, registradoresStatus, clock)
    while isVazio(unidadesFuncionais, memoria, pc):
        clock = clock+1
        writeResults(unidadesFuncionais, statusOP, registradoresStatus, clock)
        execution(statusOP, unidadesFuncionais, clock)
        read_operands(statusOP, unidadesFuncionais, registradoresStatus, clock)
        pc = issue(regBusca, unidadesFuncionais,
                   registradoresStatus, pc, clock, statusOP)
        regBusca = buscaOp(memoria, pc)
        writestatus(sys.argv[1], unidadesFuncionais,
                    statusOP, registradoresStatus, clock)
        for i in range(len(unidadesFuncionais)):
            if unidadesFuncionais[i].isBusy():
                if statusOP[unidadesFuncionais[i].getpc()].getEscrita() != -1:
                    registradoresStatus[int(
                        re.sub('[^0-9]', '', statusOP[unidadesFuncionais[i].getpc()].getfi()))] = ''
                    unidadesFuncionais[i].reset()
    clock = clock+1
    writestatus(sys.argv[1], unidadesFuncionais,
                statusOP, registradoresStatus, clock)
    return


def main():
    memoria = lerArq(sys.argv[1])
    pipeline(memoria)
    return 0


if __name__ == "__main__":
    main()
