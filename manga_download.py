#  C:\Users\Christian\AppData\Roaming\Python\Python310\Scripts\pyinstaller.exe -F --console -w --upx-dir=D:\upx-4.0.2-win64 --distpath .\ --ico ..\icone.ico -c --name "MangaDownloader 2023" .\manga_download.py

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QWidget, QFormLayout
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QFont
import os
import sys
from datetime import *
from layout import *
import funcoes
from threading import Thread
import platform

sistema = platform.system()
# busca o manga
if sistema == 'Windows':
    class Novo(QMainWindow, Ui_MainWindow):
        def __init__(self, parent=None):
            super().__init__(parent)
            super().setupUi(self)
            try:
                os.mkdir('TXT')
            except:
                pass
            try:
                os.mkdir('Baixados')
            except:
                pass
            try:
                os.mkdir('Download')
            except:
                pass

            self.anime = ''
            self.serv = ''
            self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)

            self.ed_nome.setFocus()
            self.bt_pesquisar.clicked.connect(lambda: self.buscaManga())
            self.lista_animes.itemDoubleClicked.connect(
                lambda: self.buscaCap())
            self.pushButton_2.clicked.connect(lambda: self.baixaCap())

        def buscaManga(self):
            self.lbl_pic.clear()
            self.ed_fim.setText('')
            self.ed_inicio.setText('')
            self.tx_capitulos.clear()
            self.statusbar.showMessage(
                'Aguarde enquanto estou buscando o Manga')
            t = Thread(target=self.buscaMangas)
            t.start()

        def buscaMangas(self):

            nome = self.ed_nome.text()

            if not nome == '':
                # self.frame_lista_animes.show()
                self.lista_animes.clear()
                funcoes.busca_manga('mangaDownloader', nome)
                # verifica o resultado
                lista_encontrado = []
                contador = 1

                with open(f'TXT/mangaDownloaderlista_manga.txt', 'r') as encontrado:
                    encontrado = encontrado.readlines()

                    for item in encontrado:
                        titulo, servidor, *link = item.split(';')
                        if self.rb_yabu.isChecked():
                            if 'mangayabu' in servidor:
                                lista_encontrado.append([titulo, link])
                        elif self.rb_scan.isChecked():
                            if 'scanlator' in servidor:
                                lista_encontrado.append([titulo, link])
                        elif self.rb_muito.isChecked():
                            if 'muito manga' in servidor:
                                lista_encontrado.append([titulo, link])
                        elif self.rb_union.isChecked():
                            if 'union' in servidor:
                                lista_encontrado.append([titulo, link])
                for i in lista_encontrado:
                    # print(i[0], i[1])
                    self.lista_animes.addItem(i[0])
                if len(lista_encontrado) > 0:
                    self.statusbar.showMessage(
                        'Dê um duplo clique no manga para exibir os capitulos')
                else:
                    self.statusbar.showMessage(
                        'Nenhum manga foi encontrado com esse nome')

        def buscaCap(self):
            # self.frame_lista_cap.show()
            # self.plainTextEdit.clear()
            self.statusbar.showMessage('Buscando os capítulos disponiveis...')
            t = Thread(target=self.buscaCaps)
            t.start()

        def buscaCaps(self):
            self.anime = self.lista_animes.currentItem().text()

            if self.rb_yabu.isChecked():
                self.serv = 'mangayabu'
            elif self.rb_scan.isChecked():
                self.serv = 'scanlator'
            elif self.rb_muito.isChecked():
                self.serv = 'muito manga'
            elif self.rb_union.isChecked():
                self.serv = 'union'

            with open(f'TXT/mangaDownloaderlista_manga.txt', 'r') as encontrado:
                encontrado = encontrado.readlines()

                for item in encontrado:
                    titulo, servidor, *link = item.split(';')
                    if self.serv in servidor:
                        if self.anime == titulo:
                            caminho = link[0]
                            local = self.serv
            self.exibeCaps(caminho, local)

        def exibeCaps(self, link, serv):

            capitulos = funcoes.busca_capitulos(
                'mangaDownloader', str(link).replace('\n', ''), serv)
            capp = ''
            with open('TXT/mangaDownloaderlista_capitulos.txt', 'r') as lista:
                lista = lista.readlines()

                for i in lista:
                    capp += ', '+i.split(',')[0]

            # print(capp)
            self.tx_capitulos.insertPlainText('-'+capp)
            # print(type(capp))
            # self.tx_capitulos.insertPlainText(capp)

            pixmap = QPixmap('TXT\\mangaDownloadercapa.jpg')
            self.lbl_pic.setPixmap(pixmap)
            self.lbl_pic.setScaledContents(True)
            self.statusbar.showMessage(
                'Digite o inicio e fim dos capítulos desejados e clique em Baixar')

        def baixaCap(self):
            self.statusbar.showMessage('Aguarde enquanto é feito o download')
            t = Thread(target=self.baixaCaps, args=(
                self.anime, self.ed_inicio.text(), self.ed_fim.text(), self.serv))
            t.start()

        def baixaCaps(self, manga, inicio, fim, servidor):
            # print('mangaDownloader', manga, inicio, fim, servidor)
            quantidadeCBR = funcoes.iniciaDownload(
                'mangaDownloader', manga, inicio, fim, fonte=servidor, prog=True)
            self.statusbar.showMessage('')
            # self.plainTextEdit.clear()
            self.ed_fim.setText('')
            self.ed_fim.setText('')
            # self.frame_lista_animes.hide()
            # self.frame_lista_cap.hide()
            self.ed_nome.setFocus()

    qt = QApplication(sys.argv)

    novo = Novo()
    novo.show()
    qt.exec_()

else:
    while True:
        manga = input(f'{"#"*20}\nDigite o nome do manga a pesquisar: ')
        print(f'\nAguarde enquando pesquiso o manga: "{manga}"')
        encontrados = funcoes.busca_manga('mangaDownloader', manga)

        if encontrados:
            contador = 1
            servidor_ = '.'
            for i in encontrados:
                nome, servidor = str(i).split(';')
                if servidor != servidor_:
                    print("\nServidor: "+str(servidor).upper())
                    servidor_ = servidor
                print(f'{contador}-> {nome}')
                contador += 1
            escolhido = input('\n\nDigite o numero do manga escolhido: ')
        if escolhido:
            print('\nProcurando os capítulos disponiveis...')
            with open('TXT/mangaDownloaderlista_manga.txt', 'r') as r:
                r = r.readlines()
                nome, servidor, link = r[int(escolhido)-1].split(';')

                print('\nEncontrei os seguintes capítulos:')
                print(funcoes.busca_capitulos(
                    'mangaDownloader_', link, servidor))
            capitulo = input(
                'Digite o intervalo de capítulos a ser baixado:\nEx 1-10 ou 1 10\n->: ')
        if capitulo:
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

            if inicio > fim:
                inicio, fim = fim, inicio

            capitulo = str(float(inicio)) + "-" + str(float(fim))
            quantidadeCBR = funcoes.iniciaDownload(
                'mangaDownloader_', nome, inicio, fim, servidor)
            print(quantidadeCBR)
