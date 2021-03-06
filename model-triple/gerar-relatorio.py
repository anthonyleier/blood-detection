import os
from bs4 import BeautifulSoup as bs

celulaName = input("Digite a celula para gerar o relatorio:")

def calcularMSE(test_y, predict_y):
    diferenca = test_y - predict_y
    return diferenca**2

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
            if celulaName in nome:
                contador = contador + 1

    return int(contador)

def coletarContagemTXT(path):
    arquivo = open(path, "r")
    return int(arquivo.readlines()[1])

resultados_dir = "./results-triple/"
todos_resultados = []

for pasta in os.listdir(resultados_dir):
    if celulaName.lower() in os.listdir(resultados_dir + pasta):
        todos_resultados.append(resultados_dir + pasta)

for resultado in todos_resultados:   
    print(resultado)

    coordenadas_dir = "./dataset-triple/test/coordenadas/"
    coordenadas_path = []

    dados_dir = resultado + "/" + celulaName.lower() + "/info/"
    dados_path = []

    # Relatório Antigo
    test_y = []
    predict_y = []
    nomes = []

    # Relatório Novo
    encontradas_absoluto = 0
    reais_absoluto = 0

    for arquivo in os.listdir(coordenadas_dir):
        nomes.append(arquivo.replace(".xml", ""))

    for arquivo in os.listdir(coordenadas_dir):
        coordenadas_path.append(coordenadas_dir + arquivo)

    for arquivo in os.listdir(dados_dir):
        dados_path.append(dados_dir + arquivo)

    for arquivo in coordenadas_path:
        test_y.append(contarCelulasXML(arquivo))
        reais_absoluto = reais_absoluto + contarCelulasXML(arquivo)

    for arquivo in dados_path:
        predict_y.append(coletarContagemTXT(arquivo))
        encontradas_absoluto = encontradas_absoluto + coletarContagemTXT(arquivo)

    #Relatório Antigo
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

    total_mse = []
    # Relatório Novo
    arquivo = open(resultado + "/relatorio-" + celulaName.lower() + ".txt", "w")
    arquivo.write("Relatorio de Performance do Modelo" + "\n")
    arquivo.write("Celulas reais: " + str(reais_absoluto) + "\n")
    arquivo.write("Celulas encontradas: " + str(encontradas_absoluto) + "\n")
    arquivo.write("Percentual: " + str(round((encontradas_absoluto/reais_absoluto)*100, 2)) + "%" + "\n")
    arquivo.write("Falha: " + str(abs(round((1 - (encontradas_absoluto/reais_absoluto))*100, 2))) + "%" + "\n")
    arquivo.write("\n\n")
    arquivo.write("Quantidade real" + " - " + "Quantidade prevista" + " - " + "Nome do arquivo" + " - " + "MSE" + "\n")
    for i in range(0, len(test_y)):
        mse = calcularMSE(test_y[i], predict_y[i])
        total_mse.append(mse)
        arquivo.write(str(str(test_y[i]) + " - " + str(predict_y[i]) + " - " + str(nomes[i])) + " - " + str(mse) + "\n")

    soma_mse = 0
    for mse in total_mse:
        soma_mse += mse
    
    media_mse = soma_mse / len(total_mse)
    arquivo.write("MSE: " + str(media_mse) + "\n")
    arquivo.write("rMSE: " + str(media_mse**0.5) + "\n")
    arquivo.close()
