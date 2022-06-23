from msilib.schema import ComboBox
from tkinter import*
from tkinter import ttk
import os
import sys
from anyio import open_file
from click import command
from PIL import Image

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
var_kx = DoubleVar()
var_ky = DoubleVar()
var_h = DoubleVar()
var_Tf = DoubleVar()
var_q = DoubleVar()
var_conv_abajo = StringVar()
var_conv_derecha = StringVar()
var_conv_arriba = StringVar()
var_conv_izquierda = StringVar()
var_t = DoubleVar()
var_c = DoubleVar()
var_nt = IntVar()
var_f = DoubleVar()
var_g1 = DoubleVar()
var_g2 = DoubleVar()
var_g3 = DoubleVar()
var_g4 = DoubleVar()
#definimos la funcion del boton
def Continuar():
    #boton galerkin
    button2= Button(root, text="Estacionario(Galerkin)", borderwidth=3, command=galerkin,justify="center")#Creamos el boton
    button2.grid(row=7,column=1,padx=10, pady=10)
    button2.config(cursor="hand2")
    #boton diferencias finitas
    button3= Button(root, text="Viajero (Diferencias finitas)", borderwidth=3, command=diferenciasFinitas, justify="center")#Creamos el boton
    button3.grid(row=7,column=2,padx=10, pady=10)
    button3.config(cursor="hand2")
    
    
    clf()
    
    NL,EL = uniform_mesh(var_l.get(), var_w.get(), var_p.get(), var_m.get(), var_tipo_el.get()) # Generar malla
    graph_mesh(var_tipo_el.get(),NL,EL) #Graficar malla de mesh.py


def galerkin():
    Gal=Toplevel(root)
    Gal.title("Galerkin")
    Gal.config(bg="#D7ECDE")

    label_calor= Label(Gal, text= "Generación de calor: ")
    label_calor.grid(row=0,column=0,padx=10, pady=10)

    combo_calor= ttk.Combobox(Gal,state='readonly')
    combo_calor['values'] = ('True','False')
    combo_calor.grid(row=0,column=1,columnspan=1, padx=10, pady=10)
    def Fuente_True(event):
        combo_calor = event.widget.get()
        if combo_calor == "True":
            label_kx= Label(Gal, text= "Conductividad en X: ")
            label_ky= Label(Gal, text= "Conductividad en Y: ")
            label_h= Label(Gal, text= "Coeficiente de conveccion: ")
            label_Tf= Label(Gal, text= "Temperatura del aire: ")
            label_q= Label(Gal, text= "Flujo especifico: ")
            
            label_ky.grid(row=2,padx=10, pady=10)
            label_kx.grid(row=1,padx=10, pady=10)
            label_h.grid(row=3,padx=10, pady=10)
            label_Tf.grid(row=4,padx=10, pady=10)
            label_q.grid(row=5,padx=10, pady=10)

            entrada_kx=Entry(Gal, textvariable=var_kx, borderwidth=3)
            entrada_ky=Entry(Gal, textvariable=var_ky, borderwidth=3)
            entrada_h=Entry(Gal, textvariable=var_h, borderwidth=3)
            entrada_Tf=Entry(Gal, textvariable=var_Tf, borderwidth=3)
            entrada_q=Entry(Gal, textvariable=var_q, borderwidth=3)

            entrada_kx.grid(row=1, column=1, columnspan=1, padx=10, pady=10)
            entrada_ky.grid(row=2, column=1, columnspan=1, padx=10, pady=10)
            entrada_h.grid(row=3, column=1, columnspan=1, padx=10, pady=10)
            entrada_Tf.grid(row=4, column=1, columnspan=1, padx=10, pady=10)
            entrada_q.grid(row=5, column=1, columnspan=1, padx=10, pady=10)


            label_A= Label(Gal, text= "Conveccion abajo: ")
            label_B= Label(Gal, text= "Conveccion derecha: ")
            label_C= Label(Gal, text= "Conveccion arriba: ")
            label_D= Label(Gal, text= "Conveccion izquierda: ")
            
            label_A.grid(row=6,column=0,padx=10, pady=10)
            label_B.grid(row=7,column=0,padx=10, pady=10)
            label_C.grid(row=8,column=0,padx=10, pady=10)
            label_D.grid(row=9,column=0,padx=10, pady=10)


            combo_A= ttk.Combobox(Gal,state='readonly',values=['True','False'],textvariable=var_conv_abajo)
            combo_B= ttk.Combobox(Gal,state='readonly',values=['True','False'],textvariable=var_conv_derecha)
            combo_C= ttk.Combobox(Gal,state='readonly',values=['True','False'],textvariable=var_conv_arriba)
            combo_D= ttk.Combobox(Gal,state='readonly',values=['True','False'],textvariable=var_conv_izquierda)
            
            combo_A.grid(row=6,column=1, padx=10, pady=10)
            combo_B.grid(row=7,column=1, padx=10, pady=10)
            combo_C.grid(row=8,column=1, padx=10, pady=10)
            combo_D.grid(row=9,column=1, padx=10, pady=10)

            def galerkin_true():
                os.system(f'python GalerkinTest.py {var_l.get()} {var_w.get()} {var_p.get()} {var_m.get()} {var_kx.get()} {var_ky.get()} {var_h.get()} {var_Tf.get()} {var_q.get()} {var_conv_abajo.get()} {var_conv_derecha.get()} {var_conv_arriba.get()} {var_conv_izquierda.get()}')
            button= Button(Gal, text="generar", borderwidth=3, command=galerkin_true,justify="center")#Creamos el boton
            button.grid(row=10,column=1,padx=10, pady=10)
            button.config(cursor="hand2")
        else:
            label_A= Label(Gal, text= "Neumann abajo: ")
            label_B= Label(Gal, text= "Neumann derecha: ")
            label_C= Label(Gal, text= "Neumann arriba: ")
            label_D= Label(Gal, text= "Neumann izquierda: ")
            
            label_A.grid(row=1,column=0,padx=10, pady=10)
            label_B.grid(row=2,column=0,padx=10, pady=10)
            label_C.grid(row=3,column=0,padx=10, pady=10)
            label_D.grid(row=4,column=0,padx=10, pady=10)


            combo_A= ttk.Combobox(Gal,state='readonly',values=[True,False],textvariable=var_conv_abajo)
            combo_B= ttk.Combobox(Gal,state='readonly',values=[True,False],textvariable=var_conv_derecha)
            combo_C= ttk.Combobox(Gal,state='readonly',values=[True,False],textvariable=var_conv_arriba)
            combo_D= ttk.Combobox(Gal,state='readonly',values=[True,False],textvariable=var_conv_izquierda)
                        
            combo_A.grid(row=1,column=1, padx=10, pady=10)
            combo_B.grid(row=2,column=1, padx=10, pady=10)
            combo_C.grid(row=3,column=1, padx=10, pady=10)
            combo_D.grid(row=4,column=1, padx=10, pady=10)
            def galerkin_false():
                os.system(f'python heat.py {var_l.get()} {var_w.get()} {var_p.get()} {var_m.get()} {var_tipo_el.get()} {var_conv_abajo.get()} {var_conv_derecha.get()} {var_conv_arriba.get()} {var_conv_izquierda.get()}')
            button= Button(Gal, text="generar", borderwidth=3, command=galerkin_false,justify="center")#Creamos el boton
            button.grid(row=10,column=1,padx=10, pady=10)
            button.config(cursor="hand2")

    combo_calor.current()
    combo_calor.bind("<<ComboboxSelected>>",Fuente_True)
    Gal.mainloop()

def diferenciasFinitas():
    Difer=Toplevel(root)
    Difer.title("Diferencias Finitas")
    Difer.config(bg="#D7ECDE")
    label_t= Label(Difer, text= "Tiempo de calentamiento: ")
    label_c= Label(Difer, text= "constante de calor: ")
    label_nt= Label(Difer, text= "Divisiones temporales:")
    label_f= Label(Difer, text= "Estado inicial: ")
    label_g1= Label(Difer, text= "Frontera en Y incial: ")
    label_g2= Label(Difer, text= "Frontera en Y final:")
    label_g3= Label(Difer, text= "Frontera en X inicial: ")
    label_g4= Label(Difer, text= "Frontera en X final:")
    
    label_t.grid(row=1,padx=10, pady=10)
    label_c.grid(row=2,padx=10, pady=10)
    label_nt.grid(row=3,padx=10, pady=10)
    label_f.grid(row=4,padx=10, pady=10)
    label_g1.grid(row=5,padx=10, pady=10)
    label_g2.grid(row=6,padx=10, pady=10)
    label_g3.grid(row=7,padx=10, pady=10)
    label_g4.grid(row=8,padx=10, pady=10)

    entrada_t=Entry(Difer, textvariable=var_t, borderwidth=3)
    entrada_c=Entry(Difer, textvariable=var_c, borderwidth=3)
    entrada_nt=Entry(Difer, textvariable=var_nt, borderwidth=3)
    entrada_f=Entry(Difer, textvariable=var_f, borderwidth=3)
    entrada_g1=Entry(Difer, textvariable=var_g1, borderwidth=3)
    entrada_g2=Entry(Difer, textvariable=var_g2, borderwidth=3)
    entrada_g3=Entry(Difer, textvariable=var_g3, borderwidth=3)
    entrada_g4=Entry(Difer, textvariable=var_g4, borderwidth=3)

    entrada_t.grid(row=1, column=1, columnspan=1, padx=10, pady=10)
    entrada_c.grid(row=2, column=1, columnspan=1, padx=10, pady=10)
    entrada_nt.grid(row=3, column=1, columnspan=1, padx=10, pady=10)
    entrada_f.grid(row=4, column=1, columnspan=1, padx=10, pady=10)
    entrada_g1.grid(row=5, column=1, columnspan=1, padx=10, pady=10)
    entrada_g2.grid(row=6, column=1, columnspan=1, padx=10, pady=10)
    entrada_g3.grid(row=7, column=1, columnspan=1, padx=10, pady=10)
    entrada_g4.grid(row=8, column=1, columnspan=1, padx=10, pady=10)
    def graph():  
        print("careverga")      
        
    def cendif_run():
        os.system(f'python cendif.py {var_l.get()} {var_w.get()} {var_t.get()} {var_c.get()} {var_p.get()} {var_m.get()} {var_nt.get()} {var_f.get()} {var_g1.get()} {var_g2.get()} {var_g3.get()} {var_g4.get()}')
        button2= Button(Difer, text="graficar", borderwidth=3, command=graph,justify="center")#Creamos el boton
        button2.grid(row=11,column=1,padx=10, pady=10)
        button2.config(cursor="hand2")
    button= Button(Difer, text="generar", borderwidth=3, command=cendif_run,justify="center")#Creamos el boton
    button.grid(row=10,column=1,padx=10, pady=10)
    button.config(cursor="hand2")
    Difer.mainloop()
    Difer.mainloop()

#texto informativo
label1= Label(root, text= "Ingresa la Descripción de la malla: ")
label1.grid(row=2,padx=10, pady=10)

#entrada del usuario  ingresada como variable

label_l= Label(root, text= "Tamaño X & Y: ") #asigna los valores  a GALERKINTEST.PY
label_p= Label(root, text= "Divisiones en  X & Y: ")

label_l.grid(row=3,padx=10, pady=10)
label_p.grid(row=4,padx=10, pady=10)


entrada_l=Entry(root, textvariable=var_l, borderwidth=3)
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

root.mainloop()