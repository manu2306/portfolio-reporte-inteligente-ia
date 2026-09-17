import pandas as pd

# Cargar las 4 tablas
orders = pd.read_csv("data/olist_orders_dataset.csv")
order_items = pd.read_csv("data/olist_order_items_dataset.csv")
products = pd.read_csv("data/olist_products_dataset.csv")
category_translation = pd.read_csv("data/product_category_name_translation.csv")

# Función para mostrar un resumen rápido de cada tabla
def resumen_tabla(nombre, df):
    print(f"\n===== {nombre} =====")
    print("Forma (filas, columnas):", df.shape)
    print("\nColumnas:")
    print(df.columns.tolist())
    print("\nPrimeras filas:")
    print(df.head())
    print("\nValores nulos por columna:")
    print(df.isnull().sum())

resumen_tabla("orders", orders)
resumen_tabla("order_items", order_items)
resumen_tabla("products", products)
resumen_tabla("category_translation", category_translation)

# Investigar: ¿qué status tienen los pedidos sin fecha de entrega?
pedidos_sin_entrega = orders[orders["order_delivered_customer_date"].isnull()]

print("\n===== Investigación: pedidos sin order_delivered_customer_date =====")
print("Cantidad de esos pedidos:", len(pedidos_sin_entrega))
print("\nDistribución de order_status en esos pedidos:")
print(pedidos_sin_entrega["order_status"].value_counts())