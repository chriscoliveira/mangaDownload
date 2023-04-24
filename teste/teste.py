import re
import platform
from re import I
import shutil
from telebot import types
import telebot
import logging
import os
import requests
import os
import zipfile
from natsort import natsorted
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import time
from playwright.sync_api import sync_playwright

# -*- coding: utf-8 -*-


# numero maximo permitido de download por solicitação
numeroMaximoDownload = 10

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36'}


def manga(id, manga_name):
    fonte = ['union', 'scanlator', 'muito manga']
    # fonte = ['scanlator']
    try:
        os.remove(f'TXT\\{id}lista_manga.txt')
    except:
        print('nao removido')
    for i in fonte:
        pesquisa_manga(id, manga_name, i)


def pesquisa_manga(id, manga_name, fonte):
    # de acordo com a fonte acessa o site
    tag = 'div'
    if fonte == 'union':
        site = 'https://unionleitor.top/lista-mangas'
        blocomangas = 'select2-results__option'
        tag = 'li'

    elif fonte == 'scanlator':
        site = f'https://projetoscanlator.com/?s={manga_name}&post_type=wp-manga&op=&author=&artist=&release=&adult='
        blocomangas = 'tab-summary'

    elif fonte == 'muito manga':
        site = f'https://muitomanga.com/buscar?q={manga_name}'
        blocomangas = 'boxAnimeSobreLast'

    try:
        # abre o navegador
        with sync_playwright() as p:
            browser = p.chromium.launch(
                channel='chrome', headless=True)
            page = browser.new_page()

            page.goto(site, timeout=0)

            # caso for do mangayabu faz a pesquisa
            if fonte == 'union':
                page.click('input[id="pesquisa"]')
                page.fill('input[class="select2-search__field"]', manga_name)

            time.sleep(2)
            mangas_encontrados = page.content()
            page.close()

            # faz o scrap da pagina
            mangas_encontrados = BeautifulSoup(
                mangas_encontrados, 'html.parser')

            with open('html.txt', 'w', encoding='utf-8') as f:
                f.write(mangas_encontrados.prettify())

            with open(f'TXT/{id}lista_manga.txt', 'a+') as f:
                for manga in mangas_encontrados.find_all(tag, {'class': blocomangas}):
                    # print(str(manga))
                    if fonte == 'union':
                        try:
                            link = manga.find('a').get('href')
                            nome = str(manga.text).replace(
                                'Autor:', '||').split('||')[0]
                            print(link, nome, sep='\n')
                        except:
                            print('falha ao pesquisar em '+fonte +
                                  '\nFECHE O PROGRAMA E TENTE NOVAMENTE')

                    elif fonte == 'scanlator':
                        try:
                            link = manga.find('a').get('href')
                            nome = manga.find(
                                'h3', {'class': 'h4'}).text.strip().replace(':', '')
                            print(link, nome)
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


def capturarCapitulosManga(url):
    # Fazer solicitação HTTP para a página web
    print(url)
    response = requests.get(url)

    # Analisar o HTML da página web
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar todos os links dos capítulos disponíveis
    capitulos = []
    for link in soup.find_all('a'):
        print(link.get('href'))
        # union
        if 'union' in link.get('href') and 'Cap.' in link.text:
            capitulos.append((link.text, link.get('href')))
            print('union')

        # muito manga
        elif 'muito' in link.get('href') and '#' in link.text:
            capitulos.append(
                (link.text, 'https://muitomanga.com/'+link.get('href')))
            print('muito manga')

        # scanlator
        elif 'projeto' in link.get('href') and 'Capítulo' in link.text:
            capitulos.append(
                (str(link.text).split(' ')[1], link.get('href')))
            print('scanlator')

    # Imprimir os links dos capítulos disponíveis
    resultado = []
    for capitulo in capitulos:
        cap, _link = capitulo[0], capitulo[1]
        print(cap)
        resultado.append((cap.split(' ')[1], _link))
    print(resultado)
    return resultado


def baixaImagens(url, manga, capitulo):
    # Pasta onde as imagens serão salvas
    pasta = 'imagens'

    # Criar pasta se ela não existir
    if not os.path.exists(pasta):
        os.makedirs(pasta)

    # Adicionar cabeçalho de agente do usuário à solicitação HTTP
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Fazer solicitação HTTP para a página web
    response = requests.get(url, headers=headers)

    # Analisar o HTML da página web
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar as URLs das imagens
    imagens = []

    ###########################################################################
    # verifica qual site esta tratando a página

    # union
    if 'unionleitor' in response.text:
        for img in soup.find_all('img', class_='img-responsive'):
            imagens.append(img.get('src'))

    # muito manga
    elif 'muitomanga' in response.text:
        pattern = r'var imagens_cap = \[(.*?)\];'
        result = re.search(pattern, response.text, re.DOTALL)

        if result:
            links_string = result.group(1)
            links = re.findall(r'"(.*?)"', links_string)
            for link in links:
                link_corrigido = link.replace('\\/', '/').replace('\\', '')
                imagens.append(link_corrigido)

    # projecscanlator
    elif 'Scanlator' in response.text:
        for img in soup.find_all('img', {'class': 'wp-manga-chapter-img'}):
            imagens.append(img.get('data-src'))

    print(imagens)

    ###########################################################################
    # Baixar as imagens
    for i, imagem_url in enumerate(imagens):
        print(i, imagem_url)
        # define o nome do arquivo de imagem
        nome_arquivo = f"{manga}_{capitulo}_{i+1}.jpg"
        # baixa a imagem e salva com o nome definido
        response = requests.get(imagem_url)
        with open(f'imagens\{nome_arquivo}', "wb") as f:
            f.write(response.content)

    ###########################################################################
    compactar1(manga, capitulo)


def compactar1(manga, capitulo):
    # Define o diretório a ser compactado e o nome base do arquivo ZIP resultante
    diretorio = "imagens"
    nome_base_arquivo_zip = f"{manga}_{capitulo}"

    arquivosCompactados = []
    # Define o tamanho máximo de cada arquivo em bytes (40MB)
    tamanho_maximo_arquivo = 40 * 1024 * 1024

    # Variáveis para controlar o tamanho do arquivo ZIP atual
    tamanho_arquivo_atual = 0
    numero_arquivo_atual = 1

    # Abre o primeiro arquivo ZIP para escrita
    nome_arquivo_zip = f"Baixados\\{nome_base_arquivo_zip}_{numero_arquivo_atual}.cbr"
    arquivosCompactados.append(nome_arquivo_zip)
    zip_atual = zipfile.ZipFile(nome_arquivo_zip, "w")

    lista = natsorted(os.listdir(diretorio))
    # Percorre todos os arquivos do diretório
    for nome_arquivo in lista:
        print(nome_arquivo)
        # Verifica se o arquivo é uma imagem
        if nome_arquivo.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):

            # Verifica o tamanho do arquivo
            tamanho_arquivo = os.path.getsize(
                os.path.join(diretorio, nome_arquivo))

            # Verifica se o tamanho do arquivo é menor ou igual ao tamanho máximo permitido
            if tamanho_arquivo <= tamanho_maximo_arquivo:

                # Verifica se o tamanho do arquivo atual mais o tamanho do novo arquivo é menor ou igual ao tamanho máximo permitido
                if tamanho_arquivo_atual + tamanho_arquivo <= tamanho_maximo_arquivo:

                    # Adiciona o arquivo ao ZIP atual e atualiza o tamanho do arquivo atual
                    zip_atual.write(os.path.join(diretorio, nome_arquivo))
                    tamanho_arquivo_atual += tamanho_arquivo

                else:
                    # Fecha o arquivo ZIP atual e cria um novo arquivo ZIP para os próximos arquivos
                    zip_atual.close()
                    numero_arquivo_atual += 1
                    nome_arquivo_zip = f"Baixados\\{nome_base_arquivo_zip}_{numero_arquivo_atual}.cbr"
                    arquivosCompactados.append(nome_arquivo_zip)
                    zip_atual = zipfile.ZipFile(nome_arquivo_zip, "w")
                    zip_atual.write(os.path.join(diretorio, nome_arquivo))
                    tamanho_arquivo_atual = tamanho_arquivo

            else:
                print(
                    f"O arquivo '{nome_arquivo}' excede o tamanho máximo permitido e não será incluído no ZIP.")

    # Fecha o último arquivo ZIP
    zip_atual.close()
    return arquivosCompactados


API_TOKEN = '6082868921:AAGckIy4nfdYs3ex-iesguq9XGICGeiB4VM'  # bot teste
# with open('token.txt', 'r') as f:
#     API_TOKEN = f.read()

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['ajuda', 'help'])
# funcao de ajuda para o usuario
def ajuda(message):
    msg = bot.reply_to(
        message, f'Para iniciar o bot use /baixar\n\nPara Ler os Mangas recomendo utilizar o programa ComicScreen https://play.google.com/store/apps/details?id=com.viewer.comicscreen')


@bot.message_handler(commands=['comecar', 'start', 'buscar', 'buscar manga', 'pesquisar', 'baixar', 'BuscarManga'])
# comando inicial do bot
def botBuscaManga(message):
    novo = False
    # verifica se é o primeiro uso do bot
    with open('usuarios.txt', 'r+') as usuarios:
        usuario = usuarios.readlines()
        for i in usuario:
            if not str(message.chat.id) in i:
                novo = True
        if novo:
            usuarios.write(str(message.chat.id)+'\n')
    # define o teclado para selecionar o servidor
    msg = bot.reply_to(
        message, f'Olá {message.from_user.first_name}, bem vindo ao meu bot!\nDigite o nome do mangá', parse_mode='Markdown')

    # me avisa toda vez que o usuario entrar no bot
    # if message.chat.id != 769723764:
    #     aviso = bot.send_message(
    #         769723764, f'{message.from_user.first_name} {message.from_user.last_name} entrou no bot')

    bot.register_next_step_handler(msg, botProcuraManga)


def botProcuraManga(message):
    # recebe o nome do seridor escolhido
    id = message.chat.id
    nomeManga = str(message.text).lower()
    bot.send_message(id, f'Aguarde! Buscando o mangá...')
    with open('logManga.log', 'a') as logger:
        logger.write(
            f'\nINFO: {message.chat.id} - {message.from_user.first_name} - Pesquisa manga: {nomeManga}')

    # faz uma pesquisa no servidor escolhido
    lista = manga(id, nomeManga)

    # verifica o resultado
    lista_encontrado_union = []
    lista_encontrado_scan = []
    lista_encontrado_muit = []
    contador = 1

    with open(f'TXT/{id}lista_manga.txt', 'r') as encontrado:
        encontrado = encontrado.readlines()

        for item in encontrado:
            titulo, servidor, *link = item.split(';')

            if 'union' == servidor:
                lista_encontrado_union.append([titulo, link])
            elif 'scanlator' == servidor:
                lista_encontrado_scan.append([titulo, link])
            elif 'muito manga' == servidor:
                lista_encontrado_muit.append([titulo, link])

    # cria a mensagem com os mangas
    txt_envio = ''
    if len(lista_encontrado_union) > 0:
        txt_envio = '*Servidor: Union*\n'
        for i in lista_encontrado_union:
            txt_envio += f'*{contador}* - {i[0]}\n'
            contador += 1

    if len(lista_encontrado_scan) > 0:
        txt_envio += '\n\n*Servidor: Project Scanlator*\n'
        for i in lista_encontrado_scan:
            txt_envio += f'*{contador}* - {i[0]}\n'
            contador += 1

    if len(lista_encontrado_muit) > 0:
        txt_envio += '\n\n*Servidor: Muito Mangá*\n'
        for i in lista_encontrado_muit:
            txt_envio += f'*{contador}* - {i[0]}\n'
            contador += 1
    if len(lista_encontrado_union) > 0 or len(lista_encontrado_scan) > 0 or len(lista_encontrado_muit) > 0:
        bot.send_message(
            id, f'{txt_envio}\n\nDigite o número referente ao mangá desejado', parse_mode='Markdown')
        bot.register_next_step_handler(message, botProcuraLocalizaCapitulos)
    else:
        with open('logManga.log', 'a') as logger:
            logger.write(
                f'\nERRO: {message.chat.id} - {message.from_user.first_name} - Manga não encontrado: {manga}')
        bot.reply_to(
            message, f'{txt_envio}\n\nNão foi encontrado nenhum mangá com esse nome, verifique o nome e pesquise novamente\n/buscar', parse_mode='Markdown')


def botProcuraLocalizaCapitulos(message):
    # recebe o nome do seridor escolhido
    id = message.chat.id
    numManga = str(message.text).lower()
    bot.send_message(
        message.chat.id, f'Localizando os capitulos disponiveis, aguarde um momento...')

    with open(f'TXT/{id}lista_manga.txt', 'r') as link:
        link = link.readlines()
        titulo = link[int(numManga)-1].split(';')[0]
        link_manga = link[int(numManga)-1].split(';')[2]
        fonte = link[int(numManga)-1].split(';')[1]

    print(titulo, link_manga, fonte)

    with open('logManga.log', 'a') as logger:
        logger.write(
            f'\nINFO: {message.chat.id} - {message.from_user.first_name} - Manga escolhido: {titulo}')

    if link_manga:
        capitulos = capturarCapitulosManga(link_manga)
        print(capitulos)
        capEncontrado = ''
        for i in capitulos:
            capEncontrado += f'{i[0]}, '
        print(capEncontrado)
    #     bot.send_photo(id, open(f'TXT/{id}capa.jpg', 'rb'))
        # bot.send_message(id, +'\n\nDigite o número dos capítulos do mangá para baixar, Ex: 1-10\nLimite maximo de 10 capítulos por vez')

    #     stringcap = capitulos.split(' ')
    #     listacap = []
    #     contadorcap = 0
    #     nova_listacap = False
    #     textocap = []
    #     for i in stringcap:
    #         if contadorcap + len(i) < 3000:
    #             contadorcap += len(i)
    #             textocap.append(i)
    #         else:
    #             if not nova_listacap:
    #                 nova_listacap = True
    #                 listacap.append(textocap)
    #                 textocap = []
    #             contadorcap = 0
    #             textocap.append(i)
    #     listacap.append(textocap)

    #     if len(listacap) > 1:
    #         msg = bot.send_message(id, f'''Encontrei os capitulos\n*{" ".join(listacap[0])}*''',
    #                                parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())

    #         msg = bot.send_message(id, f'''*{" ".join(listacap[1])}*\n\nDigite qual capitulo deseja:\nExemplo1 : \n1\nExemplo2 :\n1-5\n\nObs o limite de capitulos é de *{numeroMaximoDownload}*''',
    #                                parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())
    #     else:
    #         msg = bot.reply_to(message, f'''Encontrei os capitulos\n*{capitulos}*\n\nDigite qual capitulo deseja:\nExemplo1 : \n1\nExemplo2 :\n1-5\n\nObs o limite de capitulos é de *{numeroMaximoDownload}*''',
    #                            parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())

    #     with open(f'TXT/{id}mangaescolhido.txt', 'w') as escolhido:
    #         escolhido.write(f'{fonte};{titulo}')

    # bot.register_next_step_handler(msg, baixarManga)


bot.infinity_polling()

# if __name__ == "__main__":
# capturarCapitulosManga('https://unionleitor.top/pagina-manga/one-piece')
# capturarCapitulosManga(
#     'https://projetoscanlator.com/manga/mashle-magic-and-muscles/')
# capturarCapitulosManga('https://unionleitor.top/manga/solo-leveling')

# capturarCapitulosManga('https://muitomanga.com/manga/one-piece')
# baixaImagens('https://unionleitor.top/leitor/One_Piece/1081',
#              'one-piece', '1081')
# baixaImagens('https://muitomanga.com/ler/one-piece/capitulo-1',
#              'one-piece', '1')
# baixaImagens('https://projetoscanlator.com/manga/mashle-magic-and-muscles/capitulo-152/',
#              'mashle', '152')
# print(compactar1('mashle', '152'))
# manga('id', 'mashle')
