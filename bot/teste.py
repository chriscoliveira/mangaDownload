import os
import zipfile
from natsort import natsorted


def create_zip_files(directory, manganame, max_size):
    file_list = []
    current_size = 0
    zip_count = 1

    path = [os.path.join(p, file) for p, _, files in os.walk(
        os.path.abspath(directory)) for file in files]

    lista = natsorted(path)
    print(lista)

    # Lista todos os arquivos da pasta em ordem alfabética

    for file in lista:
        # Verifica se o arquivo é uma imagem JPEG
        if file.lower().endswith('.jpg'):
            file_size = os.path.getsize(file)

            # Verifica se o tamanho do arquivo excede o limite
            if current_size + file_size > max_size:
                # Cria um novo arquivo ZIP
                zip_filename = f'{manganame}_{zip_count}.cbr'
                with zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
                    # Adiciona os arquivos à nova pasta ZIP em ordem alfabética
                    for f in sorted(file_list):
                        zipf.write(f, arcname=os.path.basename(f))

                # Reseta as variáveis para o próximo arquivo ZIP
                file_list = []
                current_size = 0
                zip_count += 1

            # Adiciona o arquivo atual à lista de arquivos
            file_list.append(file)
            current_size += file_size

    # Cria o último arquivo ZIP, se houver algum arquivo restante
    if file_list:
        zip_filename = f'{manganame}_{zip_count}.cbr'
        with zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED) as zipf:
            for f in sorted(file_list):
                zipf.write(f, arcname=os.path.basename(f))


# Pasta contendo as imagens JPEG
directory = 'Download/769723764'

# Tamanho máximo do arquivo ZIP em bytes (20 MB = 20 * 1024 * 1024)
max_size = 20 * 1024 * 1024

# Cria os arquivos compactados
create_zip_files(directory, 'manda_name_ep', max_size)
