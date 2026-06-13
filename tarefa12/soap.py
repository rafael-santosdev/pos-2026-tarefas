import requests
from xml.dom.minidom import parseString

url = "http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso"

print("===== Consulta SOAP de Países =====")
print("1 - Nome do país")
print("2 - Moeda do país")
print("3 - Código telefônico internacional")

op = input("Digite a opção desejada: ")
country_code = input("Digite o código do país desejado: ").upper()

if op == "1":
    operation = "CountryName"
elif op == "2":
    operation = "CountryCurrency"
elif op == "3":
    operation = "CountryIntPhoneCode"
else:
    print("Opção inválida.")
    exit()


payload = f"""<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <{operation} xmlns="http://www.oorsprong.org/websamples.countryinfo">
            <sCountryISOCode>{country_code}</sCountryISOCode>
        </{operation}>
    </soap:Body>
</soap:Envelope>"""

headers = {
    "Content-Type": "text/xml; charset=utf-8"
}

response = requests.post(url, headers=headers, data=payload)

if response.status_code == 200:
    if op == "1":
        result = parseString(response.text).documentElement.getElementsByTagName("m:CountryNameResult")[0].firstChild.nodeValue

    elif op == "2":
        result = parseString(response.text).documentElement.getElementsByTagName("m:sName")[0].firstChild.nodeValue

    elif op == "3":
        result = parseString(response.text).documentElement.getElementsByTagName("m:CountryIntPhoneCodeResult")[0].firstChild.nodeValue

    print("\nResultado da consulta:")
    print(result)

else:
    print("Erro ao acessar o serviço SOAP.")