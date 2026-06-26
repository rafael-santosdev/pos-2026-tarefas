import requests
from getpass import getpass

api_url = "https://suap.ifrn.edu.br/api/"

user = input("user: ")
password = getpass()

data = {
    "username": user,
    "password": password
}

response = requests.post(api_url + "token/pair", json=data)
token = response.json()["access"]

headers = {
    "Authorization": f"Bearer {token}"
}

ano = input("Digite o ano letivo: ")
periodo = input("Digite o período: ")

url = api_url + f"ensino/meu-boletim/{ano}/{periodo}/"
response = requests.get(url, headers=headers)

boletim = response.json()["results"]

print("=" * 100)
print(f'{"Disciplina":<60} | {"Unid. 1":^8} | {"Unid. 2":^8} | {"Unid. 3":^8} | {"Unid. 4":^8}')
print("=" * 100)

for materia in boletim:
    print(
        f'{materia["disciplina"]:<60} | '
        f'{str(materia["nota_etapa_1"]["nota"]):^8} | '
        f'{str(materia["nota_etapa_2"]["nota"]):^8} | '
        f'{str(materia["nota_etapa_3"]["nota"]):^8} | '
        f'{str(materia["nota_etapa_4"]["nota"]):^8}'
    )

print("=" * 100)