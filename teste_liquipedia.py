import requests
from bs4 import BeautifulSoup

def buscar_partidas_furia():
    headers = {
        "User-Agent": "FuriaTelegramBot/1.0 (contato: seuemail@dominio.com)",
        "Accept": "application/json"
    }

    api_url = "https://liquipedia.net/counterstrike/api.php"
    params = {
        "action": "parse",
        "page": "FURIA/Matches",
        "format": "json"
    }

    response = requests.get(api_url, headers=headers, params=params)

    if response.status_code != 200:
        print("❌ Falha na requisição:", response.status_code)
        return []

    data = response.json()
    html = data['parse']['text']['*']
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table', class_='wikitable')

    resultados = []

    for table in tables:
        rows = table.find_all('tr')[1:]
        
        # for row in rows:
            # DEBUG
            
            # cols = row.find_all(['td', 'th'])

            # if len(cols) < 5:
            #     continue

            # # 🔍 DEBUG: Conteúdo HTML da linha
            # print("\n🔎 LINHA DEBUG:")
            # print(row.prettify())

            # try:
            #     date = cols[0].get_text(strip=True)
            #     event = cols[1].get_text(strip=True)

            #     for i, col in enumerate(cols):
            #         print(f"COLUNA {i}: {col.get_text(strip=True)}")

            #     # Ajustar índices depois 

            # except Exception as e:
            #     print("❌ Erro ao processar linha:", e)
            
        for row in rows:
            cols = row.find_all(['td', 'th'])
            if len(cols) < 9:
                continue  # ignora linhas incompletas

            try:
                date = cols[0].get_text(strip=True)
                tier = cols[1].get_text(strip=True)
                event = cols[5].get_text(strip=True)
                team1 = cols[6].get_text(strip=True)
                score = cols[7].get_text(strip=True)
                team2 = cols[8].get_text(strip=True)

                formatted = f"📅 {date} | {team1} vs {team2} | {tier} - Resultado: {score} | Evento: {event}"
                print(formatted)

            except Exception as e:
                print("❌ Erro ao processar linha:", e)

    return resultados[:10]



# Teste
if __name__ == "__main__":
    jogos = buscar_partidas_furia()
    for j in jogos:
        print(j)
