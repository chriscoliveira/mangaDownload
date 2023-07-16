# pip install pytelegrambotapi

import platform
from re import I
import shutil
from telebot import types
import telebot
import funcoes as funcoes
import logging
import os

# -*- coding: utf-8 -*-


# numero maximo permitido de download por solicitação
numeroMaximoDownload = 10

# identifica o sistema operacional do servidor e define a pasta de download
sistema = platform.system()
if sistema == 'Windows':
    folder = 'Download\\'
else:
    folder = 'Download/'


# API_TOKEN = '1641410313:AAE4pAf4se3EvdD7-INkfiUhgCVHZjLdeVE'  # bot teste
with open('token.txt', 'r') as f:
    API_TOKEN = f.read()
    print(API_TOKEN)

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['ajuda', 'help'])
# funcao de ajuda para o usuario
def ajuda(message):
    msg = bot.reply_to(
        message, f'Para iniciar o bot use /baixar\n\nPara Ler os Mangas recomendo utilizar o programa ComicScreen https://play.google.com/store/apps/details?id=com.viewer.comicscreen')


@bot.message_handler(commands=['log'])
# funcao de envio de log para o usuario
def log(message):
    if message.chat.id == 769723764:
        with open('logManga.log', 'r') as log:
            msg = bot.send_document(
                769723764, document=open('logManga.log', 'rb'))


@bot.message_handler(commands=['novo'])
# funcao de envio de log para o usuario
def novo(message):
    if message.chat.id == 769723764:
        bot.reply_to(
            message, 'Aguarde, vou buscar os ultimos capitulos dos preferidos...')
        funcoes.buscaPreferidos(message.chat.id)
        with open('novo.txt', 'r', encoding='utf-8') as file1:
            linhas = file1.readlines()
            for line in linhas:
                bot.sendMessage(
                    id, f'{line.split(",")[0]} {line.split(",")[2]}')


@bot.message_handler(commands=['comecar', 'start', 'buscar', 'buscar manga', 'pesquisar', 'baixar', 'BuscarManga'])
# comando inicial do bot
def buscaManga(message):
    print('buscaManga')
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

    bot.register_next_step_handler(msg, exibeServidores)


def exibeServidores(message):
    print('exibeServidores')
    # recebe o nome do seridor escolhido
    id = message.chat.id
    manga = str(message.text).lower()
    bot.send_message(id, f'Aguarde! Buscando o mangá...')
    with open('logManga.log', 'a') as logger:
        logger.write(
            f'\nINFO:{message.date} {message.chat.id} - {message.from_user.first_name} - Pesquisa manga: {manga}')

    # faz uma pesquisa no servidor escolhido
    x = funcoes.busca_manga(id, manga)
    print(f'{x=}')
    if len(x) > 0:
        lista_enum = [f'{i+1}. {elem}' for i, elem in enumerate(x)]
        lista = "\n".join(lista_enum)
        lista = lista.replace(';', ' -> ')

        msg = bot.reply_to(
            message, f'Encontrei estes aqui!\n\n{lista}\n\nDigite o numero do manga desejado =)', parse_mode='Markdown')
        bot.register_next_step_handler(msg, procuraCapitulos)
    else:
        bot.reply_to(
            message, f'Não foi encontrado nenhum mangá com esse nome, verifique o nome e pesquise novamente\n/buscar', parse_mode='Markdown')
        bot.register_next_step_handler(msg, buscaManga)


def procuraCapitulos(message):
    print('procuraCapitulos')
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

    with open('logManga.log', 'a') as logger:
        logger.write(
            f'\nINFO:{message.date} {message.chat.id} - {message.from_user.first_name} - Manga escolhido: {titulo}')

    if link_manga:
        capitulos = funcoes.busca_capitulos(id, link_manga, fonte)
        bot.send_photo(id, open(f'TXT/{id}capa.jpg', 'rb'))
        # bot.send_message(id, +'\n\nDigite o número dos capítulos do mangá para baixar, Ex: 1-10\nLimite maximo de 10 capítulos por vez')

        stringcap = capitulos.split(' ')
        listacap = []
        contadorcap = 0
        nova_listacap = False
        textocap = []
        for i in stringcap:
            if contadorcap + len(i) < 3000:
                contadorcap += len(i)
                textocap.append(i)
            else:
                if not nova_listacap:
                    nova_listacap = True
                    listacap.append(textocap)
                    textocap = []
                contadorcap = 0
                textocap.append(i)
        listacap.append(textocap)

        if len(listacap) > 1:
            msg = bot.send_message(id, f'''Encontrei os capitulos\n*{" ".join(listacap[0])}*''',
                                   parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())

            msg = bot.send_message(id, f'''*{" ".join(listacap[1])}*\n\nDigite qual capitulo deseja:\nExemplo1 : \n1\nExemplo2 :\n1-5\n\nObs o limite de capitulos é de *{numeroMaximoDownload}*''',
                                   parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())
        else:
            msg = bot.reply_to(message, f'''Encontrei os capitulos\n*{capitulos}*\n\nDigite qual capitulo deseja:\nExemplo1 : \n1\nExemplo2 :\n1-5\n\nObs o limite de capitulos é de *{numeroMaximoDownload}*''',
                               parse_mode='Markdown', reply_markup=telebot.types.ReplyKeyboardRemove())

        with open(f'TXT/{id}mangaescolhido.txt', 'w') as escolhido:
            escolhido.write(f'{fonte};{titulo}')

    bot.register_next_step_handler(msg, baixarManga)


def baixarManga(message):
    print('baixarManga')
    capitulo = message.text
    chat_id = message.chat.id

    bot.send_message(
        message.chat.id, f'Aguarde! Baixando o manga... Este processo pode demorar de acordo com a quantidade de capitulos\n*TENHA PACIENCIA!*', parse_mode='Markdown')

    # verifica o mangá escolhido
    with open(f'TXT/{message.chat.id}mangaescolhido.txt', 'r') as fmanga:
        fmanga = fmanga.read()
        servidor, manga = fmanga.split(';')

    with open('logManga.log', 'a') as logger:
        logger.write(
            f'\nINFO:{message.date} {message.chat.id} - {message.from_user.first_name} - Download manga: {manga}, capitulos {capitulo} em {servidor}')

    # define os capitulos escolhidos separando com '-' ' ' e ','
    # e atribui a variavel inicio e fim
    if '-' in capitulo:
        capitulo = capitulo.split('-')
        inicio = capitulo[0]
        fim = capitulo[1]
    elif ' ' in capitulo:
        capitulo = capitulo.split(' ')
        inicio = capitulo[0]
        fim = capitulo[1]
    elif ',' in capitulo:
        capitulo = capitulo.split(',')
        inicio = capitulo[0]
        fim = capitulo[1]
    else:
        inicio = capitulo
        fim = capitulo

    print(f'{inicio=}, {fim=}')
    if float(inicio) > float(fim):
        inicio, fim = fim, inicio
    print(f'{inicio=}, {fim=}')
    capitulo = str(float(inicio)) + "-" + str(float(fim))
    # calcula o numero de capitulos a serem baixados
    calculo = float(fim) - float(inicio)
    if message.chat.id == 769723764:
        numeroMaximoDownload = 15
    else:
        numeroMaximoDownload = 10
    # verifica se o numero de capitulos a serem baixados e menor ou igual ao limite
    if calculo <= (numeroMaximoDownload-1):
        # grava o log
        with open('logManga.log', 'a') as logger:
            logger.write(
                f'\nINFO:{message.date} {message.chat.id} - {message.from_user.first_name} - Download manga: {manga}, capitulos {capitulo} em {servidor}')
        print(
            f'{message.chat.id} - Baixando os capitulos {inicio} a {fim} de {manga} em {servidor}')
        bot.send_message(
            message.chat.id, f'Baixando capitulos de *{inicio} a {fim}* do mangá, aguarde...', parse_mode='Markdown')

        # faz o download dos capitulos escolhidos
        quantidadeCBR = funcoes.iniciaDownload(
            str(chat_id), manga, inicio, fim, fonte=servidor)
        print(quantidadeCBR)
        try:
            # teclado rapido para voltar ao inicio do bot
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('/baixar')

            # dependendo do sistema operacional envia os arquivos de acordo com a pasta
            # if sistema == 'Windows':
            #     bot.send_document(chat_id, document=open(
            #         f'{folder}{chat_id}\\{manga}_capitulo_{capitulo}.cbr', 'rb'))

            #     bot.send_message(
            #         chat_id, f'Download concluido! Para baixar outros capitulos, execute o comando */baixar*', reply_markup=markup, parse_mode='Markdown')
            # else:

            for i in quantidadeCBR:
                if sistema == 'Windows':
                    i = str(i).replace('\\', '/')
                    print(f'arquivo {i=}')
                try:
                    # faz uma copia do arquivo localmente
                    # arquivo = f'{folder}{chat_id}/{manga}_capitulo_{capitulo}_{i}.cbr'
                    # shutil.copy(i, 'backup')

                    # envia o arquivo para o telegram
                    print(f'arquivo {i}')
                    bot.send_document(
                        chat_id, document=open(i, 'rb'), timeout=20)
                    # msg = bot.send_message(
                    #     769723764, f'Enviado o arquivo {i} para {chat_id} {message.from_user.first_name}')
                except Exception as e:
                    print(f'erro ao enviar o arquivo: {e}')
                    logger.write(
                        f'\nERROR:{message.date} - {e} - Erro ao enviar o arquivo.\n Tente novamente\n/buscar')

            bot.send_message(
                chat_id, f'Download concluido! Para baixar outros capitulos, execute o comando */baixar* ', reply_markup=markup, parse_mode='Markdown')
            # grava o log
            with open('logManga.log', 'a') as logger:
                logger.write(
                    f'\nINFO:{message.date} {message.chat.id} - {message.from_user.first_name} - Arquivo enviado {manga}_capitulo_{capitulo}_{i}.cbr')

        except Exception as e:
            print(e)
            # grava o log
            with open('logManga.log', 'a') as logger:
                logger.write(
                    f'\nERROR:{message.date} Erro ao enviar o arquivo: {e}')
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('/baixar')
            bot.send_message(
                chat_id, f'Ocorreu um erro ao enviar o arquivo\n\nexecute o comando */baixar* para reiniciar o processo..', reply_markup=markup, parse_mode='Markdown')
        # selecionaServidorManga(message)
    else:
        # grava o log
        with open('logManga.log', 'a') as logger:
            logger.write(
                f'\nWARNING:{message.date} {message.chat.id} - {message.from_user.first_name} - Numero de capitulos a serem baixados excede o limite: {numeroMaximoDownload}')
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('/baixar')
        msg = bot.reply_to(
            message, f'*O limite de capitulos é de {numeroMaximoDownload} por vez, e voce colocou {calculo}, execute o comando /baixar para reiniciar o processo..*', parse_mode='Markdown', reply_markup=markup)
        procuraCapitulos(msg)


bot.infinity_polling()
