import os
from shutil import copyfile
from bs4 import BeautifulSoup as bs

def infoCelulas(arquivo):
    celulas = []
    content = []
    with open(arquivo, "r") as file:
        content = file.readlines()
        content = "".join(content)
        bs_content = bs(content, "lxml")

        lista_objetos = bs_content.find_all("object")
        for objeto in lista_objetos:
            nome = objeto.find("name")
            xmin = objeto.find("xmin")
            ymin = objeto.find("ymin")
            xmax = objeto.find("xmax")
            ymax = objeto.find("ymax")

            nome = str(nome)
            xmin = str(xmin)
            ymin = str(ymin)
            xmax = str(xmax)
            ymax = str(ymax)

            nome = nome[nome.find(">")+1:nome.find("</name>")]
            xmin = int(xmin[xmin.find(">")+1:xmin.find("</xmin>")])
            ymin = int(ymin[ymin.find(">")+1:ymin.find("</ymin>")])
            xmax = int(xmax[xmax.find(">")+1:xmax.find("</xmax>")])
            ymax = int(ymax[ymax.find(">")+1:ymax.find("</ymax>")])

            celulas.append([nome, xmin, ymin, xmax, ymax])

    return celulas


imagens_dir = 'bccd/BCCD/JPEGImages/'
coordenadas_dir = 'bccd/BCCD/Annotations/'

imagens_path = []
coordenadas_path = []

perc_treino = 0.8
perc_teste = 0.2

total_imagens = len(os.listdir(imagens_dir))
total_coordenadas = len(os.listdir(coordenadas_dir))

if(total_imagens == total_coordenadas):
    print("Dados integros")
else:
    print("Falha na integridade dos dados")

tamanho_treino = int(perc_treino * total_imagens)
tamanho_teste = int(perc_teste * total_imagens)

for arquivo in os.listdir(imagens_dir):
    imagens_path.append(imagens_dir + arquivo)

for arquivo in os.listdir(coordenadas_dir):
    coordenadas_path.append(coordenadas_dir + arquivo)

tupla = zip(imagens_path, coordenadas_path)
tupla = tuple(tupla)

print("Criando pastas...")

imagens_train_dir = "./model-single/dataset-single/train/imagens/"
coordenadas_train_dir = "./model-single/dataset-single/train/coordenadas/"
imagens_test_dir = "./model-single/dataset-single/test/imagens/"
coordenadas_test_dir = "./model-single/dataset-single/test/coordenadas/"

if not os.path.isdir(imagens_train_dir):
    os.makedirs(imagens_train_dir)    

if not os.path.isdir(coordenadas_train_dir):
    os.makedirs(coordenadas_train_dir)   

if not os.path.isdir(imagens_test_dir):
    os.makedirs(imagens_test_dir)    

if not os.path.isdir(coordenadas_test_dir):
    os.makedirs(coordenadas_test_dir)

contador = 0
print("Preparando imagens de treino...")
for imagem_path, coordenada_path in tupla[:tamanho_treino]:
    celulas = infoCelulas(coordenada_path)
    for celula in celulas:
        nome = "cell_" + str(contador)
        copyfile(imagem_path, imagens_train_dir + nome + ".jpg")
        arquivo = open(coordenadas_train_dir + nome + ".txt", "w")
        arquivo.write(str(celula[0]) + "\n")
        arquivo.write(str(celula[1]) + "\n")
        arquivo.write(str(celula[2]) + "\n")
        arquivo.write(str(celula[3]) + "\n")
        arquivo.write(str(celula[4]) + "\n")
        contador = contador + 1

contador = 0
print("Preparando imagens de teste...")
for imagem_path, coordenada_path in tupla[tamanho_treino:]:
    nome = "cell_" + str(contador)
    copyfile(imagem_path, imagens_test_dir + nome + ".jpg")
    copyfile(coordenada_path, coordenadas_test_dir + nome + ".xml")
    contador = contador + 1

print("Dataset carregado com sucesso")
