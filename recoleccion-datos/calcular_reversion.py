import requests

# TOKEN PERSONAL (opcional para evitar límites)
headers = {
    "Accept": "application/vnd.github.v3+json",
    # "Authorization": "token TU_TOKEN_AQUI"  # Pon tu token aquí si tienes uno
}

repo = "facebook/react"
per_page = 100
page = 1
total_commits = 0
revert_commits = 0

while True:
    url = f"https://api.github.com/repos/{repo}/commits"
    params = {
        "per_page": per_page,
        "page": page
    }
    
    response = requests.get(url, headers=headers, params=params)
    commits = response.json()
    
    if not commits or "message" in commits:
        break
    
    print(f"Página {page} - Commits obtenidos: {len(commits)}")
    
    for commit in commits:
        total_commits += 1
        message = commit["commit"]["message"].lower()
        if "revert" in message:
            revert_commits += 1
    
    page += 1

if total_commits > 0:
    frequency = (revert_commits / total_commits) * 100
    print(f"Total commits: {total_commits}")
    print(f"Commits revertidos: {revert_commits}")
    print(f"Frecuencia de reversión: {frequency:.4f}%")
else:
    print("No se encontraron commits.")
