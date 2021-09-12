
from typing import List, Tuple
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

    def getUF(self) -> List[int]:
        return self.UF

    def getRef(self) -> List[int]:
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

    def setOP(self, OP: str):
        self.op = OP

    def getOP(self) -> str:
        return self.op

    def setfi(self, fi):
        self.fi = fi

    def getfi(self) -> str:
        return self.fi

    def setfj(self, fj):
        self.fj = fj

    def getfj(self) -> str:
        return self.fj

    def setfk(self, fk):
        self.fk = fk

    def getfk(self) -> str:
        return self.fk

    def setIssue(self, issue: int):
        self.issue = issue

    def getIssue(self) -> int:
        return self.issue

    def setLeitura(self, leitura: int):
        self.leitura = leitura

    def getLeitura(self) -> int:
        return self.leitura

    def setExecucaoi(self, execucaoi: int):
        self.execucaoi = execucaoi

    def getExecucaoi(self) -> int:
        return self.execucaoi

    def setExecucaof(self, execucaof: int):
        self.execucaof = execucaof

    def getExecucaof(self) -> int:
        return self.execucaof

    def getEscrita(self) -> int:
        return self.escrita

    def setEscrita(self, escrita: int):
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


class Scoreboarding:
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
    ''' 
    Set e gets dessa classe
    '''

    def getUFs(self) -> List[UnidadeFuncionalStatus]:
        return self.unidadeFuncionais

    def getUF(self, UF: int) -> UnidadeFuncionalStatus:
        return self.unidadeFuncionais[UF]

    def getOPs(self) -> List[operacoesStatus]:
        return self.statusOp

    def getOP(self, i: int) -> operacoesStatus:
        return self.statusOp[i]

    def getRegs(self) -> List[str]:
        return self.registradores

    def getReg(self, i: int) -> str:
        return self.registradores[i]

    def setReg(self, i: int, nome: str):
        self.registradores[i] = nome

    def setOP(self, OP: operacoesStatus):
        self.statusOp.append(OP)
