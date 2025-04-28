import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from time import sleep
import random
import os
from dotenv import load_dotenv
import setup_driver

# Scrapper próximas partidas

def proximos_jogos():
    driver = setup_driver()
    driver.get("https://www.hltv.org/team/8297/furia#tab-matchesBox")
    sleep(random.uniform(2, 4))
    
    matches = []
    
    try:
        upcoming_section = driver.find_element()

