
import requests
import json

# URL da API que você deseja acessar
url = "https://animeschedule.net/api/v3/anime?year=2023&week=26"

# Fazendo a solicitação GET
response = requests.get(url)
with open("teste.txt", "w") as f:
    # Verificando se a solicitação foi bem-sucedida (código de status 200 indica sucesso)
    if response.status_code == 200:
        # Acessando os dados de resposta (em formato JSON)
        data = response.json()

        text = json.dumps(data, sort_keys=True, indent=4)
        f.write(text)

    else:
        # Caso ocorra um erro na solicitação
        print('Falha na solicitação. Código de status:', response.status_code)
