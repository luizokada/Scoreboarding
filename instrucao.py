'''
Classe que representa os status das instruçoes
'''


class instrucao:
    def __init__(self) -> None:
        self.op = ''         # OP que esta na unidade funcional
        self.fi = ''         # registrador destino
        self.fj = ''         # operando 1
        self.fk = ''         # operando 2
        self.issue = -1      # clock da emissao
        self.leitura = -1    # clock da leitura
        self.execucaoi = -1  # clock do inicio da execucao
        self.execucaof = -1  # clock do termino da execucao
        self.escrita = -1    # clock da escrita
    '''
    Sets e gets dessa classe
    '''

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


"""
Barramentos entre os estagios do pipeline
"""


class barramentoIssue:
    def __init__(self) -> None:
        self.op = ''         # OP que esta na unidade funcional
        self.fi = ''         # registrador destino
        self.fj = ''         # operando 1
        self.fk = ''         # operando 2
        self.UF = -1
        pass
    '''
    retira os dados do barramento pois a instruçao foi para o próximo estágio
    '''

    def esvazia(self):
        self.op = ''
        self.fi = ''
        self.fj = ''
        self.fk = ''
        self.UF = -1

    def getUF(self):
        return self.UF

    def setUF(self, UF: int):
        self.UF = UF

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

    def isVazio(self):
        return self.UF == -1


class barramentoRead(barramentoIssue):

    def __init__(self) -> None:
        super().__init__()
        pass


class barramentoExecute:
    def __init__(self) -> None:
        self.result = ''  # resultado da execuçao da instrucao
        self.UF = -1  # UF que esta a intrucao
        self.fi = ''  # registrador destino
        pass
    '''
    retira os dados do barramento pois a instruçao foi para o próximo estágio
    '''

    def esvazia(self):
        self.result = ''
        self.UF = -1
        self.fi = ''

    def getResult(self):
        return self.UF

    def setResult(self, result):
        self.result = result

    def getUF(self):
        return self.UF

    def setUF(self, UF: int):
        self.UF = UF

    def setfi(self, fi):
        self.fi = fi

    def getfi(self) -> str:
        return self.fi

    def isVazio(self):
        return self.UF == -1
