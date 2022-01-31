from bs4 import BeautifulSoup
import requests
import re

url = "https://www.amazon.com.br/hz/wishlist/printview/24WHLNWSZI1GN?target=_blank&ref_=lv_pv&filter=unpurchased&sort=default"
resultado = requests.get(url)
#print(resultado.text)
doc = BeautifulSoup(resultado.text, "html.parser")

precos = doc.find_all(["span"], text=re.compile("\$.*")) 
lista = []
for preco in precos:
    p = str(preco)
    n = p.replace(",",".")[8:14]
    f = float(n)
    lista.append(f)

itens = len(lista)
soma = sum(lista)
print('Para comprar todos os {} itens de sua lista serão necessários R${:.2f} .'.format(itens, soma))
