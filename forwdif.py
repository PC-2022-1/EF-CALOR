"""
Método de diferencias finitas progresivas para la resolución de
ecuaciones elipticas u_xx == k^2 u_t, se emplea este método para
la resolución de la ecuación del calor unidimensional, y generación
de pruebas con dependencia temporal en 1 dimensión.
"""

from numpy import *
import matplotlib.pyplot as plt

def forwdif(f, g1, g2, a, b, c, n, m):

    """ 
    Entrada - f = u (x, 0) funcion de estado inicial
            - g1 = u (0, t) funcion de condición frontera x = 0
            - g2 = u (a, t) funcion de condición frontera x = a
            - a y b extremos derechos de  [0, a]  y  [0, b]
            - c la constante en la ecuacion de calor
            - n y m  numero de puntos (nodos) de la cuadricula en  [0, a]  y  [0, b]
    Salida  - U matriz solución [x, t] indexing
    """

    # ------- Inicialización de Parametros ----- #

    #  Vectorización de funciones
    g1 = vectorize(g1)
    g2 = vectorize(g2)

    h = a / (n-1) # Tamaño de intervalo x
    k = b / (m-1) # Tamaño de intervalo t
    r = c**2 * k / h**2 # Constante del calor diferencial
    s = 1 - 2 * r # Transmisión del calor

    # Inicialización de valores
    U = zeros([n, m]) # Matriz solución
    V = linspace(0,b,m) # Valores frontera

    # ------- Solución del problema usando las condiciones / Generacion de U ----- #

    # Condiciones de Frontera
    U[0, :] = g1(V)
    U[n-1, :] = g2(V)

    # Generar la primera fila
    xtick = arange(h, (n-1)*h, h)
    U[1:n-1, 0] = f(xtick).T

    # Generar las filas restantes de  U
    for  j in range(1,m):
        for  i in range(1,n-1):
            U[i, j] = s * U[i, j-1] + r * (U[i-1, j-1] + U[i+1, j-1])

    return U.T
