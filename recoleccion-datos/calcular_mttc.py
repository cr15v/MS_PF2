import requests
import pandas as pd
from datetime import datetime

# TOKEN PERSONAL (opcional, para evitar límites)
headers = {
    "Accept": "application/vnd.github.v3+json",
    # "Authorization": "token TU_TOKEN_AQUI"  # Descomenta y coloca tu token aquí si tienes uno
}

repo = "facebook/react"
per_page = 100
page = 1
all_issues = []

while True:
    url = f"https://api.github.com/search/issues"
    query = f'repo:{repo} label:"Type: Bug" state:closed'
    params = {
        "q": query,
        "per_page": per_page,
        "page": page
    }
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    if "items" not in data or len(data["items"]) == 0:
        break
    
    print(f"Página {page} - Issues obtenidos: {len(data['items'])}")
    
    for issue in data["items"]:
        if "pull_request" in issue:  # Excluir PRs
            continue
        if issue["closed_at"]:
            created = datetime.strptime(issue["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            closed = datetime.strptime(issue["closed_at"], "%Y-%m-%dT%H:%M:%SZ")
            delta = (closed - created).days
            all_issues.append({
                "Issue #": issue["number"],
                "Título": issue["title"],
                "Días para resolver": delta
            })
    
    page += 1

df = pd.DataFrame(all_issues)
if not df.empty:
    mttc = df["Días para resolver"].mean()
    print(df)
    print(f"\nMTTC promedio: {mttc:.2f} días")
else:
    print("No se encontraron issues con la etiqueta 'bug'.")
