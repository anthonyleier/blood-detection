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

print("Criando pastas...")

imagens_train_dir = "./model-triple/dataset-triple/train/imagens/"
coordenadas_train_dir = "./model-triple/dataset-triple/train/coordenadas/"
imagens_test_dir = "./model-triple/dataset-triple/test/imagens/"
coordenadas_test_dir = "./model-triple/dataset-triple/test/coordenadas/"

if not os.path.isdir(imagens_train_dir):
    os.makedirs(imagens_train_dir)    

if not os.path.isdir(coordenadas_train_dir):
    os.makedirs(coordenadas_train_dir)   

if not os.path.isdir(imagens_test_dir):
    os.makedirs(imagens_test_dir)    

if not os.path.isdir(coordenadas_test_dir):
    os.makedirs(coordenadas_test_dir)    

print("Preparando imagens de treino...")
for nome, imagem_path, coordenadas_path in tupla[:tamanho_treino]:
    copyfile(imagem_path, imagens_train_dir + nome + ".jpg")
    copyfile(coordenadas_path, coordenadas_train_dir + nome + ".xml")

print("Preparando imagens de teste...")
for nome, imagem_path, coordenadas_path in tupla[tamanho_treino:]: 
    copyfile(imagem_path, imagens_test_dir + nome + ".jpg")
    copyfile(coordenadas_path, coordenadas_test_dir + nome + ".xml")
    
print("Dataset carregado com sucesso")
