from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv

# .env
load_dotenv()

# Colocar o Token do bot aqui
env = load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
        🔥Bem-vindo(a) ao FURIA Clutch Bot! 
        Use /proximos_jogos, /curiosidades ou /noticias
        
        """
    )
    
async def proximos_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Automatizar depois
    await update.message.reply_text(
        """
        📆 Próximo jogo da FURIA:
        FURIA X Team Liquid
        Data: 30/12/2025 - 19h00 (BRT)
        
        """
    )
    
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
    
app = ApplicationBuilder().token(TOKEN).build()

# Comandos
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("proximos_jogos", proximos_jogos))
app.add_handler(CommandHandler("curiosidades", curiosidades))
app.add_handler(CommandHandler("noticias", noticias))

print("Bot da FURIA rodando!")
app.run_polling






