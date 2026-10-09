"""Perfil observable de las 19 tablas analíticas; no infiere reglas de negocio."""
from pathlib import Path
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]


def main():
    filas = []
    fuentes = sorted((RAIZ / '_transversal/datos').glob('*/originales/*'))
    fuentes += sorted((RAIZ / '02_Estadistica_Business_Analytics/datos').glob('comerciosur_*.csv'))
    tablas = 0
    for archivo in fuentes:
        hojas = {'CSV': pd.read_csv(archivo)} if archivo.suffix == '.csv' else pd.read_excel(archivo, sheet_name=None)
        for hoja, df in hojas.items():
            if hoja in {'LEEME', 'Diccionario', 'Ficha_dataset'}:
                continue
            tablas += 1
            for campo, s in df.items():
                numero = pd.api.types.is_numeric_dtype(s)
                fecha = pd.api.types.is_datetime64_any_dtype(s)
                filas.append({'archivo': archivo.relative_to(RAIZ).as_posix(), 'hoja': hoja, 'campo': campo,
                              'filas': len(df), 'tipo_leido': str(s.dtype), 'faltantes': int(s.isna().sum()),
                              'valores_distintos': int(s.nunique()),
                              'min_observado': str(s.min()) if numero or fecha else '',
                              'max_observado': str(s.max()) if numero or fecha else '',
                              'categorias_observadas': ' | '.join(sorted(map(str, s.dropna().unique()))) if not numero and not fecha and s.nunique() <= 20 else ''})
    assert len(fuentes) == 13 and tablas == 19
    pd.DataFrame(filas).to_csv(Path(__file__).with_name('perfil_columnas.csv'), index=False, lineterminator='\n')
    print(f'{len(fuentes)} fuentes, {tablas} tablas analíticas, {len(filas)} columnas perfiladas.')


if __name__ == '__main__':
    main()
