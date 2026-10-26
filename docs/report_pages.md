# Páginas del reporte

El reporte (`powerbi/Superstore-dashboard.pbix`) tiene 5 páginas con un estilo común (fondo gris claro, azul `#2F6690` como color principal, celeste `#8FA8BA` como secundario, y coral `#E8735A` reservado para pérdidas y alertas). Las segmentaciones de año, región y categoría o segmento están disponibles en cada página.

## 1 · Resumen ejecutivo
**Pregunta:** ¿cómo va el negocio y de dónde vienen las ventas?
- Tarjetas: Ventas (con variación anual), Utilidad, Margen %, Pedidos y Ticket Promedio.
- Ventas mensuales frente al año anterior, con media móvil de 3 meses.
- Ventas por categoría y mapa de EE.UU. coloreado por margen.

**Hallazgo:** US$2,30 M en ventas y 12,5% de margen. Las ventas crecieron 29,5% en 2017 y 20,4% en 2018.

## 2 · Rentabilidad
**Pregunta:** ¿qué productos y regiones ganan o pierden dinero?
- Dispersión de subcategorías (margen vs. ventas) y cascada de aporte a la utilidad.
- Margen según el tramo de descuento aplicado.
- Matriz subcategoría × región con formato condicional (rojo: pérdida, ámbar: margen bajo, verde: sano).

**Hallazgo:** Muebles rinde 2,5% de margen frente a ~17% de Tecnología y Suministros. Tables (−8,6%), Bookcases (−3,0%) y Supplies (−2,6%) pierden dinero.

## 3 · Clientes
**Pregunta:** ¿quiénes compran y qué tan concentradas están las ventas?
- Clientes nuevos y recurrentes por mes, tasa de recompra, participación del top 10 y ticket promedio.
- Ventas por segmento y los 10 clientes con más ventas, con su margen.

**Hallazgo:** 595 de los 793 clientes (75%) hicieron su primera compra en 2015 y solo 11 en 2018: el crecimiento viene de la recompra. El top 10 concentra 6,7% de las ventas.

## 4 · Logística y devoluciones
**Pregunta:** ¿cómo se comportan los envíos y las devoluciones?
- Días de envío promedio (3,96), pedidos devueltos (296, 5,9% del total) y ventas devueltas.
- Días de envío por modo y tasa de devolución por categoría.
- Desempeño por responsable regional.

**Hallazgo:** la región West concentra las devoluciones: 11,7% frente a ~3% en las otras regiones.

## 5 · Descuentos y pérdidas
**Pregunta:** ¿cuánto cuesta realmente descontar?
- Utilidad por tramo de descuento y evolución anual de ventas y utilidad.
- Los 10 estados con más pérdidas y las subcategorías con menor utilidad.
- Tarjetas: pérdida total, utilidad con descuento alto, margen sin descuento, % de líneas con pérdida y descuento promedio.

**Hallazgo:** sin descuento el margen es 29,5%; entre 21% y 40% es −15% y sobre 40% llega a −77%. Las ventas con más de 20% de descuento pierden US$135 mil. Texas, Ohio, Pennsylvania e Illinois son los estados con más pérdida.
