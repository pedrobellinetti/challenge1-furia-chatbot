import requests
from bs4 import BeautifulSoup

def buscar_noticias_furia():
    headers = {
        "User-Agent": "FuriaTelegramBot/1.0 (contato: seuemail@dominio.com)",
        "Accept": "application/json"
    }

    api_url = "https://liquipedia.net/counterstrike/api.php"
    params = {
        "action": "parse",
        "page": "FURIA",
        "format": "json"
    }

    response = requests.get(api_url, headers=headers, params=params)

    if response.status_code != 200:
        print("❌ Falha na requisição:", response.status_code)
        return []

    data = response.json()
    html = data['parse']['text']['*']
    soup = BeautifulSoup(html, 'html.parser')

    noticias = []

    # Coleta de <li> com palavras-chave
    for li in soup.find_all("li"):
        texto = li.get_text(strip=True)
        if "FURIA" in texto or "signed" in texto or "joined" in texto or "left" in texto:
            noticias.append(f"📰 {texto}")

    return noticias[:10]  # Limita a 10 mais recentes
