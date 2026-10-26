#!/usr/bin/env python3
"""Calcula con pandas los valores esperados de las medidas DAX (para validar el reporte en Power BI)."""
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parent.parent
M = ROOT / "data/model"
d, f = pd.read_csv(M/"dim_date.csv"), pd.read_csv(M/"fact_sales.csv")
p, g = pd.read_csv(M/"dim_product.csv"), pd.read_csv(M/"dim_geography.csv")
x = (f.merge(d[["date_key", "year"]], left_on="order_date_key", right_on="date_key")
       .merge(p, on="product_key").merge(g, on="geo_key"))
out = ["# Valores esperados para validar las medidas DAX", "",
       "Compara estas cifras con tarjetas/tablas del reporte (con los filtros indicados). Generado por `src/expected_values.py`.", "",
       "| # | Filtro | Medida | Valor esperado |", "|---|---|---|---:|"]
n = 0
def row(flt, name, val):
    global n; n += 1; out.append(f"| {n} | {flt} | {name} | {val} |")
def block(flt, df):
    row(flt, "Ventas", f"{df.sales.sum():,.2f}")
    row(flt, "Utilidad", f"{df.profit.sum():,.2f}")
    row(flt, "Margen %", f"{100*df.profit.sum()/df.sales.sum():.2f}%")
    row(flt, "Pedidos", f"{df.order_id.nunique():,}")
block("Sin filtros", x)
block("Año 2018", x[x.year == 2018])
block("Año 2018 · Technology · West", x[(x.year == 2018) & (x.category == "Technology") & (x.region == "West")])
row("Sin filtros", "Clientes", f"{x.customer_key.nunique()}")
row("Sin filtros", "Unidades", f"{x.quantity.sum():,}")
row("Sin filtros", "Ticket Promedio", f"{x.sales.sum()/x.order_id.nunique():,.2f}")
row("Sin filtros", "Líneas con Pérdida", f"{int((x.profit<0).sum()):,}")
row("Sin filtros", "% Líneas con Pérdida", f"{100*(x.profit<0).mean():.2f}%")
row("Sin filtros", "Pérdida Total", f"{x[x.profit<0].profit.sum():,.2f}")
row("Sin filtros", "Utilidad con Descuento Alto (>20%)", f"{x[x.discount>0.2].profit.sum():,.2f}")
row("Sin filtros", "Margen Sin Descuento %", f"{100*x[x.discount==0].profit.sum()/x[x.discount==0].sales.sum():.2f}%")
row("Sin filtros", "Pedidos Devueltos", f"{x[x.is_returned].order_id.nunique()}")
row("Sin filtros", "Tasa de Devolución %", f"{100*x[x.is_returned].order_id.nunique()/x.order_id.nunique():.2f}%")
row("Sin filtros", "Días de Envío Promedio", f"{x.ship_days.mean():.2f}")
y = x.groupby("year").sales.sum()
for yr in (2016, 2017, 2018):
    row(f"Año {yr}", "Var Ventas YoY %", f"{100*(y[yr]/y[yr-1]-1):.2f}%")
t10 = x.groupby("customer_key").sales.sum().nlargest(10).sum()
row("Sin filtros", "Participación Top 10 Clientes", f"{100*t10/x.sales.sum():.2f}%")
first = x.merge(d[["date_key", "date"]], left_on="order_date_key", right_on="date_key", suffixes=("", "_d")) \
         .groupby("customer_key")["date"].min()
row("Año 2018", "Clientes Nuevos", f"{int((pd.to_datetime(first).dt.year == 2018).sum())}")
(ROOT / "docs/expected_values.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
