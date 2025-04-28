from sched import scheduler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
import logging
import asyncio
# from HLTV import HLTV
import datetime
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By # web-scrapping
from selenium.webdriver.chrome.service import Service #web-scrapping
from selenium.webdriver.chrome.options import Options #web-scrapping
from time import sleep
import random


# Configuração chromedriver para web-scrapping
chrome_driver_path = "/mnt/e/chromedriver/chromedriver.exe" # Onde está instalado o chromedriver

# Logs

logging.basicConfig (
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO
)

# .env
load_dotenv()

# Colocar o Token do bot aqui
env = load_dotenv()
token = os.getenv("TOKEN")

# Armazenar horários agendados
agendamentos = {}

async def erro_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Erro detectado: {context.error}")
    if update and hasattr(update, 'message'):
        await update.message.reply_text("⚠️ Ocorreu um erro! Tente novamente mais tarde.")



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
        🔥Bem-vindo(a) ao FURIA Clutch Bot! 
        Use /proximos_jogos, /curiosidades ou /noticias
        
        """
    )
    
async def proximos_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Busca próximos jogos
    
    # hltv = HLTV()
    
    # TESTE 
    matches = jogos_futuros()

    # Filtrar jogos da FURIA

    # furia_matches = [m for m in matches if "FURIA" in (m['team1']['name'] or "") or "FURIA" in (m['team2']['name'] or "")]
    
    # if furia_matches:
    #     match = furia_matches[0]
    #     game_time = datetime.datetime.utcfromtimestamp(match['time'] / 1000).strftime('%d/%m/%Y %H:%M (UTC)')
    #     await update.message.reply_text(f"📆 Próximo jogo da FURIA:\n{match['team1']['name']} x {match['team2']['name']}\nData: {game_time}")
    # else:
    #     await update.message.reply_text("🔍 Nenhum jogo da FURIA encontrado nos próximos dias.")



    # for match in furia_matches:
    #     print(f"{match["team1"]["name"]} vs {match["team2"]["name"]} - {match["time"]}")
    
    print(matches)
        
# def jogos_futuros():
#     url = "https://www.hltv.org/matches"
#     response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
#     soup = BeautifulSoup(response.text, 'lxml')
    
#     jogos = []
#     for match in soup.select('.upcomingMatch'):
#         team1 = match.select_one('.matchTeamName')
#         team2 = match.select('.matchTeamName')
#         timestamp = match.select_one('.matchTime')

#         # Valida se é FURIA
#         if team1 and timestamp:
#             teams = [t.text.strip() for t in team2]
#             if any("FURIA" in t for t in teams):
#                 time_unix = int(timestamp['data-unix']) / 1000
#                 data_hora = datetime.utcfromtimestamp(time_unix).strftime('%d/%m/%Y %H:%M UTC')
#                 jogos.append(f"{teams[0]} x {teams[1]} - {data_hora}")
    
#     return jogos

# # TESTE - RETIRAR DEPOIS
# matches = jogos_futuros
# print(matches)

# def historicos_jogos():
#     url = "https://liquipedia.net/counterstrike/FURIA"
#     headers = {"User-Agent": "Mozilla/5.0"}
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.text, 'lxml')

#     resultados = []
#     # Pega a seção 'Recent Results' (usando seletor da tabela)
#     for match_row in soup.select('table.infobox_matches_content tr'):
#         cells = match_row.select('td')
#         if len(cells) >= 5:
#             data = cells[0].get_text(strip=True)
#             team1 = cells[1].get_text(strip=True)
#             score = cells[2].get_text(strip=True)
#             team2 = cells[3].get_text(strip=True)
#             torneio = cells[4].get_text(strip=True)
#             resultados.append(f"{data}: {team1} {score} {team2} ({torneio})")
    
#     return resultados

async def resultados_passados(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resultados = historicos_jogos()
    if resultados:
        mensagem = "\n".join(resultados)
    else:
        mensagem = "Nenhum jogo passado encontrado."
    
    await update.message.reply_text(mensagem)
    

                
    
async def curiosidades(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
        Curiosidade: A FURIA foi fundada em 2017 e já chegou no top 5 mundial!
        """
    )
    
async def noticias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
        📰 Última notícia: FURIA anuncia novo coach para a temporada de 2025!
        """
    )
    
# Envia mensagens automáticas
async def enviar_mensagem(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    await context.bot.send_message(chat_id = job.chat_id, text = "🔥Atualização diária da FURIA!")
    
# Comando para agendar

async def agendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Formato correto: /agendar HH:MM (24h)")
        return
    
    hora_minuto = context.args[0].strip()
    print(f"Argumento recebido: {hora_minuto}") # Debug
    
    if ":" not in hora_minuto:
        await update.message.reply_text("⚠️ Erro no formato! use /agendar HH:MM (24h)")
        return
    
    try:
        hora, minuto = map(int, hora_minuto.split(":"))
        if not (0 <= hora <= 23 and 0 <= minuto <= 59):
            raise ValueError("Hora ou minuto fora inválidos.")
        
        chat_id = update.effective_chat.id
        agendamentos[chat_id] = hora_minuto
        
        # Remove agendamento anterior (se já houver)
        try:
            scheduler.remove_job(str(chat_id))
        except Exception as e:
            print(f"Nenhum job anterior pra remover: {e}")  # Debug
        
        # Agenda nova tarefa
        scheduler.add_job(
            enviar_mensagem,
            CronTrigger(hour = hora, minute = minuto),
            id = str(chat_id),
            kwargs = {"context" : context},
            replace_existing = True,
        )
        
        await update.message.reply_text(f"✅ Agendado! Você irá receber mensagens todos os dias às {hora_minuto}.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Erro no formato! Use /agendar HH:MM (24h).")
        
async def post_init(application):
    scheduler.start()
    print("Scheduler iniciado dentro do loop!")
    
        
# Setup do Bot
app = ApplicationBuilder().token(token).post_init(post_init).build()

# Agendador global
scheduler = AsyncIOScheduler()

# Comandos
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("proximos_jogos", proximos_jogos))
app.add_handler(CommandHandler("curiosidades", curiosidades))
app.add_handler(CommandHandler("noticias", noticias))
app.add_handler(CommandHandler("agendar", agendar))
app.add_handler(CommandHandler("jogos_futuros", jogos_futuros))
app.add_handler(CommandHandler("historico_jogos", historicos_jogos))

# Adiciona o handler global de erros
app.add_error_handler(erro_handler)

print(f"TOKEN: {token}")

if __name__ == "__main__":
    print("Bot da FURIA rodando")
    app.run_polling()
