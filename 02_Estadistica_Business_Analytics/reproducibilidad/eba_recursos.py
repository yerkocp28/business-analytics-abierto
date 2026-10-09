"""Cálculos compartidos de la edición EBA. Datos exclusivamente simulados."""
from pathlib import Path
import html
import numpy as np
import pandas as pd
from scipy import stats
import ipywidgets as widgets

CURSO=Path(__file__).resolve().parents[1]
RAIZ=CURSO.parent
DATOS=CURSO/'datos'
SEMILLA=20261008

def pedidos():
    df=pd.read_csv(DATOS/'comerciosur_pedidos.csv')
    assert len(df)==600 and df.id.is_unique and not df.isna().any().any()
    assert set(df.campana)=={'A','B','C'} and set(df.canal)=={'Web','Tienda'}
    return df

def poblacion():
    return pd.read_csv(DATOS/'comerciosur_marco.csv')

def serie():
    return pd.read_csv(DATOS/'comerciosur_mensual.csv',parse_dates=['mes']).set_index('mes').asfreq('MS').unidades

def ic_media(x,nivel=.95):
    x=np.asarray(x,dtype=float)
    if len(x)<2 or not np.isfinite(x).all() or not 0<nivel<1:raise ValueError('Muestra finita de al menos dos casos y nivel entre 0 y 1')
    media=x.mean();se=x.std(ddof=1)/np.sqrt(len(x));d=stats.t.ppf((1+nivel)/2,len(x)-1)*se
    return {'n':len(x),'media':media,'sd':x.std(ddof=1),'se':se,'li':media-d,'ls':media+d}

def wilson(k,n,nivel=.95):
    if n<=0 or not 0<=k<=n or not 0<nivel<1:raise ValueError('Conteos o confianza inválidos')
    z=stats.norm.ppf((1+nivel)/2);p=k/n;d=1+z*z/n
    centro=(p+z*z/(2*n))/d;radio=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return max(0,centro-radio),min(1,centro+radio)

def bayes(prevalencia=.02,sensibilidad=.9,especificidad=.95):
    if not all(0<=x<=1 for x in [prevalencia,sensibilidad,especificidad]):raise ValueError('Probabilidades fuera de [0,1]')
    tp=prevalencia*sensibilidad;fp=(1-prevalencia)*(1-especificidad)
    return {'positivos_verdaderos':tp,'falsos_positivos':fp,'posterior':tp/(tp+fp) if tp+fp else np.nan}

def tamano_muestra(error=.05,p=.5,nivel=.95,N=5000,respuesta=1):
    if not 0<error<1 or not 0<p<1 or not 0<nivel<1 or N<2 or not 0<respuesta<=1:raise ValueError('Parámetros inválidos')
    n0=stats.norm.ppf((1+nivel)/2)**2*p*(1-p)/error**2
    n=int(np.ceil(n0/(1+(n0-1)/N)))
    return {'completas':n,'invitaciones':int(np.ceil(n/respuesta)),'factible':int(np.ceil(n/respuesta))<=N}

def welch(a,b,nivel=.95):
    """Diferencia media(a)-media(b); grupos independientes."""
    a=np.asarray(a);b=np.asarray(b);r=stats.ttest_ind(a,b,equal_var=False)
    ci=r.confidence_interval(nivel)
    return {'diferencia':a.mean()-b.mean(),'t':float(r.statistic),'gl':float(r.df),'p':float(r.pvalue),'li':float(ci.low),'ls':float(ci.high)}

def holm(p):
    p=np.asarray(p,float)
    if p.ndim!=1 or not len(p) or not np.all((p>=0)&(p<=1)):raise ValueError('Vector de valores p inválido')
    orden=np.argsort(p);aj=np.minimum(1,np.maximum.accumulate(p[orden]*(len(p)-np.arange(len(p)))))
    out=np.empty_like(p);out[orden]=aj;return out

def anova(df):
    grupos=[g.tiempo_min.to_numpy() for _,g in df.groupby('campana')]
    f,p=stats.f_oneway(*grupos);fw,pw=stats.f_oneway(*grupos,equal_var=False)
    total=np.sum((df.tiempo_min-df.tiempo_min.mean())**2)
    entre=sum(len(g)*(g.mean()-df.tiempo_min.mean())**2 for g in grupos)
    return {'F':float(f),'p':float(p),'F_Welch':float(fw),'p_Welch':float(pw),'eta2':float(entre/total)}

def comparar_medias(df):
    from itertools import combinations
    rows=[]
    for a,b in combinations(['A','B','C'],2):rows.append({'contraste':b+' - '+a,**welch(df.loc[df.campana.eq(b),'tiempo_min'],df.loc[df.campana.eq(a),'tiempo_min'])})
    tabla=pd.DataFrame(rows);tabla['p_Holm']=holm(tabla.p);return tabla

def indicadores(df):
    return {'n':len(df),'ticket_medio':float(df.ticket_mil.mean()) if len(df) else None,
            'tiempo_medio':float(df.tiempo_min.mean()) if len(df) else None,
            'resueltos_pct':100*float(df.resuelto.mean()) if len(df) else None}

import sys
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))
from _transversal.evaluacion import pregunta as _pregunta

def pregunta(texto, incorrecta, correcta, explicacion, tercera):
    return _pregunta(texto, [incorrecta, correcta, tercera], 1, explicacion, mostrar=False)
