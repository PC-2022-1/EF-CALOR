"""
Método de diferencias finitas centradas para la resolución de
ecuaciones elipticas u_xx + u_yy == k^2 u_t, se emplea este método para
la resolución de la ecuación del calor bidimensional, y generación
de pruebas con dependencia temporal en 2 dimensión.
"""

from numpy import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys

def cendif(f, g1, g2, g3, g4, xf, yf, tf, c, nx, ny, nt):

    """ 
    Entrada - f = u (x, y, 0) funcion de estado inicial
            - g1 = u (0, y, t) funcion de condición frontera x = 0
            - g2 = u (xf, y, t) funcion de condición frontera x = a
            - g3 = u (x, 0, t) funcion de condición frontera y = 0
            - g4 = u (x, yf, t) funcion de condición frontera y = b
            - xf y yf extremos derechos de  [0, xf] X [0, yf]
            - tf es el extremo derecho temporal [0, tf]
            - c la constante en la ecuacion de calor
            - nx, ny y nt  numero de puntos (nodos) de la cuadricula
              en  [0, xf] X [0, yf] X [0, tf]
    Salida  - U matriz solución [x, y, t] indexing
    """

    # ------- Inicialización de Parametros ----- #

    #  Vectorización de funciones
    g1 = vectorize(g1)
    g2 = vectorize(g2)
    g3 = vectorize(g3)
    g4 = vectorize(g4)

    hx = xf / (nx-1) # Tamaño de intervalo x
    hy = yf / (ny - 1) # Tamaño de intervalo y
    ht = hx * hy / (4*c) # Tamaño de intervalo t
    r = c * ht / (hx*hy) # Constante del calor diferencial

    # Inicialización de valores
    U = zeros([nt, nx, ny]) # Matriz solución


    Vx = zeros([nt, ny]) # Valores frontera x
    Vy = zeros([nt, nx]) # Valores frontera y

    # ------- Solución del problema usando las condiciones / Generacion de U ----- #

    # Condiciones de Frontera
    U[:, (nx-1), :] = g2(Vx)
    U[:, :, 0] = g3(Vy)
    U[:, 0, :] = g1(Vx)
    U[:, :, (ny-1)] = g4(Vy)    

    # Generar la primera fila
    U[0, :, :] = f(U[0, :, :])

    # Iteramos sobre U
    for k in range(0, nt-1):
        for i in range(1, nx-1):
            for j in range(1, ny-1):
                U[k+1, i, j] = r * (U[k][i+1][j] + U[k][i-1][j] + U[k][i][j+1] + U[k][i][j-1] - 4*U[k][i][j]) + U[k][i][j]

    return U

# --- X = [x, y, t] : Vector de variables --- #
f = lambda x : float(sys.argv[8]) # Estado Inicial
g1 = lambda y : float(sys.argv[9]) # Frontera y = 0
g2 = lambda y : float(sys.argv[10]) # Frontera y = b
g3 = lambda x : float(sys.argv[11]) # Frontera x = 0
g4 = lambda x : float(sys.argv[12]) # Frontera x = a

xf = float(sys.argv[1]); yf = float(sys.argv[2]); tf = float(sys.argv[3]); c = float(sys.argv[4])
nx = int(sys.argv[5]); ny = int(sys.argv[6]); nt = int(sys.argv[7])

U = cendif(f, g1, g2, g3, g4, xf, yf, tf, c, nx, ny, nt)
u_max = U.max()

def plotheatmap(u_k, k, u_max):
  # Clear the current plot figure
    hx = xf / (nx-1) # Tamaño de intervalo x
    hy = yf / (ny - 1)

    plt.clf()
    plt.title(f"Temperature at t ={tf/nt * k:.3f} unit time")
    plt.xlabel("Nodos x")
    plt.ylabel("Nodos y")
  
    # This is to plot u_k (u at time-step k)
    plt.pcolormesh(u_k, cmap=plt.cm.Spectral_r, vmin=0, vmax=u_max)
 
  
    return plt

def animate(k):
  plotheatmap(U[k,:,:], k,u_max)
  plt.colorbar()

plt.pcolormesh(U[-1,:,:], cmap=plt.cm.Spectral_r, vmin= 0, vmax= u_max)


anim = animation.FuncAnimation(plt.figure(), animate, interval=1, frames=nt-1, repeat=False)
out = anim.save("heat_equation_solution.gif")
plt.show()