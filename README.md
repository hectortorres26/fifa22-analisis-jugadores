# FIFA 22: análisis de jugadores y predicción salarial

Proyecto de **Hector Americo Torres Huamani** · Python y análisis de datos.

[Ver cuaderno](analisis_jugadores_fifa22.ipynb) · [Abrir original en Colab](https://colab.research.google.com/drive/1ebBipDym9RX9dy4CNa8l929a0DjAVyEY) · [Portafolio](https://www.datascienceportfol.io/hectortorres26/projects/2)

## Objetivo y contenido

Explorar atributos de jugadores de FIFA 22, su valoración y sus salarios mediante análisis descriptivo y regresión lineal.

**Alcance real del modelo:** el título original habla del precio del jugador, pero el código entrena con `y = data_imputed['wage_eur']`. Por tanto, las métricas guardadas corresponden al salario y no a la valoración `value_eur` ni a un precio real de transferencia.

### Trabajo incluido

Eliminación de columnas, revisión de valores faltantes, histogramas y diagramas de dispersión, comparaciones entre clubes y jugadores, imputación por media, selección de variables mediante RFECV y regresión lineal.

### Datos

Archivo esperado: `players_22.csv`. El cuaderno lo carga desde Google Drive. La fuente exacta de descarga y su licencia no están documentadas en el cuaderno; deben verificarse antes de redistribuir el archivo.

### Resultados históricos guardados

- R²: **0,5889**.
- Error cuadrático medio: **149 700 747,52**, en unidades de salario al cuadrado.

Son salidas del original, no métricas recalculadas durante esta publicación. No deben presentarse como precisión de predicción del valor de mercado.

### Revisión técnica

- La imputación se ajusta antes de separar entrenamiento y prueba, introduciendo fuga de información.
- Se ejecuta RFECV, pero el modelo final vuelve a usar todas las variables especificadas, sin aplicar su máscara de selección.
- `value_eur` se divide entre un millón en el análisis gráfico. Algunos rótulos y comentarios posteriores siguen hablando de euros o miles; requieren unificar las unidades.
- Hay correlaciones sobre tablas con texto y uso de `sns.distplot`, una API obsoleta: la compatibilidad depende de las versiones de las librerías.
- Algunas conclusiones narrativas requieren contraste con las gráficas y escalas, por ejemplo la referencia a miles de millones.

### Próximo paso recomendado

Definir expresamente si el objetivo será salario o valoración. Separar los datos antes de ajustar transformaciones, colocar la imputación y el modelo dentro de un pipeline y comparar contra una predicción base. Si se mantiene RFECV, realizar la selección dentro de las particiones de entrenamiento y aplicarla al modelo final.

## Estado de esta publicación

Se conserva el cuaderno original, incluidas sus salidas históricas. La revisión del 9 de noviembre de 2026 fue estática: lectura del código, salidas y estructura. No se ejecutó el análisis con los datasets ni se corrigió silenciosamente el trabajo original. Los problemas anteriores deben resolverse antes de considerar reproducibles los resultados.

## Cómo explorar el proyecto

1. Abra el enlace de Colab o el archivo `.ipynb` en GitHub para consultar el trabajo.
2. Para trabajar localmente, cree un entorno virtual con `python -m venv .venv` y actívelo.
3. Instale las dependencias con `python -m pip install -r requirements.txt`.
4. Obtenga los datos desde su fuente autorizada. Ajuste las rutas `/content/drive/MyDrive/DATA_PRACTICA/` al directorio donde los haya guardado.
5. En un entorno local, omita las celdas de montaje de Google Drive, si las hay.
6. Resuelva los puntos de la revisión técnica y reinicie el kernel antes de ejecutar todas las celdas en orden.

`requirements.txt` enumera las librerías utilizadas; las versiones del entorno original no están registradas y no se ha validado una combinación exacta de versiones. Los datasets no se incluyen en este repositorio.

## Autoría y procedencia

Publicado a partir del cuaderno enlazado en el portafolio del autor. Las fuentes y licencias de los datos son independientes de la autoría del análisis. Esta publicación no añade una licencia de redistribución al código ni a los datasets.
