# Aluno: Micael Davi Lima de Oliveira - Bacharelado em Física - 21851626 - FB01
# Professor: José Francisco
# Disciplina: Cálculo Numérico 2019/2

'''
Parte I: Eliminação gaussiana sem pivoteamento

Este algoritmo teve como principal referência o código em MATLAB/Python encontrado no 
seguinte site:

Link: https://learnche.org/3E4/Assignment_2_-_2010_-_Solution/Bonus_question

'''

import numpy as np
import matplotlib.pyplot as plt

def elimination(A, b, n):
    """
    Função para realizar a eliminação do elemento pertencente à próxima linha.
    """
    print("\n")
    print("+-------------------+")
    print("+   Processamento   +")
    print("+-------------------+")
    print("\n")

    for row in range(0, n-1):
        for i in range(row+1, n):
            factor = A[i,row] / A[row,row]
            for j in range(row, n):
                A[i,j] = A[i,j] - factor * A[row,j]

            b[i] = b[i] - factor * b[row]

        print("A" + str(row+1) + "= \n")
        print('%s' % (A))

        print("\nB" + str(row+1) + "= \n")
        print('%s' % (b))
        print("--------------------")

    return A, b

def substitution(a, b, n):
    """"
    Função que efetua a substituição do elemento da linha anterior.
    """
    x = np.zeros((n,1))
    x[n-1] = b[n-1] / a[n-1, n-1]
    for row in range(n-2, -1, -1):
        sums = b[row]
        for j in range(row+1, n):
            sums = sums - a[row,j] * x[j]
        x[row] = sums / a[row,row]
    return x

def gauss(A, b):
    """
    Esta função efetua a eliminação gaussiana sem o pivoteamento
    """
    n = A.shape[0]

    # Verificação de elementos nulos nas diagonais.
    if any(np.diag(A)==0):
        print("\n Risco de uma divisao por zero, pois nao ha suporte ao pivoteamento.")

    A, b = elimination(A, b, n)
    return substitution(A, b, n)

# Rotina principal do algoritmo
while (True):
    n_eq = int(input("\n - Digite o numero total de equacoes: "))

    A = np.array(eval(input("\n - Insira a matriz A que representa o sistema de equacoes: ")))
    b = np.array(eval(input("\n - Insira o vetor B: "))) 

    x = gauss(A, b)

    print("\n")
    print("+-------------------+")
    print("+    Resultados     +")
    print("+-------------------+")
    print('\n Coordenadas referentes a solucao do sistema: \n\n%s' %x)

    plt.matshow(A)
    fig = plt.gcf()
    fig.canvas.set_window_title('Matriz de Correlação')

    plt.show()

    op = int(input("\n\n Efetuar um novo calculo? \n\n (1) Sim  \n (2) Nao \n \n Opcao: "))

    if (op == 2):
        break

