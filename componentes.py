
from typing import List, Tuple
from instrucao import operacao
import re
'''
Registrador do estágio escrita
'''


class bancoRegistradores:
    def __init__(self) -> None:
        self.pc = 0  # registrador PC
        self.regBusca = operacao()  # registrador da busca
        # registrado escrita, serve para marcar os resgistradores que foram alterados no estagio da escrita
        self.regEscrita = []
        pass

    def getPC(self):
        return self.pc

    def setPC(self, pc: int):
        self.pc = pc

    def getReBusca(self):
        return self.regBusca

    def setReBusca(self, operacao: operacao):
        self.regBusca = operacao

    def getRegEscrita(self):
        return self.regEscrita


'''
Classe que representa os status das unidade funcionais
'''


class UnidadeFuncional:
    def __init__(self) -> None:
        self.nome = ''      # nome da Unidade Funcional
        self.busy = False   # busy status
        self.op = ''        # OP que esta na unidade funcional
        self.fi = ''        # registrador destino
        self.fj = ''        # operando 1
        self.fk = ''        # operando 2
        self.qj = ''        # unidades funcionais que produziram fj
        self.qk = ''        # unidades funcionais que produziram fk
        self.rj = True      # flag para fk
        self.rk = True      # flag para fk
        self.pc = -1        # pc da instruçao usando a unidade funcional
        self.usada = False  # flag para saber se a unidade funcional pode executar um acao no ciclo
        # flag para saber se a unidade funcional pode executar um acao no ciclo
        self.executed = False
        pass
    '''
    sets e gets dos atributos    
    '''

    def isUsado(self) -> bool:
        return self.usada

    def setUsado(self, usado: bool):
        self.usada = usado

    def isExecuted(self) -> bool:
        return self.executed

    def setExecuted(self, ex: bool):
        self.executed = ex

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

    def setOP(self, op: str):
        self.op = op

    def getOP(self) -> str:
        return self.op

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

    def setfi(self, fi: str):
        self.fi = fi

    def getfi(self) -> str:
        return self.fi

    def setfj(self, fj: str):
        self.fj = fj

    def getfj(self) -> str:
        return self.fj

    def setfk(self, fk: str):
        self.fk = fk

    def getfk(self) -> str:
        return self.fk

    def getpc(self) -> int:
        return self.pc

    def setpc(self, pc: int):
        self.pc = pc

    '''
    define os atributos da UF para o deafult(como ela foi criada)
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
        self.executed = False
        self.pc = -1


'''
Classe que representa o scoreboarding
'''


class Scoreboarding:
    def __init__(self) -> None:
        # status das instruções que ja passaram do estágio de busca
        self.statusOp = [operacao()]
        self.registradores = ['']*14  # status dos registradores
    ''' 
    Set e gets dessa classe
    '''

    def getOPs(self) -> List[operacao]:
        return self.statusOp

    def getOP(self, i: int) -> operacao:
        return self.statusOp[i]

    def getRegs(self) -> List[str]:
        return self.registradores

    def getReg(self, i: int) -> str:
        return self.registradores[i]

    def setReg(self, i: int, nome: str):
        self.registradores[i] = nome

    def setOP(self, OP: operacao):
        self.statusOp.append(OP)

    def isWAW(self, operacao: operacao, registradores: List[str], regEscrita: List[int]) -> bool:
        if operacao.getfi() == 'rb':
            if registradores[13] == '' and 13 not in regEscrita.getRef():
                return False
            else:
                return True
        elif registradores[int(re.sub('[^0-9]', '', operacao.getfi()))] == '' and int(re.sub('[^0-9]', '', operacao.getfi())) not in regEscrita:
            return False
        else:
            return True

    '''
    Verifica se existe o Hazzard WAR 
    usado no writing
    '''

    def isWAR(self, unidadeFuncional: UnidadeFuncional, unidadesFuncionais: List[UnidadeFuncional]) -> bool:
        for i in range(len(unidadesFuncionais)):
            if (unidadeFuncional.getfi() == unidadesFuncionais[i].getfj() and unidadesFuncionais[i].isrj()) or (unidadeFuncional.getfi() == unidadesFuncionais[i].getfk() and unidadesFuncionais[i].isrk()):
                return True
        return False
    '''
    funçao issue do scoreboarding
    '''

    def issue(self, operacao: operacao, unidadeFuncionais: List[UnidadeFuncional], pc: int, clock: int, regEscrita) -> int:
        if not operacao.isVazio() and not self.isWAW(operacao, self.getRegs(), regEscrita):
            if operacao.getOP() == 'ld':
                UF = 0
            elif operacao.getOP() == 'muld':
                if not unidadeFuncionais[1].isBusy():
                    UF = 1
                else:
                    UF = 2
            elif operacao.getOP() == 'addd' or operacao.getOP() == 'subd':
                UF = 3
            elif operacao.getOP() == 'divd':
                UF = 4
            else:
                return
            if not unidadeFuncionais[UF].isBusy() and not unidadeFuncionais[UF].isUsado():
                unidadeFuncionais[UF].setOP(operacao.getOP())
                unidadeFuncionais[UF].setfi(operacao.getfi())
                unidadeFuncionais[UF].setfk(operacao.getfk())
                unidadeFuncionais[UF].setpc(pc)
                self.setReg(
                    int(re.sub('[^0-9]', '', operacao.getfi())), unidadeFuncionais[UF].getNome())
                try:
                    int(self.getOP(pc).getfj())
                    unidadeFuncionais[UF].setqj('')
                    unidadeFuncionais[UF].setfj('')
                    if self.getOP(pc).getfk() == 'rb':
                        unidadeFuncionais[UF].setqk(self.getReg(13))
                    else:
                        unidadeFuncionais[UF].setqk(self.getReg(
                            int(re.sub('[^0-9]', '', operacao.getfk()))))
                except ValueError:
                    unidadeFuncionais[UF].setfj(self.getOP(pc).getfj())
                    unidadeFuncionais[UF].setqk(
                        self.getReg(int(re.sub('[^0-9]', '', self.getOP(pc).getfk()))))
                    unidadeFuncionais[UF].setqj(
                        self.getReg(int(re.sub('[^0-9]', '', self.getOP(pc).getfj()))))
                unidadeFuncionais[UF].setBusy(True)
                if unidadeFuncionais[UF].getqj() != '':
                    unidadeFuncionais[UF].setrj(False)
                if unidadeFuncionais[UF].getqk() != '':
                    unidadeFuncionais[UF].setrk(False)
                self.getOP(pc).setIssue(clock)
                unidadeFuncionais[UF].setUsado(True)
                return
            else:
                return
        else:
            return
    '''
    funçao read_operands do scoreboarding
    '''

    def read_operands(self,  clock: int, unidadeFuncionais: List[UnidadeFuncional]):
        for i in range(len(unidadeFuncionais)):
            if unidadeFuncionais[i].isBusy() and not unidadeFuncionais[i].isUsado():
                if unidadeFuncionais[i].isrj() and unidadeFuncionais[i].isrk():
                    self.getOP(unidadeFuncionais[i].getpc()).setLeitura(clock)
                    unidadeFuncionais[i].setrj(False)
                    unidadeFuncionais[i].setrk(False)
                    unidadeFuncionais[i].setUsado(True)
        return

    '''
    Função que executa uma operação que esta em uma UF
    com as seguintes latencias de execução
    OP      ciclos
    ld      1
    addd    2
    subd    2
    multd   10
    divd    40
    '''

    def execution(self, clock: int, unidadeFuncionais: List[UnidadeFuncional]):
        for i in range(len(unidadeFuncionais)):
            if unidadeFuncionais[i].isBusy() and not unidadeFuncionais[i].isUsado():
                if (not unidadeFuncionais[i].isrj() and not unidadeFuncionais[i].isrk()) and unidadeFuncionais[i].getqj() == '' and unidadeFuncionais[i].getqk() == '':
                    if self.getOP(unidadeFuncionais[i].getpc()).getExecucaoi() == -1:
                        self.getOP(
                            unidadeFuncionais[i].getpc()).setExecucaoi(clock)
                        unidadeFuncionais[i].setUsado(True)
                        unidadeFuncionais[i].setExecuted(False)
                    count = clock - \
                        self.getOP(unidadeFuncionais[i].getpc()).getExecucaoi()
                    if unidadeFuncionais[i].getOP() == 'ld' and count == 0:
                        self.getOP(
                            unidadeFuncionais[i].getpc()).setExecucaof(clock)
                        unidadeFuncionais[i].setExecuted(True)
                    elif unidadeFuncionais[i].getOP() == 'addd' or unidadeFuncionais[i].getOP() == 'subd':
                        if count == 1:
                            self.getOP(
                                unidadeFuncionais[i].getpc()).setExecucaof(clock)
                            unidadeFuncionais[i].setExecuted(True)
                            unidadeFuncionais[i].setUsado(True)
                        elif count < 1:
                            unidadeFuncionais[i].setUsado(True)
                            unidadeFuncionais[i].setExecuted(False)
                    elif unidadeFuncionais[i].getOP() == 'muld':
                        if count == 9:
                            unidadeFuncionais[i].setExecuted(True)
                            self.getOP(
                                unidadeFuncionais[i].getpc()).setExecucaof(clock)
                        elif count < 9:
                            unidadeFuncionais[i].setUsado(True)
                            unidadeFuncionais[i].setExecuted(False)
                    elif unidadeFuncionais[i].getOP() == 'divd':
                        if count == 39:
                            unidadeFuncionais[i].setExecuted(True)
                            self.getOP(
                                unidadeFuncionais[i].getpc()).setExecucaof(clock)
                        elif count < 39:
                            unidadeFuncionais[i].setUsado(False)
                            unidadeFuncionais[i].setExecuted(False)
        return

    '''
    Funçao que escreve os resultados das instruções retorna um 
    registrador que nele contem as UFs e registradores que foram alterados n estágio da escrita
    '''

    def writeResults(self, clock: int, unidadeFuncionais: List[UnidadeFuncional], registradorEscrita: List[int]):
        registradorEscrita = []
        for i in range(len(unidadeFuncionais)):
            if unidadeFuncionais[i].isBusy():
                if not self.isWAR(unidadeFuncionais[i], unidadeFuncionais) and not unidadeFuncionais[i].isUsado():
                    if unidadeFuncionais[i].isExecuted():
                        self.getOP(
                            unidadeFuncionais[i].getpc()).setEscrita(clock)
                        unidadeFuncionais[i].setUsado(True)
                        for j in range(len(unidadeFuncionais)):
                            if unidadeFuncionais[j].getqj() == unidadeFuncionais[i].getNome():
                                unidadeFuncionais[j].setqj('')
                                unidadeFuncionais[j].setrj(True)
                                unidadeFuncionais[j].setUsado(True)
                            if unidadeFuncionais[j].getqk() == unidadeFuncionais[i].getNome():
                                unidadeFuncionais[j].setqk('')
                                unidadeFuncionais[j].setrk(True)
                                unidadeFuncionais[j].setUsado(True)
                        self.setReg(int(
                            re.sub('[^0-9]', '', unidadeFuncionais[i].getfi())), '')
                        registradorEscrita.append(int(
                            re.sub('[^0-9]', '', unidadeFuncionais[i].getfi())))
                        unidadeFuncionais[i].reset()
        return
    '''
    Funçao qeu simula o Bookkeeping
    '''

    def bookkeeping(self, unidadeFuncionais: List[UnidadeFuncional], clock: int, registradores: bancoRegistradores):
        self.writeResults(clock, unidadeFuncionais,
                          registradores.getRegEscrita())
        self.execution(clock, unidadeFuncionais)
        self.read_operands(clock, unidadeFuncionais)
        self.issue(registradores.getReBusca(), unidadeFuncionais,
                   registradores.getPC(), clock, registradores.getRegEscrita())
