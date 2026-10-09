# Pauta docente · Fundamentos de Business Analytics

[Guía](../guia_maestra_ba.html) · [Ruta](../RUTA_APRENDIZAJE.md)

Resolver primero las prácticas de los notebooks. Esta pauta formativa separa respuestas y errores frecuentes; no es una evaluación institucional.

<a id="nb01"></a>
## 01 · Pregunta de negocio y datos

**Consigna:** Un piloto contactará 2.000 clientes. Se supone que el abandono baja de 10% a 8%, cada retención vale 120 UM y cada contacto cuesta 2 UM. Formula decisión, unidad, horizonte y beneficio. ¿Qué dato falta para comprobar el efecto con el archivo de ventas?

**Pauta razonada:** Retenciones incrementales esperadas: 2000×(.10−.08)=40; beneficio 40×120−2000×2=800 UM. Es un escenario, no efecto estimado. El CSV de ventas no identifica clientes ni asignación a tratamiento/control: no permite comprobar retención.

**Error frecuente:** Confundir ventas con clientes o una reducción absoluta de 2 puntos con 2% relativo.

**Discusión:** ¿Qué resultado del piloto justificaría detener la campaña?

**Criterio:** Entregar una ficha con pregunta, unidad, fuente, decisión y dos límites.

<a id="nb02"></a>
## 02 · Exploración y comunicación visual

**Consigna:** Dos canales tienen 30 y 90 transacciones e ingresos de 9.000 y 18.000 UM. Calcula el ticket general, diseña un gráfico con su denominador y explica una comparación engañosa. Después construye un gráfico propio del CSV sin copiar el tablero.

**Pauta razonada:** Tickets 300 y 200; ticket general 27000/120=225 UM. El promedio simple 250 responde a canales con igual peso, no a una transacción elegida del total. El gráfico debe identificar período, cantidad de transacciones y unidad.

**Error frecuente:** Promediar promedios sin pesos o interpretar asociación como efecto del canal.

**Discusión:** ¿Cómo cambia la interpretación si el objetivo es comparar canales con igual peso?

**Criterio:** Presentar un gráfico con unidad, período, población y una interpretación verificable.

<a id="nb03"></a>
## 03 · Herramientas y caso integrador

**Consigna:** Trabaja en una copia del libro FBA_herramientas.xlsx. Filtra un canal y trimestre, calcula ingresos y ticket en Excel y pandas. Duplica una clave del catálogo y explica qué control debe detener una unión; entrega una recomendación de una página.

**Pauta razonada:** Las filas incluidas deben coincidir antes de comparar resultados. Ticket = suma de Monto / número de ID_Venta únicos. La dimensión repetida viola many_to_one; resolver el catálogo antes de unir, no compensar después dividiendo totales.

**Error frecuente:** Comparar universos distintos o sumar porcentajes de grupos.

**Discusión:** ¿Qué control distinguiría una devolución legítima de una copia duplicada?

**Criterio:** Entregar cálculo conciliado, control de cardinalidad y recomendación con sensibilidad.

<a id="nb04"></a>
## 04 · Probabilidad y simulación

**Consigna:** En 10.000 casos, prevalencia 1%, sensibilidad 90% y especificidad 95%: predice el valor de una alerta antes de calcular. Repite con prevalencia 10% y justifica el cambio. Explica qué reduce cuadruplicar las simulaciones.

**Pauta razonada:** Con 1%: VP=90 y FP=495; posterior=90/585≈15,38%. Con 10%: VP=900 y FP=450; posterior≈66,67%. Cuadruplicar N reduce aproximadamente a la mitad el error Monte Carlo, no el sesgo ni el riesgo subyacente.

**Error frecuente:** Confundir sensibilidad con probabilidad de condición dada alerta.

**Discusión:** ¿En qué situación no se cumpliría independencia entre simulaciones?

**Criterio:** Dibujar una tabla de frecuencias y explicar el efecto de n sin confundir sesgo con precisión.

<a id="nb05"></a>
## 05 · Puente hacia modelos predictivos

**Consigna:** Diseña cuatro tarjetas: datos para ajuste, selección, regla de decisión y prueba. Cambia el costo FN de 5 a 10 manteniendo FP=1 y explica qué puede cambiar antes de abrir la prueba. Formula un uso de clusters que deba validarse después.

**Pauta razonada:** La regla teórica pasa de 1/6 a 1/11 si hay calibración y la estructura de costos es esa. Umbral/selección se fijan fuera de prueba; no se elige el resultado más favorable de prueba. Los clusters describen perfiles; su uso comercial requiere evaluación posterior.

**Error frecuente:** Modificar el modelo tras mirar prueba o ordenar personas por número de cluster.

**Discusión:** ¿Cómo demostrarías valor incremental sobre contactar a todos?

**Criterio:** Informar partición, referencia, métrica, costo y un límite de generalización.
