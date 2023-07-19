from tkinter import font
from natsort import natsorted
import zipfile
import zipfile as zipf
from bs4 import BeautifulSoup
import requests
import os
import sys
from playwright.sync_api import sync_playwright
import time
import shutil
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
from time import sleep
from natsort import natsorted
import zipfile
import zipfile as zipf
import os
import colorama
import glob

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36'}
sistema = platform.system()
# busca o manga
if sistema == 'Windows':
    folder = 'Download\\'
    separador = '\\'
else:
    separador = '/'
    folder = 'Download/'
# fontes = ['union']
fontes = ['union', 'scanlator']  # , 'muito manga']


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


def unionMangas(nomeManga):
    print(f'{colorama.Fore.GREEN}> Aguarde um momento...{colorama.Fore.BLUE}')
    navegador = webdriver.Chrome(options=chrome_options)
    navegador.get('https://unionleitor.top/home')

    # clica na pesquisa
    navegador.find_element('xpath', '//*[@id="pesquisa"]').click()

    sleep(1)
    # digita o nome do manga
    pesquisa = navegador.find_element(
        'xpath', '/html/body/span/span/span[1]/input')
    pesquisa.send_keys(nomeManga)
    pesquisa.send_keys(Keys.ENTER)
    sleep(10)
    # captura o resultado
    resultado = navegador.find_element('xpath', '/html/body/span/span/span[2]')
    resultado = resultado.get_attribute('innerHTML')

    soup = BeautifulSoup(resultado, 'html.parser')
    itens = soup.find_all('div', {'class': 'col-sm-10'})
    capitulos = []
    for item in itens:
        try:
            a = item.find('a')
            special_characters = [':', ';', '\\', '/', '@', '#', '$', '*', '&']
            titulo = "".join(
                filter(lambda char: char not in special_characters, a.text))

            capitulos.append([a['href'], titulo])
        except Exception as e:
            pass
    navegador.quit()
    return capitulos


def mangaChan(nomeManga):
    print(f'{colorama.Fore.GREEN}> Aguarde um momento...{colorama.Fore.BLUE}')
    navegador = webdriver.Chrome(options=chrome_options)
    navegador.get('https://mangaschan.com/?s='+nomeManga)

    resultado = navegador.find_element(
        'xpath', '//*[@id="content"]/div[2]/div[1]/div/div[2]')
    resultado = resultado.get_attribute('innerHTML')

    soup = BeautifulSoup(resultado, 'html.parser')
    itens = soup.find_all('div', {'class': 'bsx'})

    capitulos = []
    for item in itens:
        try:
            a = item.find('a')
            special_characters = [':', ';', '\\', '/', '@', '#', '$', '*', '&']
            nome = str(item.find('div', {'class': 'tt'}).text).strip()
            titulo = "".join(
                filter(lambda char: char not in special_characters, nome))

            capitulos.append([a['href'], titulo])
        except Exception as e:
            pass

    navegador.quit()
    return capitulos


def iniciaBuscaManga(chatid, nomeManga):
    limpaArquivos(chatid, 'TXT', 'txt')
    print(chatid)

    with open('usuarios.txt', 'r') as f:
        f = f.readlines()
        with open('usuarios.txt', 'a') as fa:
            for i in f:
                if not str(chatid) in i:
                    novo = True
            if novo:
                fa.write(f'{chatid}\n')

    texto = []
    with open(f'TXT/{chatid}lista_manga.txt', 'w') as f:
        try:
            c = mangaChan(nomeManga)
            for i in c:
                link, nome = i
                texto.append(nome+" - MangaChan")
                f.write(f'{nome};mangachan;{link}\n')
        except:
            pass
        try:
            u = unionMangas(nomeManga)
            for i in u:
                link, nome = i
                texto.append(nome+" - UnionManga")
                f.write(f'{nome};union;{link}\n')
        except:
            pass
    return texto


def getCapitulosFromUrl(link):
    print(link)
    if 'unionleitor' in link:
        servidor = 'unionmanga'
    elif 'mangaschan' in link:
        servidor = 'mangachan'
    print(servidor)
    link = requests.get(link)
    soup = BeautifulSoup(link.text, 'html.parser')
    # print(soup)
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

            capitulos.append([a['href'], numeroCap])
        except:
            pass

    return capitulos


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


if __name__ == "__main__":
    pass
    # getImgFromUrl('123', 'teste',
    #               'https://mangaschan.com/one-punch-man-capitulo-223/')
    # create_zip_files('769723764', '769723764', 40*1024*1024)
    getCapitulosFromUrl('https://unionleitor.top/manga/jujutsu-kaisen')
