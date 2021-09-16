import re
from typing import List, Tuple
from componentes import UnidadeFuncional
from instrucao import instrucao

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


def writestatus(nome_arq: str, unidadesFuncionais: List[UnidadeFuncional], instrucao: List[instrucao], registradores: dict, clock: int):
    nome_arq = nome_arq.split('.')
    saida = nome_arq[0]
    saida = saida+'.out'
    arquivo = open(saida, 'a')
    arquivo.writelines('Clock:'+str(clock)+'\n')
    arquivo.write('{:-^96}\n'.format('Status Operacoes'))
    estagios = ['issue', 'read', 'execution', 'Write']
    statusOP = ['OP', 'Fi', 'Fj', 'Fk']
    for status in statusOP:
        arquivo.write("{:6}".format(status)+"|")
    for estagio in estagios:
        arquivo.write("{:16}".format(estagio)+"|")
    arquivo.write('\n')
    for i in range(len(instrucao)):
        arquivo.write("{:6}".format(instrucao[i].getOP())+"|")
        arquivo.write("{:6}".format(instrucao[i].getfi())+"|")
        arquivo.write("{:6}".format(instrucao[i].getfj())+"|")
        arquivo.write("{:6}".format(instrucao[i].getfk())+"|")
        arquivo.write('{:16}'.format(
            str(instrucao[i].getIssue()).replace('-1', ' '))+'|')
        arquivo.write('{:16}'.format(
            str(instrucao[i].getLeitura()).replace('-1', ' '))+'|')
        execucao = str(instrucao[i].getExecucaoi()).replace("-1", ' ')
        execucao = execucao+" - "
        execucao = execucao+str(instrucao[i].getExecucaof()).replace("-1", ' ')
        arquivo.write('{:^16}'.format(execucao)+'|')
        arquivo.write('{:16}'.format(
            str(instrucao[i].getEscrita()).replace('-1', ' '))+'|\n')
    arquivo.write('\n')
    arquivo.write("{:-^80}".format("Status Unidades funcionais")+'\n')
    ufstatus = ['FU', 'Busy', 'OP', 'Fi', 'Fj', 'Fk', 'Qj', 'Qk', 'Rj', 'Rk']
    for status in ufstatus:
        arquivo.write("{:7}".format(status)+"|")
    arquivo.write('\n')
    for i in range(len(unidadesFuncionais)):
        arquivo.write("{:7}".format(unidadesFuncionais[i].getNome())+"|")
        arquivo.write("{:7}".format(str(unidadesFuncionais[i].isBusy()))+"|")
        arquivo.write("{:7}".format(unidadesFuncionais[i].getOP())+"|")
        arquivo.write("{:7}".format(unidadesFuncionais[i].getfi())+"|")
        arquivo.write("{:7}".format(unidadesFuncionais[i].getfj())+"|")
        arquivo.write("{:7}".format(unidadesFuncionais[i].getfk())+"|")
        arquivo.write("{:7}".format(unidadesFuncionais[i].getqj())+"|")
        arquivo.write("{:7}".format(unidadesFuncionais[i].getqk())+"|")
        arquivo.write("{:7}".format(str(unidadesFuncionais[i].isrj()))+"|")
        arquivo.write("{:7}".format(str(unidadesFuncionais[i].isrk()))+"|")
        arquivo.write('\n')
    arquivo.write('\n')
    arquivo.write('{:-^117}\n'.format('Status Registradores'))
    regs = ['R0', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6',
            'R7', 'R8', 'R9', 'R10', 'R11', 'R12', 'RB']
    arquivo.write('    |')
    for r in regs:
        arquivo.write("{:7}".format(r)+"|")
    arquivo.write('\n')
    arquivo.write('UF  |')
    for i in registradores.keys():
        arquivo.write("{:7}".format(registradores[i])+"|")
    arquivo.write(
        '\n{:-^117}\n\n'.format(''))
    return
