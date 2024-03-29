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

servidor = 'unionmanga'
# cria o arquivo de log
if not os.path.isfile('config.cfg'):
    with open('config.cfg', 'w') as f:
        f.write('headless=true\nlog=false\n#servidor=unionmanga\servidor=mangachan')

# abre as configs do chrome
chrome_options = Options()
with open('config.cfg') as f:
    f = f.readlines()
    for i in f:
        if i.lower().startswith('headless=true'):
            chrome_options.add_argument("--headless")
        if i.lower().startswith('log=false'):
            chrome_options.add_experimental_option(
                "excludeSwitches", ['enable-logging'])
        if i.lower().startswith('servidor=mangachan'):
            servidor = 'mangachan'

print(servidor)


def criaPasta():
    try:
        os.mkdir("Baixados")
    except:
        pass
    try:
        os.mkdir("Download")
    except:
        pass


def limpa():
    # Get a list of all the file paths that ends with .txt from in specified directory
    fileList = glob.glob(f'Download\*.jpg')
    # print(fileList)
    # Iterate over the list of filepaths & remove each file.
    for filePath in fileList:
        try:
            pass
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)

# baixa a imagem


def download_image(link, img):
    folder = 'Download'
    with open(folder + '/' + img, 'wb') as handle:
        response = requests.get(link, stream=True)
        if not response.ok:
            response

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)

# captura o link da imagem


def getImgFromUrl(mangaName, url):
    print(f'{url=}')
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
        # lista_images.append([mangaName, link, contador])]
        print(link)
        try:
            download_image(link, f'{mangaName}_{contador}.jpg')
        except:
            pass
        contador += 1

    navegador.quit()
    # return lista_images

# captura os links dos capitulos


def getCapitulosFromUrl(link):
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
    return capitulos

# pesquisa na unionMangas


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

    return capitulos


# compacta os capitulos baixados em zip
def zipa(manga, capitulo):
    extensao = ['.jpg', '.png']
    fantasy_zip = zipfile.ZipFile(
        f'Baixados/{manga}_capitulo_{capitulo}.zip', 'w')

    for pasta, subfolders, files in os.walk(f'Download/'):

        for file in files:
            if file.endswith(tuple(extensao)):
                fantasy_zip.write(os.path.join(pasta, file), os.path.relpath(
                    os.path.join(pasta, file), f'Download/'), compress_type=zipfile.ZIP_DEFLATED)

    fantasy_zip.close()

    os.rename(f'Baixados/{manga}_capitulo_{capitulo}.zip',
              f'Baixados/{manga}_capitulo_{capitulo}.cbr')

    caminho = str(os.path.abspath(os.getcwd()) +
                  '\Baixados')
    print(
        f'{colorama.Fore.GREEN}>> Arquivo baixado com sucesso! em: Baixados/{manga}_capitulo_{capitulo}.cbr{colorama.Fore.BLUE}')
    try:
        os.startfile(caminho)
    except:
        pass


colorama.init()
print(colorama.Fore.BLUE +
      f"\n{'#'*80}\n{' '*30}Manga Download 2023  Servidor={servidor.upper()}\n{'#'*80}\n\n")

while True:
    criaPasta()
    limpa()

    # nome do manga
    nomeManga = input('\nDigite o nome do manga: ')
    if nomeManga:
        if servidor == 'mangachan':
            resultadopesquisa = mangaChan(nomeManga)
        else:
            resultadopesquisa = unionMangas(nomeManga)

        if resultadopesquisa:
            print('Encontrei os seguintes mangás:\n')
            for item in enumerate(resultadopesquisa):
                numero = item[0]
                nome = item[1]
                print(colorama.Fore.RED+str(numero) +
                      " - "+nome[1]+colorama.Fore.BLUE)

            # manga escolhido
            escolhido = input("\nDigite o numero escolhido: ")
            if escolhido:
                escolhido = int(escolhido)
                # capitulos disponiveis
                capitulosDisponiveis = getCapitulosFromUrl(
                    resultadopesquisa[int(escolhido)][0])
                listaDisponiveis = []
                print(capitulosDisponiveis)
                for cap in capitulosDisponiveis:
                    # if servidor=='unionmanga':
                    # listaDisponiveis.append(str(cap[1]).replace('Cap. ', ''))
                    # if servidor=='mangachan':

                    listaDisponiveis.append(str(cap[1]).replace('Cap. ', ''))

                if len(listaDisponiveis) > 0:
                    print(
                        f'\nCapitulos encontrados: {colorama.Fore.RED}{" ".join(listaDisponiveis)}{colorama.Fore.BLUE}')

                    # numero do capitulo escolhido
                    numeroCaps = input(
                        '\nDigite o numero do epsodio escolhido: ')
                    if numeroCaps:
                        print('\n')
                        # detecta varios capitulos
                        try:
                            inicio, fim = str(numeroCaps).split('-')
                        except:
                            inicio, fim = numeroCaps, numeroCaps

                        inicio = float(inicio)
                        fim = float(fim)
                        capsBaixados = False

                        # percorre a lista em busca dos capitulos para baixar
                        for i in listaDisponiveis:
                            atual = float(i)
                            print(atual)
                            if inicio <= atual <= fim:
                                capsBaixados = True

                                # getImgFromUrl(
                                #     f'{resultadopesquisa[escolhido][1]}_{atual}', resultadopesquisa[escolhido][0])

                                # getImgFromUrl(
                                #     f'{resultadopesquisa[escolhido][1]}_{atual}', capitulosDisponiveis[escolhido][0])

                        # zipa o conteudo
                        if capsBaixados:
                            zipa(
                                f'{resultadopesquisa[escolhido][1]}', f'{inicio}-{fim}')

                            limpa()
                        else:
                            print(
                                f'{colorama.Fore.RED}## Capítulo indisponivel.. {colorama.Fore.BLUE}')
            else:
                print(colorama.Fore.RED +
                      "\n\nCapítulo inválido, Tente outra vez!\n\n"+colorama.Fore.BLUE)
        else:
            print(colorama.Fore.RED +
                  "\n\nMangá inválido, Tente outra vez!\n\n"+colorama.Fore.BLUE)
    else:
        print(colorama.Fore.RED +
              "\n\nPrecisa digitar algum nome, Tente outra vez!\n\n"+colorama.Fore.BLUE)

# limpa()
# getCapitulosFromUrl(
#     'https://mangaschan.com/manga/naruto-sasuke-retsuden-uchiha-no-matsuei-to-tenkyu-no-hoshikuzu-novel/')
# getImgFromUrl('teste', 'https://mangaschan.com/one-punch-man-capitulo-222/')
# ..\venv\Scripts\pyinstaller.exe -F --console --icon="icone.ico" --distpath .\ -c --name "Novo Manga Downloader 2023" .\mangaNovo.py
