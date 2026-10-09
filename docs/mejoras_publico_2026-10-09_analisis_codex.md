# Mejoras de la colección abierta · 9 de octubre de 2026

[Biblioteca](../README.md) · [Mantenimiento](../MANTENIMIENTO.md)

## Cambios aplicados

La colección mantiene cuatro cursos, 28 notebooks y sus cuatro manuales en QMD, HTML y PDF. Se revisaron la experiencia de lectura y práctica, la coherencia entre formatos y la posibilidad de reconstruir los materiales.

| Área | Mejora |
|---|---|
| Recorrido de estudio | Cada módulo declara preparación, objetivo observable, ejemplo, práctica y criterio de logro. Las 28 rutas proceden de una fuente común y distinguen núcleo y profundización. |
| Navegación | Acceso a biblioteca, ruta y manuales; búsqueda tolerante a tildes, índice móvil plegable, salto al contenido, enlaces anterior/siguiente y modo clase en las cuatro guías. |
| Modelos Predictivos | Selector de planificación intensiva de cinco semanas o extendida de doce; corrección del ítem sobre ponderación de clases y revisión de referencias de riesgo de modelo. |
| Analítica Estratégica | Ejemplos trabajados de capacidad y valor marginal local, decisión bajo incertidumbre y valor de información, y una intervención que separa supuestos de evidencia causal. El laboratorio permite explorar 200 horas. |
| Lectura científica | Figuras ajustadas sin deformación, descripciones alternativas, ampliación con teclado, tablas y expresiones largas con desplazamiento local. |
| Controles | Nombres accesibles para controles deslizantes, indicador de valor, foco visible y recuperación de foco al cerrar una figura. |
| Entorno | Instalación nueva de las dependencias del repositorio público, kernel propio del entorno y construcción coordinada de los cuatro cursos. |
| Mantenimiento | Fuentes comunes de presentación y rutas, comando global, evidencia de comprobación, documentación de actualización y flujo de integración continua. |

La portada distingue el uso directo de las guías del uso de Jupyter para los laboratorios. Los enlaces permiten empezar por objetivos y criterios de logro, sin obligar a recorrer la totalidad del material en orden.

## Correcciones académicas concretas

- **Ponderación de clases.** La opción correcta explica que `class_weight="balanced"` cambia el objetivo de ajuste y puede cambiar tanto probabilidades como orden. No se garantiza que conserve el orden ni que mejore la calibración; se requiere validación representativa.
- **Riesgo de modelo.** La [SR 26-2 de la Reserva Federal](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.htm), de 17 de abril de 2026, reemplaza la SR 11-7. Se contextualiza como referencia estadounidense de gestión basada en riesgo.
- **Datos personales.** La [Ley 21.719](https://www.bcn.cl/leychile/Navegar?idNorma=1209272&idParte=10527471&idVersion=2026-12-01) se presenta con su entrada en vigencia general del 1 de diciembre de 2026, posterior a la fecha de esta revisión.
- **Optimización.** El valor marginal de una restricción es local: el ejemplo compara capacidades de 100, 110 y 200 horas para mostrar que no corresponde extrapolar indefinidamente el precio sombra.
- **Decisiones.** La práctica exige comparar utilidad esperada con información perfecta y explicar que el valor de información no es una mejora garantizada de cualquier estudio.
- **Comunicación causal.** La rentabilidad de una intervención se calcula bajo un efecto supuesto; una simulación no demuestra que el efecto se producirá.

## Comprobaciones y evidencia

Resultado local: **OK**. Se ejecutaron **28 notebooks, 221 celdas de código y 168 cambios de controles**, con 28 autoevaluaciones. La revisión de las publicaciones verificó **662 enlaces y anclas locales**, las nueve páginas en cuatro anchos sin desbordamiento horizontal y cuatro PDF de **19, 15, 16 y 14 páginas**, respectivamente. Los datos compartidos se conservaron sin cambios.

Además, el notebook de optimización comprueba tres combinaciones de capacidad y material, incluida la solución de 120 unidades con 240 horas, para verificar que el óptimo permanezca visible dentro de los ejes del gráfico.

La evidencia se conserva separada por función para que una captura no sustituya un cálculo y una ejecución sin errores no se confunda con eficacia pedagógica:

- Las carpetas `reproducibilidad/` de los cuatro cursos registran ejecución de notebooks, pruebas de controles y autoevaluaciones, cobertura y contraste de simuladores contra Python.
- [interfaz.json](../verificacion/interfaz.json) registra enlaces y anclas, coherencia de los 28 módulos, límites de página en PDF y 36 combinaciones de página y ancho de pantalla.
- [ultima_ejecucion.json](../verificacion/ultima_ejecucion.json) indica la fecha, versiones, modalidad y estado de la última comprobación global. El estado debe ser `OK`; una ejecución fallida no cuenta como validación.
- [Las capturas](../verificacion/capturas/) permiten inspeccionar la presentación móvil de guías y manuales.

Se ejecutaron los notebooks en un entorno nuevo de Windows con Python 3.12.13. Las publicaciones se regeneran con Quarto 1.10.18. La revisión de navegador cubre Chrome sin conexión; el flujo remoto usa Chromium y debe revisarse en Actions después de publicar el commit.

## Alcance y siguientes revisiones

Las pruebas cubren las publicaciones, sus recursos locales y las interacciones ejercitadas. La ampliación y navegación responden a teclado y los controles tienen nombres, pero esto no certifica cumplimiento completo de WCAG ni reemplaza una evaluación con tecnologías de apoyo.

La integración curricular usa las matrices existentes y agrega evidencias observables por módulo. Sigue siendo necesaria una revisión académica independiente de profundidad y carga real, junto con un piloto con estudiantes. No se midieron resultados de aprendizaje. Las funciones de Excel y de herramientas de tableros se comprueban mediante los ejemplos disponibles; no se declara una validación manual integral de aplicaciones de escritorio.

La relación con otras ediciones debe mantenerse mediante cambios editoriales trazables, adaptados a los casos de esta colección y verificados en sus tres formatos. Las mejoras futuras prioritarias son retroalimentación del piloto, contraste con una rúbrica común y pruebas de accesibilidad con lectores de pantalla.
