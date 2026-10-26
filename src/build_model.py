#!/usr/bin/env python3
"""Limpia el Superstore crudo y genera el modelo en estrella (CSV) para Power BI.

Uso:  python3 src/build_model.py
Entrada : data/raw/superstore.csv
Salida  : data/model/{dim_date,dim_customer,dim_product,dim_geography,fact_sales}.csv
          docs/cleaning_report.md  (qué se corrigió y por qué)
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data/raw/superstore.csv"
OUT = ROOT / "data/model"
OUT.mkdir(parents=True, exist_ok=True)
report = []

raw = pd.read_csv(RAW, dtype={"Postal Code": "string"})
report.append(f"- Filas en el archivo crudo: **{len(raw):,}**")

# 1) El CSV trae pegadas, debajo de los pedidos, las hojas "People" (responsable por región)
#    y "Returns" (pedidos devueltos). Se separan en tres tablas.
orders_mask = raw["Order Date"].notna()
returns_mask = (raw["Row ID"] == "Yes") & ~orders_mask
people_mask = raw["Order ID"].isin(["West", "East", "Central", "South"]) & ~orders_mask
returned_orders = set(raw.loc[returns_mask, "Order ID"])
people = raw.loc[people_mask, ["Row ID", "Order ID"]].rename(columns={"Row ID": "regional_manager", "Order ID": "region"})
df = raw[orders_mask].copy()
df["Row ID"] = df["Row ID"].astype(int)
report.append(f"- Hojas anexas separadas: **{int(returns_mask.sum())}** filas de devoluciones "
              f"({len(returned_orders)} pedidos distintos) y **{len(people)}** responsables regionales")
report.append(f"- Filas de pedidos: **{len(df):,}**")

# 2) Posibles duplicados: líneas idénticas salvo Row ID. Tienen Row ID distinto, así que no se
#    puede probar que sean un error (podría ser el mismo producto pedido dos veces): se informan y se conservan.
dups = int(df.duplicated(subset=[c for c in df.columns if c != "Row ID"]).sum())
report.append(f"- Líneas idénticas (salvo Row ID) detectadas y conservadas: **{dups}**")

# 3) Tipos y fechas
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%m/%d/%Y")
df["Ship Date"] = pd.to_datetime(df["Ship Date"], format="%m/%d/%Y")
bad_ship = int((df["Ship Date"] < df["Order Date"]).sum())
report.append(f"- Pedidos con envío anterior a la orden: **{bad_ship}**")

# 4) Código postal: texto de 5 dígitos; los faltantes (Burlington, Vermont) se completan
df["Postal Code"] = df["Postal Code"].str.replace(r"\.0$", "", regex=True).str.zfill(5)
missing_pc = df["Postal Code"].isna() | (df["Postal Code"] == "<NA>")
df["Postal Code"] = df["Postal Code"].fillna("05401")
report.append(f"- Códigos postales completados (Burlington, VT → 05401): **{int(missing_pc.sum())}**")

# 5) Productos con más de un nombre para el mismo Product ID -> nombre más frecuente
names = df.groupby("Product ID")["Product Name"].agg(lambda s: s.mode().iloc[0])
multi = int((df.groupby("Product ID")["Product Name"].nunique() > 1).sum())
df["Product Name"] = df["Product ID"].map(names)
report.append(f"- Product ID con más de un nombre (se usa el más frecuente): **{multi}**")

# --- Dimensiones -------------------------------------------------------------
dim_customer = (df[["Customer ID", "Customer Name", "Segment"]]
                .drop_duplicates("Customer ID").sort_values("Customer ID").reset_index(drop=True))
dim_customer.insert(0, "customer_key", dim_customer.index + 1)
dim_customer.columns = ["customer_key", "customer_id", "customer_name", "segment"]

dim_product = (df[["Product ID", "Product Name", "Category", "Sub-Category"]]
               .drop_duplicates("Product ID").sort_values("Product ID").reset_index(drop=True))
dim_product.insert(0, "product_key", dim_product.index + 1)
dim_product.columns = ["product_key", "product_id", "product_name", "category", "sub_category"]

geo_cols = ["Country", "Region", "State", "City", "Postal Code"]
dim_geo = df[geo_cols].drop_duplicates().sort_values(geo_cols).reset_index(drop=True)
dim_geo.insert(0, "geo_key", dim_geo.index + 1)
dim_geo.columns = ["geo_key", "country", "region", "state", "city", "postal_code"]
dim_geo = dim_geo.merge(people, on="region", how="left")
dim_geo["regional_manager"] = dim_geo["regional_manager"].fillna("Sin asignar")

dmin = pd.Timestamp(df["Order Date"].min().year, 1, 1)
dmax = pd.Timestamp(df["Ship Date"].max().year, 12, 31)
cal = pd.DataFrame({"date": pd.date_range(dmin, dmax)})
cal["date_key"] = cal["date"].dt.strftime("%Y%m%d").astype(int)
cal["year"] = cal["date"].dt.year
cal["quarter"] = cal["date"].dt.quarter
cal["quarter_label"] = "T" + cal["quarter"].astype(str)
cal["month"] = cal["date"].dt.month
cal["month_name"] = cal["date"].dt.strftime("%b")
cal["year_month"] = cal["date"].dt.strftime("%Y-%m")
cal["week_of_year"] = cal["date"].dt.isocalendar().week.astype(int)
cal["day_of_week"] = cal["date"].dt.dayofweek + 1
cal["day_name"] = cal["date"].dt.strftime("%a")
cal["is_weekend"] = cal["day_of_week"] >= 6
dim_date = cal[["date_key", "date", "year", "quarter", "quarter_label", "month", "month_name",
                "year_month", "week_of_year", "day_of_week", "day_name", "is_weekend"]]

# --- Hechos: una fila por línea de pedido -------------------------------------
f = (df.merge(dim_customer, left_on="Customer ID", right_on="customer_id")
       .merge(dim_product, left_on="Product ID", right_on="product_id")
       .merge(dim_geo.drop(columns="regional_manager"), left_on=geo_cols,
              right_on=["country", "region", "state", "city", "postal_code"]))
fact = pd.DataFrame({
    "order_line_id": f["Row ID"],
    "order_id": f["Order ID"],
    "order_date_key": f["Order Date"].dt.strftime("%Y%m%d").astype(int),
    "ship_date_key": f["Ship Date"].dt.strftime("%Y%m%d").astype(int),
    "customer_key": f["customer_key"],
    "product_key": f["product_key"],
    "geo_key": f["geo_key"],
    "ship_mode": f["Ship Mode"],
    "sales": f["Sales"].round(4),
    "quantity": f["Quantity"].astype(int),
    "discount": f["Discount"],
    "profit": f["Profit"].round(4),
    "ship_days": (f["Ship Date"] - f["Order Date"]).dt.days,
    "is_returned": f["Order ID"].isin(returned_orders),
}).sort_values("order_line_id").reset_index(drop=True)

assert len(fact) == len(df), "el join cambió el número de filas"
assert fact["order_line_id"].is_unique

for name, t in [("dim_date", dim_date), ("dim_customer", dim_customer), ("dim_product", dim_product),
                ("dim_geography", dim_geo), ("fact_sales", fact)]:
    t.to_csv(OUT / f"{name}.csv", index=False)

report += [
    "", "## Modelo resultante",
    f"- fact_sales: **{len(fact):,}** filas · dim_customer: **{len(dim_customer)}** · "
    f"dim_product: **{len(dim_product):,}** · dim_geography: **{len(dim_geo)}** · dim_date: **{len(dim_date):,}** días",
    "", "## Cifras de control (para validar las medidas DAX en Power BI)",
    f"- Ventas totales: **{fact.sales.sum():,.2f}**",
    f"- Utilidad total: **{fact.profit.sum():,.2f}**",
    f"- Margen: **{100*fact.profit.sum()/fact.sales.sum():.2f}%**",
    f"- Pedidos: **{fact.order_id.nunique():,}** · Clientes: **{fact.customer_key.nunique()}** · "
    f"Unidades: **{fact.quantity.sum():,}**",
    f"- Líneas con pérdida: **{int((fact.profit < 0).sum()):,}** "
    f"({100*(fact.profit < 0).mean():.1f}%)",
    f"- Pedidos devueltos: **{fact[fact.is_returned].order_id.nunique()}** "
    f"({100*fact[fact.is_returned].order_id.nunique()/fact.order_id.nunique():.1f}% de los pedidos)",
]
by_year = fact.merge(dim_date[["date_key", "year"]], left_on="order_date_key", right_on="date_key") \
              .groupby("year")[["sales", "profit"]].sum()
report += ["", "| Año | Ventas | Utilidad | Margen |", "|---|---:|---:|---:|"]
for y, r in by_year.iterrows():
    report.append(f"| {y} | {r.sales:,.2f} | {r.profit:,.2f} | {100*r.profit/r.sales:.2f}% |")
(ROOT / "docs").mkdir(exist_ok=True)
(ROOT / "docs/cleaning_report.md").write_text("# Reporte de limpieza\n\n" + "\n".join(report) + "\n", encoding="utf-8")
print("\n".join(report))
