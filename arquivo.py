import re
from typing import List, Tuple
from componentes import UnidadeFuncional
from instrucao import operacao

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
