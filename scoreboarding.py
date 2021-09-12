import sys
import re
from typing import List, Tuple
from componentes import Scoreboarding, regEscrita, operacao, UnidadeFuncional

'''
Nome: Luiz Fernando Okada
RA:107247
Trabalho 1 Arquitetura de Organização de computadores
'''


'''
Verifica se o arquivo de entrada possui a sintaxe das instruçoes correta
'''


def verificaOP(memoria):
    operacoes = ['ld', 'muld', 'addd', 'subd', 'divd']
    for i in range(len(memoria)):
        if memoria[i][0] not in operacoes:
            print("arquivo de entrada com sintaxe errada")
            exit()


'''
Verifica se o arquivo de entrada possui a sintaxe dos operandos correta
'''


def verificaOperandos(memoria):
    operandos = ['r0', 'r1', 'r2', 'r3', 'r4', 'r5',
                 'r6', 'r7', 'r8', 'r9', 'r10', 'r11', 'r12', 'rb']
    for i in range(len(memoria)):
        if len(memoria[i][1]) < 2:
            print("Arquivo de entrada com operandos errados")
            exit()
        else:
            if memoria[i][0] == 'ld':
                aux = memoria[i][1][1]
                aux = aux.split(')')
                aux[0] = aux[0].replace('(', '')
                memoria[i][1][1] = aux[0]
                try:
                    memoria[i][1].append(aux[1])
                except IndexError:
                    print("sintaxe de uma instrucao ld esta errada")
                    exit()
            for j in range(len(memoria[i][1])):
                memoria[i][1][j] = memoria[i][1][j].strip()
                if len(memoria[i][1]) > 3:
                    print("Arquivo de entrada com operandos errados")
                    exit()
                elif memoria[i][1][j] not in operandos:
                    if memoria[i][0] == 'ld':
                        try:
                            int(memoria[i][1][1])
                        except ValueError:
                            print("Arquivo de entrada com operandos errados")
                            exit()
                    else:
                        print("Arquivo de entrada com operandos errados")
                        exit()

    return


'''
Lê o arquivo de entrada e armazena as instruções na memória
e inicializa um arquivo em branco que será a saida
'''


def lerArq(nome_arq: str) -> Tuple[str, List[str]]:
    try:
        arquivo = open(nome_arq, 'r')
        memoria = arquivo.read().splitlines()
        for i in range(len(memoria)):
            memoria[i] = memoria[i].split(' ', 1)
            memoria[i][1] = memoria[i][1].split(',')
        verificaOP(memoria)
        verificaOperandos(memoria)
        nome_arq = nome_arq.split('.')
        saida = nome_arq[0]
        saida = saida+'.out'
        arquivo = open(saida, 'w')
        return memoria
    except FileNotFoundError:
        print("O arquivo nao existe tente executar novamente")
        exit()


'''
Funçao que representa o simulador do pipeline
'''
'''
Funçao responsável por escrever o arquivo de saida
'''


def writestatus(nome_arq: str, unidadesFuncionais: List[UnidadeFuncional], operacoes: List[operacao], registradores: List[str], clock: int):
    nome_arq = nome_arq.split('.')
    saida = nome_arq[0]
    saida = saida+'.out'
    arquivo = open(saida, 'a')
    arquivo.writelines('Clock:'+str(clock)+'\n')
    arquivo.write(
        '--------------------------------Status operacoes-------------------------------------\n')
    arquivo.write(
        'OP    |Fi  |Fj  |Fk  |issue\t\t|read\t\t|Execution\t|write\t\t|\n')

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
            arquivo.write('\t\t|')
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
            arquivo.write('\t\t|\n')
    arquivo.write('\n')
    arquivo.write(
        '------------------------Status Unidades Funcionais-------------------------\n')
    arquivo.write('FU     |'+' Busy\t|' +
                  'OP    |'+'Fi  |'+'Fj  |'+'Fk  |'+'Qj       |'+'Qk       |'+'Rj     |'+'Rk     |'+'\n')
    for i in range(len(unidadesFuncionais)):
        if i == 3:
            arquivo.write(unidadesFuncionais[i].getNome()+'    |')
        elif i == 0:
            arquivo.write(unidadesFuncionais[i].getNome()+'|')
        elif i == 4:
            arquivo.write(unidadesFuncionais[i].getNome()+' |')
        else:
            arquivo.write(unidadesFuncionais[i].getNome()+'  |')
        if unidadesFuncionais[i].isBusy():
            arquivo.write(str(unidadesFuncionais[i].isBusy())+'\t|')
            if i == 1 or i == 2:
                arquivo.write(unidadesFuncionais[i].getOP()+'  |')
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
            arquivo.write(str(unidadesFuncionais[i].isBusy())+'\t|')
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
Verifica se existe o Hazzard WAW usada no issue
'''


def isWAW(operacao: operacao, registradores: List[str], regiEscrita: regEscrita) -> bool:
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
Verifica se existe o Hazzard WAR usado no writing
'''


def isWAR(unidadeFuncional: UnidadeFuncional, unidadesFuncionais: List[UnidadeFuncional]) -> bool:
    for i in range(len(unidadesFuncionais)):
        if (unidadeFuncional.getfi() == unidadesFuncionais[i].getfj() and unidadesFuncionais[i].isrj()) or (unidadeFuncional.getfi() == unidadesFuncionais[i].getfk() and unidadesFuncionais[i].isrk()):
            return True
    return False


'''
Fução que busca a instrução na memória
É o estágio de busca do pipeline
retorna o registradoe que dentro dele tem a próxima instrução que deve ser emitida
'''


def buscaOp(Lines, pc: int) -> operacao:
    regBusca = operacao()
    if pc < len(Lines):
        regBusca.setOP(Lines[pc][0])
        regBusca.setfi(Lines[pc][1][0].strip())
        regBusca.setfj(Lines[pc][1][1].strip())
        regBusca.setfk(Lines[pc][1][2].strip())
    return regBusca


'''
Função que emite uma instrução
retorna o PC(Program Counter)
'''


def issue(operacao: operacao, scoreboarding: Scoreboarding, pc: int, clock: int, regiEscrita: regEscrita) -> int:
    if operacao.isVazio():
        return pc
    elif not isWAW(operacao, scoreboarding.getRegs(), regiEscrita):
        if operacao.getOP() == 'ld':
            UF = 0
        elif operacao.getOP() == 'muld':
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


def read_operands(scoreboarding: Scoreboarding,  clock: int, regiEscrita: regEscrita):
    for i in range(len(scoreboarding.getUFs())):
        if scoreboarding.getUF(i).isBusy() and i not in regiEscrita.getUF():
            if scoreboarding.getUF(i).isrj() and scoreboarding.getUF(i).isrk():
                if scoreboarding.getOP(scoreboarding.getUF(i).getpc()).getIssue() < clock:
                    scoreboarding.getOP(scoreboarding.getUF(
                        i).getpc()).setLeitura(clock)
                    scoreboarding.getUF(i).setrj(False)
                    scoreboarding.getUF(i).setrk(False)
    return


'''
Função que executa uma operação que esta em uma UF
com as segintes latencias de execução
OP      ciclos
ld      1
addd    2
subd    2
multd   10
divd    40
'''


def execution(scoreboarding: Scoreboarding, clock: int):
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
                elif scoreboarding.getUF(i).getOP() == 'muld':
                    if clock - scoreboarding.getOP(scoreboarding.getUF(i).getpc()).getExecucaoi() == 9:
                        scoreboarding.getOP(scoreboarding.getUF(
                            i).getpc()).setExecucaof(clock)
                elif scoreboarding.getUF(i).getOP() == 'divd':
                    if clock - scoreboarding.getOP(scoreboarding.getUF(
                            i).getpc()).getExecucaoi() == 39:
                        scoreboarding.getOP(scoreboarding.getUF(
                            i).getpc()).setExecucaof(clock)
    return


'''
Funçao que escreve os resultados das instruções retorna um 
registrador que nele contem as UFs e registradores que foram alterados n estágio da escrita
'''


def writeResults(scoreboarding: Scoreboarding, clock: int) -> regEscrita:
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
                    for j in range(len(scoreboarding.getUFs())):
                        if scoreboarding.getUF(j).getqj() == scoreboarding.getUF(i).getNome():
                            scoreboarding.getUF(j).setqj('')
                            scoreboarding.getUF(j).setrj(True)
                            alterados.setUF(j)
                        if scoreboarding.getUF(j).getqk() == scoreboarding.getUF(i).getNome():
                            scoreboarding.getUF(j).setqk('')
                            scoreboarding.getUF(j).setrk(True)
                            alterados.setUF(j)
                    scoreboarding.setReg(int(
                        re.sub('[^0-9]', '', scoreboarding.getUF(i).getfi())), '')
                    scoreboarding.getUF(i).reset()
    return alterados


'''
Verifica se o pipiline está vazio
'''


def isVazio(unidadesFuncionais: List[UnidadeFuncional], memoria, pc: int) -> bool:
    if pc < len(memoria):
        return True
    for i in range(len(unidadesFuncionais)):
        if unidadesFuncionais[i].isBusy():
            return True
    return False


def pipeline(memoria: Tuple[str, List[str]]):
    pc = 0
    clock = 0
    regBusca = operacao()
    regiEscrita = regEscrita()
    scoreboarding = Scoreboarding()
    clock = clock+1
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
        writestatus(sys.argv[1], scoreboarding.getUFs(),
                    scoreboarding.getOPs(), scoreboarding.getRegs(), clock)
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
