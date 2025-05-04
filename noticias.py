import requests
from bs4 import BeautifulSoup

def buscar_noticias_furia():
    url = "https://liquipedia.net/counterstrike/FURIA"

    headers = {
        "User-Agent": "Mozilla/5.0 (FuriaBot/1.0)",
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "❌ Erro ao acessar Liquipedia."

    soup = BeautifulSoup(response.text, "html.parser")

    # 🔍 Buscar seção de torneios futuros
    eventos = []
    tabelas = soup.find_all("table", class_="infobox_matches_content")

    for tabela in tabelas:
        linhas = tabela.find_all("tr")
        for linha in linhas:
            colunas = linha.find_all("td")
            if len(colunas) >= 3:
                data = colunas[0].get_text(strip=True)
                evento = colunas[2].get_text(strip=True)
                eventos.append((data, evento))

    if not eventos:
        return "📭 Nenhum evento futuro encontrado no momento."

    # 🛠️ Formatar como mensagem Telegram
    resposta = "📰 **Próximos eventos da FURIA:**\n\n"
    for data, evento in eventos[:5]:  # Limita aos 5 primeiros
        resposta += f"📍 *{evento}*\n🗓️ {data}\n\n"

    return resposta.strip()