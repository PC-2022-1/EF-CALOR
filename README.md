# EF-CALOR

El programa soluciona el problema del calor por medio de elementos finitos. 
Se usan dos metodos. Galerkin y diferencias finitas. 

Se implementa una interfaz que agrupa los metodos, cada uno con su respectiva aplicación. 


- Galerkin generación de calor
Incluye *mesh.py* para hacer la discretización. Se implementa la solución con elementos tipo cuadrados. El problema involucra la ecuación de calor con el termino 
de generación. En general es una superficie que se comporta como foco de calor y cuyos lados pueden tener o no convección. La solución se implementa en los
archivos *GalerkinTest.py* y *GalerkinFunRect.py* Basado en "ELEMENTOS FINITOS EN FENÓMENOS DE TRANSMISIÓN"

- Galerkin sin generación de calor
Incluye *mesh.py* para hacer la discretización. Se implementa la solución con elementos tipo cuadrados o triangulos. 
El problema involucra la ecuación de calor con posibilidad de igualarla a una función f cualquiera. Incluye condiciones de frontera tipo
Neumann o tipo Dirichlet se usan archivos *Heat.py* y *HeatFunction.py*. Basado en "Remarks around 50 lines of Matlab: short finite element
implementation"

- Diferencias finitas

