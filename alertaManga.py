import os
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
from time import sleep
from datetime import date
import telepot
import shutil

token = '5511090444:AAGGloPQ-Qh4Fwz0xgpP5rR-Yvc1nuWNK6A'
bot = telepot.Bot(token)

links = ['https://muitomanga.com/manga/one-punch-man', 'https://muitomanga.com/manga/chainsaw-man', 'https://muitomanga.com/manga/mashle',
         'https://lermanga.org/mangas/solo-leveling/', 'https://lermanga.org/mangas/one-punch-man/', 'https://lermanga.org/mangas/chainsaw-man/', 'https://lermanga.org/mangas/mashle/',
         'https://projetoscanlator.com/manga/sakamoto-days/', 'https://projetoscanlator.com/manga/mashle-magic-and-muscles/',


         ]


def buscaNovidade(linkmanga, fonte):
    today = date.today()
    d1 = today.strftime("%d-%m-%y")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(linkmanga)

        time.sleep(2)
        capitulos = page.content()
        page.close()

        capitulos = BeautifulSoup(capitulos, 'html.parser')
        data = None
        # cria a lista de capitulos

        if fonte == 'mangayabu':
            lista = capitulos.find('div', {'class': 'row rowls'})
            fotos = capitulos.find('div', {'class': 'single-bg'})

            # salva a capa do manga
            foto = fotos.find('img').get('src')

        elif fonte == 'scanlator':
            lista = capitulos.find_all('li', {'class': 'wp-manga-chapter'})
            fotos = capitulos.find('div', {'class': 'summary_image'})

            # salva a capa do manga
            foto = fotos.find('img').get('data-src')

        elif fonte == 'muito manga':
            lista = capitulos.find_all('div', {'class': 'single-chapter'})
            fotos = capitulos.find('div', {'class': 'capaMangaInfo'})

            # salva a capa do manga
            foto = fotos.find('img').get('data-src')
        elif fonte == 'lermanga':
            lista = capitulos.find('div', {'class': 'manga-chapters'})
            fotos = capitulos.find('div', {'class': 'capaMangaInfo'})

            # salva a capa do manga
            foto = fotos.find('img').get('src')

        elif fonte == 'union':
            lista = capitulos.find_all('div', {'class': 'row capitulos'})
            fotos = capitulos.find(
                'div', {'class': 'col-md-4 col-xs-12 text-center col-md-perfil'})

            # salva a capa do manga
            foto = fotos.find(
                'img').get('src')

        for item in lista:
            # separa o nome do link do capitulo
            cap = BeautifulSoup(str(item), 'html.parser')
            if fonte == 'mangayabu':
                nome = cap.find(
                    'div', {'class': 'manga-index-header'}).text
                link = cap.find('a').get('href')
                if not data:
                    data = nome
                nome = nome.replace(
                    "Capí­tulo ", "").replace('• ', '').replace('Capítulo:', '').split()[0]

            elif fonte == 'scanlator':
                nome = cap.find('a').text.strip()
                link = cap.find('a').get('href')
                if not data:
                    data = cap.find('a').text
                nome = nome.split('-')[0].strip().replace('Capítulo', '').replace(
                    '-', '.').replace(',', '.').replace('v', '.').replace('?', '')

            elif fonte == 'muito manga':
                nome = cap.find('div', {'class': 'single-chapter'}).text
                link = 'https://muitomanga.com' + \
                    str(cap.find('a').get('href'))
                if not data:
                    data = cap.find('small').text.replace('?', '')
                nome = nome.split('#')[1]
                nome = nome.split('\n')[0]

            elif fonte == 'lermanga':
                nome = cap.find(
                    'a', {'class': 'dynamic-visited'}).get('title')
                link = cap.find('a').get('href')
                if not data:
                    data = nome

                nome = nome.replace(
                    "Capítulo ", "").replace(' Ler Mangá', '').replace(' ', '').split('–')[1]
            elif fonte == 'union':
                nome = cap.find('a').text
                link = cap.find('a').get('href')
                # print(nome, link)
                if not data:
                    data = nome

                nome = nome.replace('Cap. ', '')
        # data = data.replace('/', '-')
        # print(linkmanga, str(data).strip(), d1)
        return linkmanga, data


txt = ''
with open('recente.txt', 'w', encoding='utf-8') as f:
    for link in links:
        # print(link)
        #         fonte = 'mangayabu'
        if 'scanlator' in link:
            fonte = 'scanlator'
        elif 'muitomanga' in link:
            fonte = 'muito manga'
        elif 'lermanga' in link:
            fonte = 'lermanga'

        manga, data = buscaNovidade(link, fonte)
        # print(manga, data)
        f.write(f'{link}, {manga}, {str(data).strip()}\n')

        if manga:
            txt += manga + data + '\n\n'

with open('recente.txt', 'r', encoding='utf-8') as file1, open('ultimo.txt', 'r', encoding='utf-8') as file2:
    diff = set(file1).difference(file2)

if diff:
    # print('Diferenças encontradas:')
    for line in diff:
        print(line.strip())
        bot.sendMessage(769723764, f'{line.strip()}')
else:
    print('Não há diferenças.')
os.remove('ultimo.txt')
shutil.copy('recente.txt', 'ultimo.txt')
