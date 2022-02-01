from bs4 import BeautifulSoup
import requests
import re
import statistics as stt

url = "https://www.amazon.com.br/hz/wishlist/printview/24WHLNWSZI1GN?target=_blank&ref_=lv_pv&filter=unpurchased&sort=default"
resultado = requests.get(url)
#print(resultado.text)
doc = BeautifulSoup(resultado.text, "html.parser")

## valores
precos = doc.find_all(["span"], text=re.compile("\$.*")) 
lista_p = []
for preco in precos:
    p = str(preco)
    if "<" in p:
        np = p.replace(",",".").replace("<", " ")[8:14]
    else:
        np = p.replace(",",".")[8:14]
    f = float(np)
    lista_p.append(f)

itens = len(lista_p)
soma = sum(lista_p)
media = stt.fmean(lista_p)

print('Para comprar todos os {} itens disponíveis de sua lista, com valor médio de {:.2f}, serão necessários R${:.2f}'.format(itens, media, soma))

## autores
autores = doc.find_all(text=re.compile("^de"))
lista_a = []
for autor in autores:
    a = str(autor)
    if "(Capa comum)" in a:
        na = a.replace("(Capa comum)", "")[3:-4]
        lista_a.append(na)
    elif "(Capa dura)" in a:
        na = a.replace("(Capa dura)", "")[3:-4]
        lista_a.append(na)
    elif "(Capa flexível)" in a:
        na = a.replace("(Capa flexível)", "")[3:-4]
        lista_a.append(na)
    elif "(Livro de bolso)" in a:
        na = a.replace("(Livro de bolso)", "")[3:-4]
        lista_a.append(na)
    elif "(Caixas e coleções)" in a:
        na = a.replace("(Caixas e coleções)", "")[3:-4]
        lista_a.append(na)

moda = stt.multimode(lista_a)
moda_str = " e ".join(stt.multimode(lista_a))
if len(moda) == 1:
    vezes = lista_a.count(moda_str)
    print('Eis o/a autore mais frequente de sua lista: {} ({}x)'.format(moda_str, vezes))
elif len(moda) > 1:
    vezes = lista_a.count(moda[1])
    print('Eis os autores mais frequentes de sua lista: {} ({}x)'.format(moda_str, vezes))