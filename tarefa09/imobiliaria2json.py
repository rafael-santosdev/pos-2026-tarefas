from xml.dom.minidom import parse
import json

dom = parse("imobiliaria.xml")
raiz = dom.documentElement

imoveis = raiz.getElementsByTagName("imovel")

dados = []

for item in imoveis:

    descricao = item.getElementsByTagName("descricao")[0].firstChild.nodeValue

    proprietario = item.getElementsByTagName("proprietario")[0]
    nome_proprietario = proprietario.getElementsByTagName("nome")[0].firstChild.nodeValue

    telefones = proprietario.getElementsByTagName("telefone")
    telefones_proprietario = [telefone.firstChild.nodeValue for telefone in telefones]

    emails = proprietario.getElementsByTagName("email")
    emails_proprietario = [email.firstChild.nodeValue for email in emails]

    endereco = item.getElementsByTagName("endereco")[0]
    rua = endereco.getElementsByTagName("rua")[0].firstChild.nodeValue
    bairro = endereco.getElementsByTagName("bairro")[0].firstChild.nodeValue
    cidade = endereco.getElementsByTagName("cidade")[0].firstChild.nodeValue

    numero = endereco.getElementsByTagName("numero")
    numero_imovel = numero[0].firstChild.nodeValue if numero else None

    caracteristicas = item.getElementsByTagName("caracteristicas")[0]
    tamanho = caracteristicas.getElementsByTagName("tamanho")[0].firstChild.nodeValue
    num_quartos = caracteristicas.getElementsByTagName("numQuartos")[0].firstChild.nodeValue
    num_banheiros = caracteristicas.getElementsByTagName("numBanheiros")[0].firstChild.nodeValue

    valor = item.getElementsByTagName("valor")[0].firstChild.nodeValue

    registro = {
        "descricao": descricao,
        "proprietario": {
            "nome": nome_proprietario,
            "telefones": telefones_proprietario,
            "emails": emails_proprietario
        },
        "endereco": {
            "rua": rua,
            "bairro": bairro,
            "cidade": cidade,
            "numero": numero_imovel
        },
        "caracteristicas": {
            "tamanho": tamanho,
            "numQuartos": num_quartos,
            "numBanheiros": num_banheiros
        },
        "valor": valor
    }

    dados.append(registro)

with open("imobiliaria.json", "w", encoding="utf-8") as arquivo:
    json.dump(dados, arquivo, indent=4, ensure_ascii=False)

print("Arquivo JSON gerado com sucesso!") 