import os
ep = '60.v2'
numero = ''
for i in ep:
    if i.isalpha():
        i = '.'
    numero += i.strip()
    numero = numero.replace('..', '.')
# print(numero)

tamanho = os.path.getsize('One Punch Man_219.0_1.jpg')
if tamanho == 0:
    os.remove('One Punch Man_219.0_1.jpg')
tamanho = os.path.getsize('One Punch Man_219.0_4.jpg')
print(tamanho)
