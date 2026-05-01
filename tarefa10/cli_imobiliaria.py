import json

with open("imobiliaria.json", "r", encoding="utf-8") as arquivo:
    lista_imoveis = json.load(arquivo)

print("=== IMÓVEIS DISPONÍVEIS ===")
for indice in range(len(lista_imoveis)):
    print(f"{indice + 1} - {lista_imoveis[indice]['descricao']}")

escolha = int(input("\nInforme o ID do imóvel: "))

if escolha >= 1 and escolha <= len(lista_imoveis):
    imovel = lista_imoveis[escolha - 1]

    print("\n--- INFORMAÇÕES DO IMÓVEL ---")
    print("Descrição:", imovel["descricao"])

    print("\nDados do proprietário:")
    print("Nome:", imovel["proprietario"]["nome"])

    print("Telefones:")
    for telefone in imovel["proprietario"]["telefones"]:
        print("-", telefone)

    print("Emails:")
    for email in imovel["proprietario"]["emails"]:
        print("-", email)

    print("\nEndereço:")
    print("Rua:", imovel["endereco"]["rua"])
    print("Número:", imovel["endereco"]["numero"])
    print("Bairro:", imovel["endereco"]["bairro"])
    print("Cidade:", imovel["endereco"]["cidade"])

    print("\nCaracterísticas:")
    print("Tamanho:", imovel["caracteristicas"]["tamanho"])
    print("Quartos:", imovel["caracteristicas"]["numQuartos"])
    print("Banheiros:", imovel["caracteristicas"]["numBanheiros"])

    print("\nValor:", imovel["valor"])

else:
    print("Imóvel não encontrado.")