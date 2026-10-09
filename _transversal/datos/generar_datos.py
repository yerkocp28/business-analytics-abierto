"""Genera los datos de los casos docentes de la colección abierta.

Todas las empresas son ficticias y todos los datos son simulados con mecanismos declarados en
este archivo (semilla fija). No derivan de datos institucionales ni de personas reales.
Ejecutar desde cualquier carpeta:  python _transversal/datos/generar_datos.py

Casos:
  fincordillera  · banco minorista: abandono de clientes y fraude en transacciones
  quillaymarket  · retail: ventas detalladas (Fundamentos) y demanda mensual (Modelos Predictivos)
  pulpalenga     · planta de celulosa: defectos de calidad y consumo energético
  casapeumo      · artículos para el hogar: modelo de datos para tablero (Analítica Estratégica)
  boldonet       · servicio digital: cohortes de clientes nuevos con problemas de calidad deliberados
  embudo_digital · embudo de compra por segmento de dispositivo
"""
import re
from pathlib import Path

import numpy as np
import pandas as pd

DATOS = Path(__file__).resolve().parent
SEMILLA = 20261008
MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
         "Septiembre", "Octubre", "Noviembre", "Diciembre"]


def _destino(caso):
    carpeta = DATOS / caso / "originales"
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta


def _csv(df, caso, archivo):
    df.to_csv(_destino(caso) / archivo, index=False, lineterminator="\n")


def _k_positivos(latente, k, rng):
    """Marca los k casos con mayor latente + ruido logístico.

    Es una construcción de prevalencia fija: las etiquetas son dependientes.
    No equivale a Bernoulli independientes con un intercepto logístico fijado a priori.
    """
    ruido = rng.logistic(0, 1, len(latente))
    orden = np.argsort(-(latente + ruido), kind="stable")
    y = np.zeros(len(latente), dtype=int)
    y[orden[:k]] = 1
    return y


# --------------------------------------------------------------------------- FinCordillera
def fincordillera_clientes(rng):
    n = 950
    edad = rng.integers(19, 75, n)
    antig = np.clip(np.round(rng.gamma(2.3, 38, n)), 1, 179).astype(int)
    ingreso = np.exp(rng.normal(np.log(1_050_000) + .005 * (edad - 45), .36, n))
    ingreso = (np.clip(ingreso, 350_000, 2_400_000) / 1000).round().astype(int) * 1000
    productos = np.clip(rng.poisson(2.0, n) + 1, 1, 5)
    reclamos = np.clip(rng.poisson(1.3, n), 0, 7)
    retrasos = np.clip(rng.poisson(1.0, n), 0, 5)
    app = np.clip(rng.poisson(8.0, n), 1, 21)
    regiones = ["Metropolitana", "Valparaiso", "Biobio", "La Araucania", "Antofagasta"]
    region = rng.choice(regiones, n, p=[.38, .17, .17, .14, .14])
    # Mecanismo: reclamos y retrasos elevan el riesgo; uso de app, productos y antigüedad lo
    # reducen. Edad no tiene efecto directo; influye indirectamente vía ingreso. Región tiene efecto pequeño.
    latente = (.55 * reclamos + .45 * retrasos - .13 * app - .38 * (productos - 3)
               - .007 * (antig - 85) - .25 * (ingreso - 1_100_000) / 500_000
               + np.where(region == "Antofagasta", .25, 0))
    churn = _k_positivos(latente, 266, rng)  # 28,0% de abandono
    return pd.DataFrame({
        "cliente_id": np.arange(1001, 1001 + n), "edad": edad, "antiguedad_meses": antig,
        "ingreso_mensual_clp": ingreso, "num_productos_contratados": productos,
        "frecuencia_reclamos_12m": reclamos, "retrasos_pago_12m": retrasos,
        "uso_app_movil_mensual": app, "region": region, "churn": churn})


def fincordillera_transacciones(rng):
    n = 1200
    monto = np.exp(rng.normal(np.log(38_000), .95, n))
    monto = (np.clip(monto, 2_000, 900_000) / 100).round().astype(int) * 100
    perfil = np.array([1, .6, .4, .3, .3, .5, 1.2, 2.5, 3.5, 4, 4.2, 4.5, 5, 4.6, 4.2, 4, 4.1,
                       4.4, 4.8, 4.5, 3.8, 3, 2.2, 1.5])
    hora = rng.choice(24, n, p=perfil / perfil.sum())
    pais = rng.binomial(1, .07, n)
    dispositivo = rng.binomial(1, .09, n)
    diarias = np.clip(rng.poisson(2.2, n), 0, 9)
    latente = (1.9 * pais + 1.6 * dispositivo + 1.1 * (hora <= 5) + .75 * np.log(monto / 38_000)
               + .3 * diarias)
    fraude = _k_positivos(latente, 30, rng)  # 2,5%: evento raro
    return pd.DataFrame({
        "transaccion_id": np.arange(500_000, 500_000 + n), "monto_clp": monto,
        "hora_transaccion": hora, "pais_distinto_habitual": pais, "dispositivo_nuevo": dispositivo,
        "num_transacciones_dia_cliente": diarias, "fraude": fraude})


# --------------------------------------------------------------------------- QuillayMarket
def quillaymarket_ventas_detalle(rng):
    n = 180
    dias = pd.date_range("2025-01-02", "2025-06-30", freq="D")
    fechas = np.sort(rng.choice(dias, n))
    productos = {"A": ('Notebook 14"', 529_990), "B": ("Refrigerador 300 L", 449_990),
                 "C": ('Smart TV 55"', 389_990), "D": ("Aspiradora robot", 199_990)}
    codigo = rng.choice(list(productos), n, p=[.22, .2, .3, .28])
    descuento = rng.choice([0, .05, .10], n, p=[.6, .25, .15])
    precio = np.array([productos[c][1] for c in codigo]) * (1 - descuento)
    precio = (np.round(precio / 1000) * 1000 - 10).astype(float)
    unidades = np.clip(rng.poisson(1.9, n) + 1, 1, 7)
    vendedores = ["Ignacio Fuentes", "Daniela Torres", "Benjamín Araya", "Catalina Vega",
                  "Tomás Herrera", "Javiera Castro", "Felipe Navarro", "Constanza Lagos"]
    fecha = pd.to_datetime(fechas)
    return pd.DataFrame({
        "ID_Venta": np.arange(1000, 1000 + n), "Fecha": fecha.strftime("%Y-%m-%d"),
        "Mes": [MESES[m - 1] for m in fecha.month],
        "Region": rng.choice(["Norte", "Centro", "Sur"], n, p=[.25, .45, .3]),
        "Producto": codigo, "Producto_Nombre": [productos[c][0] for c in codigo],
        "Vendedor": rng.choice(vendedores, n), "Canal": rng.choice(["Online", "Tienda física"], n, p=[.45, .55]),
        "Unidades": unidades, "Precio_Unitario": precio, "Monto": unidades * precio})


def quillaymarket_demanda_mensual(rng):
    categorias = {"Vestuario": (150, 14_000), "Alimentos": (205, 6_500),
                  "Tecnologia": (95, 23_500), "Electrohogar": (115, 18_500)}
    # Efectos aditivos y comunes a las categorías: el modelo lineal con mes categórico es la especificación correcta.
    estacion = np.array([-12, -18, 12, -8, -5, -10, -6, 0, 3, 6, 18, 48])
    filas = []
    for cat, (base, precio_ref) in categorias.items():
        for mes in range(1, 13):
            for _ in range(10):  # diez réplicas independientes por categoría y mes; no se identifica tienda ni año
                precio = precio_ref * rng.uniform(.75, 1.2)
                promo = rng.binomial(1, .35)
                mkt = rng.uniform(50_000, 900_000)
                media = (base + estacion[mes - 1] + 32 * promo - 9.0 * (precio - precio_ref) / 1000
                         + 4.5e-5 * mkt)
                ventas = max(12, round(media + rng.normal(0, 16)))
                filas.append((mes, cat, int(round(precio, -2)), promo, int(round(mkt, -3)), ventas))
    df = pd.DataFrame(filas, columns=["mes", "categoria_producto", "precio_promedio_clp",
                                      "promocion_activa", "inversion_marketing_clp", "ventas_unidades"])
    df = df.sample(frac=1, random_state=SEMILLA).reset_index(drop=True)
    # El notebook 03 controla la codificación con la primera fila: Vestuario en noviembre.
    i = df.index[(df.categoria_producto == "Vestuario") & (df.mes == 11)][0]
    df.iloc[[0, i]] = df.iloc[[i, 0]].to_numpy()
    df.insert(0, "registro_id", np.arange(1, len(df) + 1))
    return df


# --------------------------------------------------------------------------- PulpaLenga
OPTIMOS_PULPA = {"temperatura_coccion_c": 168.0, "presion_digestor_bar": 7.2,
                 "tiempo_coccion_min": 115.0, "concentracion_alcali_pct": 17.5}


def pulpalenga_calidad(rng):
    n = 950
    df = pd.DataFrame({
        "lote_id": np.arange(20_000, 20_000 + n),
        "temperatura_coccion_c": np.clip(rng.normal(168.5, 11, n), 140, 205).round(1),
        "presion_digestor_bar": np.clip(rng.normal(7.15, .95, n), 4.3, 9.9).round(2),
        "tiempo_coccion_min": np.clip(rng.normal(116, 15, n), 78, 165).round(0),
        "concentracion_alcali_pct": np.clip(rng.normal(17.7, 2.4, n), 11, 26.5).round(1),
        "humedad_madera_pct": np.clip(rng.normal(42, 7, n), 28, 64).round(1),
        "velocidad_linea_m_min": rng.uniform(530, 1100, n).round(0)})
    # Mecanismo en U: el riesgo crece al alejarse del punto óptimo de cada variable de proceso.
    latente = (.10 * (df.temperatura_coccion_c - 168).abs() + 1.15 * (df.presion_digestor_bar - 7.2).abs()
               + .04 * (df.tiempo_coccion_min - 115).abs() + .30 * (df.concentracion_alcali_pct - 17.5).abs()
               + .035 * (df.humedad_madera_pct - 42) + .0008 * (df.velocidad_linea_m_min - 800))
    df["defecto"] = _k_positivos(latente.to_numpy(), 155, rng)  # 16,3% de lotes defectuosos
    return df


def pulpalenga_energia(rng):
    n = 480
    ton = rng.uniform(180, 820, n).round(1)
    temp = np.clip(rng.normal(13, 7, n), -3, 31).round(1)
    tipo = rng.choice(["Kraft", "Mecanico"], n, p=[.6, .4])
    antig = rng.integers(1, 31, n)
    consumo = (55 + .95 * ton + 85 * (tipo == "Mecanico") + 3.1 * antig + 2.4 * np.abs(temp - 16)
               + rng.normal(0, 34, n)).round(1)
    return pd.DataFrame({"lote_id": np.arange(1, n + 1), "toneladas_producidas": ton,
                         "temperatura_ambiente_c": temp, "tipo_proceso": tipo,
                         "antiguedad_equipo_anios": antig, "consumo_energetico_mwh": consumo})


# --------------------------------------------------------------------------- CasaPeumo
def casapeumo(rng):
    regiones = ["Norte", "Centro", "Sur"]
    n_cli = 180
    clientes = pd.DataFrame({
        "IdCliente": [f"C{i:04d}" for i in range(1, n_cli + 1)],
        "Segmento": rng.choice(["Familias", "Profesionales", "Hogar joven", "Clientes frecuentes"], n_cli),
        "Región": rng.choice(regiones, n_cli, p=[.25, .45, .3]),
        "FechaAlta": pd.to_datetime("2025-03-01") + pd.to_timedelta(rng.integers(0, 420, n_cli), "D"),
        "TipoCliente": rng.choice(["Persona", "Pyme"], n_cli, p=[.85, .15])})
    clientes.loc[rng.choice(n_cli, 8, replace=False), "Segmento"] = np.nan  # vacíos deliberados
    catalogo = [("Cocina", "Cafetera", 89), ("Cocina", "Licuadora", 64), ("Cocina", "Hervidor", 42),
                ("Cocina", "Tostador", 48), ("Climatización", "Ventilador de pie", 79),
                ("Climatización", "Estufa eléctrica", 129), ("Climatización", "Purificador de aire", 249),
                ("Limpieza", "Aspiradora vertical", 199), ("Limpieza", "Vaporizador", 119),
                ("Limpieza", "Robot limpiador", 329), ("Organización", "Set de cajas", 45),
                ("Organización", "Repisa modular", 95), ("Organización", "Organizador de clóset", 139)]
    productos = pd.DataFrame(catalogo, columns=["Categoría", "Producto", "PrecioLista"])
    productos.insert(0, "IdProducto", [f"P{i:03d}" for i in range(1, len(productos) + 1)])
    productos["CostoUnitario"] = (productos.PrecioLista * rng.uniform(.6, .74, len(productos))).round(2)
    productos = productos[["IdProducto", "Categoría", "Producto", "PrecioLista", "CostoUnitario"]]

    n_v = 675
    fechas = pd.to_datetime("2026-01-01") + pd.to_timedelta(rng.integers(0, 181, n_v), "D")
    cli = rng.choice(clientes.IdCliente, n_v)
    prod = rng.choice(productos.IdProducto, n_v)
    p = productos.set_index("IdProducto")
    canal = rng.choice(["Sitio web", "Tienda física", "Marketplace"], n_v, p=[.42, .38, .2])
    sucio = rng.choice(n_v, 30, replace=False)  # variantes de escritura que deben normalizarse
    variantes = {"Sitio web": ["sitio web", " Sitio web"], "Tienda física": ["tienda física", "Tienda física "],
                 "Marketplace": ["marketplace", "MARKETPLACE"]}
    canal = canal.astype(object)
    for i in sucio:
        canal[i] = rng.choice(variantes[canal[i]])
    region_cli = clientes.set_index("IdCliente").Región
    ventas = pd.DataFrame({
        "IdVenta": [f"V{i:05d}" for i in range(1, n_v + 1)], "Fecha": fechas, "IdCliente": cli,
        "IdProducto": prod, "Canal": canal, "Región": region_cli.loc[cli].to_numpy(),
        "Unidades": rng.choice([1, 2, 3], n_v, p=[.76, .19, .05]),
        "PrecioLista": p.loc[prod, "PrecioLista"].to_numpy(),
        "DescuentoPct": np.where(rng.random(n_v) < .55, 0, rng.uniform(.05, .2, n_v)).round(4),
        "CostoUnitario": p.loc[prod, "CostoUnitario"].to_numpy(),
        "TiempoEntregaDias": np.clip(rng.poisson(1.5, n_v), 0, 7),
        "CampañaOrigen": rng.choice(["Orgánico", "Google Search", "Meta Ads", "Email"], n_v, p=[.4, .25, .2, .15])})
    ventas.loc[ventas.Canal.str.strip().str.casefold() == "tienda física", "TiempoEntregaDias"] = 0
    ventas = ventas.sort_values(["Fecha", "IdVenta"], kind="stable").reset_index(drop=True)
    ventas["IdVenta"] = [f"V{i:05d}" for i in range(1, n_v + 1)]
    duplicados = ventas.iloc[rng.choice(n_v, 5, replace=False)]  # cinco duplicados exactos
    ventas = pd.concat([ventas, duplicados]).sort_values("IdVenta", kind="stable").reset_index(drop=True)

    con_reclamo = ventas.drop_duplicates().sample(39, random_state=SEMILLA)
    resuelto = rng.choice(["Sí", "No"], 39, p=[.85, .15])
    reclamos = pd.DataFrame({
        "IdReclamo": [f"R{i:04d}" for i in range(1, 40)], "IdVenta": con_reclamo.IdVenta.to_numpy(),
        "FechaReclamo": (con_reclamo.Fecha + pd.to_timedelta(rng.integers(1, 15, 39), "D")).to_numpy(),
        "Motivo": rng.choice(["Producto defectuoso", "Pedido incompleto", "Atraso en entrega", "Atención",
                              "Problema de pago"], 39),
        "Resuelto": resuelto,
        "DiasResolucion": np.where(resuelto == "Sí", rng.integers(1, 10, 39), np.nan),
        "Satisfaccion1a5": rng.integers(1, 5, 39)}).sort_values("IdReclamo").reset_index(drop=True)

    meses = pd.date_range("2026-01-01", periods=6, freq="MS")
    filas = []
    for m in meses:
        for camp, cpc in [("Google Search", .55), ("Meta Ads", .38), ("Email", .12)]:
            impresiones = int(rng.integers(50_000, 650_000))
            clics = int(impresiones * rng.uniform(.012, .04))
            filas.append((m, camp, round(clics * cpc * rng.uniform(.9, 1.1), 2), impresiones, clics,
                          int(clics * rng.uniform(.02, .05))))
    marketing = pd.DataFrame(filas, columns=["FechaMes", "Campaña", "Inversión", "Impresiones", "Clics",
                                             "ClientesAdquiridos"])
    metas = pd.DataFrame({"FechaMes": meses, "MetaVentas": [15_500, 15_000, 17_000, 16_500, 18_000, 19_500],
                          "MetaMargenPct": .30, "MaxReclamosPor1000": 40, "MaxTiempoEntregaDias": 2.0})
    dias = pd.date_range("2026-01-01", "2026-06-30", freq="D")
    calendario = pd.DataFrame({"Fecha": dias, "Año": dias.year, "NumeroMes": dias.month,
                               "Mes": [MESES[m - 1] for m in dias.month],
                               "Trimestre": ["T1" if m <= 3 else "T2" for m in dias.month],
                               "AñoMes": dias.strftime("%Y-%m")})
    leeme = pd.DataFrame({
        "Campo": ["Propósito", "Periodo", "Empresa", "Problema", "Grano de Ventas", "Calidad",
                  "Moneda", "Origen", "Licencia"],
        "Descripción": [
            "Construir un modelo de datos y un tablero de seguimiento comercial.",
            "Enero a junio de 2026.",
            "CasaPeumo, comercializadora ficticia de artículos para el hogar.",
            "Las ventas crecen, pero la dirección duda del margen, los reclamos y la entrega.",
            "Una fila por venta; IdVenta debería ser único.",
            "Incluye duplicados exactos, variantes de escritura en Canal y segmentos vacíos a propósito.",
            "Unidades monetarias (UM) ficticias.",
            "Datos simulados con generar_datos.py de esta colección.",
            "CC BY-NC-SA 4.0."]})
    return {"LEEME": leeme, "Clientes": clientes, "Productos": productos, "Ventas": ventas,
            "Reclamos": reclamos, "Marketing": marketing, "Metas": metas, "Calendario": calendario}


# --------------------------------------------------------------------------- BoldoNet
def boldonet(rng):
    n = 240
    corte = pd.Timestamp("2026-08-05")
    ingreso = corte - pd.to_timedelta(rng.integers(5, 185, n), "D")
    programa = rng.choice(["Sí", "No"], n, p=[.45, .55])
    llamada = rng.choice(["Sí", "No"], n, p=[.6, .4])
    contenido = rng.choice(["Sí", "No"], n, p=[.5, .5])
    sesion = rng.choice(["Sí", "No"], n, p=[.35, .65])
    edad = (corte - ingreso).days
    maduro = edad >= 90
    p_abandono = .34 - .10 * (programa == "Sí") - .05 * (llamada == "Sí")
    estado = np.where(rng.random(n) < p_abandono, "Abandono", "Activo").astype(object)
    estado[~maduro] = np.where(rng.random((~maduro).sum()) < .85, None, "Activo")  # cohortes inmaduras
    estado[np.flatnonzero(maduro)[rng.choice(maduro.sum(), 6, replace=False)]] = "Pendiente"
    dias = np.where(estado == "Abandono", rng.integers(10, 90, n), np.minimum(edad, 183))
    costo = np.where(programa == "Sí", rng.integers(12, 49, n) * 1000, rng.integers(0, 4, n) * 1000)
    df = pd.DataFrame({
        "ID_cliente": [f"CLI-{i:04d}" for i in range(1, n + 1)],
        "Fecha_ingreso": pd.Series(ingreso).astype(object),
        "Segmento": rng.choice(["Básico", "Estándar", "Premium"], n, p=[.45, .4, .15]).astype(object),
        "Región": rng.choice(["Metropolitana", "Valparaíso", "Maule", "Biobío", "La Araucanía", "Los Lagos",
                              "Coquimbo", "O'Higgins"], n).astype(object),
        "Canal_ingreso": rng.choice(["Web", "App", "Tienda", "Ejecutivo", "Referido", "Campaña"], n).astype(object),
        "Programa_acompañamiento": programa.astype(object), "Llamada_bienvenida": llamada.astype(object),
        "Contenido_personalizado": contenido.astype(object), "Sesión_orientación": sesion.astype(object),
        "Estado_90_días": estado, "Días_permanencia": dias, "Costo_acompañamiento": costo,
        "Satisfacción": rng.integers(1, 6, n).astype(float),
        "Fecha_actualización": (corte - pd.to_timedelta(rng.integers(12, 36, n), "D")).to_numpy()})
    # Problemas de calidad deliberados, documentados en el diccionario:
    idx = rng.choice(n, 40, replace=False)
    df.loc[idx[:5], "Segmento"] = ["basico", "BÁSICO", "premium", "estandar", "Estandar"][:5]
    df.loc[idx[5:9], "Programa_acompañamiento"] = ["SI", "SI", "SI", "SI"]
    df.loc[idx[9:11], "Llamada_bienvenida"] = ["si", "NO"]
    df.loc[idx[11:13], "Contenido_personalizado"] = ["SÍ", "no"]
    df.loc[idx[13:15], "Sesión_orientación"] = ["N", "S"]
    df.loc[idx[15:18], "Fecha_ingreso"] = [df.loc[i, "Fecha_ingreso"].strftime("%d/%m/%Y")
                                           for i in idx[15:18]]  # texto con formato día/mes
    df.loc[idx[18], "Fecha_ingreso"] = "sin dato"
    df.loc[idx[19:21], "Días_permanencia"] = [-12, -3]
    df.loc[idx[21:23], "Costo_acompañamiento"] = [-4500, -1200]
    df.loc[idx[23:27], "Satisfacción"] = [0, 7, 6, 0]
    df.loc[idx[27:33], "Satisfacción"] = np.nan
    df.loc[idx[33], "Región"] = np.nan
    df.loc[idx[34], "Canal_ingreso"] = np.nan
    df.loc[idx[35], "Fecha_actualización"] = pd.NaT
    # Seis versiones anteriores de clientes existentes, con fecha de actualización distinta.
    versiones = df.iloc[idx[36:40].tolist() + idx[0:2].tolist()].copy()
    versiones["Fecha_actualización"] = pd.to_datetime(versiones["Fecha_actualización"]).fillna(
        corte - pd.Timedelta(days=40)) - pd.Timedelta(days=7)
    versiones["Estado_90_días"] = None
    base = pd.concat([df, versiones]).sort_values("ID_cliente", kind="stable").reset_index(drop=True)
    base["Fecha_actualización"] = pd.to_datetime(base["Fecha_actualización"])
    diccionario = pd.DataFrame({
        "Campo": list(base.columns),
        "Descripción": ["Código único del cliente", "Fecha de contratación", "Plan contratado", "Región de residencia",
                        "Canal por el que ingresó", "Participa del programa de acompañamiento",
                        "Recibió llamada de bienvenida", "Recibió contenido personalizado",
                        "Asistió a sesión de orientación", "Estado a los 90 días del ingreso",
                        "Días como cliente hasta el corte o el abandono", "Costo del acompañamiento (UM)",
                        "Satisfacción declarada", "Fecha de la última actualización del registro"],
        "Tipo esperado": ["Texto", "Fecha", "Texto categórico", "Texto categórico", "Texto categórico",
                          "Sí/No", "Sí/No", "Sí/No", "Sí/No", "Texto categórico", "Número entero",
                          "Número entero", "Número entero", "Fecha"],
        "Valores o regla esperada": ["Un registro vigente por cliente", "Últimos seis meses antes del corte",
                                     "Básico; Estándar; Premium", "Regiones incluidas en el piloto",
                                     "Web; App; Tienda; Ejecutivo; Referido; Campaña", "Sí; No", "Sí; No", "Sí; No",
                                     "Sí; No", "Activo; Abandono (solo cohortes de 90 días o más)",
                                     "Entre 0 y 183", "Mayor o igual a cero", "Entre 1 y 5",
                                     "La más reciente prevalece"]})
    ficha = pd.DataFrame({"Campo": ["Caso", "Fecha de corte", "Periodo de ingresos", "Unidad de análisis", "Origen",
                                    "Licencia"],
                          "Valor": ["BoldoNet: seguimiento de clientes nuevos (empresa ficticia)", corte,
                                    "Últimos seis meses antes del corte", "Cliente nuevo",
                                    "Datos simulados con generar_datos.py de esta colección", "CC BY-NC-SA 4.0"]})
    return {"Base_original": base, "Diccionario": diccionario, "Ficha_dataset": ficha}


# --------------------------------------------------------------------------- Embudo digital
def embudo_digital(rng):
    segmentos = ["Web escritorio", "Web móvil Android", "Web móvil iOS", "App Android", "App iOS", "Tablet"]
    anterior = np.array([14_800, 12_600, 11_200, 9_400, 8_700, 4_300])
    actual = (anterior * rng.uniform(.96, 1.08, 6)).round(-2).astype(int)
    tasa_inicio = np.array([.085, .062, .071, .098, .104, .074])
    inicios = (actual * tasa_inicio).round().astype(int)
    conversion = np.array([.72, .55, .63, .78, .81, .66])
    compras = (inicios * conversion).round().astype(int)
    return pd.DataFrame({"Segmento": segmentos, "Sesiones_anterior": anterior, "Sesiones_actual": actual,
                         "Inicios_pago": inicios, "Compras": compras, "Abandonos_pago": inicios - compras,
                         "Satisfaccion": [.79, .68, .73, .81, .83, .7]})


def _xlsx_determinista(ruta):
    """Fija autor y fechas del libro y de su ZIP interno para que el archivo sea idéntico en cada ejecución."""
    import datetime as dt
    import zipfile
    from openpyxl import load_workbook
    libro = load_workbook(ruta)
    fecha = dt.datetime(2026, 10, 8)
    libro.properties.creator = libro.properties.lastModifiedBy = "Colección abierta de Business Analytics"
    libro.properties.created = libro.properties.modified = fecha
    libro.save(ruta)
    with zipfile.ZipFile(ruta) as z:
        partes = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    with zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) as z:
        for nombre, datos in partes:
            if nombre == "docProps/core.xml":  # openpyxl escribe la hora de guardado; se fija.
                datos = re.sub(rb"(<dcterms:(?:created|modified)[^>]*>)[^<]*", rb"\g<1>2026-10-08T00:00:00Z", datos)
            info = zipfile.ZipInfo(nombre, date_time=(2026, 10, 8, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, datos)


def main():
    rng = np.random.default_rng(SEMILLA)
    _csv(fincordillera_clientes(rng), "fincordillera", "fincordillera_clientes.csv")
    _csv(fincordillera_transacciones(rng), "fincordillera", "fincordillera_transacciones.csv")
    _csv(quillaymarket_ventas_detalle(rng), "quillaymarket", "quillaymarket_ventas_detalle.csv")
    _csv(quillaymarket_demanda_mensual(rng), "quillaymarket", "quillaymarket_demanda_mensual.csv")
    _csv(pulpalenga_calidad(rng), "pulpa_lenga", "pulpalenga_calidad_pulpa.csv")
    _csv(pulpalenga_energia(rng), "pulpa_lenga", "pulpalenga_consumo_energetico.csv")
    for caso, archivo, hojas in [("casapeumo", "casapeumo_laboratorio.xlsx", casapeumo(rng)),
                                 ("boldonet", "boldonet_kpis.xlsx", boldonet(rng)),
                                 ("embudo_digital", "embudo_digital.xlsx", {"Datos originales": embudo_digital(rng)})]:
        with pd.ExcelWriter(_destino(caso) / archivo, engine="openpyxl") as xl:
            for hoja, tabla in hojas.items():
                tabla.to_excel(xl, sheet_name=hoja, index=False)
        _xlsx_determinista(_destino(caso) / archivo)
    print("Datos generados en", DATOS)


if __name__ == "__main__":
    main()
