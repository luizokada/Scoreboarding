import sys
import re
from typing import List

'''
Nome: Luiz Fernando Okada
RA:107247
Trabalho 1 Arquitetura de Organização de computadores
'''


'''
Registrador do estágio escrita
'''


class regEscrita:
    def __init__(self) -> None:
        self.registradores = []
        self.UF = []

    def setRegistrdor(self, reg: int):
        self.registradores.append(reg)

    def setUF(self, reg: int):
        self.UF.append(reg)

    def getUF(self):
        return self.UF

    def getRef(self):
        return self.registradores
        pass


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

    def setBusy(self, busy: bool):
        self.busy = busy

    def isrj(self) -> bool:
        return self.rj

    def setrj(self, rj: bool):
        self.rj = rj

    def isrk(self) -> bool:
        return self.rk

    def setrk(self, rk: bool):
        self.rk = rk

    def setOP(self, op):
        self.op = op

    def getOP(self):
        return self.op

    def setNome(self, nome: str):
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

    def setpc(self, pc: int):
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

    def setIssue(self, issue: int):
        self.issue = issue

    def getIssue(self):
        return self.issue

    def setLeitura(self, leitura: int):
        self.leitura = leitura

    def getLeitura(self):
        return self.leitura

    def setExecucaoi(self, execucaoi: int):
        self.execucaoi = execucaoi

    def getExecucaoi(self):
        return self.execucaoi

    def setExecucaof(self, execucaof: int):
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
Classe que representa o scoreboarding


'''


class scoreBoarding:
    def __init__(self) -> None:
        '''
        unidadeFuncionais[0] = Intenger
        unidadeFuncionais[1] = Mult1
        unidadeFuncionais[2] = Mult2
        unidadeFuncionais[3] = add
        unidadeFuncionais[4] = Divide
        registradoresStatus[0]....[12] = r0....r12
        registradoresStatus[13] = rb
        '''
        self.unidadeFuncionais = [UnidadeFuncionalStatus() for _ in range(5)]
        self.unidadeFuncionais[0].setNome('Integer')
        self.unidadeFuncionais[1].setNome('Mult1')
        self.unidadeFuncionais[2].setNome('Mult2')
        self.unidadeFuncionais[3].setNome('Add')
        self.unidadeFuncionais[4].setNome('Divide')
        self.statusOp = []
        self.registradores = ['']*14

    def getUFs(self):
        return self.unidadeFuncionais

    def getUF(self, UF: int):
        return self.unidadeFuncionais[UF]

    def getOPs(self):
        return self.statusOp

    def getOP(self, i: int):
        return self.statusOp[i]

    def getRegs(self):
        return self.registradores

    def getReg(self, i: int):
        return self.registradores[i]

    def setReg(self, i: int, nome: str):
        self.registradores[i] = nome

    def setOP(self, OP: operacoesStatus):
        self.statusOp.append(OP)


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
Verifica se existe o Hazzard WAW
'''


def isWAW(operacao: operacoesStatus, registradores: List[str], regiEscrita: regEscrita):
    if operacao.getfi() == 'rb':
        if registradores[13] == '' and 13 not in regiEscrita.getRef():
            return False
        else:
            return True
    elif registradores[int(re.sub('[^0-9]', '', operacao.getfi()))] == '' and int(re.sub('[^0-9]', '', operacao.getfi())) not in regiEscrita.getRef():
        return False
    else:
        return True


'''
Verifica se existe o Hazzard WAR
'''


def isWAR(unidadeFuncional: UnidadeFuncionalStatus, unidadesFuncionais: List[UnidadeFuncionalStatus]):
    for i in range(len(unidadesFuncionais)):
        if (unidadeFuncional.getfi() == unidadesFuncionais[i].getfj() and unidadesFuncionais[i].isrj()) or (unidadeFuncional.getfi() == unidadesFuncionais[i].getfk() and unidadesFuncionais[i].isrk()):
            return True
    return False


'''
Funçao que emite uma operção
'''


def issue(operacao: operacoesStatus, scoreboarding: scoreBoarding, pc: int, clock: int, regiEscrita: regEscrita):
    if operacao.isVazio():
        return pc
    elif not isWAW(operacao, scoreboarding.getRegs(), regiEscrita):
        if operacao.getOP() == 'ld':
            UF = 0
        elif operacao.getOP() == 'multd':
            if not scoreboarding.getUF(1).isBusy():
                UF = 1
            else:
                UF = 2
        elif operacao.getOP() == 'addd' or operacao.getOP() == 'subd':
            UF = 3
        elif operacao.getOP() == 'divd':
            UF = 4
        else:
            return pc
        if not scoreboarding.getUF(UF).isBusy() and UF not in regiEscrita.getUF():
            scoreboarding.getUF(UF).setOP(operacao.getOP())
            scoreboarding.getUF(UF).setfi(operacao.getfi())
            scoreboarding.getUF(UF).setfk(operacao.getfk())
            scoreboarding.getUF(UF).setpc(pc)
            scoreboarding.setReg(
                int(re.sub('[^0-9]', '', operacao.getfi())), scoreboarding.getUF(UF).getNome())
            try:
                int(operacao.getfj())
                scoreboarding.getUF(UF).setqj('')
                scoreboarding.getUF(UF).setfj('')
                if operacao.getfk() == 'rb':
                    scoreboarding.getUF(UF).setqk(scoreboarding.getReg(13))
                else:
                    scoreboarding.getUF(UF).setqk(scoreboarding.getReg(
                        int(re.sub('[^0-9]', '', operacao.getfk()))))
            except ValueError:
                scoreboarding.getUF(UF).setfj(operacao.getfj())
                scoreboarding.getUF(UF).setqk(
                    scoreboarding.getReg(int(re.sub('[^0-9]', '', operacao.getfk()))))
                scoreboarding.getUF(UF).setqj(
                    scoreboarding.getReg(int(re.sub('[^0-9]', '', operacao.getfj()))))
            scoreboarding.getUF(UF).setBusy(True)
            if scoreboarding.getUF(UF).getqj() != '':
                scoreboarding.getUF(UF).setrj(False)
            if scoreboarding.getUF(UF).getqk() != '':
                scoreboarding.getUF(UF).setrk(False)
            scoreboarding.setOP(operacao)
            scoreboarding.getOP(pc).setIssue(clock)
            return pc+1
        else:
            return pc
    else:
        return pc


'''
Funçao que executa a leitura do operandos de um operação que esta em uma UF
'''


def read_operands(scoreboarding: scoreBoarding,  clock: int, regiEscrita: regEscrita):
    for i in range(len(scoreboarding.getUFs())):
        if scoreboarding.getUF(i).isBusy() and i not in regiEscrita.getUF():
            if scoreboarding.getUF(i).isrj() and scoreboarding.getUF(i).isrk():
                if scoreboarding.getOP(scoreboarding.getUF(i).getpc()).getIssue() < clock and scoreboarding.getOP(scoreboarding.getUF(i).getpc()).getLeitura() == -1:
                    scoreboarding.getOP(scoreboarding.getUF(
                        i).getpc()).setLeitura(clock)
                    scoreboarding.getUF(i).setrj(False)
                    scoreboarding.getUF(i).setrk(False)
    return


'''
Funçao que executa uma operação que esta em uma UF
'''


def execution(scoreboarding: scoreBoarding, clock: int):
    for i in range(len(scoreboarding.getUFs())):
        if scoreboarding.getUF(i).isBusy():
            if (not scoreboarding.getUF(i).isrj() and not scoreboarding.getUF(i).isrk()) and scoreboarding.getUF(i).getqj() == '' and scoreboarding.getUF(i).getqk() == '':
                if scoreboarding.getOP(scoreboarding.getUF(i).getpc()).getExecucaoi() == -1:
                    scoreboarding.getOP(scoreboarding.getUF(
                        i).getpc()).setExecucaoi(clock)
                if scoreboarding.getUF(i).getOP() == 'ld' and scoreboarding.getOP(scoreboarding.getUF(
                        i).getpc()).getExecucaoi() == clock:
                    scoreboarding.getOP(scoreboarding.getUF(
                        i).getpc()).setExecucaof(clock)
                elif scoreboarding.getUF(i).getOP() == 'addd' or scoreboarding.getUF(i).getOP() == 'subd':
                    if clock - scoreboarding.getOP(scoreboarding.getUF(
                            i).getpc()).getExecucaoi() == 1:
                        scoreboarding.getOP(scoreboarding.getUF(
                            i).getpc()).setExecucaof(clock)
                elif scoreboarding.getUF(i).getOP() == 'multd':
                    if clock - scoreboarding.getOP(scoreboarding.getUF(
                            i).getpc()).getExecucaoi() == 9:
                        scoreboarding.getOP(scoreboarding.getUF(
                            i).getpc()).setExecucaof(clock)
                elif scoreboarding.getUF(i).getOP() == 'divd':
                    if clock - scoreboarding.getOP(scoreboarding.getUF(
                            i).getpc()).getExecucaoi() == 39:
                        scoreboarding.getOP(scoreboarding.getUF(
                            i).getpc()).setExecucaof(clock)
    return


'''
Funçao que escreve os resultados das operações
'''


def writeResults(scoreboarding: scoreBoarding, clock: int):
    alterados = regEscrita()
    for i in range(len(scoreboarding.getUFs())):
        if not isWAR(scoreboarding.getUF(i), scoreboarding.getUFs()):
            if scoreboarding.getUF(i).isBusy():
                if scoreboarding.getOP(scoreboarding.getUF(i).getpc()).getExecucaof() != -1 and scoreboarding.getOP(scoreboarding.getUF(i).getpc()).getExecucaof() < clock:
                    scoreboarding.getOP(scoreboarding.getUF(
                        i).getpc()).setEscrita(clock)
                    scoreboarding.getOP(scoreboarding.getUF(
                        i).getpc()).setFinalizada(True)
                    alterados.setRegistrdor(int(
                        re.sub('[^0-9]', '', scoreboarding.getUF(i).getfi())))
                    alterados.setUF(i)
    writestatus(sys.argv[1], scoreboarding.getUFs(),
                scoreboarding.getOPs(), scoreboarding.getRegs(), clock)
    for i in range(len(scoreboarding.getUFs())):
        if scoreboarding.getUF(i).isBusy() and i in alterados.getUF():
            for j in range(len(scoreboarding.getUFs())):
                if scoreboarding.getUF(j).getqj() == scoreboarding.getUF(i).getNome():
                    scoreboarding.getUF(j).setqj('')
                    scoreboarding.getUF(j).setrj(True)
                    alterados.setUF(j)
                if scoreboarding.getUF(j).getqk() == scoreboarding.getUF(i).getNome():
                    scoreboarding.getUF(j).setqk('')
                    scoreboarding.getUF(j).setrk(True)
                    alterados.setUF(j)
            if scoreboarding.getOP(scoreboarding.getUF(i).getpc()).getEscrita() == clock:
                scoreboarding.setReg(int(
                    re.sub('[^0-9]', '', scoreboarding.getUF(i).getfi())), '')
                scoreboarding.getUF(i).reset()

    return alterados


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


'''
Lê o arquivo de entrada e armazena as instruções na memória
'''


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
    arquivo.write(
        '--------------------------Status operacoes-------------------------------\n')
    arquivo.write(
        'OP    |Fi  |Fj  |Fk  |issue\t\t|read\t|Execution\t|write\t|\n')

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
            arquivo.write(str(operacoes[i].getLeitura())+'\t\t|')
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
            arquivo.write(str(operacoes[i].getEscrita())+'\t\t|'+'\n')
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
        elif i == 0:
            arquivo.write(unidadesFuncionais[i].getNome()+'|')
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
    regiEscrita = regEscrita()
    scoreboarding = scoreBoarding()
    regBusca = buscaOp(memoria, pc)
    writestatus(sys.argv[1], scoreboarding.getUFs(),
                scoreboarding.getOPs(), scoreboarding.getRegs(), clock)
    clock = clock+1
    pc = issue(regBusca, scoreboarding, pc, clock, regiEscrita)
    regBusca = buscaOp(memoria, pc)
    writestatus(sys.argv[1], scoreboarding.getUFs(),
                scoreboarding.getOPs(), scoreboarding.getRegs(), clock)
    clock = clock+1
    read_operands(scoreboarding, clock, regiEscrita)
    pc = issue(regBusca, scoreboarding, pc, clock, regiEscrita)
    regBusca = buscaOp(memoria, pc)
    writestatus(sys.argv[1], scoreboarding.getUFs(),
                scoreboarding.getOPs(), scoreboarding.getRegs(), clock)
    clock = clock+1
    execution(scoreboarding, clock)
    read_operands(scoreboarding, clock, regiEscrita)
    pc = issue(regBusca, scoreboarding, pc, clock, regiEscrita)
    regBusca = buscaOp(memoria, pc)
    writestatus(sys.argv[1], scoreboarding.getUFs(),
                scoreboarding.getOPs(), scoreboarding.getRegs(), clock)
    while isVazio(scoreboarding.getUFs(), memoria, pc):
        clock = clock+1
        regiEscrita = writeResults(scoreboarding, clock)
        execution(scoreboarding, clock)
        read_operands(scoreboarding, clock, regiEscrita)
        pc = issue(regBusca, scoreboarding, pc, clock, regiEscrita)
        regBusca = buscaOp(memoria, pc)
    clock = clock+1
    writestatus(sys.argv[1], scoreboarding.getUFs(),
                scoreboarding.getOPs(), scoreboarding.getRegs(), clock)
    return


def main():
    memoria = lerArq(sys.argv[1])
    pipeline(memoria)
    return 0


if __name__ == "__main__":
    main()
