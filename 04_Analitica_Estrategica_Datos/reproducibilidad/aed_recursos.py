"""Datos, casos numéricos y controles de la edición AED; sin descargas ni escritura de originales."""
from pathlib import Path
import html
import numpy as np
import pandas as pd
import ipywidgets as widgets
from IPython.display import display
from scipy.optimize import linprog

CURSO = Path(__file__).resolve().parents[1]
RAIZ = CURSO.parent
DATOS = RAIZ / '_transversal' / 'datos'
SEMILLA = 2026


def casapeumo():
    """Devuelve tablas originales y ventas depuradas con auditoría explícita."""
    archivo = DATOS/'casapeumo/originales/casapeumo_laboratorio.xlsx'
    tablas = pd.read_excel(archivo, sheet_name=None)
    base = tablas['Ventas']
    ventas = base.drop_duplicates().copy()
    if not ventas.IdVenta.is_unique:
        raise ValueError('Hay claves de venta conflictivas; no eliminar sin investigar')
    canales = {'sitio web': 'Sitio web', 'tienda física': 'Tienda física', 'marketplace': 'Marketplace'}
    normalizado = ventas.Canal.str.strip().str.casefold().map(canales)
    if normalizado.isna().any():
        raise ValueError('Canal fuera del diccionario')
    cambios = int((ventas.Canal != normalizado).sum())
    ventas['Canal'] = normalizado
    clientes = tablas['Clientes'].copy()
    clientes['Segmento'] = clientes.Segmento.fillna('Sin información')
    productos = tablas['Productos'][['IdProducto','Categoría','Producto']]
    ventas = ventas.merge(clientes[['IdCliente','Segmento','FechaAlta']], on='IdCliente', validate='many_to_one', indicator=True)
    assert (ventas['_merge'] == 'both').all()
    ventas = ventas.drop(columns='_merge').merge(productos, on='IdProducto', validate='many_to_one', indicator=True)
    assert (ventas['_merge'] == 'both').all()
    ventas = ventas.drop(columns='_merge')
    ventas['Fecha'] = pd.to_datetime(ventas.Fecha)
    ventas['Ingreso'] = ventas.Unidades * ventas.PrecioLista * (1-ventas.DescuentoPct)
    ventas['Costo'] = ventas.Unidades * ventas.CostoUnitario
    ventas['Margen'] = ventas.Ingreso - ventas.Costo
    ventas['Mes'] = ventas.Fecha.dt.strftime('%Y-%m')
    ventas['Reclamo'] = ventas.IdVenta.isin(tablas['Reclamos'].IdVenta)
    ventas['Alta_posterior'] = ventas.Fecha < pd.to_datetime(ventas.FechaAlta)
    assert ventas.Ingreso.gt(0).all() and ventas.DescuentoPct.between(0,1).all()
    auditoria = {'filas_originales': len(base), 'duplicados_exactos': len(base)-len(ventas),
                 'ventas_unicas':len(ventas), 'canales_normalizados':cambios,
                 'clientes_sin_segmento':int(tablas['Clientes'].Segmento.isna().sum()),
                 'ventas_anteriores_al_alta':int(ventas.Alta_posterior.sum())}
    return ventas, tablas, auditoria


def indicadores(frame):
    """Grano: una venta. Razones de totales, sin promediar porcentajes."""
    n = len(frame)
    ingreso, margen = float(frame.Ingreso.sum()), float(frame.Margen.sum())
    return {'ventas': n, 'ingreso': ingreso, 'margen': margen,
            'margen_pct': margen/ingreso if ingreso else np.nan,
            'ticket': ingreso/n if n else np.nan,
            'reclamos_por_1000': 1000*frame.Reclamo.sum()/n if n else np.nan,
            'entrega_media': float(frame.TiempoEntregaDias.mean()) if n else np.nan}


def boldonet():
    """Regla docente: deduplicar por actualización, marcar conflictos y no imputar estados."""
    base = pd.read_excel(DATOS/'boldonet/originales/boldonet_kpis.xlsx', sheet_name='Base_original')
    corte = pd.Timestamp('2026-08-05')  # Ficha_dataset, no fecha del equipo.
    df = base.drop_duplicates().copy()
    df['Fecha_actualización'] = pd.to_datetime(df['Fecha_actualización'], errors='coerce')
    # Una fecha conocida tiene prioridad sobre NaT; empate conflictivo exige revisión.
    conflictos = df[df.duplicated(['ID_cliente','Fecha_actualización'], keep=False)]
    if not conflictos.empty:
        raise ValueError('Versiones distintas con igual fecha de actualización')
    df = df.sort_values('Fecha_actualización',na_position='first',kind='stable').drop_duplicates('ID_cliente',keep='last').copy()
    df['Fecha_ingreso'] = pd.to_datetime(df['Fecha_ingreso'],errors='coerce',format='mixed',dayfirst=True)
    df['Programa_acompañamiento'] = df['Programa_acompañamiento'].replace({'SI':'Sí'})
    df['edad_cohorte'] = (corte-df['Fecha_ingreso']).dt.days
    df['maduro'] = df.edad_cohorte.ge(90)
    df['estado_valido'] = df['Estado_90_días'].isin(['Activo','Abandono'])
    df['elegible_kpi'] = df.maduro & df.estado_valido
    df['costo_valido'] = df.Costo_acompañamiento.ge(0)
    df['satisfaccion_valida'] = df.Satisfacción.between(1,5)
    auditoria = {'filas_originales':len(base),'clientes_unicos':len(df),
                 'versiones_retiradas':len(base)-len(df),
                 'fechas_ingreso_invalidas':int(df.Fecha_ingreso.isna().sum()),
                 'maduros_sin_estado_valido':int((df.maduro & ~df.estado_valido).sum()),
                 'no_maduros_con_estado':int((~df.maduro & df.estado_valido).sum()),
                 'costos_invalidos':int((~df.costo_valido).sum())}
    return df, auditoria


def plan_produccion(horas=100., material=90.):
    """Max 40 A + 30 B; 2A+B<=horas; A+2B<=material. Unidades divisibles."""
    if not np.isfinite([horas,material]).all() or min(horas,material)<0:
        raise ValueError('Capacidades finitas y no negativas')
    return linprog([-40.,-30.], A_ub=[[2.,1.],[1.,2.]], b_ub=[horas,material], bounds=[(0,None)]*2, method='highs')


PAGOS = np.array([[0.,0.],[-20.,80.],[15.,45.]])  # Miles de unidades monetarias, estado bajo/alto.
ALTERNATIVAS = ['No actuar','Expandir','Piloto']


def decision(prob_alta=.4):
    if not 0 <= prob_alta <= 1:
        raise ValueError('La probabilidad debe estar en [0,1]')
    prob = np.array([1-prob_alta,prob_alta])
    ev = PAGOS@prob
    con_info = PAGOS.max(axis=0)@prob
    return ev, float(con_info-ev.max())


def solar(n=10000, tasa=.10, escala_precio=1., rho=-.25, semilla=SEMILLA):
    """Caso SolarSur SIMULADO, VAN en miles de unidades monetarias (kUM).

    Un shock de precio y producción por escenario persiste cinco años.
    rho es correlación de los normales latentes, no de las variables lognormales.
    No incluye deuda, impuestos, inflación ni valor residual.
    """
    if int(n)!=n or n<2 or not np.isfinite([tasa,escala_precio,rho]).all() or tasa<0 or escala_precio<=0 or not -1<rho<1:
        raise ValueError('Parámetros fuera del dominio de la simulación')
    rng=np.random.default_rng(semilla)
    z=rng.standard_normal((int(n),2))
    z2=rho*z[:,0]+np.sqrt(1-rho*rho)*z[:,1]
    # Parametrización para E[Q]=1000 MWh y E[P]=100 UM/MWh.
    q=1000*np.exp(.12*z[:,0]-.12**2/2)
    p=100*escala_precio*np.exp(.20*z2-.20**2/2)
    costo=30.  # kUM/año, supuesto.
    flujos=(q*p/1000-costo)[:,None]*np.ones((int(n),5))
    factores=(1+tasa)**np.arange(1,6)
    van=-250+np.sum(flujos/factores,axis=1)
    return pd.DataFrame({'produccion':q,'precio':p,'VAN':van})


def resumen_solar(df):
    v=df.VAN.to_numpy(); n=len(v); prob=float(np.mean(v<0))
    return {'VAN_medio':float(v.mean()),'P_perdida':prob,
            'P05':float(np.quantile(v,.05)), 'P95':float(np.quantile(v,.95)),
            'SE_media':float(v.std(ddof=1)/np.sqrt(n)),
            'SE_probabilidad':float(np.sqrt(prob*(1-prob)/n))}


def pregunta(enunciado, opciones, correcta, explicacion):
    elegir=widgets.RadioButtons(options=opciones,value=None,layout={'width':'95%'})
    boton=widgets.Button(description='Comprobar',button_style='info')
    salida=widgets.HTML('<p role="status">Selecciona una respuesta.</p>')
    def revisar(_):
        mensaje='Selecciona una respuesta.' if elegir.value is None else ('Correcto. ' if elegir.value==opciones[correcta] else 'Revisa tu respuesta. ')+explicacion
        salida.value='<p role="status" aria-live="polite">'+html.escape(mensaje)+'</p>'
    boton.on_click(revisar)
    caja=widgets.VBox([widgets.HTML('<b>'+html.escape(enunciado)+'</b>'),elegir,boton,salida])
    display(caja)
    return caja
