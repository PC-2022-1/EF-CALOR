from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL

import dash_bootstrap_components as dbc

import pandas as pd
import plotly.graph_objs as go
from sklearn import datasets
from sklearn.cluster import KMeans
import os

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from Mesh import * #Archivo donde esta la función para generar malla y para graficar
from sympy import integrate, linear_eq_to_matrix, symbols,simplify,collect,  diff, Eq, Matrix
from sympy import *
from GalerkinFuntion import *

from numpy import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import plotly.express as px


workspace_user = os.getenv('JUPYTERHUB_USER')  # Get DS4A Workspace user name


request_path_prefix = None
if workspace_user:
    request_path_prefix = '/user/' + workspace_user + '/proxy/8050/'

app = Dash(__name__, requests_pathname_prefix=request_path_prefix, external_stylesheets=[dbc.themes.FLATLY],
                meta_tags=[{'name':'viewport', 'content':'width=device-width, initial-scale=1.0'}])
app.title = 'Elementos finitos'                 
                          

controls = dbc.Card(
    [
        dbc.Row([
            dbc.Col(
            [
                dbc.Label("Distancia en x"),
                dbc.Input(id="lenx", type="number", value=0.6),
            ]
            ),
            dbc.Col(
                [
                    dbc.Label("Distancia en y"),
                    dbc.Input(id="leny", type="number", value=0.6),
                ]
            ),
            dbc.Col(
                [
                    dbc.Label("Divisiones en x"),
                    dbc.Input(id="divx", type="number", value=5),
                ]
            ),
            dbc.Col(
                [
                    dbc.Label("Divisiones en y"),
                    dbc.Input(id="divy", type="number", value=5),
                ]
            ),
            dbc.Col(
                [
                    dbc.Label("Temperatura del aire"),
                    dbc.Input(id="Tf", type="number", value=30),
                ]
            )
            
        
        ]),
        dbc.Row([
                
            dbc.Col(
                [
                    dbc.Label("Tipo de elemento"),
                    dcc.Dropdown(
                        id="element",
                        options=[
                            {"label": "CUADRADO", "value": "CUADRADO"} ,
                            {"label": "TRIANGULO", "value": "TRIANGULO"} 
                            ],
                        value="CUADRADO",
                    ),
                ]
                ),
            
            dbc.Col(
                [
                    dbc.Label("lado 1"),
                    dcc.Dropdown(
                        id="l1",
                        options=[
                            {"label": "True", "value": True} ,
                            {"label": "False", "value": False} 
                            ],
                        value=True,
                    ),
                ]
            ),
            dbc.Col(
                [
                    dbc.Label("lado 2"),
                    dcc.Dropdown(
                        id="l2",
                        options=[
                            {"label": "True", "value": True} ,
                            {"label": "False", "value": False} 
                            ],
                        value=True,
                    ),
                ]
            ),
            dbc.Col(
                [
                    dbc.Label("lado 3"),
                    dcc.Dropdown(
                        id="l3",
                        options=[
                            {"label": "True", "value": True} ,
                            {"label": "False", "value": False} 
                            ],
                        value=True,
                    ),
                ]
            ),
            dbc.Col(
                [
                    dbc.Label("lado 4"),
                    dcc.Dropdown(
                        id="l4",
                        options=[
                            {"label": "True", "value": True} ,
                            {"label": "False", "value": False} 
                            ],
                        value=True,
                    ),
                ]
            ),
            ],style={"marginTop": "50px","align":"left"}),
        dbc.Button(id='submit_bt', n_clicks=1, children='Ejecutar',style={"marginTop":"50px"},color="info", className="me-1")
        
    ],
    body=True, className="h-100 p-5 bg-light border rounded-3"
)
    
app.layout = dbc.Container(
    [
        html.H1(["Elementos finitos"],  className="h-100 p-5 bg-light border rounded-3",style={"textAlign":"center"}),
        
       
        
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=12),
            ],
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="element-graph"), md=12,align="center"),
            ],
            align="center",
        ),
    ], 
    
)


@app.callback(
    Output("element-graph", "figure"),
    [
        Input("submit_bt","n_clicks"),
        State("lenx", "value"),
        State("leny", "value"),
        State("divx", "value"),
        State("divy", "value"),
        State("element", "value"),
        State("Tf", "value"),
        State("l1", "value"),
        State("l2", "value"),
        State("l3", "value"),
        State("l4", "value"),
    ],
)
def make_graph(n_clicks,l,w,p,m,tipoDeElemento,Tf,l1,l2,l3,l4):
    print(n_clicks,l,w,p,m,tipoDeElemento,Tf,l1,l2,l3,l4)
#     l = 0.6 #Distancia en x
#     #l=symbols('l')
#     w = 0.6 #Distancia en y
#     #w=symbols('w')
#     p = 5  #Divisiones en x
#     m = 5  #Divisiones en y

    elemLength = l/p #Largo del elemento
    elemWidth = w/m  #Ancho del elemento
    tipoDeElemento = 'CUADRADO' #Puede ser elemento tipo 'TRIANGULO' o 'CUADRADO'

    #Se genera la lista NL ("Node list") que contiene las coordenadas de cada nodo
    #y EL("Element list") que contiene la lista de nodos de cada elemento
    print("22")
    NL,EL = uniform_mesh(l, w, p, m, tipoDeElemento) # Generar malla
    print("22")
    # graph_mesh(tipoDeElemento,NL,EL) #Graficar malla

    #Definicion de condiciones iniciales

    #kx=symbols('kx')
    kx=1.2 #k conductividad en y
    #ky=symbols('kx')
    ky=1.2 #k conductividad en X

    #     #Para caso donde la superficie es fuente de calor
    #     #h=symbols('h')
    h=20 #h Coeficiente de conveccion
    #     #Tf=symbols('Tf')
    #     Tf=30 #Tf Temperatura del aire 
    #     #q=symbols('q')
    q=1000 #q Flujo especifico de calor Vatios/m3  

    #Para caso donde el calor viene del ambiente:
    # h=-20 #h Coeficiente de conveccion
    # Tf=100 #Tf Temperatura del aire 
    # q=-100 #q Flujo especifico de calor Vatios/m3 




    eqSist=[]
    dataFrame=pd.DataFrame()

#     listaLadosConv=[True,True,True,True] #Lados i-j, j-m, m-n, n-i Lista con lados con conv
    listaLadosConv=[l1,l2,l3,l4]
    dataFrameList = []  #Se juntan las dataframe de cada elemento en una lista dataFrameList
    for i in range (0, len(EL)):
        print(i)
        dataFrameList.append(galerkinMethod(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, i,l,w, listaLadosConv ))

    #print(dataFrameList)

    #Nuevo dataframe juntando todas las dataFrame con elementos. Teniendo 4x#El ecuaciones
    DataFrame = pd.concat(dataFrameList, axis=0)

    #Las ecuaciones se suma deacuerdo a los nodos, para tener #Nodos ecuaciones
    CompressedDF = DataFrame.replace(np.nan,0) #0 donde no hay termino
    CompressedDF = DataFrame.groupby("nodo").sum() #suma por columna nodo
    #CompressedDF.to_excel("ef.xlsx") #Para visualizar dataFrame comprimido
    #DataFrame.to_excel ("ef2.xlsx" ) #Para visualizar dataFrame original

    #Generación de matrices
    print("6")
    matrixFinal = np.matrix(CompressedDF.drop('indep', inplace=False, axis=1)) #Matriz de coeff final
    vectorFinal = np.array(CompressedDF['indep']) #Vector independiente para la solucion 
    CompressedDF.drop('indep', inplace=True, axis=1) #Eliminamos de CompressedDF la columna indep
    TemperatureVector =np.array(CompressedDF.columns ) #Se genera un vector con las incognitas


    #print(matrixFinal)
    #print(vectorFinal)

    #Se genera una lista para guardar como incognitas las temperaturas
    listaTemperaturas=[]
    listaprueba=[]
    listaprueba2=[]
    print("1")
    for i in TemperatureVector:
        listaTemperaturas.append(symbols(str(i)))
        listaprueba.append(str(i))

    for ele in listaprueba:
      listaprueba2.append(int(ele[1:]))

    #Para usar la funcion linsolve de numpy 
    vectorFinal = vectorFinal.astype('float32')
    matrixFinal = matrixFinal.astype('float32')

    # print(TemperatureVector)
    #Se resuelve el sistema de ecuaciones
    result=np.linalg.solve(matrixFinal, vectorFinal)
    # print(result)

    matrixCalor = np.zeros((p+1, m+1))


    listaSinOrden=[]
    for i in range (0,len(listaprueba2)):
      listaSinOrden.append([listaprueba2[i],result[i]])

    def getKey(item):
      return item[0]

    listaOrdenada=sorted(listaSinOrden, key=getKey)

    # print(listaOrdenada)

    contador=0
    for j in range(0,m+1):
        for i in range (0,p+1):
            matrixCalor[j,i]=listaOrdenada[contador][1]
            contador=contador+1
    print("2")
    #print(matrixCalor)

    # plt.imshow(matrixCalor, cmap='hot', interpolation='nearest')
    # plt.show()

    #ax = sns.heatmap(matrixCalor, linewidth=0.5,cmap="coolwarm")
    fig = px.imshow(matrixCalor, color_continuous_scale='RdBu_r' ,labels=dict(x="x", y="y", color="Temperatura"),aspect="auto")
    #fig.show()
    print("3")
    return fig

# make sure that x and y values can't be the same variable

"""
def filter_options(v):
    Disable option v
    return [
        {"label": col, "value": col, "disabled": col == v}
        for col in iris.columns
    ]

"""

# functionality is the same for both dropdowns, so we reuse filter_options
# app.callback(Output("x-variable", "options"), [Input("y-variable", "value")])(
#     filter_options
# )
# app.callback(Output("y-variable", "options"), [Input("x-variable", "value")])(
#     filter_options
# )


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8050", debug=True)