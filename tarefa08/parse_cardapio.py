from xml.dom.minidom import parse

dom = parse("cardapio.xml")

cardapio = dom.documentElement

pratos = cardapio.getElementsByTagName("prato")

print("=== CARDÁPIO ===")
for item in pratos:
    codigo = item.getAttribute("id")
    nome_prato = item.getElementsByTagName("nome")[0].firstChild.nodeValue

    print(f"{codigo} - {nome_prato}")

opcao = input("\nInforme o ID do prato desejado: ")

for item in pratos:
    if item.getAttribute("id") == opcao:

        nome_prato = item.getElementsByTagName("nome")[0].firstChild.nodeValue
        descricao = item.getElementsByTagName("descricao")[0].firstChild.nodeValue
        preco = item.getElementsByTagName("preco")[0].firstChild.nodeValue
        moeda = item.getElementsByTagName("preco")[0].getAttribute("moeda")
        calorias = item.getElementsByTagName("calorias")[0].firstChild.nodeValue
        preparo = item.getElementsByTagName("tempoPreparo")[0].firstChild.nodeValue

        ingredientes = item.getElementsByTagName("ingrediente")

        print("\n--- INFORMAÇÕES DO PRATO ---")
        print(f"Nome: {nome_prato}")
        print(f"Descrição: {descricao}")

        print("Ingredientes:")
        for ingrediente in ingredientes:
            print(f"- {ingrediente.firstChild.nodeValue}")

        print(f"Preço: {moeda} {preco}")
        print(f"Calorias: {calorias} kcal")
        print(f"Tempo de preparo: {preparo}")