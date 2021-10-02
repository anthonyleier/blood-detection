#Imports
import os
import streamlit as st
import tensorflow as tf
import urllib.request
import numpy as np
from numpy import asarray
import matplotlib.pyplot as plt
from object_detection.utils import config_util, visualization_utils as viz_utils
from object_detection.builders import model_builder
from PIL import Image, ImageDraw

# Informações
st.set_page_config(layout="wide")
st.header("Object Detection Aplicado em Células Sanguíneas")
st.write('O modelo de Deep Learning foi treinado utilizando o <a href="https://github.com/Shenggan/BCCD_Dataset" target="_blank">BCCD Dataset</a>, para fins de teste deve-se utilizar imagens dessa fonte.', unsafe_allow_html=True)

# Input da Imagem
imagem = ".model-triple/dataset-triple/test/imagens/BloodImage_00334.jpg"

# def escolheArquivo(pasta="./bccd/BCCD/JPEGImages"):
#     arquivos = os.listdir(pasta)
#     arquivo_escolhido = st.selectbox('Escolha uma imagem:', arquivos)
#     return os.path.join(pasta, arquivo_escolhido)

# imagem = escolheArquivo()

imagem = st.text_input(label="Insira o link direto da imagem:", value="https://raw.githubusercontent.com/Shenggan/BCCD_Dataset/master/BCCD/JPEGImages/BloodImage_00317.jpg")
urllib.request.urlretrieve(imagem, "imagem_cache")
imagem = "imagem_cache"

# Funções Úteis para Processamento
def detectar(input_tensor, model):
    prepross_image, formas = model.preprocess(input_tensor)
    predicao_dict = model.predict(prepross_image, formas)
    return model.postprocess(predicao_dict, formas)

def plotDetections(imagem, boxes, classes, scores, categoria, porcentagem_acerto):
    imagemDeteccao = imagem.copy()
    resultado = viz_utils.visualize_boxes_and_labels_on_image_array(
        imagemDeteccao, boxes, classes, scores, categoria, use_normalized_coordinates=True, min_score_thresh=porcentagem_acerto)
    return resultado

def convertImageToArray(path):
    image = Image.open(path)
    array = asarray(image)
    return array

# Processamento
def processar(nome, pasta_base, porcentagem_acerto):
    print("Iniciando processamento - " + nome)
    celula = 1
    offset = 1
    categorias = {celula: {'id': celula, 'name': nome}}


    tf.keras.backend.clear_session()
    num_classes = 1
    pipeline_config = pasta_base + "/pipeline.config"
    checkpoint_path = pasta_base + "/checkpoint/ckpt-1"
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


    imagem_np = np.expand_dims(convertImageToArray(imagem), axis=0)
    imagem_tensor = tf.convert_to_tensor(imagem_np, dtype=tf.float32)
    imagem_detectada = detectar(imagem_tensor, model)
    imagem_pronta = plotDetections(imagem_np[0],
        imagem_detectada['detection_boxes'][0].numpy(),
        imagem_detectada['detection_classes'][0].numpy().astype(np.uint32) + offset,
        imagem_detectada['detection_scores'][0].numpy(),
        categorias, porcentagem_acerto)
    print("Processamento finalizado! - " + nome)

    scores = imagem_detectada['detection_scores'][0].numpy()

    pontuacao = np.squeeze(scores)
    contador = 0
    for i in range(100):
        if scores is None or pontuacao[i] > porcentagem_acerto:
                contador = contador + 1

    return {"imagem": imagem_pronta, "contador": contador}

wbc_model_path = "./model-triple/results-triple/24_0.02_500_0.5_ssd_resnet50_v1_fpn_640x640_coco17_tpu-8/wbc/model"
rbc_model_path = "./model-triple/results-triple/24_0.1_500_0.1_ssd_resnet50_v1_fpn_640x640_coco17_tpu-8/rbc/model"
platelets_model_path = "./model-triple/results-triple/24_0.05_500_0.5_ssd_resnet50_v1_fpn_640x640_coco17_tpu-8/platelets/model"

col1, col2, col3 = st.columns(3)

col1.subheader("WBC")
wbc = processar("WBC", wbc_model_path, 0.5)
col1.image(image=wbc['imagem'], caption=str(wbc['contador']) + " células encontradas!")

col2.subheader("RBC")
rbc = processar("RBC", rbc_model_path, 0.1)
col2.image(image=rbc['imagem'], caption=str(rbc['contador']) + " células encontradas!")

col3.subheader("Platelets")
platelets = processar("Platelets", platelets_model_path, 0.5)
col3.image(image=platelets['imagem'], caption=str(platelets['contador']) + " células encontradas!")
