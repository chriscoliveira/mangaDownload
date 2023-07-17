# import telepot

import telepot
from telepot.loop import MessageLoop

import platform
from re import I
import shutil
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
# with open('token.txt', 'r') as f:
#     API_TOKEN = f.read()
#     print(API_TOKEN)

# Dicionário para rastrear o estado do usuário
user_states = {}


def handle_message(msg):
    idusr = msg["chat"]['id']
    nomeusr = msg["chat"]['first_name']
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        message = msg['text']

        if message == '/start' or message == '/buscar' or message == '/baixar':
            bot.sendMessage(chat_id, f'Olá {nomeusr}, Digite o nome do manga')

            user_states[chat_id] = 'step1'

        elif message == '/ajuda':
            bot.sendMessage(
                chat_id, f'Para iniciar o bot use /baixar\n\nPara Ler os Mangas recomendo utilizar o programa ComicScreen https://play.google.com/store/apps/details?id=com.viewer.comicscreen')
            bot.stop()
        else:
            handle_next_step(chat_id, message)


def handle_next_step(chat_id, message):
    # Obtém o estado atual do usuário
    print(chat_id)
    state = user_states.get(chat_id)

    #########################################################################################
    # pesquisa o nome do manga
    #########################################################################################

    if state == 'step1':
        funcoes.limpaArquivos(chat_id, 'Download', 'jpg')
        manga = message
        bot.sendMessage(
            chat_id, 'Aguarde um momento enquanto faço uma pesquisa...')
        x = funcoes.iniciaBuscaManga(chat_id, manga)
        print(f'{x=}')
        if len(x) > 0:
            lista_enum = [f'{i+1}. {elem}' for i, elem in enumerate(x)]
            lista = "\n".join(lista_enum)
            lista = lista.replace(';', ' -> ')
            bot.sendMessage(
                chat_id, f'Encontrei estes aqui!\n\n{lista}\n\nDigite o numero do manga desejado ')
            user_states[chat_id] = 'step2'
        else:
            bot.sendMessage(
                chat_id, f'Não foi encontrado nenhum manga com esse nome.. \n/buscar')
            user_states[chat_id] = 'step1'
        # Atualiza o estado do usuário para 'step2'

    #########################################################################################
    # busca os capitulos do mangas
    #########################################################################################

    elif state == 'step2':
        try:
            numero = int(message)-1
            with open(f"TXT/{chat_id}lista_manga.txt") as f:
                resultadopesquisa = f.readlines()

            user_states['nome_manga'] = resultadopesquisa[numero].split(";")[0]
            user_states['servidor'] = resultadopesquisa[numero].split(";")[1]
            user_states['link_manga'] = resultadopesquisa[numero].split(";")[2]
            bot.sendMessage(chat_id, 'Pesquisando os capítulos disponiveis...')
            capitulosDisponiveis = funcoes.getCapitulosFromUrl(
                resultadopesquisa[numero].split(";")[2])
            listaDisponiveis = []

            for cap in capitulosDisponiveis:
                listaDisponiveis.append(
                    str(cap[1]).replace('Cap. ', ''))

            if len(listaDisponiveis) > 0:
                with open(f'TXT/{chat_id}listaDisponiveis.txt', 'w') as fh:
                    for line in capitulosDisponiveis:
                        fh.write(f'{line[1]};{line[0]}\n')
                bot.sendMessage(
                    chat_id, f'\nCapitulos encontrados:  {" ".join(listaDisponiveis)}\nDigite qual capitulo deseja:\nExemplo1 : \n1\nExemplo2 :\n1-5\n\nObs o limite de capitulos é de 10')
                user_states[chat_id] = 'step3'

            else:
                bot.sendMessage(
                    chat_id, "Nao foi encontrado nenhum capitulos, selecione uma das opções encontradas acima:")
                user_states[chat_id] = 'step2'

        except ValueError as e:
            bot.sendMessage(chat_id, 'Opção invalida! '+str(e))

    #########################################################################################
    # inicia o download
    #########################################################################################

    elif state == 'step3':
        # Realiza a lógica para a etapa 2
        nome_manga = user_states.get('nome_manga')
        link_manga = user_states.get('link_manga')
        servidor = user_states.get('servidor')
        print(nome_manga, servidor, link_manga)
        bot.sendMessage(chat_id, f'Aguarde o download dos arquivos, dependendo da quantidade de paginas este processo pode demorar um pouco... Por favor não envie outra solicitação, aguarde o termino.......')
        try:
            opcao = message
            print(f'opcao {opcao}=')
            try:
                inicio, fim = str(opcao).split('-')
            except:
                inicio, fim = opcao, opcao

            inicio = float(inicio)
            fim = float(fim)
            quantidade = fim - inicio
            if quantidade < 10:
                capsBaixados = False

                with open(f'TXT/{chat_id}listaDisponiveis.txt') as f:
                    f = f.readlines()
                listaDisponiveis = []
                for i in f:
                    listaDisponiveis.append(i.split(";"))

                print(inicio, fim, capsBaixados)
                # percorre a lista em busca dos capitulos para baixar
                cont = 0
                for i in listaDisponiveis:
                    atual = float(i[0])
                    if inicio <= atual <= fim:
                        capsBaixados = True
                        print(str(listaDisponiveis[cont][1]).strip())
                        funcoes.getImgFromUrl(chat_id, f'{user_states["nome_manga"]}_{atual}', servidor, str(
                            listaDisponiveis[cont][1]).strip())

                    cont += 1
                max_size = 45 * 1024 * 1024
                bot.sendMessage(chat_id, 'Compactando o manga, aguarde....')
                arquivos_enviar = funcoes.create_zip_files(
                    chat_id, f'{user_states["nome_manga"]}_{inicio}_{fim}', max_size)
                contagem = 0
                bot.sendMessage(chat_id, 'Enviando os arquivos CBR...')
                for i in arquivos_enviar:
                    bot.sendDocument(chat_id, document=open(i, 'rb'))
                    contagem += 1
                if contagem > 0:
                    bot.sendMessage(
                        chat_id, 'Todas as partes foram enviadas....\nEnvie o comando /buscar para uma nova pesquisa.')
                    user_states[chat_id] = 'step1'
                else:
                    bot.sendMessage(
                        chat_id, 'Ocorreu um erro....\nEnvie o comando /buscar para uma nova pesquisa.')
                    user_states[chat_id] = 'step1'
            else:
                bot.sendMessage(
                    chat_id, 'Limite de download é de 10 capítulos por vez, tente novamente')
                user_states[chat_id] = 'step3'
        except ValueError:
            bot.sendMessage(
                chat_id, 'Ocorreu um erro, tente novamente!\n\n/buscar')

    #########################################################################################
    #
    #########################################################################################

    else:
        bot.sendMessage(chat_id, 'Desculpe, não entendi o que você disse.')


# bot = telepot.Bot('6211370557:AAGWzCnAhxT_xTEkNOtRS_GIjugnlPWdkvY')
bot = telepot.Bot('5301844040:AAHCF19e3PwfBUeEbiWlVKdWls6MRdA9dDc')
MessageLoop(bot, handle_message).run_as_thread()

# Mantém o programa em execução
while True:
    pass
