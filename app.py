from sched import scheduler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
import logging
import asyncio
import requests
from bs4 import BeautifulSoup
from time import sleep
import random
import comandos_telegram
import funcoes_busca_jogos
import setup_driver
from datetime import datetime
from buscar_partidas_furia import *

# Configuração chromedriver para web-scrapping
chrome_driver_path = "/mnt/e/chromedriver/chromedriver-win64/chromedriver.exe" # Onde está instalado o chromedriver

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
    
async def historico_partidas(update: object, context: ContextTypes.DEFAULT_TYPE):
    passadas, _ = buscar_partidas_furia()
    
    if not passadas:
        await update.message.reply_text(
            "Nenhuma partida passada encontrada"
        )
        return
    
    texto = "\n\n".join(passadas)
    await update.message.reply_text(texto)

async def partidas_futuras(update: object, context: ContextTypes.DEFAULT_TYPE):
    _, futuras = buscar_partidas_furia()
    
    if not futuras:
        await update.message.reply_text(
            "Nenhuma partida futura encontrada"
        )
        return
    texto =  "\n\n".join(futuras) 
    await update.message.reply_text(texto)

# Agendar lembrete para partidas futuras

async def enviar_lembrete(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    await context.bot.send_message(
        chat_id=job.chat_id,
        text=f"⏰ Lembrete de partida!\n{job.data}"
    )

# Agendar lembrete com horário específico
def agendar_lembrete_partida(update, context: ContextTypes.DEFAULT_TYPE, datetime_obj: datetime, mensagem: str):
    context.job_queue.run_once(
        enviar_lembrete,
        when = datetime_obj,
        chat_id = update.effective_chat.id,
        data = mensagem
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
    

        
async def post_init(application):
    scheduler.start()
    print("Scheduler iniciado dentro do loop!")
    
        
# Setup do Bot
app = ApplicationBuilder().token(token).post_init(post_init).build()

# Agendador global
scheduler = AsyncIOScheduler()

# Comandos
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("partidas_futuras", partidas_futuras))
app.add_handler(CommandHandler("historico_partidas", historico_partidas))
app.add_handler(CommandHandler("curiosidades", curiosidades))
app.add_handler(CommandHandler("noticias", noticias))
app.add_handler(CommandHandler("agendar", agendar))

# Adiciona o handler global de erros
app.add_error_handler(erro_handler)

print(f"TOKEN: {token}")

if __name__ == "__main__":
    print("Bot da FURIA rodando")
    app.run_polling()
