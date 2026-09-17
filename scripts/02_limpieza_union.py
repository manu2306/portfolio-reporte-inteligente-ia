import pandas as pd

# 1. Cargar las 4 tablas
orders = pd.read_csv("data/olist_orders_dataset.csv")
order_items = pd.read_csv("data/olist_order_items_dataset.csv")
products = pd.read_csv("data/olist_products_dataset.csv")
category_translation = pd.read_csv("data/product_category_name_translation.csv")

# 2. Limpiar 'orders': eliminar pedidos sin fecha de entrega real
orders_limpio = orders.dropna(subset=["order_delivered_customer_date"])

# 3. Convertir las columnas de fecha a tipo fecha real (no texto)
columnas_fecha = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]
for columna in columnas_fecha:
    orders_limpio[columna] = pd.to_datetime(orders_limpio[columna])

# 4. Limpiar 'products': rellenar categoría faltante
products_limpio = products.copy()
products_limpio["product_category_name"] = products_limpio["product_category_name"].fillna("sin_categoria")

# 5. Unir las 4 tablas en una sola
df = orders_limpio.merge(order_items, on="order_id", how="left")
df = df.merge(products_limpio, on="product_id", how="left")
df = df.merge(category_translation, on="product_category_name", how="left")

# 6. A los productos "sin_categoria", la traducción a inglés les queda vacía (no existen en esa tabla) -> completarla también
df["product_category_name_english"] = df["product_category_name_english"].fillna("sin_categoria")

# 7. Crear la columna clave: ¿el pedido llegó tarde?
df["atraso"] = df["order_delivered_customer_date"] > df["order_estimated_delivery_date"]

# 8. Revisar que quedó bien
print("Forma final del dataset unido:", df.shape)
print("\nValores nulos por columna:")
print(df.isnull().sum())
print("\nPorcentaje de pedidos con atraso:", round(df["atraso"].mean() * 100, 2), "%")

# 9. Guardar el resultado
df.to_csv("data/olist_unido_limpio.csv", index=False)
print("\n✅ Dataset unido y limpio guardado en data/olist_unido_limpio.csv")