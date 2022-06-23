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
from GalerkinFunRect import *
from diff import *
from heat import *

from numpy import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import plotly.express as px



def GalerkinResult(dataFrameList,p,m):
  #Nuevo dataframe juntando todas las dataFrame con elementos. Teniendo 4x#El ecuaciones
    try:
        DataFrame = pd.concat(dataFrameList, axis=0)

        #Las ecuaciones se suma deacuerdo a los nodos, para tener #Nodos ecuaciones
        CompressedDF = DataFrame.replace(np.nan,0) #0 donde no hay termino
        CompressedDF = DataFrame.groupby("nodo").sum() #suma por columna nodo
        #CompressedDF.to_excel("ef.xlsx") #Para visualizar dataFrame comprimido
        #DataFrame.to_excel ("ef2.xlsx" ) #Para visualizar dataFrame original

        #Generación de matrices
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
        #print(result)

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
    except Exception as e: 
        print(e)
        return []
    return  matrixCalor

workspace_user = os.getenv('JUPYTERHUB_USER')  # Get DS4A Workspace user name


request_path_prefix = None
if workspace_user:
    request_path_prefix = '/user/' + workspace_user + '/proxy/8050/'

app = Dash(__name__, requests_pathname_prefix=request_path_prefix, external_stylesheets=[dbc.themes.FLATLY],
                meta_tags=[{'name':'viewport', 'content':'width=device-width, initial-scale=1.0'}])
app.title = 'Elementos finitos'                 
                          
controls2= dbc.Card(
    [
        dbc.Row([
            dbc.Col(
            [
                dbc.Label("Distancia en x"),
                dbc.Input(id="xf", type="number", value=0.6),
            ]
            ),
            dbc.Col(
                [
                    dbc.Label("Distancia en y"),
                    dbc.Input(id="yf", type="number", value=0.6),
                ]
            ),
            dbc.Col(
                [
                    dbc.Label("nodos en x"),
                    dbc.Input(id="nx", type="number", value=5),
                ]
            ),
            dbc.Col(
                [
                    dbc.Label("nodos en y"),
                    dbc.Input(id="ny", type="number", value=5),
                ]
            ),
            dbc.Col(
                [
                    dbc.Label("nodos en t"),
                    dbc.Input(id="nt", type="number", value=5),
                ]
            )
           
            
        
        ]),
        dbc.Row([
            dbc.Col(
            [
                dbc.Label("funcion estado inicial"),
                dbc.Input(id="f", type="number", value=100),
            ]
            ),
            dbc.Col(
                [
                    dbc.Label("funcion cf x"),
                    dbc.Input(id="g1", type="number", value=25),
                ]
            ),
            dbc.Col(
                [
                    dbc.Label("funcion cf x"),
                    dbc.Input(id="g2", type="number", value=25),
                ]
            ),
            dbc.Col(
                [
                    dbc.Label("funcion cf y"),
                    dbc.Input(id="g3", type="number", value=25),
                ]
            ),
            dbc.Col(
                [
                    dbc.Label("funcion cf y"),
                    dbc.Input(id="g4", type="number", value=25),
                ]
            ),
            
            
        
        ])
        
    ],
    body=True, className="h-100 p-5 bg-light border rounded-3"
)
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
                    dbc.Label("Divisiones"),
                    dbc.Input(id="div", type="number", value=5),
                ]
            ),
            dbc.Col(
                [
                    dbc.Label("Temperatura de ambiente"),
                    dbc.Input(id="Tf", type="number", value=30),
                ]
            )
            
        
        ]),
        dbc.Row([
            
            dbc.Col(
                [
                    dbc.Label("lado superior"),
                    dcc.Dropdown(
                        id="l1",
                        options=[
                            {"label": "Convección", "value": 1} ,
                            {"label": "No convección", "value": 0} 
                            ],
                        value=1,
                    ),
                ]
            ),
            dbc.Col(
                [
                    dbc.Label("lado derecho"),
                    dcc.Dropdown(
                        id="l2",
                        options=[
                            {"label": "Convección", "value": 1} ,
                            {"label": "No convección", "value": 0} 
                            ],
                        value=1,
                    ),
                ]
            ),
            dbc.Col(
                [
                    dbc.Label("lado inferior"),
                    dcc.Dropdown(
                        id="l3",
                        options=[
                            {"label": "Convección", "value": 1} ,
                            {"label": "No convección", "value": 0} 
                            ],
                        value=1,
                    ),
                ]
            ),
            dbc.Col(
                [
                    dbc.Label("lado izquierdo"),
                    dcc.Dropdown(
                        id="l4",
                        options=[
                            {"label": "Convección", "value": 1} ,
                            {"label": "No convección", "value": 0} 
                            ],
                        value=1,
                    ),
                ]
            ),
            ],style={"marginTop": "50px","align":"left"})
        
        
    ],
    body=True, className="h-100 p-5 bg-light border rounded-3"
)
controls3 = dbc.Card(
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
                    dbc.Label("Temperatura lado"),
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
                    dbc.Label("lado inferior"),
                    dcc.Dropdown(
                        id="l1",
                        options=[
                            {"label": "Neumann", "value": 1} ,
                            {"label": "Dirichlet", "value": 0} 
                            ],
                        value=0,
                    ),
                ]
            ),
            dbc.Col(
                [
                    dbc.Label("lado derecho"),
                    dcc.Dropdown(
                        id="l2",
                        options=[
                            {"label": "Neumann", "value": 1} ,
                            {"label": "Dirichlet", "value": 0} 
                            ],
                        value=1,
                    ),
                ]
            ),
            dbc.Col(
                [
                    dbc.Label("lado superior"),
                    dcc.Dropdown(
                        id="l3",
                        options=[
                            {"label": "Neumann", "value": 1} ,
                            {"label": "Dirichlet", "value": 0} 
                            ],
                        value=1,
                    ),
                ]
            ),
            dbc.Col(
                [
                    dbc.Label("lado izquierdo"),
                    dcc.Dropdown(
                        id="l4",
                        options=[
                            {"label": "Neumann", "value": 1} ,
                            {"label": "Dirichlet", "value": 0} 
                            ],
                        value=1,
                    ),
                ]
            ),
            ],style={"marginTop": "50px","align":"left"}),
        dbc.Row(
            [
               
                dbc.Col(
                [
                    dbc.Label("constante de contacto"),
                    dbc.Input(id="g_f", type="number", value=20),
                ]
            )
            ],
        style={"marginTop": "50px","align":"left"})
        
        
    ],
    body=True, className="h-100 p-5 bg-light border rounded-3"
)
graph1=dcc.Graph(id="element-graph")
graph2=dcc.Graph(id="element-graph2")
graph3=dcc.Graph(id="element-graph3")
app.layout = dbc.Container(
    [
        html.H1(["Elementos finitos"],  className="h-100 p-5 bg-light border rounded-3",style={"textAlign":"center"}),
        
       
        
        html.Hr(),
        dbc.Row(
            [
                 dcc.Dropdown(
                        id="element2",
                        options=[
                            {"label": "Metodo Galerkin (como fuente de calor)", "value": "Metodo Galerkin1"} ,
                            {"label": "Metodo Galerkin (fuente externa)", "value": "Metodo Galerkin2"}, 
                            {"label": "Diferencias finitas", "value": "Diferencias finitas"} 
                            ],
                        value="Metodo Galerkin"
                    ),
                dbc.Col(controls, md=12,id="panelcontrol"),
                dbc.Button(id='submit_bt', n_clicks=0, children='Ejecutar',style={"marginTop":"50px"},color="info", className="me-1")
            ],
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(graph1, md=12,align="center"),
            ],
            align="center",id="grafico"
        ),
    ], 
    
)
@app.callback(
    [Output("panelcontrol", "children"),Output("grafico","children")],
    [
        Input("element2","value")
    ]
)
def change_control(option):
    if option=="Diferencias finitas":
        return controls2,graph2
    elif option=="Metodo Galerkin2":
        return controls3,graph3
    return controls,graph1

@app.callback(
    Output("element-graph", "figure"),
    [
        Input("submit_bt","n_clicks"),
        State("lenx", "value"),
        State("leny", "value"),
        State("div", "value"),
        
        State("Tf", "value"),
        State("l1", "value"),
        State("l2", "value"),
        State("l3", "value"),
        State("l4", "value"),
    ],
)
def make_graph(n_clicks,l,w,div,Tf,l1,l2,l3,l4):
    print(n_clicks,l,w,div,Tf,l1,l2,l3,l4)

    p=div
    m=div
    #Definicion de condiciones iniciales

    #kx=symbols('kx')
    kx=1.2 #k conductividad en y
    #ky=symbols('kx')
    ky=1.2 #k conductividad en X
    tipoDeElemento="CUADRADO"
    #Para caso donde la superficie es fuente de calor
    #h=symbols('h')
    h=20 #h Coeficiente de conveccion h=-20
    #Tf=symbols('Tf')
    
    #q=symbols('q')
    q=1000 #q Flujo especifico de calor Vatios/m3   q=-100 


    elemLength = l/p #Largo del elemento
    elemWidth = w/m  #Ancho del elemento
    
    listaLadosConv=[l1,l2,l3,l4] #Lados i-j, j-m, m-n, n-i Lista con lados con conv


    #Se genera la lista NL ("Node list") que contiene las coordenadas de cada nodo
    #y EL("Element list") que contiene la lista de nodos de cada elemento
    NL,EL = uniform_mesh(l, w, p, m, tipoDeElemento) # Generar malla
    graph_mesh(tipoDeElemento,NL,EL) #Graficar malla

    #galerkinMethodRect retorna un dataframe por elemento
    dataFrameList = []  #Se juntan las dataframe de cada elemento en una lista dataFrameList
    for i in range (0, len(EL)):
        dataFrameList.append(galerkinMethodRect(elemLength, elemWidth, NL, EL, h, Tf, kx, ky, q, i,l,w, listaLadosConv ))
    #print(dataFrameList)
    
    matrixCalor = GalerkinResult(dataFrameList,p,m) #GalerkinResult organiza, combina y reduce los dataframes, los convierte en matrices 
    #y se encuentra la solución al sistema de ecuaciones que se guarda en una matriz solución (matrixCalor)
    
    fig = px.imshow(matrixCalor, color_continuous_scale='RdBu_r' ,labels=dict(x="x", y="y", color="Temperatura"),origin='lower')
    
    return fig

# make sure that x and y values can't be the same variable

@app.callback(
    Output("element-graph2", "figure"),
    [
        Input("submit_bt","n_clicks"),
        State("xf", "value"),
        State("yf", "value"),
        State("nx", "value"),
        State("ny", "value"),
        State("nt", "value"),
        State("f", "value"),
        State("g1", "value"),
        State("g2", "value"),
        State("g3", "value"),
        State("g4", "value"),
        
        
        
    ],
)
def make_graph2(n_clicks,xf,yf,nx,ny,nt,f,g1,g2,g3,g4):
    tf=100
    matrix=fin_dif(xf,yf,tf,nx,ny,nt,f,g1,g2,g3,g4)
    figure = px.imshow(matrix, color_continuous_scale='RdBu_r' ,labels=dict(x="x", y="y", color="Temperatura"),origin='lower')
        

    return figure


@app.callback(
    Output("element-graph3", "figure"),
    [
        Input("submit_bt","n_clicks"),
        State("lenx", "value"),
        State("leny", "value"),
        State("divx", "value"),
        State("divy", "value"),
        State("Tf","value"),
        State("element", "value"),
        State("l4", "value"),
        State("l2", "value"),
        State("l3", "value"),
        State("l1", "value"),
        State("g_f", "value"),
    ],
)
def make_graph3(n_clicks,l,w,p,m,temp,Te,l1,l2,l3,l4,g):
    
    figure=sq_tr_garlekin(l,w,p,m,temp,Te,l1,l2,l3,l4,g)
    return figure
# functionality is the same for both dropdowns, so we reuse filter_options
# app.callback(Output("x-variable", "options"), [Input("y-variable", "value")])(
#     filter_options
# )
# app.callback(Output("y-variable", "options"), [Input("x-variable", "value")])(
#     filter_options
# )


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8050", debug=False)