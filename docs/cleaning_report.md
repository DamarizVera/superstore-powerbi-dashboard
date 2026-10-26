# Reporte de limpieza

- Filas en el archivo crudo: **10,800**
- Hojas anexas separadas: **800** filas de devoluciones (296 pedidos distintos) y **4** responsables regionales
- Filas de pedidos: **9,994**
- Líneas idénticas (salvo Row ID) detectadas y conservadas: **1**
- Pedidos con envío anterior a la orden: **0**
- Códigos postales completados (Burlington, VT → 05401): **11**
- Product ID con más de un nombre (se usa el más frecuente): **32**

## Modelo resultante
- fact_sales: **9,994** filas · dim_customer: **793** · dim_product: **1,862** · dim_geography: **632** · dim_date: **1,826** días

## Cifras de control (para validar las medidas DAX en Power BI)
- Ventas totales: **2,297,200.86**
- Utilidad total: **286,397.02**
- Margen: **12.47%**
- Pedidos: **5,009** · Clientes: **793** · Unidades: **37,873**
- Líneas con pérdida: **1,871** (18.7%)
- Pedidos devueltos: **296** (5.9% de los pedidos)

| Año | Ventas | Utilidad | Margen |
|---|---:|---:|---:|
| 2015 | 484,247.50 | 49,543.97 | 10.23% |
| 2016 | 470,532.51 | 61,618.60 | 13.10% |
| 2017 | 609,205.60 | 81,795.17 | 13.43% |
| 2018 | 733,215.26 | 93,439.27 | 12.74% |
