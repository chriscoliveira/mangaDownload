from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
from time import sleep
from datetime import date
import telepot
from natsort import natsorted
import platform
import requests
from urllib.parse import quote
import sqlite3

sistema = platform.system()

# busca o manga
if sistema == 'Windows':
    folder = 'Download\\'
    separador = '\\'
else:
    separador = '/'
    folder = 'Download/'

token = '5511090444:AAGGloPQ-Qh4Fwz0xgpP5rR-Yvc1nuWNK6A'
bot = telepot.Bot(token)

links = ['https://unionleitor.top/manga/dandadan', 'https://unionleitor.top/pagina-manga/one-punch-man',
         'https://unionleitor.top/manga/chainsaw-man', 'https://unionleitor.top/manga/mashle-magic-and-muscles',
         'https://unionleitor.top/pagina-manga/solo-leveling', 'https://mangaschan.com/manga/jujutsu-kaisen/', 'https://mangaschan.com/manga/tokyo-revengers/', 'https://mangaschan.com/manga/chainsaw-man/', 'https://mangaschan.com/manga/black-clover/', 'https://mangaschan.com/manga/sakamoto-days/', 'https://mangaschan.com/manga/mashle-magic-and-muscles/', 'https://mangaschan.com/manga/dandadan/']

envio = [769723764]  # , 1299478866]
# conn = sqlite3.connect('manga.db')
# cursor = conn.cursor()


# def buscaNovidade(linkmanga, fonte):
#     today = date.today()
#     d1 = today.strftime("%d-%m-%y")

#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#         page.goto(linkmanga)

#         time.sleep(2)
#         capitulos = page.content()
#         page.close()

#         capitulos = BeautifulSoup(capitulos, 'html.parser')
#         data = None
#         # cria a lista de capitulos

#         if fonte == 'mangayabu':
#             lista = capitulos.find('div', {'class': 'row rowls'})
#             fotos = capitulos.find('div', {'class': 'single-bg'})

#             # salva a capa do manga
#             foto = fotos.find('img').get('src')

#         elif fonte == 'scanlator':
#             lista = capitulos.find_all('li', {'class': 'wp-manga-chapter'})
#             fotos = capitulos.find('div', {'class': 'summary_image'})

#             # salva a capa do manga
#             foto = fotos.find('img').get('data-src')

#         elif fonte == 'muito manga':
#             lista = capitulos.find_all('div', {'class': 'single-chapter'})
#             fotos = capitulos.find('div', {'class': 'capaMangaInfo'})

#             # salva a capa do manga
#             foto = fotos.find('img').get('data-src')
#         elif fonte == 'lermanga':
#             lista = capitulos.find('div', {'class': 'manga-chapters'})
#             fotos = capitulos.find('div', {'class': 'capaMangaInfo'})

#             # salva a capa do manga
#             foto = fotos.find('img').get('src')

#         elif fonte == 'union':
#             lista = capitulos.find_all('div', {'class': 'row capitulos'})
#             # fotos = capitulos.find(
#             #     'div', {'class': 'col-md-4 col-xs-12 text-center col-md-perfil'})

#             # salva a capa do manga
#             # foto = fotos.find(
#             #     'img').get('src')

#         elif fonte == 'firemangas':
#             lista = capitulos.find_all(
#                 'a', {'class': 'link-dark'})
#             fotos = capitulos.find('div', {'class': 'thumb'})

#             # salva a capa do manga
#             foto = fotos.find(
#                 'img').get('src')

#         for item in lista:
#             # separa o nome do link do capitulo
#             cap = BeautifulSoup(str(item), 'html.parser')
#             if fonte == 'mangayabu':
#                 nome = cap.find(
#                     'div', {'class': 'manga-index-header'}).text
#                 link = cap.find('a').get('href')
#                 if not data:
#                     data = nome
#                 nome = nome.replace(
#                     "Capí­tulo ", "").replace('• ', '').replace('Capítulo:', '').split()[0]

#             elif fonte == 'scanlator':
#                 nome = cap.find('a').text.strip()
#                 link = cap.find('a').get('href')
#                 if not data:
#                     data = cap.find('a').text
#                 nome = nome.split('-')[0].strip().replace('Capítulo', '').replace(
#                     '-', '.').replace(',', '.').replace('v', '.').replace('?', '')

#             elif fonte == 'muito manga':
#                 nome = cap.find('div', {'class': 'single-chapter'}).text
#                 link = 'https://muitomanga.com' + \
#                     str(cap.find('a').get('href'))
#                 if not data:
#                     data = cap.find('small').text.replace('?', '')
#                 nome = nome.split('#')[1]
#                 nome = nome.split('\n')[0]

#             elif fonte == 'lermanga':
#                 nome = cap.find(
#                     'a', {'class': 'dynamic-visited'}).get('title')
#                 link = cap.find('a').get('href')
#                 if not data:
#                     data = nome

#                 nome = nome.replace(
#                     "Capítulo ", "").replace(' Ler Mangá', '').replace(' ', '').split('–')[1]
#             elif fonte == 'union':
#                 nome = cap.find('a').text
#                 link = cap.find('a').get('href')
#                 # print(nome, link)
#                 if not data:
#                     data = nome

#                 nome = nome.replace('Cap. ', '')

#             elif fonte == 'firemangas':
#                 nome = cap.find('a').text
#                 nome = nome.replace('VistoCapítulo ', '').split(' ')[0]
#                 link = cap.find('a').get('href')
#                 # print(nome, link)
#                 if not data:
#                     data = nome

#                 nome = nome.replace('Cap. ', '')

#         # data = data.replace('/', '-')
#         # print(linkmanga, str(data).strip(), d1)
#         return linkmanga, data


# txt = ''

# with open('/Scripts/recente.txt', 'a', encoding='utf-8') as f:
#     with open('/Scripts/recente.txt', 'r', encoding='utf-8') as fr:
#         fr = fr.read()
#         for link in links:

#             if 'scanlator' in link:
#                 fonte = 'scanlator'
#             elif 'muitomanga' in link:
#                 fonte = 'muito manga'
#             elif 'union' in link:
#                 fonte = 'union'
#             elif 'lermanga' in link:
#                 fonte = 'lermanga'
#             elif 'firemangas' in link:
#                 fonte = 'firemangas'
#             try:
#                 manga, data = buscaNovidade(link, fonte)

#                 if not f'{link},{str(data).strip()}\n' in fr:
#                     f.write(f'{link},{str(data).strip()}\n')
#                     for u in envio:
#                         bot.sendMessage(
#                             int(u), f'{link},{str(data).strip()}\n')
#                 # f.write(f'{link}, {manga}, {str(data).strip()}\n')
#                 # log.write(
#                 #     f'{date.today()}-ADD-{link}, {manga}, {str(data).strip()}\n')
#             except Exception as e:
#                 print(f'{date.today()}-ERR-{link=} {e=}\n')
#             try:
#                 if manga:
#                     txt += manga + data + '\n\n'
#             except:
#                 print('erro')


def getCapitulosFromUrl(link):
    if 'unionleitor' in link:
        servidor = 'unionmanga'
    elif 'mangaschan' in link:
        servidor = 'mangachan'

    link = requests.get(link)
    soup = BeautifulSoup(link.text, 'html.parser')

    if servidor == 'unionmanga':
        itens = soup.find_all('div', {'class': 'row capitulos'})
    elif servidor == 'mangachan':
        itens = soup.find_all('div', {'class': 'eph-num'})

    capitulos = []
    for item in itens:
        try:
            a = item.find('a')
            if servidor == 'unionmanga':
                numeroep = str(a.text).replace('Cap. ', '')
            elif servidor == 'mangachan':
                numeroep = str(item.find('span', {'class': 'chapternum'}).text).replace(
                    'Capítulo ', '')
            numero = ''
            for char in numeroep:
                if char.isalpha():
                    char = '.'
                numero += char.strip()
                numero = numero.replace('..', '.')

            numeroCap = float(numero)
            # print([a['href'], numeroCap])
            capitulos.append([a['href'], numeroCap])
        except:
            pass
    # print(capitulos)
    return f'{capitulos[0][0]} {capitulos[0][1]}'


with open('/Scripts/recente.txt', 'a', encoding='utf-8') as f:
    with open('/Scripts/recente.txt', 'r', encoding='utf-8') as fr:
        fr = fr.read()

        for i in links:
            manga = getCapitulosFromUrl(i)
            if not manga in fr:
                f.write(manga)
                for u in envio:
                    bot.sendMessage(int(u), f'{manga}\n')
