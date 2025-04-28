import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from time import sleep
import random
from dotenv import load_dotenv
import os

# Configurações do chromedriver
chromedriver_path = "/mnt/e/chromedriver/chromedriver.exe"

# Token do bot
load_dotenv()
token = os.getenv("TOKEN")

# Configuração do selenium
def setup_driver():
    options = Options()
    options.add_argument("--disable-blink-features-AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    service = Service(executable_path = chromedriver_path)
    driver = webdriver.Chrome(service = service, options = options)
    
    # Evitar detecção pelo site
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    
    return driver 
    