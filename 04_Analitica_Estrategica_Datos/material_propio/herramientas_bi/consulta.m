// Crear un parámetro RutaArchivo con la ruta local a casapeumo_laboratorio.xlsx.
let
    Libro = Excel.Workbook(File.Contents(RutaArchivo), null, true),
    Encabezados = Table.PromoteHeaders(Libro{[Item="Ventas", Kind="Sheet"]}[Data], [PromoteAllScalars=true]),
    Tipos = Table.TransformColumnTypes(Encabezados, {{"IdVenta", type text}, {"Fecha", type date},
        {"Unidades", Int64.Type}, {"PrecioLista", type number}, {"DescuentoPct", type number},
        {"CostoUnitario", type number}, {"TiempoEntregaDias", type number}}),
    SinCopias = Table.Distinct(Tipos),
    Unicas = if Table.RowCount(Table.Distinct(SinCopias, {"IdVenta"})) <> Table.RowCount(SinCopias)
             then error "Claves de venta conflictivas" else SinCopias,
    Canal = Table.TransformColumns(Unicas, {{"Canal", each
        let c = Text.Lower(Text.Trim(_)) in
        if c = "sitio web" then "Sitio web" else if c = "tienda física" then "Tienda física"
        else if c = "marketplace" then "Marketplace" else error "Canal desconocido", type text}}),
    Ingreso = Table.AddColumn(Canal, "Ingreso", each [Unidades] * [PrecioLista] * (1-[DescuentoPct]), type number),
    Margen = Table.AddColumn(Ingreso, "Margen", each [Ingreso]-[Unidades]*[CostoUnitario], type number)
in
    Margen
