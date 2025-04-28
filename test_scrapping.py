import requests
from bs4 import BeautifulSoup

def buscar_resultados_passados_furia():
    url = "https://www.hltv.org/results?team=8297"  # 8297 é o ID da FURIA
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    resultados = []
    for match in soup.select('.result-con'):
        data = match.select_one('.result-date').text.strip()
        times = [t.text.strip() for t in match.select('.team')]
        score = match.select_one('.result-score').text.strip()
        resultados.append(f"{data}: {times[0]} {score} {times[1]}")
    
    return resultados

# Teste rápido
matches = buscar_resultados_passados_furia()
for match in matches[:5]:
    print(match)
