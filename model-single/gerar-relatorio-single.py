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

def contador(celulas_arq):
    count_wbc = 0
    count_rbc = 0
    count_platelets = 0

    for celula in celulas_arq:
        nome = celula[0]
        if nome == "WBC":
            count_wbc = count_wbc + 1
        elif nome == "RBC":
            count_rbc =  count_rbc + 1
        elif nome == "Platelets":
            count_platelets =  count_platelets + 1

        count = [count_wbc, count_rbc, count_platelets]
        
    return count

def getContadores(path):
    arquivo = open(path, "r")
    linhas = arquivo.readlines()
    count_wbc = int(linhas[1].replace("\n", ""))
    count_rbc = int(linhas[3].replace("\n", ""))
    count_platelets = int(linhas[5].replace("\n", ""))
    count = [count_wbc, count_rbc, count_platelets]      
    return count

def calculaGeral(contadores):
    count_wbc = 0
    count_rbc = 0
    count_platelets = 0

    for elemento in contadores:
        count_wbc = count_wbc + elemento[0]
        count_rbc = count_rbc + elemento[1]
        count_platelets = count_platelets + elemento[2]

    return [count_wbc, count_rbc, count_platelets]

def preparaString(total, encontrados, porcentagem):
    total = str(total)
    encontrados = str(encontrados)
    porcentagem = str(round(porcentagem, 2))

    string = ""
    string = string + "Total: " + total + "\n"
    string = string + "Encontrados: " + encontrados + "\n"
    string = string + "Porcentagem: " + encontrados + "/" + total + " (" + porcentagem + "%)"  + "\n"

    return string




resultados_dir = "./model-single/results-single/"
todos_resultados = []

for pasta in os.listdir(resultados_dir):
    todos_resultados.append(resultados_dir + pasta)

coordenadas_dir = "./model-single/dataset-single/test/coordenadas/"
celulas_arq = []

for arquivo in os.listdir(coordenadas_dir):
    celulas_arq.append(infoCelulas(coordenadas_dir + arquivo))

contadores_teste = []

for elemento in celulas_arq:
    contadores_teste.append(contador(elemento))

for resultado in todos_resultados:   
    print(resultado) 

    info_dir = resultado + "/info/"
    contadores_predito = []

    for arquivo in os.listdir(info_dir):
        contadores_predito.append(getContadores(info_dir + arquivo))

    print("Contadores Teste:", calculaGeral(contadores_teste))
    print("Contadores Predito:", calculaGeral(contadores_predito))

    contador_teste = calculaGeral(contadores_teste)
    contador_predito = calculaGeral(contadores_predito)

    wbc_total = contador_teste[0]
    rbc_total = contador_teste[1]
    platelets_total = contador_teste[2]

    wbc_encontrados = contador_predito[0]
    rbc_encontrados = contador_predito[1]
    platelets_encontrados = contador_predito[2]

    wbc_porcentagem = (wbc_encontrados / wbc_total) * 100
    rbc_porcentagem = (rbc_encontrados / rbc_total) * 100
    platelets_porcentagem = (platelets_encontrados / platelets_total) * 100

    arquivo = open(resultado + "/relatorio-single.txt", "w")
    arquivo.write("WBC\n")
    wbc = preparaString(wbc_total, wbc_encontrados, wbc_porcentagem)
    arquivo.write(wbc)

    arquivo.write("\nRBC\n")
    rbc = preparaString(rbc_total, rbc_encontrados, rbc_porcentagem)
    arquivo.write(rbc)

    arquivo.write("\nPlatelets\n")
    platelets = preparaString(platelets_total, platelets_encontrados, platelets_porcentagem)
    arquivo.write(platelets)