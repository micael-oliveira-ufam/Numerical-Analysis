# Aluno: Micael Davi Lima de Oliveira - Bacharelado em Física - 21851626 - FB01
# Professor: José Francisco
# Disciplina: Cálculo Numérico 2019/2

"""
Parte II: Eliminação de Gauss_Jordan com pivoteamento parcial

Este algoritmo é uma adaptação do Algorithm 2.2.1  
encontrado no livro de Métodos Numéricos aplicados 
à Engenharia(1999) by Schilling and Harris.

"""

from numpy import*
from copy import*

import matplotlib.pyplot as plt

def GaussJordan(A,b):
    """
    Esta função retorna o vetor "x" presente
    no produto interno A.x=b.
    
    É assumido que "A" é uma matriz quadrada "n x n"
    onde, "m" e "b" constituem os elementos da matriz.
    """

    print("\n")
    print("+-------------------+")
    print("+   Processamento   +")
    print("+-------------------+")
    print("\n")

    n,m = A.shape
    # C constitui uma matriz auxiliar de segurança, e portanto, será importante
    # armazenar a matriz inicial e ser modificada com as iterações.
    C = zeros((n,m+1),float)
    C[:,0:n],C[:,n] = A, b

    for j in range(n):
        # Primeiro, é efetuado o pivoteamento parcial.
        p = j # O elemento da diagonal atual será escolhido como pivô.
        # Busca por um pivô alternativo que seja o maior elemento da coluna.
        for i in range(j+1,n):
            if abs(C[i,j]) > abs(C[p,j]): p = i
        if abs(C[p,j]) < 1.0e-16:
            print ("A matriz apresenta a propriedade de singularidade.")
            return b 
        #  Haverá uma troca de linha, para encontrar o maior elemento da diagonal.
        C[p,:],C[j,:] = copy(C[j,:]),copy(C[p,:])
        # Agora, haverá a eliminação do termo
        pivot = C[j,j]
        C[j,:] = C[j,:] / pivot
        for i in range(n):
            if i == j: continue
            C[i,:] = C[i,:] - C[i,j]*C[j,:]
        print("A" + str(j+1) + "= \n")
        print(C[:,0:n])

        print("\nB" + str(j+1) + "= \n")
        print(C[:,n])

        print("--------------------")
    I,x = C[:,0:n],C[:,n]
    return x

# Rotina principal do programa
while (True):        
    
    n_eq = int(input("\n - Digite o numero total de equacoes: "))

    A = array(eval(input("\n - Insira a matriz A que representa o sistema de equacoes: ")))
    b = array(eval(input("\n - Insira o vetor B: "))) 

    x = GaussJordan(A,b)

    print("\n")
    print("+-------------------+")
    print("+    Resultados     +")
    print("+-------------------+")
    print('\n Coordenadas referentes a solucao do sistema:\n\n')

    print ("x=", x)
    print ("Ax=", dot(A,x))

    plt.matshow(A)
    fig = plt.gcf()
    fig.canvas.set_window_title('Matriz de Correlação')

    plt.show()

    op = int(input("\n\n Efetuar um novo calculo? \n\n (1) Sim  \n (2) Nao \n \n Opcao: "))

    if (op == 2):
        break   