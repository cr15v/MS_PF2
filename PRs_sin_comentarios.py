import pandas as pd
import requests

# --- CONFIGURACIÓN ---
archivo = "C:/Users/CASA/Documents/cris/uni/6 semestre/metricas/MS_PF2/MS_PF2.xlsx"
columna_urls = "comments_url"   
token_github = "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"  

# --- CARGA DE DATOS ---
df = pd.read_excel(archivo, sheet_name="PRs")
urls = df[columna_urls]

# --- AUTENTICACIÓN ---
headers = {"Authorization": f"token {token_github}"}

# --- PROCESAMIENTO ---
sin_comentarios = 0
total_prs = len(urls)

for i, url in enumerate(urls):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        comentarios = response.json()
        
        if not comentarios:  # Lista vacía = sin comentarios
            sin_comentarios += 1
    except Exception as e:
        print(f"Error con la URL {url}: {e}")

# --- RESULTADO ---
if total_prs > 0:
    porcentaje = (sin_comentarios / total_prs) * 100
    print(f"\nPorcentaje de PRs sin comentarios: {porcentaje:.2f}%")
else:
    print("No hay PRs en el archivo.")
