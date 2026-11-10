# FIFA 22: estimación de la valoración de jugadores

Modelo de regresión para estimar la valoración de jugadores de FIFA 22 con Python, pandas y scikit-learn. Compara una referencia por mediana, Ridge y gradient boosting con preprocesamiento dentro de validación cruzada. En 3.833 jugadores de prueba, el modelo seleccionado obtiene un MAE de 152.336 EUR y R² de 0,975, con análisis de errores e importancia de variables. Los resultados corresponden a valoraciones del videojuego.

**Repositorio:** [fifa22-analisis-jugadores](https://github.com/hectortorres26/fifa22-analisis-jugadores)

**Alcance:** Estimar `value_eur`, la valoración asignada a los jugadores dentro de FIFA 22, a partir de doce atributos deportivos y físicos. El alcance es la estructura de valoración del videojuego; no el salario (`wage_eur`) ni el precio de un traspaso real.
