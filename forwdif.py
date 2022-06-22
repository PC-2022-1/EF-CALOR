"""
Método de diferencias finitas progresivas para la resolución de
ecuaciones elipticas u_xx == k^2 u_t, se emplea este método para
la resolución de la ecuación del calor unidimensional, y generación
de pruebas con dependencia temporal en 1 dimensión.
"""

from numpy import *

def forwdif(f, g1, g2, xf, tf, c, n, m):

    """ 
    Entrada - f = u (x, 0) funcion de estado inicial
            - g1 = u (0, t) funcion de condición frontera x = 0
            - g2 = u (xf, t) funcion de condición frontera x = a
            - xf y tf extremos derechos de  [0, xf]  y  [0, tf] * (Pendiente la combinación de la malla) *
            - c la constante en la ecuacion de calor
            - n y m  numero de puntos (nodos) de la cuadricula en  [0, xf]  X  [0, tf]
    Salida  - U matriz solución [x, t] indexing
    """

    # ------- Inicialización de Parametros ----- #

    #  Vectorización de funciones
    g1 = vectorize(g1)
    g2 = vectorize(g2)

    h = xf / (n-1) # Tamaño de intervalo x
    k = tf / (m-1) # Tamaño de intervalo t
    r = c**2 * k / h**2 # Constante del calor diferencial
    s = 1 - 2 * r # Transmisión del calor

    # Inicialización de valores
    U = zeros([n, m]) # Matriz solución
    V = linspace(0, tf, m) # Valores frontera

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

f = lambda x : sin(pi*x/4)
g1 = lambda t : 0*t
g2 = lambda t : exp(-pi**2*t)
U = forwdif(f, g1, g2, 2, .6, 4, 5, 4)
print(U)