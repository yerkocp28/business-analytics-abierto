# Datos de los casos

[Volver al inicio](../../README.md)

[Catálogo completo y contratos](CATALOGO.md): grano, claves, unidades, disponibilidad, relaciones e incidencias de los 13 archivos fuente. [Perfil observable de columnas](perfil_columnas.csv).

Todas las empresas son **ficticias** y todos los datos son **simulados** con [generar_datos.py](generar_datos.py) (semilla fija `20261008`). Cada mecanismo está declarado en el código: qué variables influyen, con qué signo y qué defectos de calidad se introducen a propósito. No provienen de organizaciones ni de personas reales; los nombres de vendedores son inventados.

```bash
python _transversal/datos/generar_datos.py   # regenera exactamente los mismos archivos
```

Las carpetas `originales/` contienen los archivos fuente: los notebooks los leen sin modificarlos y guardan cualquier transformación en memoria.

| Caso | Archivo | Filas | Uso | Contenido |
|---|---|--:|---|---|
| FinCordillera (banca) | [fincordillera_clientes.csv](fincordillera/originales/fincordillera_clientes.csv) | 950 | Fundamentos 05; Modelos Predictivos 01, 02, 04, 06 | Perfil de clientes y abandono (`churn`, 28%) |
| FinCordillera | [fincordillera_transacciones.csv](fincordillera/originales/fincordillera_transacciones.csv) | 1.200 | Modelos Predictivos 05 | Transacciones con fraude como evento raro (30 casos, 2,5%) |
| QuillayMarket (retail) | [quillaymarket_ventas_detalle.csv](quillaymarket/originales/quillaymarket_ventas_detalle.csv) | 180 | Fundamentos 01–05 y guía | Ventas de enero a junio con región, producto, canal y vendedor |
| QuillayMarket | [quillaymarket_demanda_mensual.csv](quillaymarket/originales/quillaymarket_demanda_mensual.csv) | 480 | Modelos Predictivos 01, 03, 07 | 4 categorías × 12 meses × 10 réplicas independientes; sin tienda ni año, no es un panel temporal |
| PulpaLenga (celulosa) | [pulpalenga_calidad_pulpa.csv](pulpa_lenga/originales/pulpalenga_calidad_pulpa.csv) | 950 | Modelos Predictivos 05 | Variables del digestor y lotes defectuosos (16,3%); el riesgo crece al alejarse del punto óptimo |
| PulpaLenga | [pulpalenga_consumo_energetico.csv](pulpa_lenga/originales/pulpalenga_consumo_energetico.csv) | 480 | Modelos Predictivos 03 | Consumo energético por lote |
| CasaPeumo (hogar) | [casapeumo_laboratorio.xlsx](casapeumo/originales/casapeumo_laboratorio.xlsx) | 8 hojas | Analítica Estratégica 01–03 | Modelo de datos para tablero: ventas, clientes, productos, reclamos, marketing, metas y calendario. Incluye duplicados exactos, variantes de escritura en `Canal` y segmentos vacíos |
| BoldoNet (servicio digital) | [boldonet_kpis.xlsx](boldonet/originales/boldonet_kpis.xlsx) | 246 | Analítica Estratégica 01, 03 | Cohortes de clientes nuevos con versiones duplicadas, fechas en dos formatos, categorías mal escritas, costos negativos y estados no maduros |
| Embudo digital | [embudo_digital.xlsx](embudo_digital/originales/embudo_digital.xlsx) | 6 | Analítica Estratégica 07 | Sesiones, inicios de pago y compras por segmento de dispositivo |

Estadística Aplicada usa su propio caso simulado, [ComercioSur](../../02_Estadistica_Business_Analytics/datos/README.md).

Los datos se distribuyen bajo la misma licencia que el material ([CC BY-NC-SA 4.0](../../LICENSE)); el generador, bajo [MIT](../../LICENSE-CODE).
