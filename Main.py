from tkinter import*
import os
import sys

from matplotlib.pyplot import clf
from Mesh import uniform_mesh,graph_mesh

root=Tk()



root.title("Analisis de Elementos Finitos")                       #Creamos el root que contiene todo
#root.geometry("450x150")
root.resizable(1,1)                    #la ventana no se puede cambiar de tamaño
#root.iconbitmap("fibo.ico")                                              #icono
#root.config(bg="Gray")



#variable donde se guarda el dato input
var_l= DoubleVar()
var_w= DoubleVar()
var_p= IntVar()
var_m= IntVar()

#definimos la funcion del boton
def galerkin():
    os.system(f'python GalerkinTest.py {var_l.get()} {var_w.get()} {var_p.get()} {var_m.get()}')
def diferenciasFinitas():
    os.system(f'python copia_diff.py')
def Continuar():
    button2= Button(root, text="Estacionario(Galerkin)", borderwidth=3, command=galerkin)#Creamos el boton
    button2.grid(row=18,column=1)
    button2.config(cursor="hand2")
    button2= Button(root, text="Viajero (Diferencias finitas)", borderwidth=3, command=diferenciasFinitas)#Creamos el boton
    button2.grid(row=18,column=2)
    button2.config(cursor="hand2")
    clf()
    tipoDeElemento = 'CUADRADO'
    NL,EL = uniform_mesh(var_l.get(), var_w.get(), var_p.get(), var_m.get(), tipoDeElemento) # Generar malla
    graph_mesh(tipoDeElemento,NL,EL) #Graficar malla de mesh.py

    

#texto informativo
label1= Label(root, text= "Ingresa la Descripción de la malla: ")
label1.grid(row=2,padx=10, pady=10)

#entrada del usuario  ingresada como variable

label_l= Label(root, text= "Ingresa l,w: ") #asigna los valores  a GALERKINTEST.PY
label_p= Label(root, text= "Ingresa p,m: ")

label_l.grid(row=3,padx=10, pady=10)
label_p.grid(row=4,padx=10, pady=10)


entrada_l=Entry(root,textvariable=var_l, borderwidth=3)
entrada_w=Entry(root, textvariable=var_w, borderwidth=3)
entrada_p=Entry(root, textvariable=var_p, borderwidth=3)
entrada_m=Entry(root, textvariable=var_m, borderwidth=3)

entrada_l.grid(row=3, column=1, columnspan=1, padx=10, pady=10)
entrada_w.grid(row=3, column=2, columnspan=1, padx=10, pady=10)
entrada_p.grid(row=4, column=1, columnspan=1, padx=10, pady=10)
entrada_m.grid(row=4, column=2, columnspan=1, padx=10, pady=10)



#Botones
button1= Button(root, text="Continuar", borderwidth=3,command=Continuar)#Creamos el boton
button1.grid(row=10,column=1)
button1.config(cursor="hand2")

# button2= Button(root, text="Aproximación Galerkin", borderwidth=3)#Creamos el boton
# button2.grid(row=10,column=1)
# button2.config(cursor="hand2")


#desplegar





root.mainloop()
