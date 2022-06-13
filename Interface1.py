from tkinter import*
import os
import sys

root=Tk()


root.title("Analisis de Elementos Finitos")                       #Creamos el root que contiene todo
root.geometry("450x150")
root.resizable(1,1)                    #la ventana no se puede cambiar de tamaño
#root.iconbitmap("fibo.ico")                                              #icono
#root.config(bg="Gray")

num= StringVar()                        #variable donde se guarda el dato input

#definimos la funcion del boton
def Diff():
    os.system('python copia_diff.py')

    

#texto informativo
label1= Label(root, text= "Ingresa las condiciones de frontera: ")
label1.grid(row=2,padx=10, pady=10)

#entrada del usuario  ingresada como variable
entry1=Entry(root, textvariable=num, borderwidth=3)
entry1.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

#Botones
button1= Button(root, text="Diferencias Finitas", borderwidth=3,command=Diff)#Creamos el boton
button1.grid(row=4)
button1.config(cursor="hand2")

button2= Button(root, text="Aproximación Galerkin", borderwidth=3)#Creamos el boton
button2.grid(row=4,column=1)
button2.config(cursor="hand2")


#desplegar





root.mainloop()
