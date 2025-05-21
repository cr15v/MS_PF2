import pandas as pd
import requests

# --- CONFIGURACIÓN INICIAL ---
archivo = "C:/Users/CASA/Documents/cris/uni/6 semestre/metricas/MS_PF2/MS_PF2.xlsx"
hoja = "PRs"
columna_url = "review_comments_url"
token = "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"

# Encabezados para autenticación
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github+json"
}

# Leer la hoja específica del Excel
df = pd.read_excel(archivo, sheet_name=hoja)

# Validación de la columna
if columna_url not in df.columns:
    raise Exception(f"La columna '{columna_url}' no se encuentra en la hoja '{hoja}'.")

# Lista para almacenar número de revisores únicos
revisores_por_pr = []

# Revisión PR por PR
for url in df[columna_url]:
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        usuarios = {c["user"]["login"] for c in data if c.get("user")}
        revisores_por_pr.append(len(usuarios))
    
    except Exception as e:
        print(f"Error al procesar {url}: {e}")
        revisores_por_pr.append(None)

# Agregar la nueva columna al DataFrame
df["n_revisores_aprox"] = revisores_por_pr

# Guardar el resultado
df.to_excel("resultado_con_revisores.xlsx", index=False)

print("Archivo generado: resultado_con_revisores.xlsx")