# Reporte Inteligente: Pipeline de Datos + IA + Automatización

Pipeline automatizado que limpia y cruza datos de e-commerce, calcula métricas de atraso en las entregas, genera un informe ejecutivo con IA, lo grafica, y lo envía por email — todo orquestado con n8n, corriendo en local sin costo.

## Demo

[Ver el video de la demo](./Demo-video.mp4) — el workflow completo corriendo de punta a punta, desde el disparo manual hasta el mail con el informe y el gráfico.

## Pregunta guía

¿Cómo automatizar, de punta a punta, el análisis de atrasos en pedidos —desde los datos crudos hasta un informe ejecutivo en la bandeja de entrada— sin que alguien tenga que armarlo a mano cada vez?

## Dataset

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle) — dataset real y multi-tabla de un marketplace brasileño. Se usan 4 tablas: pedidos, ítems de pedido, productos y traducción de categorías.

## Estructura del proyecto
```
reporte-inteligente/
├── data/ # datos crudos y generados (no incluidos en el repo, ver "Cómo correrlo")
├── scripts/
│ ├── 01_exploracion.py
│ ├── 02_limpieza_union.py
│ ├── 03_metricas.py
│ └── 04_generar_informe.py
├── workflow.json # workflow de n8n exportado
├── requirements.txt
└── README.md
```

## Cómo correrlo

1. Cloná el repositorio y entrá a la carpeta del proyecto.
2. Creá y activá un entorno virtual:
python -m venv venv
venv\Scripts\Activate.ps1 # Windows
3. Instalá las dependencias:
pip install -r requirements.txt
4. Descargá el dataset desde [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) y colocá los archivos CSV dentro de `data/`.
5. Creá un archivo `.env` en la raíz con tu API key de [Groq](https://console.groq.com): `GROQ_API_KEY=tu_api_key`.
6. Corré `scripts/02_limpieza_union.py` y `scripts/03_metricas.py` para generar el dataset limpio y las métricas por período.
7. Levantá n8n con Docker Desktop (requiere WSL2 en Windows), montando la carpeta `data/` como volumen.
8. Importá `workflow.json` en n8n y configurá las credenciales: Header Auth para Groq, y SMTP para Gmail (con una contraseña de aplicación).
9. Ejecutá el workflow desde el Manual Trigger, eligiendo qué período procesar en el nodo "Edit Fields1".

## Metodología

1. **Limpieza de datos:** se descartan los pedidos sin fecha de entrega (no comparables), se completan las categorías de producto faltantes, y se cruzan las 4 tablas en un único dataset.
2. **Cálculo de métricas por período:** general y por trimestre, para poder generar reportes de distintos rangos de tiempo sin tocar el resto del pipeline.
3. **Generación del informe con IA:** un prompt estructurado (con reglas explícitas y ejemplos anti-alucinación) le pide a un LLM (Groq) que redacte el informe ejecutivo a partir de las métricas, sin inventar datos que no estén en el JSON de entrada.
4. **Generación del gráfico:** en paralelo, se arma la configuración de un gráfico de barras y se genera la imagen con QuickChart.io.
5. **Entrega:** el informe de texto y el gráfico se combinan y se envían por email.

## Resultado

Sobre el dataset completo, el 7.91% de las líneas de pedido llegan con atraso. Las categorías con mayor incidencia de atraso son minoritarias en volumen pero con porcentajes muy altos (algunas superan el 15-20%), mientras que categorías de alto volumen se mantienen con atrasos bajos y estables.

## Recomendación de negocio

Concentrar recursos logísticos y de gestión de inventario en las categorías con mayor porcentaje de atraso, revisando los flujos de picking, embalaje y transporte específicos de esas líneas — en vez de aplicar mejoras genéricas a todo el catálogo.

## Limitaciones

- El porcentaje de atraso se calcula sobre líneas de pedido, no sobre pedidos únicos.
- Las métricas son instantáneas generadas corriendo los scripts de Python a mano — no se actualizan solas ni leen datos en vivo.
- El trigger del workflow es manual, por decisión (para poder mostrarlo en la demo grabada).
- Corre sobre las capas gratuitas de Groq y QuickChart, con los límites de uso que eso implica.

## Autor
Manuel Corzo

## Autor

Manuel Corzo
