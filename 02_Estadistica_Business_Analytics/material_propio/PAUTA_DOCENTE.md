# Pauta docente · Estadística Aplicada a Business Analytics

[Guía](../guia_maestra_eba.html) · [Ruta](../RUTA_APRENDIZAJE.md)

Resolver primero las prácticas de los notebooks. Esta pauta formativa separa respuestas y errores frecuentes; no es una evaluación institucional.

<a id="nb01"></a>
## 01 · Problema, descripción y muestreo

**Consigna:** Una muestra toma el mismo número de pedidos Web y Tienda. Sus medias son 10 y 20 minutos, pero la población contiene 70% Web y 30% Tienda. Estima la media poblacional y contrasta con el promedio sin ponderar. Redacta la ficha de muestreo.

**Pauta razonada:** Media ponderada=.7×10+.3×20=13 min; promedio sin pesos=15. Los pesos provienen del marco, no de la cuota muestral. Distinguir objetivo finito de pedidos futuros; el diseño y la cobertura son parte del contrato.

**Error frecuente:** Usar cuotas muestrales como si fueran pesos poblacionales.

**Discusión:** ¿Qué ocurriría si no se conociera la proporción de Tienda?

**Criterio:** Entregar contrato de análisis con población, diseño, estimando y fuentes de sesgo.

<a id="nb02"></a>
## 02 · Probabilidad, Bayes y distribuciones

**Consigna:** Construye una tabla 2×2 para 10.000 alertas potenciales con prevalencia 3%, sensibilidad 85% y especificidad 94%. Calcula P(riesgo|alerta) sin llamar al helper. Elige una distribución para llegadas y justifica un supuesto que podría fallar.

**Pauta razonada:** VP=255, FN=45, FP=582, VN=9118; posterior=255/837≈30,47%. Poisson exige supuestos sobre tasa e independencia; ráfagas o congestión pueden invalidarlos. Los conteos son esperados.

**Error frecuente:** Aplicar especificidad a todos los casos en vez de a los negativos.

**Discusión:** ¿Por qué una alerta no equivale a una clasificación confirmada?

**Criterio:** Calcular e interpretar el posterior 180/670 y explicar por qué no equivale a sensibilidad.

<a id="nb03"></a>
## 03 · Estimación e intervalos

**Consigna:** Con n=25 pedidos independientes, media 12 minutos y SD=5, construye el IC t del 95% paso a paso. Indica qué parámetro cubre. Compara con n=100 manteniendo media y SD.

**Pauta razonada:** SE=5/√25=1; t24≈2,064; IC≈[9,936;14,064]. Para n=100, SE=.5 y t99≈1,984: [11,008;12,992]. Se estima la media de la población objetivo, no el rango del 95% de los pedidos.

**Error frecuente:** Sustituir SD por SE o asignar probabilidad posterior al parámetro fijo.

**Discusión:** ¿Se conserva la validez si los 25 pedidos pertenecen a una misma sucursal?

**Criterio:** Reportar estimación, intervalo, unidad, población objetivo y condiciones de validez.

<a id="nb04"></a>
## 04 · Correlación y regresión

**Consigna:** Un modelo de tiempo incluye ticket, canal y campaña. El coeficiente de ticket es .08 min por mil UM. Interpreta un incremento de 20 mil UM, distingue IC del coeficiente e intervalo de un pedido y propone un diagnóstico de residuos.

**Pauta razonada:** Cambio condicional esperado 1,6 min manteniendo las otras variables fijas y dentro del rango. No es una intervención causal. El IC cuantifica incertidumbre del parámetro; el intervalo predictivo incluye variación individual. Revisar residuos frente a ajuste, tiempo y grupos.

**Error frecuente:** Interpretar HC3 como solución para especificación incorrecta o dependencia ignorada.

**Discusión:** ¿Qué información necesitarías para defender un efecto causal del ticket?

**Criterio:** Justificar especificación, interpretar un coeficiente y señalar un límite causal.

<a id="nb05"></a>
## 05 · Contrastes, ANOVA y decisión

**Consigna:** B−A en tiempo tiene IC95% [−6,−2] min y estimación −4. B cuesta 5 UM adicionales por pedido y ahorrar un minuto vale 1 UM. Decide si significación estadística basta para recomendar B y elige la prueba para datos independientes o pareados.

**Pauta razonada:** Beneficio estimado 4−5=−1 UM; al transformar el intervalo: [2−5,6−5]=[−3,1]. Mejora de tiempo no implica rentabilidad. Welch para grupos independientes; contraste de diferencias si las mismas unidades se miden dos veces, con sus supuestos.

**Error frecuente:** Equiparar p pequeño con conveniencia económica o parear observaciones arbitrariamente.

**Discusión:** ¿Qué cambia si se comparan las tres campañas y luego se elige la mejor?

**Criterio:** Entregar diferencia, IC, p, ajuste por multiplicidad y una decisión condicionada.

<a id="nb06"></a>
## 06 · Series y pronóstico

**Consigna:** Para reales [120,150,180], una referencia predice [110,160,170] y otro método [125,140,190]. Calcula MAE. Dibuja entrenamiento, selección y prueba por fechas para un horizonte de tres meses; explica cuándo se conoce cada error.

**Pauta razonada:** MAE referencia=10; segundo=(5+10+10)/3≈8,33. La comparación requiere el mismo horizonte y orígenes. Cada error solo está disponible al observar su fecha objetivo; no se mezcla prueba en la selección.

**Error frecuente:** Comparar horizontes distintos o calibrar con resultados posteriores a la emisión.

**Discusión:** ¿Es válido tratar errores de orígenes solapados como independientes?

**Criterio:** Dibujar las ventanas y explicar métrica, referencia y dependencia entre errores solapados.

<a id="nb07"></a>
## 07 · Visualización y herramientas

**Consigna:** Filtra Tienda en ComercioSur y concilia cantidad, tiempo medio y resolución en Python, Excel y la consulta Power Query entregada. Diseña una tarea de usuario que evalúe comprensión del tablero manteniendo iguales los datos.

**Pauta razonada:** Primero conciliar universo y tipos; cantidades suman, medias/tasas se recalculan desde numeradores y denominadores. Registrar valores y filtros en cada herramienta. Un experimento de comprensión puede medir aciertos/tiempo con asignación y tareas iguales; no demuestra por sí solo impacto comercial.

**Error frecuente:** Atribuir cambios comerciales al diseño sin contrafactual.

**Discusión:** ¿Cuál es la diferencia entre una fórmula escrita y una fórmula recalculada por Excel?

**Criterio:** Entregar un tablero con unidades, filtros y totales conciliados; identificar qué se ejecutó.

<a id="nb08"></a>
## 08 · Integrador y comunicación

**Consigna:** Una campaña reduce tiempo: IC de B−A [−5,−1] min. Para resolución el IC de diferencia es [−.06,.02]; el margen de no inferioridad predefinido es −.03. Redacta un memo de 100 palabras con decisión, incertidumbre y siguiente evidencia.

**Pauta razonada:** Hay reducción de tiempo bajo el diseño, pero no se acredita no inferioridad de resolución porque el límite inferior −.06 cruza −.03. No rechazo de igualdad no demuestra equivalencia. Proponer decisión condicionada a costos/guardarraíl y un diseño con precisión suficiente.

**Error frecuente:** Convertir un resultado no significativo en ausencia de deterioro.

**Discusión:** ¿Qué información del diseño debe acompañar ambos intervalos?

**Criterio:** Entregar memo, cálculo, gráfico y defensa con población, sensibilidad y siguiente evidencia.
