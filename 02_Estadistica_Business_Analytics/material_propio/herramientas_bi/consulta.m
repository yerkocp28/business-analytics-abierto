// Crear un parámetro de texto RutaArchivo con la ruta local a comerciosur_pedidos.csv.
let
    Fuente = Csv.Document(File.Contents(RutaArchivo), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Encabezados = Table.PromoteHeaders(Fuente, [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Encabezados, {{"id", Int64.Type}, {"canal", type text},
        {"campana", type text}, {"ticket_mil", type number}, {"tiempo_min", type number}, {"resuelto", Int64.Type}}, "en-US"),
    Verificado = if Table.RowCount(Table.Distinct(Tipos, {"id"})) <> Table.RowCount(Tipos)
                 then error "id duplicado: investigar antes de agregar" else Tipos
in
    Verificado
