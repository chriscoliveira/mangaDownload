from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import colorama
from bs4 import BeautifulSoup
from time import sleep
from datetime import date
import telepot
from natsort import natsorted
import platform
import requests
from urllib.parse import quote
import zipfile
import zipfile as zipf
import os
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

links = ['https://unionleitor.top/manga/dandadan',
         'https://unionleitor.top/manga/chainsaw-man', 'https://unionleitor.top/pagina-manga/one-punch-man',
         'https://unionleitor.top/manga/mashle-magic-and-muscles',
         'https://unionleitor.top/pagina-manga/solo-leveling', 'https://mangaschan.com/manga/jujutsu-kaisen/', 'https://mangaschan.com/manga/tokyo-revengers/', 'https://mangaschan.com/manga/chainsaw-man/', 'https://mangaschan.com/manga/black-clover/', 'https://mangaschan.com/manga/sakamoto-days/', 'https://mangaschan.com/manga/mashle-magic-and-muscles/', 'https://mangaschan.com/manga/dandadan/']

envio = [769723764]  # , 1299478866]
# conn = sqlite3.connect('manga.db')


# abre as configs do chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option(
    "excludeSwitches", ['enable-logging'])


def limpaArquivos(id, pasta, ext):
    print('>>> funcoes - limpaTXT')
    import os
    import glob
    # Get a list of all the file paths that ends with .txt from in specified directory
    if pasta == 'Download':
        fileList = glob.glob(f'Download/{id}/*.{ext}')
    elif pasta == 'TXT':
        fileList = glob.glob(f'TXT/{id}*.{ext}')

    # Iterate over the list of filepaths & remove each file.
    for filePath in fileList:
        try:
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)


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
    print(f'{capitulos[0][0]} {capitulos[0][1]}')
    return f'{capitulos[0][0]} {capitulos[0][1]}'


def getImgFromUrl(id, mangaName, servidor, url):

    try:
        os.mkdir(f'Download/{id}')
    except Exception as e:
        print(f'{e}')

    print(f'{colorama.Fore.GREEN}> Baixando {mangaName} -> {url}{colorama.Fore.BLUE}')
    navegador = webdriver.Chrome(options=chrome_options)
    navegador.get(url)
    imagens = navegador.find_elements(By.TAG_NAME, 'img')

    lista_images = []
    contador = 1
    for img in imagens:

        if servidor == 'unionmanga':
            link = img.get_attribute('src')
        if servidor == 'mangachan':
            link = img.get_attribute('data-src')

        print(link)
        try:
            download_image(id, link, f'{mangaName}_{contador}.jpg')

        except Exception as e:
            print(f'erro {e}')
            try:
                os.remove(f'Download/{id}/{mangaName}_{contador}.jpg')
            except:
                pass
        contador += 1
    navegador.quit()


def download_image(id, link, img):
    folder = f'Download/{id}/'
    with open(folder + '/' + img, 'wb') as handle:
        response = requests.get(link, stream=True)
        if not response.ok:
            response

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)


def create_zip_files(id, manganame, max_size):
    file_list = []
    current_size = 0
    zip_count = 1
    arquivos_compactados = []
    path = [os.path.join(p, file) for p, _, files in os.walk(
        os.path.abspath(f"Download/{id}/")) for file in files]

    lista = natsorted(path)
    print(lista)

    # Lista todos os arquivos da pasta em ordem alfabética

    for file in lista:
        # Verifica se o arquivo é uma imagem JPEG
        if file.lower().endswith('.jpg'):
            file_size = os.path.getsize(file)

            # Verifica se o tamanho do arquivo excede o limite
            if current_size + file_size > max_size:
                # Cria um novo arquivo ZIP
                zip_filename = f'Baixados/{manganame}_{zip_count}.cbr'
                with zipfile.ZipFile(zip_filename, 'w') as zipf:
                    # Adiciona os arquivos à nova pasta ZIP em ordem alfabética
                    for f in sorted(file_list):
                        zipf.write(f, arcname=os.path.basename(f))
                arquivos_compactados.append(
                    f'Baixados/{manganame}_{zip_count}.cbr')
                # Reseta as variáveis para o próximo arquivo ZIP
                file_list = []
                current_size = 0
                zip_count += 1

            # Adiciona o arquivo atual à lista de arquivos
            file_list.append(file)
            current_size += file_size

    # Cria o último arquivo ZIP, se houver algum arquivo restante
    if file_list:
        arquivos_compactados.append(f'Baixados/{manganame}_{zip_count}.cbr')
        zip_filename = f'Baixados/{manganame}_{zip_count}.cbr'
        with zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
            for f in sorted(file_list):
                zipf.write(f, arcname=os.path.basename(f))
    return arquivos_compactados


with open('recente.txt', 'a', encoding='utf-8') as f:
    with open('recente.txt', 'r', encoding='utf-8') as fr:
        fr = fr.read()

        for i in links:
            manga = getCapitulosFromUrl(i)
            if not manga in fr:
                limpaArquivos('saiu hoje', 'Download', 'jpg')
                f.write(manga+'\n')
                for u in envio:
                    print(u)
                    if 'unionleitor' in manga:
                        servidor = 'unionmanga'
                    else:
                        servidor = 'mangachan'
                    nome = f"{manga.split(' ')[0].split('/')[-2]}_{manga.split(' ')[0].split('/')[-1]}"
                    print(nome)
                    getImgFromUrl('saiu hoje', nome, servidor,
                                  manga.split(' ')[0])
                    zipa = create_zip_files(
                        'saiu hoje', f'{nome}', max_size=45 * 1024 * 1024)
                    for i in zipa:
                        bot.sendMessage(int(u), f'Acabou de sair... {nome}')
                        bot.sendDocument(int(u), document=open(i, 'rb'))
                    # bot.sendMessage(int(u), f'{manga}\n')

limpaArquivos('saiu hoje', 'Download', 'jpg')