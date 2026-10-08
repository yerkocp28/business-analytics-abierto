# Datos didácticos ComercioSur

Empresa ficticia. Todos los registros se generan mediante [generar_datos.py](../reproducibilidad/generar_datos.py), semilla 20261008. No describen una organización real. Son un caso común para todo el curso.

| Archivo | Unidad / cantidad | Uso |
|---|---|---|
| [Marco](comerciosur_marco.csv) | 5.000 pedidos de clientes distintos | Población finita conocida para estudiar muestreo y sesgo |
| [Pedidos](comerciosur_pedidos.csv) | Muestra aleatoria simple sin reemplazo de 600 pedidos del marco | Descripción, regresión, experimentos, tablero |
| [Mensual](comerciosur_mensual.csv) | 72 meses consecutivos, enero 2020 a diciembre 2025 | Validación temporal; serie independiente del archivo de pedidos |
| [Pareado](comerciosur_pareado.csv) | 80 personas medidas antes y después | Contraste pareado; sin grupo control concurrente |

En pedidos y marco, `id` es clave única; `canal` es Web/Tienda, asignado con probabilidades .65/.35; `campana` es A/B/C, asignada aleatoriamente con igual probabilidad. La asignación de campaña es independiente del canal. `ticket_mil` expresa miles de unidades monetarias (UM), con distribución asimétrica; `tiempo_min` expresa minutos de atención; `resuelto` vale 1 cuando se resuelve el requerimiento. B reduce el tiempo esperado en 4 minutos y C en 7 respecto de A; el canal Web agrega 3 minutos. El ruido de tiempo tiene desviación 7. La resolución tiene probabilidades .72/.78/.82 para A/B/C. Estos efectos pertenecen al generador, no son estimaciones ni garantías comerciales.

El canal es observacional: su asociación con ticket no identifica efecto causal. La inferencia causal de campañas solo se justifica en este mundo simulado con asignación aleatoria, observación completa, ausencia de interferencia y tratamiento bien definido. Una implementación real debe comprobar esas condiciones. La serie mensual tiene tendencia, estacionalidad anual y ruido; no se deben unir sus meses con pedidos, que no tienen fecha.

Los intervalos habituales de los laboratorios describen una superpoblación de pedidos futuros bajo estabilidad e independencia; el laboratorio de muestreo distingue ese objetivo de estimar la media del marco finito, para el que utiliza corrección por población finita. No mezclar ambos objetivos.
