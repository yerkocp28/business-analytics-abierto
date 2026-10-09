# Catálogo y contratos de los datos

[Biblioteca](../../README.md) · [Casos compartidos](README.md) · [ComercioSur](../../02_Estadistica_Business_Analytics/datos/README.md) · [Perfil de columnas](perfil_columnas.csv)

Edición revisada: 9 de octubre de 2026. Hay **13 archivos fuente: 10 CSV y 3 XLSX**. Los Excel contienen 12 hojas: nueve analíticas y tres de documentación. En total son **19 tablas analíticas**. Todos los registros son sintéticos. Los libros de trabajo de Fundamentos y Estadística y los controles BI son productos derivados; no constituyen nuevas fuentes independientes.

El perfil de columnas publica tipo leído, cantidad de faltantes, cardinalidad y rango observado. **Un rango observado no define un dominio admisible.** Los contratos siguientes definen grano, unidades, reglas, disponibilidad y relaciones. Los identificadores son claves artificiales, nunca variables explicativas. No se deben unir archivos por coincidencia de números de identificación.

## Archivos, grano y relaciones

| Fuente / hoja | Filas originales | Una fila representa | Clave y relación permitida |
|---|---:|---|---|
| FinCordillera / clientes | 950 | Cliente en un corte simulado | `cliente_id`, única; sin fecha real ni horizonte documentado de abandono |
| FinCordillera / transacciones | 1200 | Transacción simulada | `transaccion_id`, única; no hay `cliente_id`, no unir con clientes |
| QuillayMarket / ventas_detalle | 180 | Venta de un producto | `ID_Venta`, única; enero–junio 2025; no identifica al comprador |
| QuillayMarket / demanda_mensual | 480 | Réplica independiente para categoría y mes del año | `registro_id`, única; 4 categorías × 12 meses × 10 réplicas; no hay tienda ni año |
| PulpaLenga / calidad_pulpa | 950 | Lote del experimento de calidad | `lote_id`, única dentro de este archivo |
| PulpaLenga / consumo_energetico | 480 | Lote de otro experimento | `lote_id`, única; no es la misma población que calidad |
| ComercioSur / marco | 5000 | Pedido de un cliente distinto | `id`, única; población finita simulada |
| ComercioSur / pedidos | 600 | Pedido seleccionado sin reemplazo del marco | `id`, subconjunto exacto del marco; unión uno a uno |
| ComercioSur / mensual | 72 | Mes calendario | `mes`, única y consecutiva; enero 2020–diciembre 2025; independiente de pedidos |
| ComercioSur / pareado | 80 | Persona observada antes y después | `id`, única; identificador propio, no une con pedidos |
| CasaPeumo / Clientes | 180 | Cliente | `IdCliente`, única |
| CasaPeumo / Productos | 13 | Producto del catálogo | `IdProducto`, única |
| CasaPeumo / Ventas | 680 | Venta, incluyendo 5 copias exactas | Tras retirar copias: 675 `IdVenta` únicas; Clientes y Productos se unen muchos a uno |
| CasaPeumo / Reclamos | 39 | Reclamo asociado a una venta | `IdReclamo`, única; `IdVenta` referencia Ventas; agregar antes de unir si hay varios reclamos por venta |
| CasaPeumo / Marketing | 18 | Campaña y mes | Clave compuesta `FechaMes`, `Campaña`; no atribuir ventas individuales a esta tabla agregada |
| CasaPeumo / Metas | 6 | Meta mensual | `FechaMes`, única; comparar después de agregar Ventas al mismo mes |
| CasaPeumo / Calendario | 181 | Día calendario | `Fecha`, única; enero–junio 2026; unión muchos a uno desde Ventas |
| BoldoNet / Base_original | 246 | Versión de un cliente | `ID_cliente` + `Fecha_actualización`; resolver versiones para obtener 240 clientes |
| Embudo digital / Datos originales | 6 | Segmento de dispositivo agregado | `Segmento`, única; sin sesiones individuales ni fechas calendario |

Las otras hojas son `LEEME` de CasaPeumo y `Diccionario` y `Ficha_dataset` de BoldoNet. No se suman a las observaciones de sus casos.

## Diccionario semántico por caso

### FinCordillera

- `cliente_id` y `transaccion_id`: identificadores enteros. `edad`: años; `antiguedad_meses`: meses; `region`: categoría geográfica del generador. `ingreso_mensual_clp`: CLP por mes, positivo.
- `num_productos_contratados`, `frecuencia_reclamos_12m`, `retrasos_pago_12m` y `uso_app_movil_mensual`: conteos de productos, reclamos en 12 meses, retrasos en 12 meses y usos mensuales de la aplicación, respectivamente. No tienen fecha de captura individual.
- `monto_clp`: CLP por transacción, positivo; `hora_transaccion`: entero 0–23. `pais_distinto_habitual` y `dispositivo_nuevo`: indicadores 0/1. `num_transacciones_dia_cliente`: conteo diario simulado; al desplegar debe garantizarse que cuente solo lo disponible hasta la decisión.
- `churn` y `fraude`: etiquetas binarias posteriores al hecho; nunca entran como predictores. El horizonte de churn y la demora de confirmación de fraude no están definidos por un calendario real. La partición aleatoria enseña evaluación transversal, sin demostrar validez temporal de producción.
- No hay faltantes intencionales. El generador fija exactamente 266 abandonos y 30 fraudes mediante ranking de riesgo más ruido. Las etiquetas no son Bernoulli independientes con prevalencia estimada del mercado. La edad tiene un efecto indirecto vía ingreso; no es una variable totalmente desvinculada del resultado.

### QuillayMarket

- Ventas: `Fecha` es fecha ISO; `Mes` es su etiqueta en español, no una clave temporal independiente. `Region`, `Producto`, `Producto_Nombre`, `Vendedor` y `Canal` son categorías; los nombres de vendedores son ficticios. `Unidades` es cantidad entera positiva; `Precio_Unitario` y `Monto` se expresan en CLP. Debe cumplirse `Monto = Unidades × Precio_Unitario`.
- Demanda: `mes` es entero 1–12 y `categoria_producto` pertenece a Vestuario, Alimentos, Tecnologia o Electrohogar. `precio_promedio_clp` está en CLP por unidad; `inversion_marketing_clp` en CLP por réplica; `promocion_activa` es 0/1; `ventas_unidades` es cantidad positiva. `registro_id` no codifica tiempo.
- No hay faltantes intencionales. Las 480 filas permiten regresión transversal con estacionalidad declarada. **No forman un panel de tiendas ni una serie de 480 meses.** Estadística usa ComercioSur mensual; MPN07 genera una serie adicional de 72 meses en memoria a partir del perfil estacional de QuillayMarket, con tendencia y ruido declarados. Las ventas detalladas y la demanda proceden de simulaciones distintas; no se concilian como si fueran un único negocio registrado.
- Precio, promoción y presupuesto se tratan como información conocida para un escenario. En una aplicación real deben fijarse antes del resultado. Una asociación predictiva no prueba que cambiar una variable produzca el efecto estimado.

### PulpaLenga

- Calidad: `temperatura_coccion_c` en °C; `presion_digestor_bar` en bar; `tiempo_coccion_min` en minutos; `concentracion_alcali_pct` y `humedad_madera_pct` en porcentaje 0–100; `velocidad_linea_m_min` en metros/minuto. `defecto` es etiqueta posterior 0/1, con 155 positivos fijados por el generador.
- Energía: `toneladas_producidas` en toneladas; `temperatura_ambiente_c` en °C, puede ser negativa; `tipo_proceso` es Kraft/Mecanico; `antiguedad_equipo_anios` en años; `consumo_energetico_mwh` en MWh por lote, positivo.
- No hay faltantes intencionales ni calendario de proceso. Las mediciones de operación pueden estar disponibles durante o después del lote: definir el instante de decisión antes de usarlas para una alerta anticipada. No hay identificador común que autorice unir ambos experimentos.

### ComercioSur

- Marco y pedidos: `canal` es Web/Tienda; `campana` es A/B/C; `ticket_mil` se mide en miles de UM; `tiempo_min` en minutos; `resuelto` es 0/1. Los tres resultados se observan después de la atención. Campaña fue asignada aleatoriamente en el generador; canal es observacional. No hay faltantes.
- Mensual: `mes` es el primer día de cada mes, no una fecha de venta; `unidades` son ventas agregadas. Al emitir un pronóstico solo se conoce el historial hasta el último mes cerrado. Esta es la serie regular multianual almacenada como CSV; no incluye las simulaciones generadas en memoria por los notebooks.
- Pareado: `antes` y `despues` son minutos medidos sobre la misma persona. `id` empareja ambas mediciones. No hay control concurrente: una diferencia temporal no identifica por sí sola un efecto causal.
- Las inferencias sobre el marco finito deben declarar muestreo y corrección por población finita. La extrapolación a pedidos futuros requiere estabilidad de la superpoblación. Véase el [mecanismo detallado](../../02_Estadistica_Business_Analytics/datos/README.md).

### CasaPeumo

- Clientes: `IdCliente`, `Segmento`, `Región`, `FechaAlta` y `TipoCliente` describen identidad, segmento comercial, región, alta y tipo Persona/Pyme. Ocho segmentos están vacíos: se muestran como «Sin información», sin inventar una clasificación.
- Productos: `IdProducto`, `Categoría` y `Producto` identifican el catálogo. `PrecioLista` y `CostoUnitario` están en UM por unidad; no son CLP ni miles de UM.
- Ventas: `IdVenta`, `Fecha`, `IdCliente`, `IdProducto`, `Canal`, `Región`, `Unidades`, `PrecioLista`, `DescuentoPct`, `CostoUnitario`, `TiempoEntregaDias` y `CampañaOrigen`. Descuento se expresa como fracción 0–1, unidades como conteo positivo y entrega en días. Ingreso = unidades × precio × (1 − descuento); margen = ingreso − unidades × costo. El plazo efectivo de entrega es posterior a la venta, no un predictor disponible al comprar.
- Reclamos: `IdReclamo`, `IdVenta`, `FechaReclamo`, `Motivo`, `Resuelto`, `DiasResolucion` y `Satisfaccion1a5`. Resolución es Sí/No y satisfacción debe estar entre 1 y 5. Seis plazos vacíos corresponden a reclamos no resueltos: **no imputar cero días**. Reclamos y satisfacción son información posterior a la compra.
- Marketing: `FechaMes`, `Campaña`, `Inversión` (UM), `Impresiones`, `Clics` y `ClientesAdquiridos` (conteos). Son agregados sintéticos independientes de una atribución individual. Metas: `MetaVentas` en UM, `MetaMargenPct` en fracción, `MaxReclamosPor1000` como tasa por mil ventas y `MaxTiempoEntregaDias` en días, para cada `FechaMes`.
- Calendario: `Fecha`, `Año`, `NumeroMes`, `Mes`, `Trimestre`, `AñoMes` son fecha y sus atributos; año-mes ordena los períodos sin mezclar años.
- Se retiran cinco copias exactas y se normalizan 30 variantes de canal. Persisten 63 ventas anteriores al alta registrada: se marcan como incidencia, no se cambian fechas para forzar coherencia. Antes de medir captación o antigüedad deben investigarse. La colección enseña este límite de la simulación.

### BoldoNet

El diccionario de 14 variables está incluido en el propio libro. La fecha de corte contractual es **2026-08-05**. `Costo_acompañamiento` está en UM, `Días_permanencia` en días y `Satisfacción` es ordinal 1–5. Las cuatro variables de intervención son Sí/No; normalizar sus variantes antes de utilizarlas. Segmento, región y canal son categorías nominales.

Se conserva la versión con última actualización conocida por cliente; una fecha desconocida no desplaza una conocida. Empates conflictivos requieren revisión. En los 240 clientes resultantes se observan:

| Incidencia | Casos | Tratamiento docente |
|---|---:|---|
| Actualización anterior al ingreso | 21 | Marcar y comparar KPI principal con elegibilidad estricta |
| Actualización ausente | 1 | Marcar; no asumir fecha válida |
| Ingreso inválido | 1 | No puede acreditar madurez |
| Satisfacción fuera de 1–5 | 4 | Excluir del resumen de satisfacción, conservar incidencia |
| Satisfacción ausente | 6 | Reportar cobertura, no sustituir por satisfacción media |
| Permanencia negativa | 2 | Excluir de análisis de duración |
| Costo negativo | 2 | Excluir del costo válido y declarar denominador |
| Maduros sin estado válido | 6 | No imputar retención; mostrar cotas de sensibilidad |
| Inmaduros con estado aparentemente válido | 18 | No incorporar al KPI a 90 días |

Hay 127 clientes maduros y 121 con estado válido. La elegibilidad estricta de fechas también produce 121 en esta edición: una incidencia puede ser real sin alterar ese KPI concreto. No sumar incidencias como clientes distintos, porque pueden superponerse. Programa y resultados observados no prueban causalidad sin controlar diseño y selección. Estado a 90 días, permanencia, costo realizado y satisfacción son posteriores al ingreso; no usarlos para anticipar retención desde el día cero.

### Embudo digital

`Segmento` distingue seis dispositivos/plataformas. `Sesiones_anterior`, `Sesiones_actual`, `Inicios_pago`, `Compras` y `Abandonos_pago` son conteos agregados; debe cumplirse `Compras ≤ Inicios_pago ≤ Sesiones_actual` y `Abandonos_pago = Inicios_pago − Compras`. `Satisfaccion` es una proporción 0–1, no la escala 1–5 de otros casos.

Los períodos «anterior» y «actual» carecen de fechas explícitas; no pueden convertirse en una serie temporal. No hay IDs de usuario, exposición al tratamiento ni asignación aleatoria. Sirve para diagnóstico del embudo y planificación de un experimento, no para atribuir impacto causal ni calcular intervalos de satisfacción sin conocer su denominador.

## Simulaciones adicionales dentro de los notebooks

MPN07 y su guía generan 72 meses de QuillayMarket (2020–2025), con semilla 2026, tendencia, índice estacional derivado de las réplicas y ruido normal. Es una serie sintética nueva, no una recuperación de años o tiendas omitidos. Fundamentos contiene simulaciones de probabilidad y modelos; MPN incluye ruido controlado, datos faltantes inducidos y escenarios de deriva. Analítica Estratégica genera escenarios de SolarSur, carteras, colas y políticas secuenciales desde supuestos declarados. Estos objetos se reconstruyen al ejecutar sus celdas y no aumentan el inventario de 13 archivos fuente.

## Reproducción y uso docente

Los originales se conservan sin alteraciones. Los generadores usan semilla `20261008`; las transformaciones y exclusiones se aplican en memoria. El [perfil](perfil_columnas.csv) se actualiza con `python _transversal/datos/perfilar.py`. Los controles metodológicos verifican además el PSI, la independencia de calibración, la disponibilidad temporal y las incidencias de BoldoNet.

Estos datos cubren práctica transversal, una serie mensual, un caso pareado, un modelo comercial de varias tablas y problemas de calidad. Faltan paneles longitudinales identificados, datos de producción externa y eventos con fecha de disponibilidad completa. La profundización de posgrado requiere ampliar fuentes y diseño, no presentar estos casos sintéticos como evidencia de mercado.

Datos y material: [CC BY-NC-SA 4.0](../../LICENSE). Código: [MIT](../../LICENSE-CODE).
