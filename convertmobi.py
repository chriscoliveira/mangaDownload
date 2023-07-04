import subprocess
from docx import Document
from PIL import Image
import os
from natsort import natsorted


def listall(pasta, extensao):
    caminhos = [os.path.join(pasta, nome) for nome in os.listdir(pasta)]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    arq = natsorted(
        [arq for arq in arquivos if arq.lower().endswith(f".{extensao}")])

    return arq


def unzipp(arquivo):
    # importing the zipfile module
    from zipfile import ZipFile

    # loading the temp.zip and creating a zip object
    with ZipFile(arquivo, 'r') as zObject:

        # Extracting all the members of the zip
        # into a specific location.
        zObject.extractall(
            path="tem")


def convert_to_mobi(listaImagens, nome):
    doc = Document()

    # Adiciona cada imagem ao documento
    for imagem in listaImagens:
        doc.add_picture(imagem)

    # Salva o documento em .docx
    doc.save(f'{nome}.docx')

    # Converte o documento .docx em .mobi
    subprocess.call(['C:\Program Files\Calibre2\ebook-convert.exe',
                    f'{nome}.docx', f'{nome}.mobi'])
    os.remove(f'{nome}.docx')


try:
    os.mkdir('mobi')
except:
    pass

try:
    os.removedirs('temp')
except:
    pass

print("\n\n\nLista de Arquivos CBR Disponiveis para Conversao\n")
arquivos = listall('Baixados', 'cbr')
[print(i, j) for i, j in enumerate(arquivos)]

escolha = input("\nDigite o numero do arquivo: ")
# os.remove("temp")
unzipp(arquivos[int(escolha)])

imagens = listall("temp", "jpg")
print(imagens)
convert_to_mobi(imagens, f'{arquivos[int(escolha)]}')
