import pandas as pd
import requests
import time

# === CONFIGURA TU TOKEN AQUÍ ===
TOKEN = "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"
HEADERS = {"Authorization": f"token {TOKEN}"}

# === CARGAR ARCHIVO DE EXCEL ===
df = pd.read_excel("C:/Users/CASA/Documents/cris/uni/6 semestre/metricas/MS_PF2/issues_all4.xlsx")  # cambia el nombre si es necesario

# Verificamos que contenga el campo 'events_url'
if 'events_url' not in df.columns:
    raise ValueError("El archivo no contiene una columna llamada 'events_url'.")

# Columnas que agregaremos
df['reabierto'] = False
df['estado_actual'] = ""

for i, row in df.iterrows():
    url = row['events_url']
    try:
        r = requests.get(url, headers=HEADERS)
        events = r.json()
        
        # Verificar si hay evento 'reopened'
        reopened = any(event.get("event") == "reopened" for event in events)
        df.at[i, 'reabierto'] = reopened

        # Obtener estado actual del issue
        issue_url = "/".join(url.split("/")[:-1])  # elimina /events al final
        issue = requests.get(issue_url, headers=HEADERS).json()
        df.at[i, 'estado_actual'] = issue.get("state", "desconocido")

        time.sleep(0.5)  # para no sobrepasar el rate limit

    except Exception as e:
        print(f"Error en fila {i}: {e}")
        df.at[i, 'reabierto'] = "error"
        df.at[i, 'estado_actual'] = "error"

# === GUARDAR RESULTADOS ===
df.to_excel("issues_con_reabiertos.xlsx", index=False)
print("Listo: Se guardó como 'issues_con_reabiertos.xlsx'")
