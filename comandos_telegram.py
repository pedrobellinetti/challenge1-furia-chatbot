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
from setup_driver import *
from funcoes_busca_jogos import *

# Comandos do Bot 

async def proximos_jogos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Buscando próximos jogos da FURIA...")
    
    matches = buscar_proximos_jogos()
    
    if matches:
        msg = "🔥 Próximos jogos da FURIA: \n + \n".join(matches)
    else:
        msg = "❌ Nenhum jogo futuro encontrado"
    await update.message.reply_text(msg)
    
async def resultados(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Buscando resultados recentes da FURIA...")
    results = historico_jogos()
    
    if results:
        msg = "🔥 Resultados recentes da FURIA: \n + \n".join(results[:5]) # Mostra os 5 primeiros resultados
    else:
        msg = "❌ Nenhum resultado recente encontrado."
    await update.message.reply_text(msg)
    

    