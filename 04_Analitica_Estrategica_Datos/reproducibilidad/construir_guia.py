"""Regenera la guía autónoma a partir de la plantilla y datos locales depurados."""
import json
import numpy as np
from aed_recursos import CURSO, SEMILLA, casapeumo, boldonet


def main():
    ventas,_,auditoria=casapeumo()
    agregado=ventas.groupby(['Canal','Región','Mes']).agg(n=('IdVenta','size'),ingreso=('Ingreso','sum'),margen=('Margen','sum'),reclamos=('Reclamo','sum')).reset_index()
    agregado=agregado.rename(columns={'Canal':'canal','Región':'region','Mes':'mes'})
    c,_=boldonet();m=c.loc[c.maduro];o=c.loc[c.elegible_kpi]
    datos={'ventas':agregado.to_dict('records'),'auditoria':auditoria,
           'cohorte':{'maduros':len(m),'observados':len(o),'activos':int(o['Estado_90_días'].eq('Activo').sum())},
           'normales':np.random.default_rng(SEMILLA).standard_normal((2000,2)).round(8).tolist()}
    plantilla=(CURSO/'material_propio/guia_maestra_aed.template.html').read_text(encoding='utf-8')
    assert plantilla.count('@@DATOS@@')==1
    salida=plantilla.replace('@@DATOS@@',json.dumps(datos,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'))
    (CURSO/'guia_maestra_aed.html').write_text(salida,encoding='utf-8')
    print('Guía construida: 675 ventas agregadas, 2000 pares normales, sin dependencias de red.')


if __name__=='__main__':main()
