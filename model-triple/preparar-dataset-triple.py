import os
from shutil import copyfile
from bs4 import BeautifulSoup as bs


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

print("Preparando imagens de treino...")
for grupo in tupla[:tamanho_treino]:
    copyfile(grupo[1], "./model-triple/dataset-triple/train/imagens/" + grupo[0] + ".jpg")
    copyfile(grupo[2], "./model-triple/dataset-triple/train/coordenadas/" + grupo[0] + ".xml")

print("Preparando imagens de teste...")
for grupo in tupla[tamanho_treino:]: 
    copyfile(grupo[1], "./model-triple/dataset-triple/test/imagens/" + grupo[0] + ".jpg")
    copyfile(grupo[2], "./model-triple/dataset-triple/test/coordenadas/" + grupo[0] + ".xml")
    

print("Dataset carregado com sucesso")
