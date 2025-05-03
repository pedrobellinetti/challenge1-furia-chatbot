# jobs.py

from telegram.ext import ContextTypes
from telegram import Update
from datetime import datetime

# Função que será chamada no horário programado
async def enviar_lembrete(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    await context.bot.send_message(
        chat_id=job.chat_id,
        text=f"⏰ Lembrete de partida!\n{job.data}"
    )

# Agendar lembrete com data/hora específica
def agendar_lembrete_partida(update: Update, context: ContextTypes.DEFAULT_TYPE, datetime_obj: datetime, mensagem: str):
    context.job_queue.run_once(
        enviar_lembrete,
        when=datetime_obj,
        chat_id=update.effective_chat.id,
        data=mensagem
    )
