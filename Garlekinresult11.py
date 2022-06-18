def GalerkinResult(dataFrameList):
  #Nuevo dataframe juntando todas las dataFrame con elementos. Teniendo 4x#El ecuaciones
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

  return  matrixCalor