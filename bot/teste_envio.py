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
with open('token.txt', 'r') as f:
    API_TOKEN = f.read()
    print(API_TOKEN)

# Dicionário para rastrear o estado do usuário
user_states = {}


def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        message = msg['text']

        if message == '/start':
            bot.sendMessage(chat_id, 'Digite o nome do manga')
            # Define o estado inicial do usuário como 'step1'
            user_states[chat_id] = 'step1'
            # bot.sendMessage(chat_id, 'Por favor, digite seu nome:')
        elif message == '/ajuda':
            bot.sendMessage(
                chat_id, f'Para iniciar o bot use /baixar\n\nPara Ler os Mangas recomendo utilizar o programa ComicScreen https://play.google.com/store/apps/details?id=com.viewer.comicscreen')
            bot.stop()
        else:
            handle_next_step(chat_id, message)


def handle_next_step(chat_id, message):
    # Obtém o estado atual do usuário
    state = user_states.get(chat_id)

    if state == 'step1':
        manga = message
        print(f'manga {manga}=')
        x = funcoes.iniciaBuscaManga(id, manga)
        print(f'{x=}')
        if len(x) > 0:
            lista_enum = [f'{i+1}. {elem}' for i, elem in enumerate(x)]
            lista = "\n".join(lista_enum)
            lista = lista.replace(';', ' -> ')
        bot.sendMessage(
            chat_id, f'Encontrei estes aqui!\n\n{lista}\n\nDigite o numero do manga desejado ')
        # Realiza a lógica para a etapa 1
        bot.sendMessage(chat_id, f'digite o numero do manga')
        # Atualiza o estado do usuário para 'step2'
        user_states[chat_id] = 'step2'
    elif state == 'step2':
        # Realiza a lógica para a etapa 2
        tipomanga = message
        print(f'manga {tipomanga}=')
        bot.sendMessage(chat_id, f'digite o capitulo')
        user_states[chat_id] = 'step3'
    elif state == 'step3':
        # Realiza a lógica para a etapa 2
        try:
            opcao = int(message)
            print(f'opcao {opcao}=')
            bot.sendMessage(chat_id, f'digite o inicio e fim')
            user_states[chat_id] = 'step4'
        except ValueError:
            bot.sendMessage(
                chat_id, 'Idade inválida. Por favor, digite um número inteiro.')
    elif state == 'step4':
        # Realiza a lógica para a etapa 2

        bot.sendMessage(chat_id, f'baixando')
        user_states[chat_id] = 'step4'

    else:
        bot.sendMessage(chat_id, 'Desculpe, não entendi o que você disse.')


bot = telepot.Bot('6211370557:AAGWzCnAhxT_xTEkNOtRS_GIjugnlPWdkvY')
MessageLoop(bot, handle_message).run_as_thread()

# Mantém o programa em execução
while True:
    pass
