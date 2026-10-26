# Valores esperados para validar las medidas DAX

Valores de control calculados de forma independiente con pandas (`src/expected_values.py`). Las medidas DAX del reporte entregan estas mismas cifras con los filtros indicados.

| # | Filtro | Medida | Valor esperado |
|---|---|---|---:|
| 1 | Sin filtros | Ventas | 2,297,200.86 |
| 2 | Sin filtros | Utilidad | 286,397.02 |
| 3 | Sin filtros | Margen % | 12.47% |
| 4 | Sin filtros | Pedidos | 5,009 |
| 5 | Año 2018 | Ventas | 733,215.26 |
| 6 | Año 2018 | Utilidad | 93,439.27 |
| 7 | Año 2018 | Margen % | 12.74% |
| 8 | Año 2018 | Pedidos | 1,687 |
| 9 | Año 2018 · Technology · West | Ventas | 95,959.15 |
| 10 | Año 2018 · Technology · West | Utilidad | 18,983.80 |
| 11 | Año 2018 · Technology · West | Margen % | 19.78% |
| 12 | Año 2018 · Technology · West | Pedidos | 177 |
| 13 | Sin filtros | Clientes | 793 |
| 14 | Sin filtros | Unidades | 37,873 |
| 15 | Sin filtros | Ticket Promedio | 458.61 |
| 16 | Sin filtros | Líneas con Pérdida | 1,871 |
| 17 | Sin filtros | % Líneas con Pérdida | 18.72% |
| 18 | Sin filtros | Pérdida Total | -156,131.29 |
| 19 | Sin filtros | Utilidad con Descuento Alto (>20%) | -135,376.06 |
| 20 | Sin filtros | Margen Sin Descuento % | 29.51% |
| 21 | Sin filtros | Pedidos Devueltos | 296 |
| 22 | Sin filtros | Tasa de Devolución % | 5.91% |
| 23 | Sin filtros | Días de Envío Promedio | 3.96 |
| 24 | Año 2016 | Var Ventas YoY % | -2.83% |
| 25 | Año 2017 | Var Ventas YoY % | 29.47% |
| 26 | Año 2018 | Var Ventas YoY % | 20.36% |
| 27 | Sin filtros | Participación Top 10 Clientes | 6.70% |
| 28 | Año 2018 | Clientes Nuevos | 11 |
