from bs4 import BeautifulSoup
import requests
import os
import sys
from playwright.sync_api import sync_playwright
import time
import platform

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36'}
sistema = platform.system()
# busca o manga
if sistema == 'Windows':
    folder = 'Download\\'
    divisor = '\\'
else:
    divisor = '/'
    folder = 'Download/'


with sync_playwright() as p:
    if sistema == 'Windows':
        browser = p.chromium.launch(
            channel='chrome', headless=True, args=['--start-maximized'])
    else:
        browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    site = 'https://unionleitor.top/lista-mangas'
    blocomangas = 'select2-results__option'

    page.goto(site, timeout=0)
    page.click('input[id="pesquisa"]')
    page.fill('input[class="select2-search__field"]', 'solo leveling')

    time.sleep(2)
    mangas_encontrados = page.content()
    page.close()
    mangas_encontrados = BeautifulSoup(mangas_encontrados, 'html.parser')

    with open(f'TXT/xxxlista_manga.txt', 'a+') as f:
        for manga in mangas_encontrados.find_all('li', {'class': blocomangas}):
            print(manga)
            # if str('solo leveling').lower() in str(nome).lower():
            link = manga.find('a').get('href')
            nome = str(manga.text).replace('Autor:', '||').split('||')[0]
            f.write(f'{nome};union;{link}\n')
