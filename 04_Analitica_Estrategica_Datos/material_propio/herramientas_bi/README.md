# Práctica de Power Query y Power BI

Fuente: `_transversal/datos/casapeumo/originales/casapeumo_laboratorio.xlsx`, desde la raíz de la colección. Datos sintéticos.

1. Crear el parámetro de texto `RutaArchivo` con la ruta local al archivo.
2. Crear una consulta en blanco, abrir Editor avanzado y pegar [consulta.m](consulta.m). Nombrarla `Ventas`.
3. Comprobar cantidad de filas, tipos, claves y unidades antes de cargar.
4. Crear por separado las medidas de [medidas.dax](medidas.dax). Conservar porcentajes como fracciones y formatearlos como porcentaje.
5. Crear tarjetas y barras; filtrar un grupo, registrar el universo y contrastar con [controles.csv](controles.csv).
6. Entregar captura, filtros y tabla de conciliación. Una apariencia correcta no basta si los totales difieren.

Los archivos M y DAX son fuentes editables para la práctica. Los controles numéricos se calculan en Python;
su importación y ejecución en Power BI/Excel Desktop debe comprobarse en esa herramienta. No se distribuye un PBIX
ni se afirma haber ejecutado un motor que no está disponible en el entorno de construcción.

Para extender a un modelo estrella, cargar dimensiones únicas por separado y relacionarlas con el hecho.
No unir ventas con marketing o metas mensuales a nivel de fila. Guardar el original y documentar la depuración.
