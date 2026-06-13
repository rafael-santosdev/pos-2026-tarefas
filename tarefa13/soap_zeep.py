import zeep

print("Iniciando o programa...")

wsdl_url = "https://www.dataaccess.com/webservicesserver/NumberConversion.wso?WSDL"

print("Conectando ao serviço SOAP...")

client = zeep.Client(wsdl=wsdl_url)

print("Conexão realizada com sucesso.")

number = input("Digite um número inteiro: ")

result = client.service.NumberToWords(
    ubiNum=int(number)
)

print("Número por extenso em inglês:")
print(result)