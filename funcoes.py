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
fontes = ['union', 'scanlator', 'muito manga', ]


def busca_manga(id, manga_name, servidor):
    print(f'{"#"*60}\n\nProcurando nos sites pelo mangá: {manga_name}\n\n{"#"*60}\n\n')
    try:
        os.remove(f'TXT/{id}lista_manga.txt')
    except:
        pass

    # for i in fontes:
    mangas = pesquisa_manga(id, manga_name, fonte=servidor)

    # if not mangas:
    #     mangas = pesquisa_manga(id, manga_name.split(' ')[0], fonte=i)
    return mangas


def pesquisa_manga(id, manga_name, fonte):
    # de acordo com a fonte acessa o site
    tag = 'div'
    if fonte == 'union':
        site = 'https://unionleitor.top/lista-mangas'
        blocomangas = 'select2-results__option'
        tag = 'li'
    elif fonte == 'firemangas':
        site = 'https://firemangas.com/'
        blocomangas = 'ui-autocomplete'
        tag = 'ul'
    elif fonte == 'mangayabu':
        site = 'https://www.mangayabu.top/lista-de-mangas/'
        blocomangas = 'ycard-details'

    elif fonte == 'scanlator':
        site = 'https://projetoscanlator.com/manga-2/?m_orderby=views'
        blocomangas = 'badge-pos-1'

    elif fonte == 'muito manga':
        site = f'https://muitomanga.com/buscar?q={manga_name}'
        blocomangas = 'boxAnimeSobreLast'

    elif fonte == 'lermanga':
        site = f'https://lermanga.org/?s={manga_name}'
        blocomangas = 'flw-item'

    try:
        # abre o navegador
        with sync_playwright() as p:
            browser = p.chromium.launch(
                channel='chrome', headless=True, args=['--start-maximized'])
            page = browser.new_page()

            page.goto(site, timeout=100000)

            # caso for do mangayabu faz a pesquisa
            if fonte == 'mangayabu':
                page.fill('input[id="mangasearch"]', manga_name)

            elif fonte == 'union':
                page.click('input[id="pesquisa"]')
                page.fill('input[class="select2-search__field"]', manga_name)

            elif fonte == 'firemangas':
                page.click('div[class="search"]')
                page.fill('input[id="searchInput"]', manga_name)

            time.sleep(5)
            mangas_encontrados = page.content()
            page.close()

            # faz o scrap da pagina
            mangas_encontrados = BeautifulSoup(
                mangas_encontrados, 'html.parser')

            with open(f'TXT/{id}lista_manga.txt', 'a+') as f:
                for manga in mangas_encontrados.find_all(tag, {'class': blocomangas}):
                    # print(str(manga))
                    if fonte == 'union':
                        try:
                            link = manga.find('a').get('href')
                            nome = str(manga.text).replace(
                                'Autor:', '||').split('||')[0]
                            # print(link, nome, sep='\n')
                        except:
                            print('falha ao pesquisar em '+fonte +
                                  '\nFECHE O PROGRAMA E TENTE NOVAMENTE')
                    elif fonte == 'firemangas':
                        try:
                            itens = manga.find_all('li')
                            for i in itens:
                                try:
                                    link = i.find(
                                        'a', class_='link-block')['href']
                                    nome = i.find(
                                        'span', class_='series-title').text

                                    f.write(f'{nome};{fonte};{link}\n')
                                except:
                                    pass
                        except Exception as e:
                            print('falha ao pesquisar em '+fonte+' ' +
                                  str(e)+'\nFECHE O PROGRAMA E TENTE NOVAMENTE')
                        link = ''
                        nome = ''
                    elif fonte == 'mangayabu':
                        try:
                            link = manga.find('a').get('href')
                            nome = manga.find('a').get('title').replace(
                                ':', '').replace('/', ' ').replace('\\', ' ').replace('?', '')
                        except:
                            print('falha ao pesquisar em '+fonte +
                                  '\nFECHE O PROGRAMA E TENTE NOVAMENTE')
                    elif fonte == 'scanlator':
                        try:
                            link = manga.find('a').get('href')
                            nome = manga.find(
                                'h3', {'class': 'h5'}).text.strip().replace(':', '')
                        except:
                            print('falha ao pesquisar em '+fonte +
                                  '\nFECHE O PROGRAMA E TENTE NOVAMENTE')
                    elif fonte == 'muito manga':
                        try:
                            link = 'https://muitomanga.com' + \
                                str(manga.find('a').get('href'))
                            nome = manga.find(
                                'h3').text.strip().replace(':', '')
                        except:
                            print('falha ao pesquisar em '+fonte +
                                  '\nFECHE O PROGRAMA E TENTE NOVAMENTE')
                    elif fonte == 'lermanga':
                        try:
                            lista = capitulos.find_all(
                                'div', {'class': 'row capitulos'})
                            fotos = capitulos.find(
                                'div', {'class': 'col-md-4 col-xs-12 text-center col-md-perfil'})
                        except:
                            print('falha ao pesquisar em '+fonte +
                                  '\nFECHE O PROGRAMA E TENTE NOVAMENTE')
                    try:
                        if str(manga_name).lower() in str(nome).lower():
                            f.write(f'{nome};{fonte};{link}\n')
                    except:
                        pass

            # preenche a lista de mangas encontrados
            listagem = []
            with open(f'TXT/{id}lista_manga.txt', 'r') as f:
                lista = f.readlines()
                for item in lista:
                    listagem.append(
                        f"{item.split(';')[0]};{item.split(';')[1]}")
            return listagem
    except Exception as e:
        print(f'ocorreu esse erro::: {e}')
# mostra os capitulos do manga


def busca_capitulos(id, manga_link, fonte):
    # print(f'{"#"*60}\n\nBuscandos os capitulos disponiveis em: {manga_link}\n\n{"#"*60}\n\n')

    with sync_playwright() as p:
        if sistema == 'Windows':
            browser = p.chromium.launch(channel='chrome', headless=True)
        else:
            browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(manga_link, timeout=0)

        time.sleep(2)
        capitulos = page.content()
        page.close()

        capitulos = BeautifulSoup(capitulos, 'html.parser')

        data = None
        # cria a lista de capitulos
        with open(f'TXT/{id}lista_capitulos.txt', 'w') as txt_cap:
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

            elif fonte == 'firemangas':
                lista = capitulos.find_all(
                    'a', {'class': 'link-dark'})
                fotos = capitulos.find('div', {'class': 'thumb'})

                # salva a capa do manga
                foto = fotos.find(
                    'img').get('src')

            with open(f'TXT/{id}capa.jpg', 'wb') as handle:
                response = requests.get(foto, stream=True)
                if not response.ok:
                    response

                for block in response.iter_content(1024):
                    if not block:
                        break
                    handle.write(block)

            num_capitulos = []
            for item in lista:
                # print(item)
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

                elif fonte == 'firemangas':
                    nome = cap.find('a').text
                    nome = nome.replace('VistoCapítulo ', '').split(' ')[0]
                    link = cap.find('a').get('href')
                    # print(nome, link)
                    if not data:
                        data = nome

                    nome = nome.replace('Cap. ', '')

                txt_cap.write(f'{nome}, {link}\n')
                num_capitulos.append(nome)
                # print(num_capitulos)

        # retorna os capitulos na lista de capitulos

        capitulos = num_capitulos[::-1]
        caps = ", ".join(capitulos)
        retorno = caps + f'\nUltimo capitulo lançado em {data.strip()}'

        return retorno


def iniciaDownload(id, nome_manga, inicio, fim, fonte='mangayabu', prog=False):
    inicio = inicio.replace(',', '.')
    fim = fim.replace(',', '.')

    nome_manga = str(nome_manga).replace(' ', '_')
    # apaga a pasta download
    try:
        # print('Apagando a pasta download...')
        folder = f'Download/{id}'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    except:
        pass

    print('Iniciando o download...')
    with open(f'TXT/{id}lista_capitulos.txt', 'r') as f:
        linhas = f.readlines()
        for linha in linhas:
            inicio = float(inicio)
            fim = float(fim)
            atual = str(linha.split(',')[0])
            try:
                atual = float(atual)
                baixados = ''
                if inicio <= atual <= fim:
                    # print(linha)
                    range_atual = str(inicio)+"_"+str(fim)
                    baixados = baixaPaginas(id, nome_manga, str(
                        atual), linha.split(',')[1], range_atual, fonte)
            except:
                pass
    if sistema == 'Windows':
        listagem = f'Download\\'
    else:
        listagem = f'Download/'
    print('Download finalizado!')
    print('Compactando arquivos...')
    if prog:
        quantidadeCBR = zipa(id, nome_manga, f'{inicio}-{fim}')
    else:
        quantidadeCBR = zipa1(id, [listagem, ], nome_manga, f'{inicio}-{fim}')
    return quantidadeCBR


def baixaPaginas(id, manga, capitulo, link, range_atual, fonte='mangayabu'):
    lista_baixados = []

    with sync_playwright() as p:
        if sistema == 'Windows':
            browser = p.chromium.launch(channel='chrome', headless=True)
        else:
            browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(link, timeout=0)
        time.sleep(5)
        pagina = page.content()

        with open(f'TXT/{id}paginas.html', 'w', encoding='UTF-8') as f:

            f.write(pagina)
        page.close()

    # cria um pagina html com as imagens do capitulo

    with open(f'TXT/{id}paginas.html', 'r', encoding='UTF-8') as f:
        pagina = f.read()
        imagens = BeautifulSoup(pagina, 'html.parser')
        if fonte == 'mangayabu':
            imgs = imagens.find('div', class_="table-of-contents")
            imgs = imgs.find_all('img')
        elif fonte == 'lermanga':
            imgs = imagens.find('div', class_="reader-area")
            imgs = imgs.find_all('img')
        elif fonte == 'union':
            imgs = imagens.find('div', class_="col-sm-12 text-center")
            imgs = imgs.find_all('img')
        elif fonte == 'firemangas':
            imgs = imagens.find('div', class_='readchapter read-slideshow')
            imgs = imgs.find_all('img')
        elif fonte == 'scanlator':
            imgs = imagens.find_all('img', {'class': 'wp-manga-chapter-img'})
        elif fonte == 'muito manga':
            imgs = imagens.find_all('script')
            for img in imgs:
                if 'imagens_cap' in str(img):
                    imgs = str(img).replace('\\', '').replace('\n', '').replace('"', '').replace('[', '').replace(
                        ']', '').replace(';', '').split('=')[1]
                    imgs = imgs.split('<')[0]
                    imgs = imgs.split(',')
        # print(imgs)
        cont = 0

        for img in imgs:

            if fonte == 'muito manga':
                print(f'Baixando o capitulo {capitulo}. {img}')
                # print(img)
                download_img(id, manga, capitulo,
                             f'{manga}_{capitulo}_{cont}.jpg', img, range_atual)
                lista_baixados.append(capitulo)
                cont += 1
            elif fonte == 'mangayabu' or fonte == 'lermanga' or fonte == 'union' or fonte == 'firemangas':
                # print(img)
                linkImg = str(img.get('src')
                              ).replace('http:', 'https:').strip()
                print(f'Baixando o capitulo {capitulo}. {linkImg}')
                download_img(id, manga, capitulo,
                             f'{manga}_{capitulo}_{cont}.jpg', linkImg, range_atual)
                lista_baixados.append(capitulo)
                cont += 1
            else:
                # print(img)
                linkImg = str(img.get('data-src')
                              ).replace('http:', 'https:').strip()
                print(f'Baixando o capitulo {capitulo}. {linkImg}')
                download_img(id, manga, capitulo,
                             f'{manga}_{capitulo}_{cont}.jpg', linkImg, range_atual)
                lista_baixados.append(capitulo)
                cont += 1

    return lista_baixados


def download_img(id, manga, capitulo, img, url, range_atual):

    # cria a pasta
    try:
        os.mkdir("Download")
    except Exception as e:
        pass
    # cria a pasta
    try:
        os.mkdir(f"Download/{id}")
    except Exception as e:
        pass
    # baixa a imagen

    with open(folder + id + '/' + img, 'wb') as handle:
        response = requests.get(url, stream=True)
        if not response.ok:
            response

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)


# compacta os capitulos baixados em zip
def zipa(id, manga, capitulo):
    extensao = ['.jpg', '.png']
    fantasy_zip = zipfile.ZipFile(
        f'Baixados/{manga}_capitulo_{capitulo}.zip', 'w')

    for pasta, subfolders, files in os.walk(f'Download/{id}'):

        for file in files:
            if file.endswith(tuple(extensao)):
                fantasy_zip.write(os.path.join(pasta, file), os.path.relpath(
                    os.path.join(pasta, file), f'Download/{id}'), compress_type=zipfile.ZIP_DEFLATED)

    fantasy_zip.close()

    os.rename(f'Baixados/{manga}_capitulo_{capitulo}.zip',
              f'Baixados/{manga}_capitulo_{capitulo}.cbr')

    limpaTXT({id}, 'txt')
    limpaTXT({id}, 'jpg')
    limpaTXT({id}, 'html')
    caminho = str(os.path.abspath(os.getcwd()) +
                  '\Baixados')
    print(caminho)
    os.startfile(caminho)


def zipa1(id, lista, manga, capitulo):
    # print(id, lista, manga, capitulo, sep='\n')
    total = 0
    quantidadeZip = 1
    nomesZip = []
    path = [os.path.join(p, file) for p, _, files in os.walk(
        os.path.abspath(f'Download/{id}')) for file in files]

    lista = natsorted(path)
    listaZip = []
    listaTmp = []
    for i in lista:
        # print(i)
        size = os.path.getsize(i)
        if total > 41943040:  # limita o zip a 40mb
            listaZip.append(listaTmp)
            total = size
            listaTmp = []
            listaTmp.append(
                f"{str(i.split('/')[-3])}/{str(i.split('/')[-2])}/{str(i.split('/')[-1])}")
        else:
            total += size
            listaTmp.append(
                f"{str(i.split(separador)[-3])}/{str(i.split(separador)[-2])}/{str(i.split(separador)[-1])}")
    # print(listaTmp)
    listaZip.append(listaTmp)

    contador = 0
    for i in listaZip:
        nomeManga = i[0].split('/')[-1].split('_')[0]

        fantasy_zip = zipfile.ZipFile(
            f'{folder}{id}/{manga}_capitulo_{capitulo}_parte_{contador}.zip', 'w')
        for x in i:
            dados = x.split('/')
            pasta = f'{dados[0]}/{dados[1]}'
            file = dados[-1]
            if file.endswith('.jpg'):
                fantasy_zip.write(os.path.join(pasta, file), os.path.relpath(
                    os.path.join(pasta, file), f'Download/{id}'), compress_type=zipfile.ZIP_DEFLATED)
        fantasy_zip.close()
        os.rename(f'{folder}{id}/{manga}_capitulo_{capitulo}_parte_{contador}.zip',
                  f'{folder}{id}/{manga}_capitulo_{capitulo}_parte_{contador}.cbr')
        shutil.copyfile(f'{folder}{id}/{manga}_capitulo_{capitulo}_parte_{contador}.cbr',
                        f'Baixados/{manga}_capitulo_{capitulo}_parte_{contador}.cbr')
        nomesZip.append(
            f'{folder}{id}/{manga}_capitulo_{capitulo}_parte_{contador}.cbr')
        contador += 1

    limpaTXT({id}, 'txt')
    limpaTXT({id}, 'jpg')
    limpaTXT({id}, 'html')
    return nomesZip


def limpaTXT(id, ext):
    import os
    import glob
    # Get a list of all the file paths that ends with .txt from in specified directory
    fileList = glob.glob(f'{id}*.{ext}')
    # Iterate over the list of filepaths & remove each file.
    for filePath in fileList:
        try:
            os.remove(filePath)
        except:
            print("Error while deleting file : ", filePath)


def log(N=20):
    texto = ''
    with open('exemplo.log', 'r') as f:
        for line in (f.readlines()[-N:]):
            texto += line+'\n'
    return texto

# C:\Users\Christian\AppData\Roaming\Python\Python310\Scripts\pyinstaller.exe -F --console -w --upx-dir=D:\upx-4.0.2-win64 --distpath .\ --ico ..\icone.ico -c --name "MangaDownloader 2023" .\manga_download.py


if __name__ == "__main__":
    pass

    print(busca_manga('101010', 'bleach'))
    # print(busca_capitulos(
    #     '101010', 'https://firemangas.com/manga/ler/52', 'firemangas'))
    # print(busca_capitulos(
    #     '101010', 'https://mangayabu.top/manga/oyasumi-punpun/', 'mangayabu'))

    # print(zipa1(769723764, ['Download\\'], 'One Punch-Man', '206.0-206.0'))

    # while True:
    #     manga = input(f'{"#"*20}\nDigite o nome do manga a pesquisar: ')
    #     print(f'\nAguarde enquando pesquiso o manga: "{manga}"')
    #     encontrados = busca_manga('local_', manga)

    #     if encontrados:
    #         contador = 1
    #         servidor_ = '.'
    #         for i in encontrados:
    #             nome, servidor = str(i).split(';')
    #             if servidor != servidor_:
    #                 print("\nServidor: "+str(servidor).upper())
    #                 servidor_ = servidor
    #             print(f'{contador}-> {nome}')
    #             contador += 1
    #         escolhido = input('\n\nDigite o numero do manga escolhido: ')
    #     if escolhido:
    #         print('\nProcurando os capítulos disponiveis...')
    #         with open('TXT/local_lista_manga.txt', 'r') as r:
    #             r = r.readlines()
    #             nome, servidor, link = r[int(escolhido)-1].split(';')

    #             print('\nEncontrei os seguintes capítulos:')
    #             print(busca_capitulos('local_', link, servidor))
    #         capitulo = input(
    #             'Digite o intervalo de capítulos a ser baixado:\nEx 1-10 ou 1 10\n->: ')
    #     if capitulo:
    #         if '-' in capitulo:
    #             capitulo = capitulo.split('-')
    #             inicio = capitulo[0]
    #             fim = capitulo[1]
    #         elif ' ' in capitulo:
    #             capitulo = capitulo.split(' ')
    #             inicio = capitulo[0]
    #             fim = capitulo[1]
    #         elif ',' in capitulo:
    #             capitulo = capitulo.split(',')
    #             inicio = capitulo[0]
    #             fim = capitulo[1]
    #         else:
    #             inicio = capitulo
    #             fim = capitulo

    #         if inicio > fim:
    #             inicio, fim = fim, inicio

    #         capitulo = str(float(inicio)) + "-" + str(float(fim))
    #         quantidadeCBR = iniciaDownload(
    #             'local_', nome, inicio, fim, servidor)
    #         print(quantidadeCBR)
