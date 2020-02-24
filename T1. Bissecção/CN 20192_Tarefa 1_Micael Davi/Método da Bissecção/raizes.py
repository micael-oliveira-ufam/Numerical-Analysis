from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from numpy import*

from PyQt5.QtWidgets import QMessageBox

import numpy as np
from math import*
import matplotlib.pyplot as plt

import sys
import os

app = QtWidgets.QApplication([])
dlg = uic.loadUi("raizes.ui")  

dlg.bt_conf1.setIcon(QtGui.QIcon('Images/ok.png'))
dlg.bt_conf2.setIcon(QtGui.QIcon('Images/ok.png'))
dlg.bt_conf3.setIcon(QtGui.QIcon('Images/ok.png'))
dlg.bt_conf4.setIcon(QtGui.QIcon('Images/ok.png'))

coef = 0
aux = 0
cont_term = 0 
max_it = 0
epsilon = 0
aprox = 0

metodo = 0   # 0 para bisseccao; 1 para falsa posicao
m0 = 0 # valor inicial para a média aritmética ou ponderada dos 
       # extremos do intervalo


# Construction of table#

table 	= QTableWidget()
tableItem 	= QTableWidgetItem()
table.setWindowTitle("Resultados obtidos")
table.resize(650, 450)
table.setRowCount(1)
table.setColumnCount(6)

table.setHorizontalHeaderItem(0, QTableWidgetItem("a_n"))
table.setHorizontalHeaderItem(1, QTableWidgetItem("b_n"))
table.setHorizontalHeaderItem(2, QTableWidgetItem("m_n"))
table.setHorizontalHeaderItem(3, QTableWidgetItem("f(a_n)"))
table.setHorizontalHeaderItem(4, QTableWidgetItem("f(b_n)"))
table.setHorizontalHeaderItem(5, QTableWidgetItem("f(m_n)"))

def f(x):
    funcao = 0
    for i in range(size(coef)):
        funcao = funcao + float(coef[i]) * x ** int(size(coef) - i - 1)  
    return funcao

def conf1():
   dlg.bt_conf1.setEnabled(False)
   dlg.txt_gr.setEnabled(False) 
   dlg.txt_coef.setEnabled(True)
   dlg.bt_conf2.setEnabled(True)
   dlg.cb_coef.setEnabled(True)    

   global coef
   coef = zeros(int(dlg.txt_gr.text()) + 1)   

   sup = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
   for i in range(int(dlg.txt_gr.text()) + 1):     
    dlg.cb_coef.addItem("x" + str(int(dlg.txt_gr.text())-i).translate(sup))   

def conf2(): 
    global cont_term
    
    if (dlg.txt_coef.text() != ""):
        coef[dlg.cb_coef.currentIndex()] = dlg.txt_coef.text()
        dlg.cb_coef.setCurrentIndex(dlg.cb_coef.currentIndex()+1) 

        if (cont_term == size(coef)-1):
            dlg.cb_coef.setEnabled(False)
            dlg.bt_conf2.setEnabled(False)
            dlg.txt_coef.setEnabled(False)
            dlg.txt_it.setEnabled(True)
            dlg.bt_conf3.setEnabled(True)
        else:
            dlg.txt_coef.setText("")   

        cont_term += 1
   
    print(coef)   

def conf3():
    global max_it
    max_it = int(dlg.txt_it.text())

    dlg.bt_conf3.setEnabled(False)
    dlg.txt_it.setEnabled(False)
    dlg.bt_conf4.setEnabled(True)
    dlg.txt_pr.setEnabled(True)

def conf4():
    global epsilon
    epsilon = float(dlg.txt_pr.text())

    global aprox
    aprox = len(dlg.txt_pr.text()) - 1  

    dlg.bt_conf4.setEnabled(False)
    dlg.txt_pr.setEnabled(False)
    dlg.bt_mfp.setEnabled(True)
    dlg.bt_mb.setEnabled(True)

    dlg.lb_eq2.setEnabled(True)
    dlg.lb_n2.setEnabled(True)
    dlg.lb_pr2.setEnabled(True)    

    dlg.plot_f.setEnabled(True)
    dlg.actionComparar.setEnabled(True)
    dlg.lb_a.setEnabled(True)
    dlg.lb_b.setEnabled(True) 

    aux = "f(x) = "
    sup = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

    for i in range(size(coef)):
        aux = aux + str(abs(coef[i])) + "x" + str(size(coef) - i - 1).translate(sup) 
        if ((i) <= (size(coef) - 2)):
            if (coef[i+1] >= 0):
                aux = aux + " + "
            else:
                aux = aux + " - "

    dlg.lb_eq2.setText(aux)
    dlg.lb_n2.setText("i = " + str(max_it))
    dlg.lb_pr2.setText("ε = " + str(epsilon))

dlg.bt_conf1.clicked.connect(conf1)  
dlg.bt_conf2.clicked.connect(conf2)        
dlg.bt_conf3.clicked.connect(conf3)        
dlg.bt_conf4.clicked.connect(conf4) 

def graf():
    X = np.linspace(float(dlg.lb_a.text()), float(dlg.lb_b.text()), 200, endpoint=True)
    F = f(X)

    plt.grid(True)
    plt.grid(b=True, which='major', color='#666666', linestyle='-', alpha=0.4)
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='--', alpha=0.20)

    plt.plot(X,F)
    plt.show()

def raizes():  
    dlg.lb_r2.setEnabled(True)
    dlg.lb_r3.setEnabled(True)
    dlg.lb_tot_it2.setEnabled(True)
    dlg.c_parada.setEnabled(True)
    dlg.lb_obs2.setEnabled(True)          

    aut = 0
   
    if (dlg.lb_a.text() == "") or (dlg.lb_b.text() == ""):
        choice = QMessageBox.information(dlg, 'Intervalo de busca', "Por favor, insira um intervalo de busca.", QMessageBox.Ok)               
    
    if ((dlg.lb_a.text() != "") and (dlg.lb_b.text() != "")) or (aut == 1):  

        global a_n
        global b_n
        global m_n
        
        global f_m_n 
        global f_a_n
        global f_b_n

        global n

        a_n = float(dlg.lb_a.text())
        b_n = float(dlg.lb_b.text())      
        m_n_= 0    

        f_m_n = 0     
        f_a_n = 0
        f_b_n = 0    

        global a
        global b
        global m
        global f_a
        global f_b
        global f_m

        a = zeros(1000)
        b = zeros(1000)
        m = zeros(1000)
        f_a = zeros(1000)
        f_b = zeros(1000)
        f_m = zeros(1000)      

        n = 1
        
        for n in range(1, max_it+1):
            
            f_m_n = 0     
            f_a_n = 0
            f_b_n = 0  

            if (metodo == 0): # Método da Bissecção
                m_n = (a_n + b_n)/2        
            
            if (metodo == 1): # Método da Falsa Posição

                for i in range(size(coef)):
                    f_a_n = f_a_n + float(coef[i]) * (a_n) ** int(size(coef) - i - 1)
                    f_b_n = f_b_n + float(coef[i]) * (b_n) ** int(size(coef) - i - 1)    

                m_n = (b_n) - ((f_b_n*(b_n - a_n)) / (f_b_n - f_a_n))

            for i in range(size(coef)):
                f_a_n = f_a_n + float(coef[i]) * (a_n) ** int(size(coef) - i - 1)
                f_b_n = f_b_n + float(coef[i]) * (b_n) ** int(size(coef) - i - 1)    
                f_m_n = f_m_n + float(coef[i]) * (m_n) ** int(size(coef) - i - 1)      
            
            if (f_a_n)*(f_m_n) < 0:                
                b_n = m_n

            if (f_b_n)*(f_m_n) < 0:
                a_n = m_n       

            a[n-1] = a_n
            b[n-1] = b_n
            m[n-1] = m_n
            f_a[n-1] = f_a_n
            f_b[n-1] = f_b_n
            f_m[n-1] = f_m_n

            if (f_m[n-1]) == 0:
                dlg.lb_obs2.setText("Encontrou-se 1 solução real exata.")
                dlg.lb_obs2.setStyleSheet("color: green")
                dlg.lb_r2.setText("x₁ = " + str(round(m[n-1], aprox)))
                dlg.lb_r3.setText("f(x₁) = " + str(round(f_m[n-1], aprox)))
                dlg.lb_tot_it2.setText("i = " + str(n))              
                break

            if (f_a_n)*(f_b_n) > 0:
                dlg.lb_obs2.setText("Não existem existem raízes reais neste intervalo.")
                dlg.lb_obs2.setStyleSheet("color: red")
                dlg.lb_r2.setText("x₁ ≈ " + str(round(m[n-1], aprox)))   
                dlg.lb_r3.setText("f(x₁) ≈ " + str(round(f_m[n-1], aprox))) 
                dlg.lb_tot_it2.setText("i = " + str(n))          

                dlg.c_parada.setText("Raiz real não encontrada")

                break       
            
            if abs(m_n) < sqrt(10): # Condição de parada por Teste Absoluto de Erro
                if (abs(b_n - a_n) <= epsilon) or (abs(f_m_n) <= epsilon): # Condição de parada suscetível a falhas --> incidência de erros encontra-se nesta linha
                    dlg.lb_obs2.setText("Encontrou-se uma solução real aproximada.")
                    dlg.lb_obs2.setStyleSheet("color: green")
                    dlg.lb_r2.setText("x₁ ≈ " + str(round(m[n-1], aprox)))   
                    dlg.lb_r3.setText("f(x₁) ≈ " + str(round(f_m[n-1], aprox))) 
                    dlg.lb_tot_it2.setText("i = " + str(n))        

                    if abs(b_n - a_n) <= epsilon:
                        dlg.c_parada.setText("b_n - a_n <= epsilon")
                    else:
                        dlg.c_parada.setText("f_m_n <= epsilon") 

                    break 

            if (abs(m_n) >= sqrt(10)): # Condição de parada por Teste Relativo de Erro
                if (abs(b_n - a_n) / abs(b_n)) <= epsilon : # Condição de parada suscetível a falhas --> incidência de erros encontra-se nesta linha
                    dlg.lb_obs2.setText("Encontrou-se uma solução real aproximada.")
                    dlg.lb_obs2.setStyleSheet("color: green")
                    dlg.lb_r2.setText("x₁ ≈ " + str(round(m[n-1], aprox)))   
                    dlg.lb_r3.setText("f(x₁) ≈ " + str(round(f_m[n-1], aprox))) 
                    dlg.lb_tot_it2.setText("i = " + str(n))             

                    dlg.c_parada.setText("[(b_n - a_n) / (b_n)] <= epsilon")

                    break                    
         
        table.show()
        table.setRowCount(n)   
        k = 0
        for k in range(n):
            table.setItem(k,0, QTableWidgetItem(str(round(a[k], aprox))))
            table.setItem(k,1, QTableWidgetItem(str(round(b[k], aprox))))
            table.setItem(k,2, QTableWidgetItem(str(round(m[k], aprox))))
            table.setItem(k,3, QTableWidgetItem(str(round(f_a[k], aprox))))
            table.setItem(k,4, QTableWidgetItem(str(round(f_b[k], aprox))))
            table.setItem(k,5, QTableWidgetItem(str(round(f_m[k], aprox)))) 
        
        global n0
        global m0
        global f0

        global n1
        global m1
        global f1

        if (metodo == 0):
            n0 = str(n)
            m0 = str(round(m[k], aprox))
            f0 = str(round(f_m[k], aprox))    

        if (metodo == 1):
            n1 = str(n)
            m1 = str(round(m[k], aprox))
            f1 = str(round(f_m[k], aprox))
        
        if (abs(f_m_n) > epsilon) and ((f_a_n)*(f_b_n)) < 0:
            dlg.lb_obs2.setText("Não foi possível atingir a precisão.")  
            dlg.lb_obs2.setStyleSheet("color: red") 
            dlg.lb_r2.setText("x₁ ≈ " + str(round(m[n-1], aprox))) 
            dlg.lb_r3.setText("f(x₁) ≈ " + str(round(f_m[n-1], aprox)))    
            dlg.lb_tot_it2.setText("i = " + str(n)) # não alterar para n-1   

            if (n >= max_it):
                dlg.c_parada.setText("Iterações excedidas")
            else:
                dlg.c_parada.setText("Desconhecido")

def bisseccao():
    global metodo
    metodo = 0
  
    dlg.groupBox_3.setTitle("Método da Bissecção")    
    raizes()

def falsa_posicao():
    global metodo
    metodo = 1      

    dlg.groupBox_3.setTitle("Método da Falsa Posição")      
    raizes()

def novo():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def sair():
    app.exit()

def comp():      
    bisseccao()  
    falsa_posicao()

    choice = QMessageBox.information(dlg, 'Comparativo entre métodos', "------------------------------------------ \n + Método da Bissecção: \n ----------------------------------------- \n" + " Raiz real aproximada ≈ " + m0 + " \n Valor de f(x) ≈ " + f0 + "\n Total de iterações = " + n0 + " \n \n -----------------------------------------\n + Método da Falsa Posição: \n ----------------------------------------- \n" + " Raiz real aproximada ≈ " + m1 + " \n Valor de f(x) ≈ " + f1 + "\n Total de iterações = " + n1, QMessageBox.Ok)  

def sobre():
    choice = QMessageBox.information(dlg, 'Agradecimentos', "Agradeço muito a Deus, por me dar esperança em viver. E ainda que eu não mereça tamanho amor, me consola nos momentos mais tristes de minha vida. \n \n Este projeto foi criado com o auxílio da plataforma \"Qt for Python\" durante a construção da interface gráfica. Para a plotagem dos gráficos houve o auxílio da biblioteca \"Matplotlib\".  \n \n E por fim, este trabalho foi criado por um estudante de Física, Micael Davi Lima de Oliveira. E com o auxílio e orientação do professor José Francisco de Magalhães Netto. \n \n Developed in September, 2019" , QMessageBox.Ok)

dlg.bt_mfp.triggered.connect(falsa_posicao) 
dlg.bt_mb.triggered.connect(bisseccao) 
dlg.plot_f.triggered.connect(graf) 
dlg.actionNovo.triggered.connect(novo) 
dlg.actionSair.triggered.connect(sair) 
dlg.actionComparar.triggered.connect(comp) 
dlg.actionSobre.triggered.connect(sobre)
   
dlg.show()                                                                           
app.exec()