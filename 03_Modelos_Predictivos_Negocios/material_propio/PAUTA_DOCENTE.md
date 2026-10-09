# Pauta docente · Modelos Predictivos para los Negocios

[Guía](../guia_maestra_mpn.html) · [Ruta](../RUTA_APRENDIZAJE.md)

Resolver primero las prácticas de los notebooks. Esta pauta formativa separa respuestas y errores frecuentes; no es una evaluación institucional.

<a id="nb01"></a>
## 01 · Problema predictivo

**Consigna:** Se quiere predecir abandono al inicio de un trimestre. Hay reclamos del trimestre anterior, fecha de cancelación y descuento ofrecido después de cancelar. Define Y, unidad, instante y baseline; justifica variables admisibles y distingue el ejemplo de red fija de entrenar una red.

**Pauta razonada:** Reclamos previos pueden ser admisibles; cancelación y descuento posterior son fuga. Y necesita horizonte de abandono explícito. Baseline de prevalencia aprendido en ajuste; comparar AP/costo según decisión. La red fija ilustra propagación, no aprendizaje de pesos.

**Error frecuente:** Usar disponibilidad en la base como equivalente a disponibilidad al decidir.

**Discusión:** ¿Cómo probarías que el pipeline operativo respeta el instante de corte?

**Criterio:** Entregar ficha de problema, referencia y justificación de una técnica; explicar la red mínima.

<a id="nb02"></a>
## 02 · Preparación sin fuga

**Consigna:** Los ingresos altos presentan más ausencias. Propón dos tratamientos, explica sus límites y diseña la validación. La tasa base es .28 y el criterio acordado AP≥2×base y AUC≥.70: informa cumplimiento con tus resultados, incluso si falla.

**Pauta razonada:** Mediana e indicador de ausencia pueden ser comparadores; ninguno elimina por sí solo MNAR. Buscar otra fuente y documentar incertidumbre. Cada transformación se ajusta dentro del entrenamiento correspondiente. El umbral AP es .56; informar AP/AUC y no rebajar el criterio para aprobar.

**Error frecuente:** Imputar con toda la tabla o declarar que un buen AUC elimina sesgo de selección.

**Discusión:** ¿Qué harías si el modelo no alcanza el criterio antes de la prueba?

**Criterio:** Demostrar separación de datos, contrato de variables y transformaciones ajustadas sin prueba.

<a id="nb03"></a>
## 03 · Regresión de demanda

**Consigna:** Con modelo congelado que predice 20 y residuos absolutos de calibración [1,2,3,4,5,6,7,8,9], calcula el intervalo conformal 80%. Identifica qué conjunto puede elegir alpha y qué cambia si reajustas después con calibración.

**Pauta razonada:** k=ceil(10×.8)=8; q=8; intervalo [12,28]. Alpha se selecciona con CV interna de ajuste, reestimando el escalador por fold. Reajustar tras calibrar invalida la justificación de ese cuantil; hay que reservar/calibrar de nuevo con datos independientes.

**Error frecuente:** Confundir conjunto de selección con calibración o prometer cobertura por segmento.

**Discusión:** ¿Qué ocurre si se pide un nivel que el tamaño de calibración no permite?

**Criterio:** Reportar MAE/RMSE, referencia, diagnóstico y diferencia entre IC de media e intervalo predictivo.

<a id="nb04"></a>
## 04 · Clasificación de abandono

**Consigna:** Probabilidad base .25 y odds ratio 1.5 por una unidad: calcula la nueva probabilidad. Luego compara dos modelos en los mismos clientes de validación y explica qué incertidumbre de la diferencia debes examinar antes de prometer superioridad.

**Pauta razonada:** Chances base=1/3; nuevas=.5; probabilidad=1/3. Remuestrear pares de clientes preserva el emparejamiento de predicciones para una diferencia condicional; para incluir selección/entrenamiento hay que repetir ese proceso. No elegir el modelo con la prueba.

**Error frecuente:** Multiplicar directamente la probabilidad por el odds ratio o usar intervalos marginales como prueba de diferencia.

**Discusión:** ¿Un AUC mayor siempre produce una campaña más rentable?

**Criterio:** Justificar modelo y política con métricas fuera de muestra y límites de utilidad.

<a id="nb05"></a>
## 05 · Validación, métricas y umbral

**Consigna:** Con TP=30, FN=10, FP=20, TN=140 y costos FN=8, FP=2, calcula precisión, recall y costo medio. Fija una política antes de evaluar. Explica qué captura el bootstrap sobre predicciones OOF ya calculadas.

**Pauta razonada:** Precisión=.60; recall=.75; costo=(10×8+20×2)/200=.60 UM/caso; t*=.2 si hay calibración y ese modelo de costos. Bootstrap de pares OOF fijos es condicional a esas predicciones; no reproduce toda la incertidumbre de selección/entrenamiento.

**Error frecuente:** Optimizar el umbral en prueba o llamar a un intervalo condicional garantía operacional.

**Discusión:** ¿Cuántos eventos positivos sostienen tu estimación de recall?

**Criterio:** Documentar selección, datos reservados y costo; no inferir calibración por coincidencia de umbrales.

<a id="nb06"></a>
## 06 · Limitaciones y comunicación

**Consigna:** Una variable binaria pasa de proporciones [.90,.10] a [.60,.40]. Calcula PSI conservando dos categorías. Propón un tratamiento para un faltante y una categoría nueva y redacta una alerta sin afirmar caída del AUC.

**Pauta razonada:** PSI=(−.3)ln(.6/.9)+.3ln(.4/.1)≈.5375. Las categorías nuevas y faltantes deben tener conteos explícitos; documentar regularización de ceros. Investigar registro/población/proceso y esperar etiquetas para medir desempeño.

**Error frecuente:** Colapsar una variable discreta en un único intervalo o usar PSI como prueba causal.

**Discusión:** ¿Por qué el PSI numérico depende del esquema de tramos y de epsilon?

**Criterio:** Entregar ficha con evidencia, incertidumbre, umbral de revisión y propuesta de mejora.

<a id="nb07"></a>
## 07 · Pronóstico de demanda

**Consigna:** Al emitir en abril solo se observan resultados hasta marzo. Un error de pronóstico tiene objetivo abril y otro marzo. Decide cuáles pueden calibrar el intervalo y escribe una condición con fechas. Explica el límite de usar el mismo backtest para escoger y evaluar el método.

**Pauta razonada:** Solo el error con objetivo marzo está disponible. Condición fecha_objetivo < fecha_emision. Un origen temprano no basta si su horizonte termina después del corte. Si se selecciona con el backtest, se requiere otra ventana para evaluar la selección.

**Error frecuente:** Partir orígenes por la mitad sin comprobar cuándo se conoce la respuesta.

**Discusión:** ¿Cómo incorporarías retrasos en la llegada de etiquetas?

**Criterio:** Explicar horizonte, cobertura observada, referencia y límites de cambios del proceso.
