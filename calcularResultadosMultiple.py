import os
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

def contarCelulasXML(lista):
    contador_wbc = 0
    contador_rbc = 0
    contador_platelets = 0

    for celula in lista:
        if celula[0] == "WBC":
            contador_wbc = contador_wbc + 1
        if celula[0] == "RBC":
            contador_rbc = contador_rbc + 1
        if celula[0] == "Platelets":
            contador_platelets = contador_platelets + 1
    
    return contador_wbc, contador_rbc, contador_platelets

coordenadas_dir = "./dataset-multiple/test/coordenadas/"
coordenadas_path = []

dados_dir = "./results/multiple/info/"
dados_path = []

test_y_wbc = []
predict_y_wbc = []

test_y_rbc = []
predict_y_rbc = []

test_y_platelets = []
predict_y_platelets = []

for arquivo in os.listdir(coordenadas_dir):
    coordenadas_path.append(coordenadas_dir + arquivo)

for arquivo in os.listdir(dados_dir):
    dados_path.append(dados_dir + arquivo)

for arquivo in coordenadas_path:
    test_y_wbc.append(contarCelulasXML(infoCelulas(arquivo))[0])

for arquivo in coordenadas_path:
    test_y_rbc.append(contarCelulasXML(infoCelulas(arquivo))[1])

for arquivo in coordenadas_path:
    test_y_platelets.append(contarCelulasXML(infoCelulas(arquivo))[2])

for arquivo in dados_path:
    file = open(arquivo, "r")
    predict_y_wbc.append(int(file.readlines()[1].replace("\n","")))    
    file.close()

for arquivo in dados_path:
    file = open(arquivo, "r")
    predict_y_rbc.append(int(file.readlines()[3].replace("\n","")))
    file.close()

for arquivo in dados_path:
    file = open(arquivo, "r")
    predict_y_platelets.append(int(file.readlines()[5].replace("\n","")))
    file.close()

total_wbc = 0
total_rbc = 0
total_platelets = 0

for elemento in test_y_wbc:
    total_wbc = total_wbc + elemento

for elemento in test_y_rbc:
    total_rbc = total_rbc + elemento

for elemento in test_y_platelets:
    total_platelets = total_platelets + elemento

acertos_wbc = 0
acertos_rbc = 0
acertos_platelets = 0

erros_wbc = 0
erros_rbc = 0
erros_platelets = 0

for i in range(0, len(test_y_wbc)):
    erros_wbc = test_y_wbc[i] - predict_y_wbc[i]

    if predict_y_wbc[i] > test_y_wbc[i]:
        acertos_wbc = test_y_wbc[i]
    else:
        acertos_wbc = predict_y_wbc[i]

for i in range(0, len(test_y_rbc)):
    erros_rbc = test_y_rbc[i] - predict_y_rbc[i]

    if predict_y_rbc[i] > test_y_rbc[i]:
        acertos_rbc = test_y_rbc[i]
    else:
        acertos_rbc = predict_y_rbc[i]

for i in range(0, len(test_y_platelets)):
    erros_platelets = test_y_platelets[i] - predict_y_platelets[i]

    if predict_y_platelets[i] > test_y_platelets[i]:
        acertos_platelets = test_y_platelets[i]
    else:
        acertos_platelets = predict_y_platelets[i]

porc_acertos_wbc = (acertos_wbc/total_wbc) * 100
porc_acertos_rbc = (acertos_rbc/total_rbc) * 100
porc_acertos_platelets = (acertos_platelets/total_platelets) * 100

porc_erros_wbc = (erros_wbc/total_wbc) * 100
porc_erros_rbc = (erros_rbc/total_rbc) * 100
porc_erros_platelets = (erros_platelets/total_wbc) * 100

total_wbc = "Total WBC: " + str(total_wbc) + " (100%)"
acertos_wbc = "Acertos WBC: " + str(acertos_wbc) + " (" + str(round(porc_acertos_wbc, 2)) + "%)"
erros_wbc = "Erros WBC: " + str(erros_wbc) + " (" + str(round(porc_erros_wbc, 2)) + "%)"

total_rbc = "Total RBC: " + str(total_rbc) + " (100%)"
acertos_rbc = "Acertos RBC: " + str(acertos_rbc) + " (" + str(round(porc_acertos_rbc, 2)) + "%)"
erros_rbc = "Erros RBC: " + str(erros_rbc) + " (" + str(round(porc_erros_rbc, 2)) + "%)"

total_platelets = "Total Platelets: " + str(total_platelets) + " (100%)"
acertos_platelets = "Acertos Platelets: " + str(acertos_platelets) + " (" + str(round(porc_acertos_platelets, 2)) + "%)"
erros_platelets = "Erros Platelets: " + str(erros_platelets) + " (" + str(round(porc_erros_platelets, 2)) + "%)"

print(total_wbc)
print(acertos_wbc)
print(erros_wbc)
print()

print(total_rbc)
print(acertos_rbc)
print(erros_rbc)
print()

print(total_platelets)
print(acertos_platelets)
print(erros_platelets)

arquivo = open("relatorio-multiple.txt", "w")
arquivo.write(total_wbc + "\n")
arquivo.write(acertos_wbc + "\n")
arquivo.write(erros_wbc + "\n")
arquivo.write("\n")
arquivo.write(total_rbc + "\n")
arquivo.write(acertos_rbc + "\n")
arquivo.write(erros_rbc + "\n")
arquivo.write("\n")
arquivo.write(total_platelets + "\n")
arquivo.write(acertos_platelets + "\n")
arquivo.write(erros_platelets + "\n")
arquivo.write("\n")
arquivo.close()