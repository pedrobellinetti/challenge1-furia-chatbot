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
from setup_driver import *

# Scrapper próximas partidas

def proximos_jogos():
    driver = setup_driver()
    driver.get("https://www.hltv.org/team/8297/furia#tab-matchesBox")
    sleep(random.uniform(2, 4))
    
    matches = []
    
    try:
        upcoming_section = driver.find_element(By.ID, "upcomingMatchesBox")
        upcoming_rows = upcoming_section.find_elements(By.CLASS_NAME, "match")
        for row in upcoming_rows:
            date = row.find_element(By.CLASS_NAME, "matchTime").text
            teams = row.find_elements(By.CLASS_NAME, "matchTeamName")
            bo_format = row.find_element(By.CLASS_NAME, "matchMeta").text
            
            if len(teams) == 2:
                team1 = teams[0].text
                team2 = teams[1].text
                matches.append(f"📆 {date} - {team1} vs {team2} ({bo_format})")
    except Exception as e:
        print("Erro ao buscar partidas futuras: ", e)
        
    driver.quit()
    return matches

def historico_jogos():
    driver = setup_driver()
    driver.get("https://www.hltv.org/team/8297/furia#tab-matchesBox")
    sleep(random.uniform(2, 4))
    
    results = []
    try:
        past_section = driver.find_element(By.ID, "pastMatchesBox")
        past_rows = past_section.find_elements(By.CLASS_NAME, "result-con")
        
        for row in past_rows:
            date = row.find_element(By.CLASS_NAME, "time").text
            teams = row.find_elements(By.CLASS_NAME, "team")
            score = row.find_element(By.CLASS_NAME, "result-score").text    
            bo_format = row.find_element(By.CLASS_NAME, "map-text").text
            
            if len(teams) == 2:
                team1 = teams[0].text
                team2 = teams[1].text
                results.append(f"📆 {date} - {team1} {score} vs {team2} {score} ({bo_format})")
    except Exception as e:
        print(f"Erro ao buscar partidas passadas: {e}")
        
    driver.quit()
    return results


                

