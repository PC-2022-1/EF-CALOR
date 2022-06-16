from tkinter import*
import os
import sys

root=Tk()


root.title("Analisis de Elementos Finitos")                       #Creamos el root que contiene todo
#root.geometry("450x150")
root.resizable(1,1)                    #la ventana no se puede cambiar de tamaño
#root.iconbitmap("fibo.ico")                                              #icono
#root.config(bg="Gray")

num= StringVar()                        #variable donde se guarda el dato input

#definimos la funcion del boton
def Continuar():
    os.system('python Interface1.py')
    root.quit()

    

#texto informativo
label1= Label(root, text= "Ingresa la Descripción de la malla: ")
label1.grid(row=2,padx=10, pady=10)

#entrada del usuario  ingresada como variable

label_l= Label(root, text= "Ingresa L: ")
label_l.grid(row=3,column=0,padx=10, pady=10)
entrada_l=Entry(root,textvariable=num, borderwidth=3)
entrada_l.grid(row=3, column=1, columnspan=1, padx=10, pady=10)

entrada_w=Entry(root, textvariable=num, borderwidth=3)
entrada_w.grid(row=3, column=2, columnspan=1, padx=10, pady=10)

label_p= Label(root, text= "Ingresa P: ")
label_p.grid(row=4,column=0,padx=10, pady=10)

entrada_p=Entry(root, textvariable=num, borderwidth=3)
entrada_p.grid(row=4, column=1, columnspan=1, padx=10, pady=10)

entrada_m=Entry(root, textvariable=num, borderwidth=3)
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
