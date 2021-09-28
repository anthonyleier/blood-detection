import matplotlib.pyplot as plt
import os
import random
import numpy as np
import tensorflow as tf
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw
from numpy import asarray
from bs4 import BeautifulSoup as bs

from object_detection.utils import config_util, visualization_utils as viz_utils
from object_detection.builders import model_builder

porcentagem_acerto = 0.1

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

        mensagem = str(contador) + " WBCs"

        plt.imsave(nome, imagemDeteccao)
        img = Image.open(nome)
        editor = ImageDraw.Draw(img)
        editor.text((10, 10), mensagem, fill=(255, 255, 0))

        img.save(nome)
    else:
        plt.imshow(imagemDeteccao)

tf.keras.backend.clear_session()
print('Construindo modelo e restaurando pesos para fine-tuning...', flush=True)

# Parâmetros do modelo
num_classes = 1
pipeline_config = './prototype/saves/wbc/pipeline.config'
checkpoint_path = './prototype/saves/wbc/checkpoint/ckpt-1'

# Importação e definição
configs = config_util.get_configs_from_pipeline_file(pipeline_config)
model_config = configs['model']
model_config.ssd.num_classes = num_classes
model_config.ssd.freeze_batchnorm = True

# Construção do Modelo
model = model_builder.build(model_config=model_config, is_training=True)

fakebox_predictor = tf.compat.v2.train.Checkpoint(_base_tower_layers_for_heads=model._box_predictor._base_tower_layers_for_heads,
                                                  _box_prediction_head=model._box_predictor._box_prediction_head)
fake_model = tf.compat.v2.train.Checkpoint(
    _feature_extractor=model._feature_extractor, _box_predictor=fakebox_predictor)

checkpoint = tf.compat.v2.train.Checkpoint(model=fake_model)
checkpoint.restore(checkpoint_path).expect_partial()

# image, shapes = model.preprocess(tf.zeros([1, 640, 640, 3]))
# prediction_dict = model.predict(image, shapes)
# _ = model.postprocess(prediction_dict, shapes)

print('Pesos restaurados!')


test_image_dir = './model-triple/dataset-triple/test/imagens/'
test_images = []
test_images_nomes = []

for elemento in os.listdir(test_image_dir):
    imagem = os.path.join(test_image_dir, elemento)
    test_images_nomes.append(elemento)
    test_images.append(np.expand_dims(convertImageToArray(imagem), axis=0))

@tf.function
def detectar(input_tensor):
    prepross_image, formas = model.preprocess(input_tensor)
    predicao_dict = model.predict(prepross_image, formas)
    return model.postprocess(predicao_dict, formas)


imagem_path = "./prototype/saves/resultados/"
wbc_id = 1
categorias = {wbc_id: {'id': wbc_id, 'name': 'wbc'}}

offset = 1
for i in range(len(test_images)):
    test_tensor = tf.convert_to_tensor(test_images[i], dtype=tf.float32)
    deteccoes = detectar(test_tensor)

    plotDetections(
        test_images[i][0],
        deteccoes['detection_boxes'][0].numpy(),
        deteccoes['detection_classes'][0].numpy().astype(np.uint32) + offset,
        deteccoes['detection_scores'][0].numpy(),
        categorias, nome=imagem_path + test_images_nomes[i])