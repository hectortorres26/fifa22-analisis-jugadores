# Cambios respecto a la versión original

## Revisión técnica y editorial — 2026-11-10

| Problema original | Corrección |
|---|---|
| El objetivo declarado era precio, pero se entrenaba con `wage_eur` | Objetivo coherente y explícito: `value_eur`, valoración del videojuego |
| Imputación antes de separar los datos | Imputación dentro del pipeline y de cada partición de validación |
| Selección RFECV no aplicada al modelo final y mezcla de unidades | Doce predictores explícitos; selección por CV; todas las métricas en EUR |
| Gráficos con API obsoleta y conclusiones no verificadas | Gráficos regenerables, referencia, errores por rango y límites del alcance |

Se añaden pruebas, dependencias fijadas, fuentes documentadas y resultados de ejecución. Las cifras nuevas corresponden al protocolo y los datasets identificados en esta revisión.

**Trazabilidad:** [cuaderno original](https://github.com/hectortorres26/fifa22-analisis-jugadores/blob/420ad20f5aabeab2901a1270194053a5af660570/analisis_jugadores_fifa22.ipynb) · [comparación completa](https://github.com/hectortorres26/fifa22-analisis-jugadores/compare/420ad20f5aabeab2901a1270194053a5af660570...main) · [historial](https://github.com/hectortorres26/fifa22-analisis-jugadores/commits/main).
