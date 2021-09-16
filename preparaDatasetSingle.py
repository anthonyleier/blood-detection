import os
from shutil import copyfile
from bs4 import BeautifulSoup as bs


def encontraWBC(arquivo):
    content = []
    with open(arquivo, "r") as file:
        content = file.readlines()
        content = "".join(content)
        bs_content = bs(content, "lxml")
        lista_objetos = bs_content.find_all("object")

        for objeto in lista_objetos:
            nome = objeto.find("name")
            if "WBC" in nome:
                return True

    return False


imagens_dir = 'bccd/BCCD/JPEGImages/'
coordenadas_dir = 'bccd/BCCD/Annotations/'

nomes = []
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

for nome in os.listdir(imagens_dir):
    nome = nome.replace(".jpg", '')
    nomes.append(nome)

for arquivo in os.listdir(imagens_dir):
    imagens_path.append(imagens_dir + arquivo)

for arquivo in os.listdir(coordenadas_dir):
    coordenadas_path.append(coordenadas_dir + arquivo)

tupla = zip(nomes, imagens_path, coordenadas_path)
tupla = tuple(tupla)
print(tupla[0])

print("Carregando imagens de treino...")
for grupo in tupla[:tamanho_treino]:
    if(encontraWBC(grupo[2])):
        copyfile(grupo[1], "./dataset-single/train/imagens/" + grupo[0] + ".jpg")
        copyfile(grupo[2], "./dataset-single/train/coordenadas/" + grupo[0] + ".xml")
    else:
        print("Não encontrado no treino")

print("Carregando imagens de teste...")
for grupo in tupla[tamanho_treino:]:
    if(encontraWBC(grupo[2])):
        copyfile(grupo[1], "./dataset-single/test/imagens/" + grupo[0] + ".jpg")
        copyfile(grupo[2], "./dataset-single/test/coordenadas/" + grupo[0] + ".xml")
    else:
        print("Não encontrado no teste")

print("Dataset carregado com sucesso")
