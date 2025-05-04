# jobs.py

from telegram.ext import ContextTypes
from telegram import Update
from datetime import datetime
from dateutil import parser

# Função que será chamada no horário programado
async def enviar_lembrete_partida(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    await context.bot.send_message(
        chat_id=job.chat_id,
        text=f"⏰ Lembrete de partida!\n{job.data}"
    )

# Agendar lembrete com data/hora específica
def agendar_lembrete_partida(update: Update, context: ContextTypes.DEFAULT_TYPE, datetime_obj: datetime, mensagem: str):
    context.job_queue.run_once(
        enviar_lembrete_partida,
        when=datetime_obj,
        chat_id=update.effective_chat.id,
        data=mensagem
    )

async def lembrar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use: /lembrar 1 (por exemplo, para a 1ª partida listada)")
        return
    
    try:
        idx = int(context.args[0]) - 1 
        partidas = context.chat_data["partidas_futuras", []]
        
        if idx < 0 or idx >= len(partidas):
            await update.message.reply_text("Número inválido")
            return
        
        partida_str = partidas[idx]
        
        # Extrair data e hora do texto
        
        data_txt = partida_str.split("|")[0].replace("📅", "").strip()
        
        try:
            data_partida = parser.parse(data_txt, dayfirst = True)
            
        except Exception as e:
            await update.message.reply_text("Não consegui interpretar a data da partida.")
            return
        
        lembrar(update, context, data_partida, partida_str) 
        await update.message.reply_text(f"Lembrete agendado para {data_partida.strftime('%d%m%Y %H:%M')}")
        
    except Exception as e:
        await update.message.reply_text("Ocorreu um erro ao processar o lembrete.")
        print("Erro no /lembrar: \n", e)
        
import asyncio
from telegram import Update, Message, Chat, User
from telegram.ext import CallbackContext


