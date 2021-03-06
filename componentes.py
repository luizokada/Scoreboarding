
from instrucao import instrucao, barramentoExecute, barramentoIssue, barramentoRead, instrucaoStatus
from typing import List, Tuple
import re


'''
Classe que representa os bancos de registradores usados no pipiline e entre os estágios do pipeline
'''


class bancoRegistradores:
    def __init__(self) -> None:
        self.pc = 0  # registrador PC
        # registrador da busca serve como baramento entre bisca e emissao
        self.regBusca = instrucao()
        # registrado escrita, serve como um barramento entre a escrita e a emissao
        self.regEscrita = []
        # registrado escrita, serve como um barramento entre a emissao e leitura
        self.regIssue = [barramentoIssue() for _ in range(5)]
        # registrado escrita, serve como um barramento entre a leitura e execucao
        self.regRead = [barramentoRead() for _ in range(5)]
        # registrado escrita, serve como um barramento entre a execucao e escrita
        self.regExecute = [barramentoExecute() for _ in range(5)]
        pass

    def getPC(self):
        return self.pc

    def setPC(self, pc: int):
        self.pc = pc

    def getReBusca(self):
        return self.regBusca

    def setReBusca(self, instrucao: instrucao):
        self.regBusca = instrucao

    def getReIssue(self):
        return self.regIssue

    def setReIssue(self, dado: barramentoIssue, i):
        self.regIssue[i] = dado

    def getReRead(self):
        return self.regRead

    def setReRead(self, dado: barramentoRead, i):
        self.regRead[i] = dado

    def setReExecute(self, dado: barramentoExecute, i):
        self.regExecute[i] = dado

    def getReExecute(self):
        return self.regExecute

    def getRegEscrita(self):
        return self.regEscrita

    def resetRegEscrita(self):
        self.regEscrita = []

    def setRegEscrita(self, i: int):
        self.regEscrita.append(i)


'''
Classe que representa as unidade funcionais
'''


class UnidadeFuncional:
    def __init__(self) -> None:
        self.nome = ''      # nome da Unidade Funcional
        self.busy = False   # busy status
        self.instru = instrucao()
        self.qj = ''        # unidades funcionais que produziram fj
        self.qk = ''        # unidades funcionais que produziram fk
        self.rj = True      # flag para fk
        self.rk = True      # flag para fk
        self.pc = -1        # pc da instruçao usando a unidade funcional
        self.usada = False  # flag para saber se a unidade funcional pode executar um acao no ciclo
        # flag que alerta o scoreboarding que a execuçao de um instruçao foi finalizada

        pass
    '''
    sets e gets dos atributos    
    '''

    def getInstrucao(self):
        return self.instru

    def setInstrucao(self, instrucao: instrucao):
        self.instru.setOP(instrucao.getOP())
        self.instru.setfk(instrucao.getfk())
        self.instru.setfi(instrucao.getfi())
        if instrucao.getOP() == 'ld':
            self.instru.setfj('')
        else:
            self.instru.setfj(instrucao.getfj())

    def isUsado(self) -> bool:
        return self.usada

    def setUsado(self, usado: bool):
        self.usada = usado

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

    def setNome(self, nome: str):
        self.nome = nome

    def getNome(self) -> str:
        return self.nome

    def setqj(self, qj: str):
        self.qj = qj

    def getqj(self) -> str:
        return self.qj

    def setqk(self, qk: str):
        self.qk = qk

    def getqk(self) -> str:
        return self.qk

    def getpc(self) -> int:
        return self.pc

    def setpc(self, pc: int):
        self.pc = pc

    '''
    define os atributos da UF para o deafult(como ela foi criada)
    '''

    def reset(self):
        self.busy = False
        self.instru.setOP('')
        self.instru.setfi('')
        self.instru.setfj('')
        self.instru.setfk('')
        self.rj = True
        self.rk = True
        self.readOperands = False
        self.executed = False
        self.pc = -1


'''
Classe que representa o scoreboarding
'''


class Scoreboarding:
    def __init__(self) -> None:
        # status das instruções que ja passaram do estágio de busca
        self.statusOp = [instrucaoStatus(instrucao())]
        # status dos registradores
        self.registradores = {'r0': '', 'r1': '', 'r2': '', 'r3': '', 'r4': '', 'r5': '',
                              'r6': '', 'r7': '', 'r8': '', 'r9': '', 'r10': '', 'r11': '', 'r12': '', 'rb': ''}
        self.issued = False  # variavel que notifica para o processador que foi feito uma emissao
    ''' 
    Set e gets dessa classes
    '''

    def setIssued(self, issued: bool):
        self.issued = issued

    def isIssued(self):
        return self.issued

    def getOPs(self) -> List[instrucaoStatus]:
        return self.statusOp

    def getOP(self, i: int) -> instrucaoStatus:
        return self.statusOp[i]

    def getRegs(self) -> dict:
        return self.registradores

    def getReg(self, i: str) -> str:
        return self.registradores[i]

    def setReg(self, i: str, nome: str):
        self.registradores[i] = nome

    def setOP(self, OP: instrucao):
        self.statusOp.append(OP)

    '''
    Verifica se existe o Hazzard WARW
    usado na emissao
    '''

    def isWAW(self, instrucao: instrucao, registradores: List[str], regEscrita: List[int]) -> bool:
        if registradores[instrucao.getfi()] == '' and instrucao.getfi() not in regEscrita:
            return False
        else:
            return True
    '''
    Verifica se existe o Hazzard WAR 
    usado no writing
    '''

    def isWAR(self, unidadeFuncional: UnidadeFuncional, unidadesFuncionais: List[UnidadeFuncional]) -> bool:
        for i in range(len(unidadesFuncionais)):
            if (unidadeFuncional.getInstrucao().getfi() == unidadesFuncionais[i].getInstrucao().getfj() and unidadesFuncionais[i].isrj()) or (unidadeFuncional.getInstrucao().getfi() == unidadesFuncionais[i].getInstrucao().getfk() and unidadesFuncionais[i].isrk()):
                return True
        return False
    '''
    Faz a emissao de uma instruçao que aj foi buscada
    '''

    def issue(self, unidadeFuncionais: List[UnidadeFuncional], registradores: bancoRegistradores, clock: int):
        if not registradores.getReBusca().isVazio() and not self.isWAW(registradores.getReBusca(), self.getRegs(), registradores.getRegEscrita()):
            if registradores.getReBusca().getOP() == 'ld':
                UF = 0
            elif registradores.getReBusca().getOP() == 'multd':
                if not unidadeFuncionais[1].isBusy():
                    UF = 1
                else:
                    UF = 2
            elif registradores.getReBusca().getOP() == 'addd' or registradores.getReBusca().getOP() == 'subd':
                UF = 3
            elif registradores.getReBusca().getOP() == 'divd':
                UF = 4
            else:
                return
            if not unidadeFuncionais[UF].isBusy() and not unidadeFuncionais[UF].isUsado():
                unidadeFuncionais[UF].setBusy(True)
                unidadeFuncionais[UF].setInstrucao(registradores.getReBusca())
                unidadeFuncionais[UF].setpc(registradores.getPC())
                self.setReg(registradores.getReBusca().getfi(),
                            unidadeFuncionais[UF].getNome())
                if UF == 0:
                    unidadeFuncionais[UF].setqj('')
                else:
                    unidadeFuncionais[UF].setqj(self.getReg(
                        registradores.getReBusca().getfj()))
                unidadeFuncionais[UF].setqk(self.getReg(
                    registradores.getReBusca().getfk()))
                if unidadeFuncionais[UF].getqj() != '':
                    unidadeFuncionais[UF].setrj(False)
                if unidadeFuncionais[UF].getqk() != '':
                    unidadeFuncionais[UF].setrk(False)
                self.getOP(registradores.getPC()).setIssue(clock)
                unidadeFuncionais[UF].setUsado(True)
                self.setIssued(True)
                aux = barramentoIssue()
                aux.setfi(unidadeFuncionais[UF].getInstrucao().getfi())
                aux.setfj(unidadeFuncionais[UF].getInstrucao().getfj())
                aux.setfk(unidadeFuncionais[UF].getInstrucao().getfj())
                aux.setOP(unidadeFuncionais[UF].getInstrucao().getOP())
                aux.setUF(UF)
                registradores.setReIssue(aux, UF)
                return
            else:
                self.setIssued(False)
                return
        else:
            self.setIssued(False)
            return
    '''
    Faz a leitura de operados de uma instruçao que ja foi emitida
    '''

    def read_operands(self,  clock: int, unidadeFuncionais: List[UnidadeFuncional], registradores: bancoRegistradores):
        for i in range(len(registradores.getReIssue())):
            if registradores.getReIssue()[i].getUF() != -1:
                UF = registradores.getReIssue()[i].getUF()
                if not unidadeFuncionais[UF].isUsado():
                    if unidadeFuncionais[UF].isrj() and unidadeFuncionais[i].isrk():
                        self.getOP(
                            unidadeFuncionais[UF].getpc()).setLeitura(clock)
                        unidadeFuncionais[UF].setrj(False)
                        unidadeFuncionais[UF].setrk(False)
                        unidadeFuncionais[UF].setqj('')
                        unidadeFuncionais[UF].setqk('')
                        unidadeFuncionais[UF].setUsado(True)
                        aux = barramentoRead()
                        aux.setfi(unidadeFuncionais[UF].getInstrucao().getfi())
                        aux.setfj(unidadeFuncionais[UF].getInstrucao().getfj())
                        aux.setfk(unidadeFuncionais[UF].getInstrucao().getfj())
                        aux.setOP(unidadeFuncionais[UF].getInstrucao().getOP())
                        aux.setUF(UF)
                        registradores.setReRead(aux, UF)
                        registradores.getReIssue()[i].esvazia()

        return

    '''
    Faz a execuçao de uma instruçao cujo os operando ja foram Lidos
    com as seguintes latencias de execução
    OP      ciclos
    ld      1
    addd    2
    subd    2
    multd   10
    divd    40
    '''

    def execution(self, clock: int, unidadeFuncionais: List[UnidadeFuncional], registradores: bancoRegistradores):
        for i in range(len(registradores.getReRead())):
            if registradores.getReRead()[i].getUF() != -1:
                UF = registradores.getReRead()[i].getUF()
                if not unidadeFuncionais[UF].isUsado():
                    if self.getOP(unidadeFuncionais[UF].getpc()).getExecucaoi() == -1:
                        self.getOP(
                            unidadeFuncionais[UF].getpc()).setExecucaoi(clock)
                        unidadeFuncionais[UF].setUsado(True)
                    count = clock - \
                        self.getOP(
                            unidadeFuncionais[UF].getpc()).getExecucaoi()
                    aux = barramentoExecute()
                    aux.setfi(unidadeFuncionais[UF].getInstrucao().getfi())
                    aux.setUF(UF)
                    if unidadeFuncionais[UF].getInstrucao().getOP() == 'ld' and count == 0:
                        self.getOP(
                            unidadeFuncionais[UF].getpc()).setExecucaof(clock)
                        aux.setResult('resultado')
                        registradores.setReExecute(aux, UF)
                        registradores.getReRead()[i].esvazia()
                    elif unidadeFuncionais[UF].getInstrucao().getOP() == 'addd' or unidadeFuncionais[UF].getInstrucao().getOP() == 'subd':
                        if count == 1:
                            self.getOP(
                                unidadeFuncionais[UF].getpc()).setExecucaof(clock)
                            unidadeFuncionais[UF].setUsado(True)
                            aux.setResult('resultado')
                            registradores.setReExecute(aux, UF)
                            registradores.getReRead()[i].esvazia()
                        elif count < 1:
                            unidadeFuncionais[UF].setUsado(True)
                    elif unidadeFuncionais[UF].getInstrucao().getOP() == 'multd':
                        if count == 9:
                            aux.setResult('resultado')
                            registradores.setReExecute(aux, UF)
                            registradores.getReRead()[i].esvazia()
                            self.getOP(
                                unidadeFuncionais[UF].getpc()).setExecucaof(clock)
                        elif count < 9:
                            unidadeFuncionais[UF].setUsado(True)
                    elif unidadeFuncionais[UF].getInstrucao().getOP() == 'divd':
                        if count == 39:
                            aux.setResult('resultado')
                            registradores.setReExecute(aux, UF)
                            registradores.getReRead()[i].esvazia()
                            self.getOP(
                                unidadeFuncionais[UF].getpc()).setExecucaof(clock)
                        elif count < 39:
                            unidadeFuncionais[UF].setUsado(False)
        return

    '''
    Funçao que escreve os resultados das instruções obtidos no estagio de execuçao
    '''

    def writeResults(self, clock: int, unidadeFuncionais: List[UnidadeFuncional], registradores: bancoRegistradores):
        # toda vez que entra na escrita reseta esse registrador pois ja se alterou o ciclo
        registradores.resetRegEscrita()
        for i in range(len(registradores.getReExecute())):
            if registradores.getReExecute()[i].getUF() != -1:
                UF = registradores.getReExecute()[i].getUF()
                if not unidadeFuncionais[UF].isUsado():
                    if not self.isWAR(unidadeFuncionais[UF], unidadeFuncionais):
                        self.getOP(
                            unidadeFuncionais[UF].getpc()).setEscrita(clock)
                        unidadeFuncionais[UF].setUsado(True)
                        for j in range(len(unidadeFuncionais)):
                            if unidadeFuncionais[j].getqj() == unidadeFuncionais[UF].getNome():
                                unidadeFuncionais[j].setrj(True)
                                unidadeFuncionais[j].setUsado(True)
                            if unidadeFuncionais[j].getqk() == unidadeFuncionais[UF].getNome():
                                unidadeFuncionais[j].setrk(True)
                                unidadeFuncionais[j].setUsado(True)
                        self.setReg(
                            unidadeFuncionais[UF].getInstrucao().getfi(), '')
                        # salva o id do registrador que foi alterado nesse ciclo, para evitar que ocorra uma emissão
                        # de instruções que estavam bloqueda por WAW
                        registradores.getReExecute()[i].esvazia()
                        registradores.setRegEscrita(
                            unidadeFuncionais[UF].getInstrucao().getfi())
                        unidadeFuncionais[UF].reset()
        return
    '''
    Funçao que simula o Bookkeeping
    '''

    def bookkeeping(self, unidadeFuncionais: List[UnidadeFuncional], clock: int, registradores: bancoRegistradores):
        self.writeResults(clock, unidadeFuncionais, registradores)
        self.execution(clock, unidadeFuncionais, registradores)
        self.read_operands(clock, unidadeFuncionais, registradores)
        self.issue(unidadeFuncionais, registradores, clock)
