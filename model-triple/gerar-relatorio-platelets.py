import os
from bs4 import BeautifulSoup as bs

def contarCelulasXML(arquivo):
    contador = 0
    content = []
    with open(arquivo, "r") as file:
        content = file.readlines()
        content = "".join(content)
        bs_content = bs(content, "lxml")
        lista_objetos = bs_content.find_all("object")

        for objeto in lista_objetos:
            nome = objeto.find("name")
            if "Platelets" in nome:
                contador = contador + 1

    return int(contador)

def coletarContagemTXT(path):
    arquivo = open(path, "r")
    return int(arquivo.readlines()[1])

resultados_dir = "./model-triple/results-triple/"
todos_resultados = []

for pasta in os.listdir(resultados_dir):
    todos_resultados.append(resultados_dir + pasta)
    
coordenadas_dir = "./model-triple/dataset-triple/test/coordenadas/"
coordenadas_path = []

for resultado in todos_resultados:   
    print(resultado)

    dados_dir = resultado + "/platelets/info/"
    dados_path = []

    test_y = []
    predict_y = []
    nomes = []

    for arquivo in os.listdir(coordenadas_dir):
        nomes.append(arquivo.replace(".xml", ""))

    for arquivo in os.listdir(coordenadas_dir):
        coordenadas_path.append(coordenadas_dir + arquivo)

    for arquivo in os.listdir(dados_dir):
        dados_path.append(dados_dir + arquivo)

    for arquivo in coordenadas_path:
        test_y.append(contarCelulasXML(arquivo))

    for arquivo in dados_path:
        predict_y.append(coletarContagemTXT(arquivo))

    total = len(test_y)
    acertos = 0
    erros = 0

    for i in range(0, len(test_y)):
        acertou = test_y[i] == predict_y[i]
        if acertou:
            acertos = acertos + 1
        else:
            erros = erros + 1


    porc_acertos = (acertos/total) * 100
    porc_erros = (erros/total) * 100

    total = "Total: " + str(total) + " (100%)"
    acertos = "Acertos: " + str(acertos) + " (" + str(round(porc_acertos, 2)) + "%)"
    erros = "Erros: " + str(erros) + " (" + str(round(porc_erros, 2)) + "%)"

    print(total)
    print(acertos)
    print(erros)

    arquivo = open(resultado + "/relatorio-platelets.txt", "w")
    arquivo.write(total + "\n")
    arquivo.write(acertos + "\n")
    arquivo.write(erros + "\n")
    arquivo.write("\n")
    arquivo.write("Valor desejado" + " - " + "Valor predito" + " - " + "Nome do arquivo" + "\n")
    for i in range(0, len(test_y)):
        arquivo.write(str(str(test_y[i]) + " - " + str(predict_y[i]) + " - " + str(nomes[i])) + "\n")
    arquivo.close()
