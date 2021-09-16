
import sys
from typing import List, Tuple
from instrucao import instrucao, instrucaoStatus
from componentes import Scoreboarding, UnidadeFuncional, bancoRegistradores
from arquivo import writestatus, lerArq

'''
Nome: Luiz Fernando Okada
RA:107247
Trabalho 1 Arquitetura de Organização de computadores
'''

"""
Classe que representa o processador 
"""


class processador:
    def __init__(self) -> None:
        # unidades funcionais do processador
        self.unidadeFuncionais = [UnidadeFuncional() for _ in range(5)]
        self.unidadeFuncionais[0].setNome('Integer')
        self.unidadeFuncionais[1].setNome('Mult1')
        self.unidadeFuncionais[2].setNome('Mult2')
        self.unidadeFuncionais[3].setNome('Add')
        self.unidadeFuncionais[4].setNome('Divide')
        # banco de registradores
        self.registradores = bancoRegistradores()
        self.clock = 0  # clock de inicio
        self.scoreboard = Scoreboarding()  # scoreboard do processador
        pass

    '''
    Verifica se o pipiline está vazio
    '''

    def isVazio(self, instrucoes: List[instrucaoStatus], memoria, pc: int) -> bool:
        if pc+1 < len(memoria):
            return True
        for i in range(len(instrucoes)):
            if instrucoes[i].getEscrita() == -1:
                return True
        return False
    """
    Funçao que seta a flag Usado das UFS como False pois começou um novo cilco
    
    """

    def novoCiclo(self, unidadeFuncionais: List[UnidadeFuncional]):
        for uf in unidadeFuncionais:
            uf.setUsado(False)

    '''
    Fução que busca a instrução na memória
    É o estágio de busca do pipeline
    retorna o registrador que dentro dele tem a próxima instrução que deve ser emitida
    '''

    def buscaOp(self, memoria, instrucoes: List[instrucaoStatus], registradores: bancoRegistradores, issued: bool):
        # tratamento para o primeiro ciclo de clock quando nao se tem nada no pipeline
        if registradores.getPC() == 0 and not issued:
            registradores.getReBusca().setOP(memoria[registradores.getPC()][0])
            registradores.getReBusca().setfi(
                memoria[registradores.getPC()][1][0].strip())
            registradores.getReBusca().setfj(
                memoria[registradores.getPC()][1][1].strip())
            registradores.getReBusca().setfk(
                memoria[registradores.getPC()][1][2].strip())
            aux = instrucaoStatus(registradores.getReBusca())
            instrucoes[0] = aux
        elif registradores.getPC() < len(memoria) and issued:
            registradores.setReBusca(instrucao())
            if registradores.getPC()+1 < len(memoria):
                registradores.getReBusca().setOP(
                    memoria[registradores.getPC()+1][0])
                registradores.getReBusca().setfi(
                    memoria[registradores.getPC()+1][1][0].strip())
                registradores.getReBusca().setfj(
                    memoria[registradores.getPC()+1][1][1].strip())
                registradores.getReBusca().setfk(
                    memoria[registradores.getPC()+1][1][2].strip())
                aux = instrucaoStatus(registradores.getReBusca())
                instrucoes.append(aux)
                registradores.setPC(registradores.getPC()+1)
            else:
                registradores.setPC(registradores.getPC()+1)
        else:
            return
    '''
    Funcao que simula o pipeline 
    O inicio dela(antes do while) é a incializaçao do pipiline quando se nao tem nenhuma instruçao
    nos estagios
    O laco é o ciclo completo de um pipeline 
    '''

    def pipeline(self, memoria: Tuple[str, List[str]]):
        while self.isVazio(self.scoreboard.getOPs(), memoria, self.registradores.getPC()):
            self.clock = self.clock+1
            self.novoCiclo(self.unidadeFuncionais)
            self.scoreboard.bookkeeping(
                self.unidadeFuncionais, self.clock, self.registradores)
            self.buscaOp(memoria, self.scoreboard.getOPs(),
                         self.registradores, self.scoreboard.isIssued())
            writestatus(sys.argv[1], self.unidadeFuncionais,
                        self.scoreboard.getOPs(), self.scoreboard.getRegs(), self.clock)
        self.clock = self.clock+1
        writestatus(sys.argv[1], self.unidadeFuncionais,
                    self.scoreboard.getOPs(), self.scoreboard.getRegs(), self.clock)
        return


def main():
    Processador = processador()
    memoria = lerArq(sys.argv[1])
    Processador.pipeline(memoria)
    return 0


if __name__ == "__main__":
    main()
