import requests
from bs4 import BeautifulSoup
from datetime import datetime

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
    
    response = requests.get(api_url, headers = headers, params = params)
    
    if response.status_code != 200:
        
        print("Falha na requisição: ", response.status_code)
        return [],[]
    
    data = response.json()
    html = data['parse']['text']['*']
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table', class_ = 'wikitable')
    
    partidas_passadas = []
    partidas_futuras = []
    
    for table in tables:
        
        rows = table.find_all('tr')[1:] ## Ignora o cabeçalho
        
        for row in rows:
            
            cols = row.find_all(['td', 'th'])
            if len(cols) < 9:
                continue
            
            try:
                date = cols[0].get_text(strip=True)
                tier = cols[1].get_text(strip=True)
                event = cols[5].get_text(strip=True)
                team1 = cols[6].get_text(strip=True)
                score = cols[7].get_text(strip=True)
                team2 = cols[8].get_text(strip=True)
                
                texto = f"📅 {date} | 🆚 {team1} vs {team2} | 🎯 Tier: {tier} | 🏆 Evento: {event}"
                
                # Partida já jogada
                if score: 
                    texto += f" | ✅ Resultado: {score}"
                    partidas_passadas.append(texto)
                    
                # ⏳ Partida futura
                else:  
                    partidas_futuras.append(texto)

            except Exception as e:
                print("❌ Erro ao processar linha:", e)

    return partidas_passadas[:10], partidas_futuras[:10]  # limitar se quiser

