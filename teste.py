import sys


def main():
    nome_arq = sys.argv[1]
    arquivo = open(nome_arq, 'r')
    Lines = arquivo.readlines()
    linha = []
    for lines in Lines:
        linha.append(lines.strip())
    print(linha)
    for i in range(len(linha)):
        string1 = linha[i].split()
    print(string1)
    operacao = string1[1]
    print(operacao.split(","))
    return 0


if __name__ == "__main__":
    main()
