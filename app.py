from sched import scheduler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
import logging
from datetime import datetime
from buscar_partidas_furia import *
from dateutil import parser
import asyncio
from noticias import buscar_noticias_furia
from telegram import Update, Message, Chat, User
from telegram.ext import CallbackContext
from lembretes import agendar_lembrete_partida, enviar_lembrete_partida


# Agendador global
scheduler = AsyncIOScheduler()

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
        
        /historico_partidas — Mostra partidas anteriores e seus resultados
        /partidas_futuras — Exibe as próximas partidas
        /lembrar_partida — Agenda lembrete para partidas futuras
        /agendar HH:MM — Define um horário fixo para notificações diárias
        /curiosidades — Exibe fatos interessantes sobre a FURIA
        /noticias — Busca notícias em tempo real da equipe via Liquipedia        
        
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
    
    # Salva para utilizar com /lembrar
    context.chat_data["partidas_futuras"] = futuras
    
    texto =  "\n\n".join(
        [f"{i+1}. {p}"
        for i,p in enumerate(futuras)]
        )
    await update.message.reply_text
    (f"""Próximas partidas: \n\n{texto}\n\n
    Use /lembrar [número] para receber lembrete"""
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
    noticias = buscar_noticias_furia()
    
    if not noticias:
        await update.message.reply_text("⚠️ Nenhuma notícia encontrada.")
        return
    
    texto = "\n\n".join(noticias)
    await update.message.reply_text(f"🗞️ Últimas notícias da FURIA:\n\n{texto}")


        
async def post_init(application):
    scheduler.start()
    print("Scheduler iniciado dentro do loop!")
    return None

      
# Setup do Bot
app = ApplicationBuilder().token(token).post_init(post_init).build()

# Comandos
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("partidas_futuras", partidas_futuras))
app.add_handler(CommandHandler("historico_partidas", historico_partidas))
app.add_handler(CommandHandler("lembrar_partida", enviar_lembrete_partida))
app.add_handler(CommandHandler("curiosidades", curiosidades))
app.add_handler(CommandHandler("noticias", noticias))
app.add_handler(CommandHandler("agendar", agendar))

app.add_handler(CommandHandler("enviar_mensagem", enviar_mensagem))

# Adiciona o handler global de erros
app.add_error_handler(erro_handler)

print(f"TOKEN: {token}")

if __name__ == "__main__":
    print("Bot da FURIA rodando")
    app.run_polling()

