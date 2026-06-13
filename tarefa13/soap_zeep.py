import zeep

wsdl_url = "http://www.dataaccess.com/webservicesserver/NumberConversion.wso?WSDL"

client = zeep.Client(wsdl=wsdl_url)

number = input("Digite um número inteiro: ")

result = client.service.NumberToWords(
    ubiNum=number
)

print("Número por extenso em inglês:")
print(result)