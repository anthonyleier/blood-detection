#Imports
import os
import streamlit as st
import tensorflow as tf
import numpy as np
from numpy import asarray
import matplotlib.pyplot as plt
from object_detection.utils import config_util, visualization_utils as viz_utils
from object_detection.builders import model_builder
from PIL import Image, ImageDraw

# Informações
st.write("# Protótipo de Object Detection Aplicado em Células Sanguíneas")
st.write("O modelo de Deep Learning foi treinado utilizando o BCCD Dataset (https://github.com/Shenggan/BCCD_Dataset)")
st.write("Portanto, para fins de teste deve-se utilizar imagens dessa fonte.")

# Input da Imagem
imagem = ".model-triple/dataset-triple/test/imagens/BloodImage_00334.jpg"

def escolheArquivo(pasta="./model-triple/dataset-triple/test/imagens"):
    arquivos = os.listdir(pasta)
    arquivo_escolhido = st.selectbox('Escolha uma imagem:', arquivos)
    return os.path.join(pasta, arquivo_escolhido)

imagem = escolheArquivo()

# Processamento
porcentagem_acerto = 0.5
wbc_id = 1
offset = 1
categorias = {wbc_id: {'id': wbc_id, 'name': 'wbc'}}

tf.keras.backend.clear_session()
num_classes = 1
pipeline_config = './model-triple/results-triple/24_0.02_500_0.5_ssd_resnet50_v1_fpn_640x640_coco17_tpu-8/wbc/model/pipeline.config'
checkpoint_path = './model-triple/results-triple/24_0.02_500_0.5_ssd_resnet50_v1_fpn_640x640_coco17_tpu-8/wbc/model/checkpoint/ckpt-1'
configs = config_util.get_configs_from_pipeline_file(pipeline_config)
model_config = configs['model']
model_config.ssd.num_classes = num_classes
model_config.ssd.freeze_batchnorm = True
model = model_builder.build(model_config=model_config, is_training=True)
checkpoint = tf.compat.v2.train.Checkpoint(model=model)
checkpoint.restore(checkpoint_path).expect_partial()
image, shapes = model.preprocess(tf.zeros([1, 640, 640, 3]))
prediction_dict = model.predict(image, shapes)
_ = model.postprocess(prediction_dict, shapes)

def detectar(input_tensor):
    prepross_image, formas = model.preprocess(input_tensor)
    predicao_dict = model.predict(prepross_image, formas)
    return model.postprocess(predicao_dict, formas)

def plotDetections(imagem, boxes, classes, scores, categoria):
    imagemDeteccao = imagem.copy()
    resultado = viz_utils.visualize_boxes_and_labels_on_image_array(
        imagemDeteccao, boxes, classes, scores, categoria, use_normalized_coordinates=True, min_score_thresh=porcentagem_acerto)
    return resultado

def convertImageToArray(path):
    image = Image.open(path)
    array = asarray(image)
    return array

imagem_np = np.expand_dims(convertImageToArray(imagem), axis=0)
imagem_tensor = tf.convert_to_tensor(imagem_np, dtype=tf.float32)
imagem_detectada = detectar(imagem_tensor)
imagem_pronta = plotDetections(imagem_np[0],
    imagem_detectada['detection_boxes'][0].numpy(),
    imagem_detectada['detection_classes'][0].numpy().astype(np.uint32) + offset,
    imagem_detectada['detection_scores'][0].numpy(),
    categorias)

st.write("Resultado WBC:")
st.image(imagem_pronta, caption=None, width=None, use_column_width=None, clamp=False, channels='RGB', output_format='auto')
