# Superstore · Dashboard de Ventas y Rentabilidad en Power BI

Proyecto de inteligencia de negocios: datos crudos de retail → modelo en **estrella** limpio → **medidas DAX** → reporte de 4 páginas en Power BI centrado en *dónde el negocio gana y dónde pierde dinero*.

🇬🇧 English version: [README.md](README.md)

> **Estado:** terminado. El reporte (`powerbi/Superstore-dashboard.pbix`) tiene 5 páginas; las medidas clave se validaron contra valores calculados de forma independiente con pandas ([docs/expected_values.md](docs/expected_values.md)).

## Preguntas de negocio
1. ¿Cómo evolucionan las ventas y la utilidad año a año?
2. ¿Qué categorías, subcategorías, regiones y estados destruyen margen?
3. ¿Cuál es el costo real de los descuentos?
4. ¿Cómo son los clientes (nuevos vs. recurrentes, concentración del top 10)?
5. ¿Cómo se comportan los modos de envío y las devoluciones?

## Qué dicen los datos
(Cifras calculadas sobre los datos limpios, 2015–2018, 9.994 líneas, 5.009 pedidos, 793 clientes.)

- Ventas **US$2,30 M**, utilidad **US$286 K**, margen **12,5%**. Ventas +29,5% en 2017 y +20,4% en 2018.
- **Los descuentos explican las pérdidas**: sin descuento el margen es 29,5%; entre 20% y 40% baja a −15% y sobre 40% llega a −77%. Las líneas con más de 20% de descuento pierden **US$135 K** en total.
- **Muebles es el punto débil**: margen 2,5% vs. ~17% en Tecnología y Suministros de oficina. *Tables* (−8,6%), *Bookcases* (−3,0%) y *Supplies* (−2,6%) pierden dinero.
- **Geografía**: la región Central tiene 7,9% de margen vs. 14,9% en West; Texas (−US$25,7 K) y Pensilvania (−US$15,6 K) son estados con pérdida.
- 18,7% de las líneas son con pérdida y 5,9% de los pedidos fueron devueltos.

## Estructura del repositorio
```
data/raw/               CSV original (dataset de ejemplo Superstore)
data/model/             modelo en estrella limpio (5 CSV)
src/build_model.py      limpieza + modelado (pandas)
src/expected_values.py  valores esperados para validar el DAX
powerbi/                Superstore-dashboard.pbix · measures.dax
docs/                   modelo de datos, páginas del reporte, reporte de limpieza, valores de validación
screenshots/            páginas del reporte (PNG)
```

## Vista del reporte

**1 · Resumen ejecutivo** — KPIs con variación anual, ventas mensuales vs. año anterior con media móvil de 3 meses, ventas por categoría y mapa por estado.
![Resumen ejecutivo](screenshots/01_resumen_ejecutivo.png)

**2 · Rentabilidad** — margen vs. ventas por subcategoría, cascada de utilidad, margen por tramo de descuento y matriz subcategoría × región con formato condicional.
![Rentabilidad](screenshots/02_rentabilidad.png)

**3 · Clientes** — clientes nuevos vs. recurrentes, tasa de recompra, concentración del top 10 y principales clientes.
![Clientes](screenshots/03_clientes.png)

**4 · Logística y devoluciones** — días de envío por modo, tasa de devolución por categoría y por responsable regional (West concentra las devoluciones: 11,7% vs. ~3% en el resto).
![Logística y devoluciones](screenshots/04_logistica_y_devoluciones.png)

**5 · Descuentos y pérdidas** — utilidad por tramo de descuento, evolución anual, los 10 estados con pérdidas y las subcategorías con menor utilidad.
![Descuentos y pérdidas](screenshots/05_descuentos_y_perdidas.png)

## Cómo explorarlo
- **Ver el reporte:** abre `powerbi/Superstore-dashboard.pbix` en Power BI Desktop, o mira las capturas de arriba. La descripción página por página está en [docs/report_pages.md](docs/report_pages.md).
- **Modelo de datos y limpieza:** [docs/data_model.md](docs/data_model.md) (esquema en estrella y relaciones) y [docs/cleaning_report.md](docs/cleaning_report.md) (qué se corrigió y por qué).
- **DAX:** todas las medidas están documentadas en [powerbi/measures.dax](powerbi/measures.dax).
- **Validación:** [docs/expected_values.md](docs/expected_values.md) lista valores de control calculados de forma independiente con pandas.
- **Regenerar el modelo de datos:** `python3 src/build_model.py` (requiere pandas). Si el `.pbix` pide la ubicación de los datos, apúntalo a `data/model`.

## Habilidades demostradas
Limpieza y modelado de datos (Python/pandas) · modelado dimensional · DAX (inteligencia de tiempo, `USERELATIONSHIP`, `RANKX`, `TOPN`, títulos dinámicos, formato condicional) · Power Query (M) · diseño de dashboards y storytelling · validación de datos.

## Dataset
Sample Superstore (minorista ficticio de EE.UU., 2015–2018), dataset de ejemplo público popularizado por Tableau. Copia usada: [leonism/sample-superstore](https://github.com/leonism/sample-superstore).
