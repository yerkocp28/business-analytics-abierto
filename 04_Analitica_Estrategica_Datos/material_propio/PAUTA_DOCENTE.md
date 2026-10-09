# Pauta docente · Analítica Estratégica de Datos

[Guía](../guia_maestra_aed.html) · [Ruta](../RUTA_APRENDIZAJE.md)

Resolver primero las prácticas de los notebooks. Esta pauta formativa separa respuestas y errores frecuentes; no es una evaluación institucional.

<a id="nb01"></a>
## 01 · Proceso y calidad

**Consigna:** Hay 100 clientes maduros: 72 activos, 18 abandonos y 10 estados desconocidos; además 40 inmaduros. Calcula retención observada y límites por faltantes. Documenta una actualización previa al ingreso sin inventar fechas.

**Pauta razonada:** Retención observada=72/90=.80; límites entre 72/100=.72 y 82/100=.82. Los 40 inmaduros se informan aparte. Marcar la cronología, consultar significado y comparar sensibilidad; una fecha conflictiva no equivale a abandono.

**Error frecuente:** Usar 140 como denominador o imputar el estado faltante para mejorar el KPI.

**Discusión:** ¿Qué diferencia hay entre cobertura de estado y representatividad?

**Criterio:** Entregar contrato, auditoría, denominadores y registro de exclusiones reproducible.

<a id="nb02"></a>
## 02 · Selección de técnicas

**Consigna:** Obtén tres segmentos con otra semilla y compara la partición con la original. Explica por qué comparar etiquetas 0/1/2 directamente puede fallar. Diseña un uso y una comprobación comercial posteriores.

**Pauta razonada:** Los números de cluster son arbitrarios; usar ARI sobre las mismas unidades permite comparar sin depender del nombre de la etiqueta. Estabilidad alta no demuestra utilidad. Para una campaña hace falta resultado, costo y evaluación de intervención.

**Error frecuente:** Confundir silhouette, estabilidad y rentabilidad como una única métrica.

**Discusión:** ¿Puede haber grupos estables que no ayuden a decidir?

**Criterio:** Justificar técnica, referencia, validación y una implicación práctica que no confunda asociación y efecto.

<a id="nb03"></a>
## 03 · KPIs y dashboard

**Consigna:** Dos unidades generan ingresos 100 y 900 UM, con margen 10 y 50 UM. Calcula margen agregado. Diseña cuatro tarjetas con fórmula, período, denominador, responsable y acción; concilia una con la consulta Power Query entregada.

**Pauta razonada:** Margen agregado=60/1000=6%; el promedio de 10% y 5,56% no responde al total. Tarjetas posibles: margen, reclamos por mil, entrega y cobertura de estado. Cada filtro debe conservar el grano y mostrar base.

**Error frecuente:** Mezclar ventas con marketing mensual mediante un join que multiplica filas.

**Discusión:** ¿Cómo comprobarías que la medida cambia correctamente con un filtro?

**Criterio:** Entregar ficha de KPI y tablero con fuente, población, período y acción ante desviaciones.

<a id="nb04"></a>
## 04 · Optimización y restricciones

**Consigna:** Reformula producción A/B para 130 horas y 100 unidades de material. Resuelve, verifica restricciones y compara contra una solución factible elegida a mano. Explica qué no demuestra el óptimo matemático.

**Pauta razonada:** Intersección: A=160/3, B=70/3; contribución=8500/3 UM. Se verifica 2A+B=130 y A+2B=100, no negatividad y estado del solver. Factibilidad del modelo no demuestra exactitud de capacidades, divisibilidad o demanda.

**Error frecuente:** Sumar recursos con unidades diferentes o extrapolar un precio sombra sin reoptimizar.

**Discusión:** ¿Qué restricción agregarías si A solo se produce en lotes de diez?

**Criterio:** Presentar variables, objetivo, restricciones, solución, holguras y una decisión de capacidad.

<a id="nb05"></a>
## 05 · Alternativas e información

**Consigna:** Con probabilidad de demanda alta .6, calcula EV de expandir y pilotar, EVPI y el precio máximo defendible de información perfecta. Dibuja la secuencia señal→decisión→resultado y distingue EVPI de EVSI neto.

**Pauta razonada:** Expandir=40, piloto=33 kUM. Con información perfecta: .4×15+.6×80=54; EVPI=14. Una señal imperfecta vale a lo sumo 14 bruto bajo este modelo; restar costo para obtener valor neto. Probabilidades posteriores se calculan por Bayes.

**Error frecuente:** Descontar dos veces inversión o interpretar EVPI como precio mínimo de cualquier estudio.

**Discusión:** ¿Qué cambia si el decisor no acepta pérdidas en ningún estado?

**Criterio:** Entregar matriz de pagos, alternativa, sensibilidad y cota del costo de información.

<a id="nb06"></a>
## 06 · SolarSur y Monte Carlo

**Consigna:** Duplica N manteniendo el modelo y después cambia shocks persistentes por anuales independientes. Predice qué cambia en SE y en la dispersión de VAN antes de ejecutar. Redacta una recomendación con límite de riesgo supuesto.

**Pauta razonada:** Duplicar N reduce SE aproximadamente por 1/√2, sin cambiar la distribución objetivo. Cambiar dependencia temporal modifica la distribución del VAN; no es mejora numérica. Separar P(pérdida), percentiles, SE y supuestos; no ajustar el límite para aprobar.

**Error frecuente:** Presentar un IC Monte Carlo como incertidumbre total del proyecto.

**Discusión:** ¿Qué parámetro económico necesitas estimar con datos externos antes de decidir?

**Criterio:** Informar VAN, pérdida, SE de la media, supuestos y sensibilidad de una recomendación.

<a id="nb07"></a>
## 07 · Integración e implementación

**Consigna:** Un piloto cubre 10.000 pedidos: riesgo base .06, reducción relativa supuesta .15, costo evitado 25 UM y costo total 1.500 UM. Calcula beneficio y reducción absoluta. Prepara memo, alternativas y tres hitos de seguimiento.

**Pauta razonada:** Evitados=90; beneficio=2250−1500=750 UM; reducción absoluta=.009, o .9 puntos porcentuales. Son supuestos, no impacto observado. Definir asignación, métrica primaria, guardarraíl, responsable, fecha y condición de parada.

**Error frecuente:** Comunicar 15 puntos porcentuales o presentar retorno supuesto como evidencia causal.

**Discusión:** ¿Qué dato te haría preferir no implementar el piloto?

**Criterio:** Entregar memo con alternativas, factibilidad, incertidumbre, piloto, responsable y criterio de revisión.

<a id="nb08"></a>
## 08 · Profundización prescriptiva

**Consigna:** Elige una estación: precio no lineal, cartera, cola o política secuencial. Para precio con costo 20 y q=120−2p, deriva el óptimo en [20,60]. Para otra estación, entrega hipótesis, referencia y sensibilidad, usando los prerrequisitos indicados.

**Pauta razonada:** Precio: contribución=(p−20)(120−2p); derivada=160−4p; p*=40, q=40 y contribución=800. Segunda derivada −4 y dominio verifican óptimo. En cartera/colas/políticas exigir supuestos, restricciones y contraste independiente; un MDP conocido es planificación, no aprendizaje de transiciones.

**Error frecuente:** Interpretar un solver exitoso o una trayectoria UCB favorable como garantía de despliegue.

**Discusión:** ¿Qué parte de la solución dejaría de ser válida si el modelo estuviera mal especificado?

**Criterio:** Defender supuestos, criterio de riesgo, comparación independiente y límite de transferencia.
