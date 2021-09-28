from http.server import BaseHTTPRequestHandler, HTTPServer
import numpy as np
import tensorflow as tf
from PIL import Image, ImageDraw
from numpy import asarray
from object_detection.utils import config_util, visualization_utils as viz_utils
import matplotlib.pyplot as plt
import os


porcentagem_acerto = 0.1
offset = 1

# Converte a imagem em array


def convertImageToArray(path):
    image = Image.open(path)
    array = asarray(image)
    return array


# Imprime as detecções na imagem
def plotDetections(imagem, boxes, classes, scores, categoria, nome=None):
    imagemDeteccao = imagem.copy()
    viz_utils.visualize_boxes_and_labels_on_image_array(
        imagemDeteccao, boxes, classes, scores, categoria, use_normalized_coordinates=True, min_score_thresh=porcentagem_acerto)

    if nome:
        pontuacao = np.squeeze(scores)
        contador = 0
        for i in range(100):
            if scores is None or pontuacao[i] > porcentagem_acerto:
                contador = contador + 1

        mensagem = str(contador) + " WBCs"

        plt.imsave(nome, imagemDeteccao)
        img = Image.open(nome)
        editor = ImageDraw.Draw(img)
        editor.text((10, 10), mensagem, fill=(255, 255, 0))

        img.save(nome)
    else:
        plt.imshow(imagemDeteccao)


def detectar(model, input_tensor):
    prepross_image, formas = model.preprocess(input_tensor)
    predicao_dict = model.predict(prepross_image, formas)
    return model.postprocess(predicao_dict, formas)


def modelagem(model, imagem):
    imagem_adaptada = np.expand_dims(convertImageToArray(imagem), axis=0)
    tensor = tf.convert_to_tensor(imagem_adaptada, dtype=tf.float32)
    deteccao = detectar(model, tensor)
    wbc_id = 1
    categorias = {wbc_id: {'id': wbc_id, 'name': 'wbc'}}
    plotDetections(
        imagem_adaptada[0],
        deteccao['detection_boxes'][0].numpy(),
        deteccao['detection_classes'][0].numpy().astype(np.uint32) + offset,
        deteccao['detection_scores'][0].numpy(),
        categorias, nome="imagem.jpg")


class handler(BaseHTTPRequestHandler):

    model = "modelo"
    imagem = "imagem"

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        modelagem(self.model, self.imagem)

        self.wfile.write(bytes("Teste de Modelo", "utf8"))
        self.wfile.write(bytes(str(self.imagem), "utf8"))


def start(modelo, imagem):
    with HTTPServer(('', 8000), handler) as server:
        handler.model = modelo
        handler.imagem = imagem
        server.serve_forever()
