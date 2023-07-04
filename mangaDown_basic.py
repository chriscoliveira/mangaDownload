import os
import funcoes
from threading import Thread


def criaPastas():
    try:
        os.mkdir('Baixados')
    except:
        pass
    try:
        os.mkdir('Download')
    except:
        pass
    try:
        os.mkdir('TXT')
    except:
        pass


criaPastas()


def exibeServidor(link):
    if 'union' in link:
        opcao = 'union'
    elif 'scanlator' in link:
        opcao = 'scanlator'
    elif 'muitomanga' in link:
        opcao = 'muito manga'
    elif 'mangayabu' in link:
        opcao = 'magayabu'
    elif 'firemangas' in link:
        opcao = 'firemangas'
    return opcao


def buscaManga(manga: str, servidor: str):

    funcoes.busca_manga('', manga, servidor)
    encontrado = False
    with open(f'TXT/lista_manga.txt', 'r') as encontrado:
        encontrado = encontrado.readlines()
    return encontrado


def buscaCapitulos(link: str):

    opcao = exibeServidor(link)

    funcoes.busca_capitulos('', link, opcao)

    capp = ''
    with open(f'TXT/lista_capitulos.txt', 'r') as lista:
        lista = lista.readlines()
        for i in lista:
            # print(i)
            capp += ', '+i.split(',')[0]

    return capp


while True:
    # inicia
    print(f'\n\n{"#"*30}\nMangá Downloader\n{"#"*30}\n\n')
    manga = input("Digite o nome do manga a pesquisar: ")
    servidor = input(
        "Em qual servidor quer buscar:\n1 - Union Manga\n2 - Muito Manga\n3 - Project Scanlator\n0 - Sair\n: ")
    try:
        if servidor == "1":
            servidor = "union"
        elif servidor == "2":
            servidor = "muito manga"
        elif servidor == "3":
            servidor = "scanlator"
        else:
            break
    except:
        print("Opção inválida")

    # busca o manga
    resultado = buscaManga(manga, servidor)
    if not resultado == False:
        cont = 1
        for i in resultado:
            print(f'{cont} - {i.split(";")[0]}')
            cont += 1

        numeroCap = input("\n\nDigite o número da opção desejada: ")

        # busca os capitulos
        try:
            caps = buscaCapitulos(
                link=resultado[int(numeroCap)-1].split(";")[2])
            print(caps)
        except:
            print("Capitulo invalido")
            break

        # inicia o download
        numeroDownload = input(
            "\n\nDigite o número dos capitulos:\nEx: 1 (para baixar o captulo 1\nEx: 1-10 (para baixar do 1 ao 10)\n: ")
        manga = resultado[int(numeroCap)-1].split(";")[0]
        link = resultado[int(numeroCap)-1].split(";")[2]

        opcao = exibeServidor(link)

        try:
            inicio, fim = numeroDownload.split('-')
        except:
            inicio, fim = numeroDownload, numeroDownload
        print(f'\n\nIniciando o Download, aguarde...\n')
        funcoes.iniciaDownload('', manga, inicio, fim, opcao, prog=True)
        # os.startfile("Baixados")
    else:
        break
