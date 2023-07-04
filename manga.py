import tkinter as tk
from tkinter import ttk
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


def limpaLista():
    for item in lsMangas.get_children():
        lsMangas.delete(item)


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


def pbuscaManga():
    t = Thread(target=buscaManga)
    t.start()


def buscaManga():
    # deleta o conteudo do componentes
    for item in lsMangas.get_children():
        lsMangas.delete(item)
    try:
        edCapitulos.delete('1.0', tk.END)
        edInicio.delete('1.0', tk.END)
        edFim.delete('1.0', tk.END)
    except:
        pass

    opcao = valor_radio.get()
    if opcao == 'Union Mangá':
        opcao = 'union'
    elif opcao == 'Project Scanlator':
        opcao = 'scanlator'
    elif opcao == 'Muito Mangá':
        opcao = 'muito manga'
    elif opcao == 'MangáYabu':
        opcao = 'magayabu'
    elif opcao == 'FireMangás':
        opcao = 'firemangas'

    limpaLista()

    funcoes.busca_manga('', edNomeManga.get(), opcao)

    with open(f'TXT/lista_manga.txt', 'r') as encontrado:
        encontrado = encontrado.readlines()

        for item in encontrado:
            titulo, servidor, *link = item.split(';')
            if opcao == 'mangayabu':
                if opcao in servidor:
                    lsMangas.insert("", tk.END, text=titulo, values=(link))
            elif opcao == 'scanlator':
                if opcao in servidor:
                    lsMangas.insert("", tk.END, text=titulo, values=(link))
            elif opcao == 'muito manga':
                if opcao in servidor:
                    lsMangas.insert("", tk.END, text=titulo, values=(link))
            elif opcao == 'union':
                if opcao in servidor:
                    lsMangas.insert("", tk.END, text=titulo, values=(link))
            elif opcao == 'firemangas':
                if opcao in servidor:
                    lsMangas.insert("", tk.END, text=titulo, values=(link))


def buscaCapitulos(event):

    item = lsMangas.selection()[0]  # obtem o item selecionado
    link = lsMangas.item(item)["values"][0]  # obtem o valor da coluna 2
    print(link)
    opcao = exibeServidor(link)

    funcoes.busca_capitulos('', link, opcao)

    capp = ''
    with open(f'TXT/lista_capitulos.txt', 'r') as lista:
        lista = lista.readlines()
        for i in lista:
            print(i)
            capp += ', '+i.split(',')[0]

    edCapitulos.delete("1.0", "end")
    edCapitulos.insert('1.0', capp)


def pbaixarCaps():
    t = Thread(target=baixarCaps)
    t.start()


def baixarCaps():
    item = lsMangas.selection()[0]  # obtem o item selecionado
    link = lsMangas.item(item)["values"][0]  # obtem o valor da coluna 2
    manga = str(lsMangas.item(item)["text"]).replace(':', '')
    opcao = exibeServidor(link)
#     t = Thread(target=tIniciaDown, args=(manga, opcao))
#     t.start()


# def tIniciaDown(manga, opcao):
    funcoes.iniciaDownload('', manga, edInicio.get(),
                           edFim.get(), opcao, prog=True)


def clique_botao():
    caminho = str(os.path.abspath(os.getcwd()) +
                  '\Baixados')
    caminho = caminho.replace("\\", "\\\\")
    try:
        os.startfile(caminho)
    except Exception as e:
        print("Error " + str(e))


# Cria a janela principal
janela = tk.Tk()
janela.title("Manga Download")

# Primeira linha
linha1 = tk.Frame(janela)
linha1.pack(fill=tk.X, padx=5, pady=5)

tk.Label(linha1, text="Nome Mangá:").pack(
    side=tk.LEFT, padx=5, pady=5,)
edNomeManga = tk.Entry(linha1, width=30, font='arial 14')
edNomeManga.pack(side=tk.LEFT, padx=5, pady=5)

btPesquisar = tk.Button(linha1, text="Pesquisar", command=pbuscaManga)
btPesquisar.pack(side=tk.LEFT, padx=5, pady=5)

btBaixados = tk.Button(linha1, text="Baixados", command=clique_botao)
btBaixados.pack(side=tk.LEFT, padx=5, pady=5)

# Segunda linha
linha2 = tk.Frame(janela)
linha2.pack(fill=tk.X, padx=5, pady=5)

tk.Label(linha2, text="Servidores:").pack(side=tk.LEFT, padx=5, pady=5)

opcoes = ["Union Mangá", "Muito Mangá", "Project Scanlator"]
valor_radio = tk.StringVar()
valor_radio.set(opcoes[0])

for opcao in opcoes:
    tk.Radiobutton(linha2, text=opcao, variable=valor_radio,
                   value=opcao).pack(side=tk.LEFT, padx=5, pady=5)

# Terceira linha
linha3 = tk.Frame(janela)
linha3.pack(fill=tk.X, padx=5, pady=5)

tk.Label(linha3, text="Mangás Encontrados:").pack(fill=tk.X, padx=5, pady=5)

lsMangas = ttk.Treeview(linha3, selectmode='browse')

vsb = ttk.Scrollbar(linha3, orient="vertical", command=lsMangas.yview)
vsb.pack(side='right', fill='y')

lsMangas.configure(yscrollcommand=vsb.set)

lsMangas["columns"] = ("col1")
lsMangas.heading("#0", text="Mangá")
lsMangas.column("#0", width=100)
lsMangas.heading("col1", text="Link")
lsMangas.column("col1", width=100)

lsMangas.pack(fill=tk.BOTH, padx=5, pady=5)

lsMangas.bind('<Double-1>', buscaCapitulos)

# Quarta linha
linha4 = tk.Frame(janela)
linha4.pack(fill=tk.X, padx=5, pady=5)

tk.Label(linha4, text="Capítulos Disponíveis:").pack(
    fill=tk.X, padx=5, pady=5)


edCapitulos = tk.Text(linha4, height=20, width=50,
                      font='arial 9')
# Add a Scrollbar(horizontal)
v = ttk.Scrollbar(linha4, orient='vertical', command=edCapitulos.yview)
v.pack(side='right', fill='y')
edCapitulos.pack(fill=tk.BOTH, padx=5, pady=5)

# Quinta linha
linha5 = tk.Frame(janela)
linha5.pack(fill=tk.X, padx=5, pady=5)

tk.Label(linha5, text="Selecione os capítulos:\tInício:").pack(side=tk.LEFT)

edInicio = tk.Entry(linha5, font='arial 14', width=10)
edInicio.pack(side=tk.LEFT)

tk.Label(linha5, text="Fim:").pack(side=tk.LEFT)

edFim = tk.Entry(linha5, font='arial 14', width=10)
edFim.pack(side=tk.LEFT, padx=5, pady=5)

btBaixar = tk.Button(linha5, text="Baixar", command=pbaixarCaps)
btBaixar.pack(side=tk.LEFT, padx=5, pady=5)

print(f'{30*"#"}\n\nNAO FECHE ESTA JANELA!!!!!!!!!!!!!!!')

# Abre a janela
janela.mainloop()
