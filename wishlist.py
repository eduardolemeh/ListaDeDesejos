from bs4 import BeautifulSoup
import requests
import re
import statistics as stt
import matplotlib.pyplot as plt
import random
from tkinter import *
from tkinter import messagebox

# url
print('Insira a url da versão para impressão de sua lista de desejos:')
url = input('')
resultado = requests.get(url)
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

# autores
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
elif len(moda) > 1:
    vezes = lista_a.count(moda[1])

# livros
livros = doc.find_all(class_="a-text-bold")
lista_l = []
for livro in livros:
    l = str(livro)
    nl = l[26:-7]
    lista_l.append(nl)
qlqr = random.choice(lista_l)

# display
window = Tk()
window.withdraw()
a = str('''Para comprar todos os {} itens disponíveis de sua lista, com valor médio de R${:.2f}, serão necessários R${:.2f}\n
Eis o/a autore mais frequente de sua lista: {} ({}x)\n
Por que não dá uma olhada em "{}"?'''.format(itens, media, soma, moda_str, vezes, qlqr))
messagebox.showinfo('Resultados', a)

# grafico valores
intervalos = ['<9,9', '10 - 19,9', '20 - 29,9', '30 - 39,9', '40 - 49,9', '50 - 59,9', '60 - 69,9', '70 - 79,9', '>80']
qntd = [0, 0, 0, 0, 0, 0, 0, 0, 0]

for intervalo in lista_p:
    i = float(intervalo)
    if i < 10:
        qntd[0] += 1
    elif 10 <= i < 20:
        qntd[1] += 1
    elif 20 <= i < 30:
        qntd[2] += 1
    elif 30 <= i < 40:
        qntd[3] += 1
    elif 40 <= i < 50:
        qntd[4] += 1
    elif 50 <= i < 60:
        qntd[5] += 1
    elif 60 <= i < 70:
        qntd[6] += 1
    elif 70 <= i < 80:
        qntd[7] += 1
    elif i > 80:
        qntd[8] += 1

plt.figure(figsize=(8.0, 6.0))
plt.yticks(fontsize=9)
plt.xticks(fontsize=8)
plt.title('Valores')
plt.ylabel('Quantidade')
plt.xlabel('Valor', color='blue')
plt.axis(ymin=0, ymax=70)
plt.bar(intervalos, qntd, width=0.65)

plt.show()