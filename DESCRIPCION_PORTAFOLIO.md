# FIFA 22: estimación de la valoración de jugadores

Modelo de regresión para estimar la valoración de jugadores de FIFA 22 con Python, pandas y scikit-learn. Compara una referencia por mediana, Ridge y gradient boosting con preprocesamiento dentro de validación cruzada. En 3.833 jugadores de prueba, el modelo seleccionado obtiene un MAE de 152.336 EUR y R² de 0,975, con análisis de errores e importancia de variables. Los resultados corresponden a valoraciones del videojuego.

**Repositorio:** [fifa22-analisis-jugadores](https://github.com/hectortorres26/fifa22-analisis-jugadores)

**Alcance:** Estimar `value_eur`, la valoración asignada a los jugadores dentro de FIFA 22, a partir de doce atributos deportivos y físicos. El alcance es la estructura de valoración del videojuego; no el salario (`wage_eur`) ni el precio de un traspaso real.

## Versión publicada en datascienceportfol.io

Actualizada el 10 de noviembre de 2026. [Ver proyecto publicado](https://www.datascienceportfol.io/hectortorres26/projects/2).

**Título:** FIFA 22: estimación de la valoración de jugadores

**Resumen de la tarjeta:**

Estimación de valoraciones de FIFA 22 con Python y scikit-learn. En 3.833 jugadores de prueba, gradient boosting obtuvo un MAE de 152.336 EUR y R² de 0,975. Incluye comparación con una referencia, análisis de errores y código reproducible. El objetivo es la valoración del videojuego.

El [texto completo publicado](docs/portafolio.html) conserva el contenido y los enlaces de la página: objetivo, herramientas, metodología, resultados, interpretación, calidad y reproducibilidad.
