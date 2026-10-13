# Correcciones de calidad de notebooks y datos

Fecha: 9 de octubre de 2026. Alcance: los cuatro cursos y 28 notebooks de la colección abierta. Esta revisión corrige los hallazgos de ejecución, metodología y diseño didáctico de la auditoría; conserva los 13 archivos fuente de datos.

## Cambios metodológicos

| Hallazgo | Corrección | Comprobación |
|---|---|---|
| Escalado previo a la validación interna de Ridge/Lasso en MPN03 | `GridSearchCV` recibe el pipeline completo con escalador y modelo | Se instrumenta el escalador de la función publicada: diez ajustes sobre 80 de 100 filas para dos valores de alpha y cinco pliegues; un reajuste final sobre 100 |
| Selección y calibración reutilizaban observaciones | Partición 60/10/10/20 para ajuste, selección, calibración y prueba; modelo congelado antes de calibrar | 288/48/48/96 observaciones disjuntas; cuantil conformal por estadístico de orden; mismo flujo en NB, guía y QMD |
| Calibración temporal incluía respuestas aún futuras | MPN07 comprueba `objetivo = origen + horizonte − 1 < primera emisión de verificación` | Prueba con horizontes 1, 3 y 6; fechas y cantidad efectiva de errores visibles en el notebook |
| PSI nulo ante cambios de una variable binaria/constante | Categorías explícitas para variables discretas, faltantes y categorías nuevas; tramos continuos aprendidos solo de referencia | Cambio 5%→80% produce PSI ≈ 3,248; constante que cambia se detecta; identidad produce cero |
| Incertidumbre presentada con alcance excesivo | Se explicita qué omite el bootstrap de predicciones OOF fijas y que la SD entre pliegues es descriptiva | Explicación alineada en MPN05/06, guía y manual; no se usa solapamiento de intervalos marginales como prueba formal |
| MASE < 1 interpretado como superioridad futura automática | Se distingue el error escalado por la referencia histórica de una comparación sobre el mismo período futuro | NB07, QMD, guía y pregunta de autoevaluación aclaran el denominador y la comparación necesaria |
| Conflictos temporales y valores inválidos de BoldoNet incompletos | Banderas de actualización, satisfacción y permanencia; comparación de elegibilidad principal y estricta | Se detectan 21 actualizaciones anteriores al ingreso, cuatro satisfacciones fuera de rango y dos permanencias negativas; ambos KPI tienen 121 elegibles |

La comparación de métodos en MPN07 sigue siendo retrospectiva. Si se elige un método con ese backtest, hace falta una ventana adicional para evaluar la selección. La cobertura empírica se informa aunque difiera del nivel nominal; no se cambia el nivel para aprobar un resultado. Los intervalos conformales requieren intercambiabilidad y no garantizan cobertura por categoría ni ante extrapolación.

## Enseñanza y evaluación

- Los 28 notebooks incorporan una práctica nueva con cálculo, interpretación, supuestos y discusión. Las soluciones, errores frecuentes y orientaciones se publican en cuatro pautas docentes separadas. Son accesibles al estudiante como apoyo formativo, no un banco secreto de examen.
- Las opciones de autoevaluación se mezclan con semilla derivada de la pregunta. La respuesta correcta ya no ocupa sistemáticamente la segunda posición: aparece en la primera en 12 notebooks, en la segunda en ocho y en la tercera en ocho. Estadística pasa de dos a tres alternativas. La retroalimentación se comprueba para cada opción.
- Los tiempos proceden de una sola tabla: explicación, práctica y trabajo autónomo. Se eliminaron las once contradicciones detectadas y la afirmación general de que cada notebook cabía en 90 minutos. Son estimaciones docentes, pendientes de pilotaje con estudiantes.
- Estadística muestra pasos intermedios en ponderación, frecuencias de Bayes, intervalos t e interpretación de coeficientes. Los cálculos auxiliares siguen disponibles, con resultados que pueden contrastarse a mano.
- Analítica Estratégica incorpora estabilidad de clusters mediante ARI, visualización de región factible, árbol de información, contraste de dependencia temporal en Monte Carlo, memo y seguimiento. El notebook avanzado explicita prerrequisitos y alcance introductorio de sus estaciones.
- Fundamentos reorganiza el laboratorio de modelos por tramos y entrega un libro propio para el ejercicio de herramientas. Los módulos de profundización son una base técnica para discutir en posgrado; no equivalen a un tratamiento exhaustivo de cada especialidad.

Fuentes compartidas: [rutas y tiempos](../_transversal/rutas.py), [prácticas y pautas](../_transversal/practicas.py) y [autoevaluación](../_transversal/evaluacion.py). El constructor actualiza los bloques generados sin duplicarlos.

## Recursos de herramientas

| Recurso | Entrega | Límite de la comprobación |
|---|---|---|
| Fundamentos | [FBA_herramientas.xlsx](../01_Fundamentos_Business_Analytics/material_propio/FBA_herramientas.xlsx): datos, fórmulas, valores de control e instrucciones | Sustituye la referencia a un libro ausente; agregados contrastados con Python |
| Estadística | [EBA_tablero_excel.xlsx](../02_Estadistica_Business_Analytics/material_propio/EBA_tablero_excel.xlsx) con seis fórmulas preservadas y resultados cacheados | Caché calculado por Python, no por Excel Desktop |
| Estadística / BI | [Consulta M, medidas DAX y controles](../02_Estadistica_Business_Analytics/material_propio/herramientas_bi/README.md) | Importación editable y conciliación por filtro; no se ejecutó el motor nativo |
| Analítica Estratégica / BI | [Consulta M, medidas DAX y controles](../04_Analitica_Estrategica_Datos/material_propio/herramientas_bi/README.md) | Deduplicación, normalización y medidas de CasaPeumo; no se entrega ni se certifica un PBIX |

Al copiar secciones del manual a la guía de Estadística, el constructor reubica los enlaces relativos de cualquier recurso. Esto corrige también la navegación hacia las nuevas prácticas BI.

## Estado de los datos

El [catálogo](../_transversal/datos/CATALOGO.md) cubre las 13 fuentes (10 CSV y tres XLSX), 19 tablas analíticas y sus relaciones. El [perfil](../_transversal/datos/perfil_columnas.csv) describe 133 columnas; las hojas documentales quedan identificadas por separado.

Se distinguen unidades CLP, UM y miles de UM; fechas de observación y disponibilidad; claves válidas; significado de nulos y dominios. QuillayMarket demanda se describe como 480 réplicas transversales, sin tienda ni año. La serie multianual es ComercioSur mensual, con 72 meses. PulpaLenga calidad y energía son experimentos independientes. El pareado no incluye grupo control y el embudo no contiene sesiones individuales.

Se conservan los defectos que permiten enseñar calidad: duplicados, categorías con variantes, cohortes inmaduras, fechas conflictivas y respuestas faltantes. Se muestran banderas, denominadores y análisis de sensibilidad. Corregir el análisis no significa fabricar valores plausibles en los originales.

## Evidencia y límites

La evidencia de la reconstrucción está en [verificación global](../verificacion/ultima_ejecucion.json), [interfaz](../verificacion/interfaz.json) y los archivos `ejecucion_notebooks.json`, `verificacion_widgets.json` y `verificacion_edicion.json` de cada curso. Los notebooks se ejecutan desde un kernel nuevo; se prueban cambios reales de parámetros y se revisan errores capturados dentro de widgets.

La ejecución local completa finalizó correctamente. Resultado por curso:

| Curso | Notebooks ejecutados | Celdas de código | Cambios de controles probados | Manual PDF |
|---|---:|---:|---:|---:|
| Fundamentos | 5 | 38 | 42 | 19 páginas |
| Estadística | 8 | 65 | 36 | 15 páginas |
| Modelos Predictivos | 7 | 68 | 56 | 17 páginas |
| Analítica Estratégica | 8 | 60 | 34 | 15 páginas |
| **Total** | **28** | **231** | **168** | **4 manuales** |

Se comprobaron 672 enlaces locales y anclas y nueve páginas en cuatro anchos de pantalla (36 comprobaciones, sin desbordamientos). La revisión visual corrigió cuatro notas que heredaban el estilo de la barra lateral; la regresión comprueba su ancho dentro del contenido. La generación repetida de rutas, prácticas y pautas dejó iguales las 62 fuentes examinadas.

Las [13 fuentes se regeneraron idénticas byte por byte](../verificacion/datos_fuente.json) y se compararon con la base anterior. En MPN03, el intervalo nominal de 80% obtuvo cobertura de 79,17% en 96 casos de prueba, con semiancho 18,706 unidades y 48 casos de calibración. Se informa el resultado observado, no se promete una cobertura idéntica en otra muestra.

Los diez controles adicionales están en [verificar_metodologia.py](../_transversal/verificar_metodologia.py) y forman parte de la construcción completa y del flujo de GitHub Actions. El procedimiento reproducible se documenta en [MANTENIMIENTO.md](../MANTENIMIENTO.md).

La ejecución técnica y la coherencia entre formatos no sustituyen revisión académica de pares ni pilotaje. No se ha ejecutado Excel Desktop o Power BI; no se presenta esa validación como realizada. Esta corrección corresponde a la edición abierta y no acredita sincronización de otra edición.
