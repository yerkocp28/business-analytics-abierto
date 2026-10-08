"""Incrusta en la guía FBA las ventas de QuillayMarket usadas por el simulador de filtros."""
from pathlib import Path
import json
import re

from fba_recursos import ventas

CURSO = Path(__file__).resolve().parents[1]
GUIA = CURSO / "guia_maestra_ba.html"


def main():
    df = ventas()
    filas = [{"Fecha": f.strftime("%Y-%m-%d"), "Region": r, "Producto": p, "Unidades": float(u), "Monto": float(m)}
             for f, r, p, u, m in df[["Fecha", "Region", "Producto", "Unidades", "Monto"]].itertuples(index=False)]
    texto = GUIA.read_text(encoding="utf-8")
    nuevo, n = re.subn(r"const FBA_VENTAS = \[.*?\];", lambda _: "const FBA_VENTAS = " + json.dumps(filas, ensure_ascii=False) + ";",
                       texto, count=1, flags=re.S)
    assert n == 1, "No se encontró la constante FBA_VENTAS en la guía"
    GUIA.write_text(nuevo, encoding="utf-8", newline="")
    print(f"Guía FBA: {len(filas)} ventas incrustadas")


if __name__ == "__main__":
    main()
