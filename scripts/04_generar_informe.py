import json
import os
from dotenv import load_dotenv
from groq import Groq

# 1. Cargar la API key desde el archivo .env
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# 2. Cargar las métricas que ya calculamos
with open("data/metricas_resumen.json", "r", encoding="utf-8") as f:
    metricas = json.load(f)

# 3. Armar el prompt: la instrucción + los datos, en un solo texto
prompt = f"""### ROL
Sos un analista de logística senior en una empresa de e-commerce, especializado
en traducir datos operativos en informes ejecutivos claros, directos y accionables
para la gerencia.

### CONTEXTO
La gerencia necesita entender rápidamente el estado de los atrasos en la entrega
de pedidos para tomar decisiones. A continuación se te proporcionarán los datos
de atrasos por categoría de producto (porcentajes de atraso, volúmenes, u otras
métricas relevantes):

{json.dumps(metricas, indent=2, ensure_ascii=False)}

### TAREA
Con base ÚNICAMENTE en los datos anteriores, escribí un resumen ejecutivo que cubra:
1. Panorama general del nivel de atraso (visión agregada de la empresa).
2. Las categorías de producto más problemáticas, citando sus porcentajes exactos
   tal como aparecen en los datos.
3. Las categorías con mejor desempeño, citando sus porcentajes exactos.
4. Una recomendación concreta y cualitativa para la empresa (ej. "priorizar
   recursos en la categoría X"), sin prometer porcentajes de mejora, plazos ni
   metas que no estén respaldados por los datos.

### FORMATO
- Máximo 200 palabras.
- Prosa ejecutiva (sin bullets salvo que ayuden a la claridad), tono directo y
  profesional.
- Cada cifra mencionada debe corresponder textualmente a un valor presente en
  los datos de entrada.

### REGLAS (restricciones anti-alucinación)
- Usá ÚNICAMENTE los números provistos. Prohibido inventar, estimar, redondear
  de forma engañosa o inferir cifras, porcentajes de mejora, objetivos o plazos
  que no estén explícitamente en los datos.
- Si un dato necesario para alguno de los 4 puntos no está presente, decilo
  explícitamente en lugar de completarlo con una suposición (ej. "no se
  proporcionan datos de tendencia histórica").
- Las recomendaciones deben ser cualitativas y accionables, nunca cuantitativas,
  a menos que la meta cuantitativa ya esté en los datos.
- No uses adjetivos exagerados ("crítico", "alarmante") a menos que estén
  justificados directamente por la magnitud de los números dados.
- Antes de entregar la respuesta final, revisá internamente que cada cifra
  citada exista tal cual en los datos de entrada.

### EJEMPLOS
Mal (alucina una meta): "Se recomienda reducir los atrasos en Electrónica en
un 15% durante el próximo trimestre."

Bien (cualitativo, sin inventar cifras): "Se recomienda priorizar recursos
logísticos en la categoría Electrónica, dado que concentra el mayor porcentaje
de atraso (32%) según los datos actuales."
"""
# 4. Conectarse a Groq y pedirle la respuesta
client = Groq(api_key=api_key)

respuesta = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role": "user", "content": prompt}
    ],
)

informe = respuesta.choices[0].message.content

# 5. Mostrar el informe generado
print(informe)

# 6. Guardarlo en un archivo
with open("data/informe_ejecutivo.md", "w", encoding="utf-8") as f:
    f.write(informe)

print("\n✅ Informe guardado en data/informe_ejecutivo.md")