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
from tensorflow.keras.models import load_model

new_model = load_model(os.path.join('WhiteCellClass','models','Classify_White_Blood_Cell_Final_Cropped.h5'))
classList = ['Basófilo', 'Eosinófilo', 'Linfócito', 'Monócito', 'Neutrófilo']

# Informações
st.set_page_config(layout="wide")
st.header("Object Detection e CNN Aplicado em Células Sanguíneas")
st.write('O modelo Object Detection para detecção foi treinado utilizando o <a href="https://github.com/Shenggan/BCCD_Dataset" target="_blank">BCCD Dataset</a>, para fins de teste deve-se utilizar imagens dessa fonte.', unsafe_allow_html=True)
st.write('O modelo CNN de Classificação foi treinado utilizando o <a href="https://data.mendeley.com/datasets/snkd93bnjr/1" target="_blank">PBC Dataset</a>.', unsafe_allow_html=True)

# Input da Imagem
#def escolheArquivo(pasta="./WhiteCellClass/test"):
#    arquivos = os.listdir(pasta)
#    arquivo_escolhido = st.selectbox('Escolha uma imagem:', arquivos)
#    return os.path.join(pasta, arquivo_escolhido)

#imagem = escolheArquivo()

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
    classes = []
    classe = ''
    cropped_image = ''
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
    imagem_tensor = tf.convert_to_tensor(value=imagem_np, dtype=tf.float32)
    imagem_detectada = detectar(imagem_tensor, model)
    imagem_pronta = plotDetections(imagem_np[0],
        imagem_detectada['detection_boxes'][0].numpy(),
        imagem_detectada['detection_classes'][0].numpy().astype(np.uint32) + offset,
        imagem_detectada['detection_scores'][0].numpy(),
        categorias, porcentagem_acerto)
    
    cropped_image = imagem_pronta
    
    if nome == 'WBC':
        scores    = imagem_detectada['detection_scores'][0]
        boxes     = imagem_detectada['detection_boxes'][0]
        imgShape  = imagem_pronta.shape
        im_height = imgShape[0]
        im_width  = imgShape[1]
        
        for idx in range(len(boxes)):
            if scores[idx] >= porcentagem_acerto:
                #Region of Interest
                y_min = int(boxes[idx][0] * im_height * .9)
                y_min = (y_min if y_min > 0 and y_min < im_height else boxes[idx][0])
                
                x_min = int(boxes[idx][1] * im_width * .9)
                x_min = (x_min if x_min > 0 and x_min < im_width else boxes[idx][1])
                
                y_max = int(boxes[idx][2] * im_height)
                y_max = (y_max if y_max > 0 and y_max < im_height else boxes[idx][2])
                
                x_max = int(boxes[idx][3] * im_width)
                x_max = (x_max if x_max > 0 and x_max < im_width else boxes[idx][3])

                cropped_image = tf.image.crop_to_bounding_box(imagem_np[0], y_min, x_min, y_max - y_min, x_max - x_min).numpy()

                new_pred = new_model.predict(np.expand_dims(tf.image.resize(cropped_image, (200,200)),0))

                classe = classList[np.argmax(new_pred)]
                classes.append([np.round(scores[idx].numpy(),2), classe, cropped_image, new_pred.round(2) * 100])

    
    print("Processamento finalizado! - " + nome)

    scores = imagem_detectada['detection_scores'][0].numpy()

    pontuacao = np.squeeze(scores)
    contador = 0
    for i in range(100):
        if scores is None or pontuacao[i] > porcentagem_acerto:
                contador = contador + 1

    return {"imagem": imagem_pronta, "contador": contador, "classes": classes}

wbc_model_path = "./model-triple/results-triple/24_0.02_500_0.5_ssd_resnet50_v1_fpn_640x640_coco17_tpu-8/wbc/model"
rbc_model_path = "./model-triple/results-triple/24_0.1_500_0.1_ssd_resnet50_v1_fpn_640x640_coco17_tpu-8/rbc/model"
platelets_model_path = "./model-triple/results-triple/24_0.05_500_0.5_ssd_resnet50_v1_fpn_640x640_coco17_tpu-8/platelets/model"

col1, col2, col3 = st.columns(3)

col1.subheader("WBC")
wbc = processar("WBC", wbc_model_path, 0.5)
col1.image(image=wbc['imagem'], caption=str(wbc['contador']) + " células encontradas!")

if wbc["classes"]:
    col1.subheader("Classes: "+str(classList))
    
    for Class in wbc["classes"]:
        col1.image(image=Class[2], caption="Célula " +Class[1]+ " com " + str(Class[0]) + "% de detecção!! Predição por Classe: "+str(np.squeeze(Class[3], axis=0)))

col2.subheader("RBC")
rbc = processar("RBC", rbc_model_path, 0.3)
col2.image(image=rbc['imagem'], caption=str(rbc['contador']) + " células encontradas!")

col3.subheader("Platelets")
platelets = processar("Platelets", platelets_model_path, 0.5)
col3.image(image=platelets['imagem'], caption=str(platelets['contador']) + " células encontradas!")
