"""
Método de diferencias finitas centradas para la resolución de
ecuaciones elipticas u_xx + u_yy == k^2 u_t, se emplea este método para
la resolución de la ecuación del calor bidimensional, y generación
de pruebas con dependencia temporal en 2 dimensión.
"""

from numpy import *

def cendiff(f, g1, g2, g3, g4, xf, yf, tf, c, nx, ny, nt):

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
    U = zeros([tf, xf, yf]) # Matriz solución


    Vx = linspace(0, yf, ny) # Valores frontera x
    Vy = linspace(0, xf, nx) # Valores frontera y

    # ------- Solución del problema usando las condiciones / Generacion de U ----- #

    # Condiciones de Frontera
    U[:, :, 0] = g1(Vx)  # Extremo x = 0 #### Ojo: Matrices
    U[:, :, ny] = g2(Vx) # Extremo x = xf

    U[:, 0, :] = g3(Vy)  # Extremo y = 0
    U[:, ny, :] = g4(Vy) # Extremo y = yf

    # Generar la primera fila
    U[0, :, :] = f(U[0, :, :])

    # Iteramos sobre U
    for k in range(0, nt, ht):
        for i in range(1, nx, hx):
            for j in range(1, ny, hy):
                U[k+1, i, j] = r * (u[k][i+1][j] + u[k][i-1][j] + u[k][i][j+1] + u[k][i][j-1] - 4*u[k][i][j]) + u[k][i][j]

    return U

    f, g1, g2, g3, g4, xf, yf, tf, c, nx, ny, nt
#f = lambda x, y, t : 0*(x + y)*t
#g1 = lambda y, t : sin()
