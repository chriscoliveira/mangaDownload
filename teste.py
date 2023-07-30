from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option(
    "excludeSwitches", ['enable-logging'])

link = 'https://www.crunchyroll.com/pt-br/simulcastcalendar?filter=premium'


navegador = webdriver.Chrome(options=chrome_options)
navegador.get(link)
time.sleep(7)
# Localizar o elemento do calendário na página usando By.ID
# calendario_element = navegador.find_element(By.CLASS_NAME, 'calendar')

# Tirar o screenshot do calendário
navegador.save_screenshot('calendario_crunchyroll.png')

# Fechar o navegador
navegador.close()
