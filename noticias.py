import requests
from bs4 import BeautifulSoup
import re

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

    for li in soup.find_all("li"):
        texto = li.get_text(strip=True)

        if len(texto) < 20:
            continue

        if re.search(r"\b(FURIA|signed|joined|part ways|left|announce|promote|moves?)\b", texto, re.IGNORECASE):
            texto_corrigido = texto

            # 1️⃣ Corrige colagem de letras: paccaVINI => pacca VINI
            texto_corrigido = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', texto_corrigido)
            # 2️⃣ Corrige palavras coladas com "and", "with", "from" etc.
            texto_corrigido = re.sub(r'(and|with|from|as|to)', r' \1 ', texto_corrigido)
            # 3️⃣ Remove espaços duplicados criados no processo
            texto_corrigido = re.sub(r'\s+', ' ', texto_corrigido).strip()

            # Traduções básicas
            traducoes = {
                "signed": "assinou com",
                "joins": "entrou para",
                "joined": "entrou para",
                "part ways with": "encerrou vínculo com",
                "left": "saiu da",
                "announces": "anunciou",
                "announce": "anunciou",
                "promote": "promoveu",
                "promoted": "foi promovido",
                "moved": "foi movido",
                "moves": "movimentou"
            }

            for en, pt in traducoes.items():
                texto_corrigido = re.sub(rf"\b{en}\b", pt, texto_corrigido, flags=re.IGNORECASE)

            # Garante que termina com ponto
            if not texto_corrigido.endswith('.'):
                texto_corrigido += '.'

            noticias.append(f"📰 {texto_corrigido}")

    return noticias[:10]
