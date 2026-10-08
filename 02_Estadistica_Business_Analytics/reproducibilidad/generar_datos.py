"""Generador documentado de datos ficticios, sin datos personales ni servicios remotos."""
from pathlib import Path
import numpy as np
import pandas as pd
from eba_recursos import DATOS, SEMILLA

def main():
    DATOS.mkdir(exist_ok=True);rng=np.random.default_rng(SEMILLA);n=5000
    canal=rng.choice(['Web','Tienda'],n,p=[.65,.35]);campana=rng.choice(['A','B','C'],n)
    ticket=np.round(rng.lognormal(np.log(45),.4,n)+8*(canal=='Tienda'),2)
    tiempo=np.round(38+3*(canal=='Web')-4*(campana=='B')-7*(campana=='C')+rng.normal(0,7,n),2)
    resuelto=rng.binomial(1,.72+.06*(campana=='B')+.10*(campana=='C'),n)
    marco=pd.DataFrame({'id':np.arange(1,n+1),'canal':canal,'campana':campana,'ticket_mil':ticket,'tiempo_min':tiempo,'resuelto':resuelto})
    marco.to_csv(DATOS/'comerciosur_marco.csv',index=False)
    marco.sample(n=600,random_state=SEMILLA).sort_values('id').to_csv(DATOS/'comerciosur_pedidos.csv',index=False)
    t=np.arange(72);y=np.round(180+.6*t+18*np.sin(2*np.pi*t/12)+rng.normal(0,5,72),2)
    pd.DataFrame({'mes':pd.date_range('2020-01-01',periods=72,freq='MS'),'unidades':y}).to_csv(DATOS/'comerciosur_mensual.csv',index=False)
    antes=rng.normal(40,8,80);despues=antes-3+rng.normal(0,4,80)
    pd.DataFrame({'id':np.arange(1,81),'antes':antes.round(2),'despues':despues.round(2)}).to_csv(DATOS/'comerciosur_pareado.csv',index=False)
    print('Cuatro conjuntos simulados generados con semilla',SEMILLA)

if __name__=='__main__':main()
