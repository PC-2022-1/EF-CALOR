# TEST-GALEKRIN

Se implementa el metodo de Galerkin para resolver el problema de elementos finitos para la ecuación del calor. 

El archivo *PruebaGarlekin* implementa el metodo en terminos de incognitas. Este se debe implementar para varios elementos (Refinar la malla)
El archivo *PruebaNumericaGarlekin* toma los valores del ejemplo presentado en el paper "Elementos Finitos en fenomenos de transmisión" para un solo elemento de 4 nodos. 

En el archivo *GalerkinFunction* se hace la funcion para reproducir en forma general el sistema de ecuaciones por Nodo acorde a las coordenadas de los mismos.
En el archivo *GalerkinTest* se llama a la funcion GarlekinFunction para generar varios sistemas de ecuaciones dependiente del numero de elementos.
