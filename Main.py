from msilib.schema import ComboBox
from tkinter import*
from tkinter import ttk
import os
import sys
from click import command

from matplotlib.pyplot import clf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Mesh import uniform_mesh,graph_mesh

root=Tk()
root.title("Analisis de Elementos Finitos")                    #Creamos el root que contiene todo
#root.geometry("450x150")
root.resizable(1,1)                    #la ventana no se puede cambiar de tamaño
#root.iconbitmap("EF.ico")                                              #icono
root.config(bg="#D7ECDE")




#variable donde se guarda el dato input
var_l= DoubleVar()
var_w= DoubleVar()
var_p= IntVar()
var_m= IntVar()
var_tipo_el= StringVar()
#definimos la funcion del boton

def Continuar():
    #boton galerkin
    button2= Button(root, text="Estacionario(Galerkin)", borderwidth=3, command=galerkin)#Creamos el boton
    button2.grid(row=7,column=1,padx=10, pady=10)
    button2.config(cursor="hand2")
    #boton diferencias finitas
    button3= Button(root, text="Viajero (Diferencias finitas)", borderwidth=3, command=diferenciasFinitas)#Creamos el boton
    button3.grid(row=7,column=2,padx=10, pady=10)
    button3.config(cursor="hand2")
    
    
    clf()
    
    NL,EL = uniform_mesh(var_l.get(), var_w.get(), var_p.get(), var_m.get(), var_tipo_el.get()) # Generar malla
    graph_mesh(var_tipo_el.get(),NL,EL) #Graficar malla de mesh.py


def galerkin():
    Gal=Toplevel(root)
    Gal.title("Galerkin")
    Gal.config(bg="#D7ECDE")

    #Button(Gal,text="Button2").grid()
    var_gen_calor= StringVar()

    label_calor= Label(Gal, text= "Generación de calor: ")
    label_calor.grid(row=0,column=0,padx=10, pady=10)

    combo_calor= ttk.Combobox(Gal,state='readonly',values=['True','False'],textvariable=var_gen_calor)
    combo_calor.grid(row=0,column=1,columnspan=1, padx=10, pady=10)

    if var_gen_calor.get() == True:
        os.system(f'python heat.py {var_l.get()} {var_w.get()} {var_p.get()} {var_m.get()} {var_tipo_el.get()}')

    label_A= Label(Gal, text= "Lado A: ")
    label_B= Label(Gal, text= "Lado B: ")
    label_C= Label(Gal, text= "Lado C: ")
    label_D= Label(Gal, text= "Lado D: ")
    
    label_A.grid(row=1,column=0,padx=10, pady=10)
    label_B.grid(row=2,column=0,padx=10, pady=10)
    label_C.grid(row=3,column=0,padx=10, pady=10)
    label_D.grid(row=4,column=0,padx=10, pady=10)


    combo_A= ttk.Combobox(Gal,state='readonly',values=['True','False'])
    combo_B= ttk.Combobox(Gal,state='readonly',values=['True','False'])
    combo_C= ttk.Combobox(Gal,state='readonly',values=['True','False'])
    combo_D= ttk.Combobox(Gal,state='readonly',values=['True','False'])
    
    
    
    combo_A.grid(row=1,column=1, padx=10, pady=10)
    combo_B.grid(row=2,column=1, padx=10, pady=10)
    combo_C.grid(row=3,column=1, padx=10, pady=10)
    combo_D.grid(row=4,column=1, padx=10, pady=10)


    








    Gal.mainloop()



    #os.system(f'python heat.py {var_l.get()} {var_w.get()} {var_p.get()} {var_m.get()} {var_tipo_el.get()}')

def diferenciasFinitas():
    Difer=Toplevel(root)
    Difer.title("Diferencias Finitas")
    Difer.config(bg="#D7ECDE")
    #os.system(f'python copia_diff.py')





    Difer.mainloop()

#texto informativo
label1= Label(root, text= "Ingresa la Descripción de la malla: ")
label1.grid(row=2,padx=10, pady=10)

#entrada del usuario  ingresada como variable

label_l= Label(root, text= "Tamaño x,y: ") #asigna los valores  a GALERKINTEST.PY
label_p= Label(root, text= "Divisiones en  x,y: ")

label_l.grid(row=3,padx=10, pady=10)
label_p.grid(row=4,padx=10, pady=10)


entrada_l=Entry(root,textvariable=var_l, borderwidth=3)
entrada_w=Entry(root, textvariable=var_w, borderwidth=3)
entrada_p=Entry(root, textvariable=var_p, borderwidth=3)
entrada_m=Entry(root, textvariable=var_m, borderwidth=3)

combo= ttk.Combobox(state='readonly',values=['CUADRADO','TRIANGULO'], textvariable=var_tipo_el)
combo.grid(row=5,column=1,padx=10, pady=10)

entrada_l.grid(row=3, column=1, columnspan=1, padx=10, pady=10)
entrada_w.grid(row=3, column=2, columnspan=1, padx=10, pady=10)
entrada_p.grid(row=4, column=1, columnspan=1, padx=10, pady=10)
entrada_m.grid(row=4, column=2, columnspan=1, padx=10, pady=10)



#Botones
button1= Button(root, text="Continuar", borderwidth=3,command=Continuar)#Creamos el boton
button1.grid(row=6,column=1)
button1.config(cursor="hand2")

# button2= Button(root, text="Aproximación Galerkin", borderwidth=3)#Creamos el boton
# button2.grid(row=10,column=1)
# button2.config(cursor="hand2")


#desplegar





root.mainloop()
