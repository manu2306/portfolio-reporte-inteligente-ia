import pandas as pd
import json

df = pd.read_csv("data/olist_unido_limpio.csv")
df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

def calcular_resumen(subset):
    total_lineas_pedido = len(subset)
    porcentaje_atraso_general = round(subset["atraso"].mean() * 100, 2)

    atraso_por_categoria = (
        subset.groupby("product_category_name_english")["atraso"]
        .agg(["mean", "count"])
        .rename(columns={"mean": "porcentaje_atraso", "count": "cantidad_pedidos"})
    )
    atraso_por_categoria["porcentaje_atraso"] = (atraso_por_categoria["porcentaje_atraso"] * 100).round(2)

    categorias_confiables = atraso_por_categoria[atraso_por_categoria["cantidad_pedidos"] >= 30]

    top5_categorias_atraso = (
        categorias_confiables.sort_values("porcentaje_atraso", ascending=False)
        .head(5)
        .to_dict(orient="index")
    )
    top5_categorias_a_tiempo = (
        categorias_confiables.sort_values("porcentaje_atraso", ascending=True)
        .head(5)
        .to_dict(orient="index")
    )

    return {
        "total_lineas_pedido": total_lineas_pedido,
        "porcentaje_atraso_general": porcentaje_atraso_general,
        "top5_categorias_con_mas_atraso": top5_categorias_atraso,
        "top5_categorias_con_menos_atraso": top5_categorias_a_tiempo,
    }

# 1. Resumen general (con TODOS los pedidos, como hasta ahora)
resumen_general = calcular_resumen(df)
with open("data/metricas_resumen_general.json", "w", encoding="utf-8") as f:
    json.dump(resumen_general, f, indent=2, ensure_ascii=False)
print("✅ Guardado: data/metricas_resumen_general.json")

# 2. Un resumen por trimestre, para los 4 trimestres con más pedidos
df["trimestre"] = df["order_purchase_timestamp"].dt.to_period("Q").astype(str)
trimestres_top4 = df["trimestre"].value_counts().head(4).index.tolist()

for trimestre in trimestres_top4:
    subset = df[df["trimestre"] == trimestre]
    resumen_trimestre = calcular_resumen(subset)
    nombre_archivo = f"data/metricas_resumen_{trimestre}.json"
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        json.dump(resumen_trimestre, f, indent=2, ensure_ascii=False)
    print(f"✅ Guardado: {nombre_archivo}")