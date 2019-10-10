import os
import re
import cv2
import numpy as np 
from google.colab.patches import cv2_imshow
import tensorflow as tf
import keras
# Import the libraries needed for saving models
# Note that in some other tutorials these are framed as coming from tensorflow_serving_api which is no longer correct
from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import tag_constants, signature_constants, signature_def_utils_impl

img = cv2.imread('/content/drive/My Drive/kaggle/cancer/base_dir/ham10000_images_part_1/ISIC_0024306.jpg')
     
print(img.shape)
imCopy = img.copy()
imgOut = cv2.resize(imCopy,(224,224))
print(imgOut.shape)
cv2_imshow(imgOut)


from keras.models import load_model
# model_name = tf_serving_keras_mobilenetv2
#model = load_model(f"model.h5")

def top_3_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=3)


def top_2_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=2)


keras.metrics.top_3_accuracy = top_3_accuracy
keras.metrics.top_2_accuracy = top_2_accuracy

model = load_model('model.h5')
print(model.summary())

# images will be the input key name
# scores will be the out key name
prediction_signature = tf.saved_model.signature_def_utils.predict_signature_def(
    {
    "images": model.input
    }, {
    "scores": model.output
    })

# export_path is a directory in which the model will be created
export_path = os.path.join(
    tf.compat.as_bytes('models/export/{}'.format(model)),
    tf.compat.as_bytes('1'))

# SavedModelBuilder will create the directory if it does not exist
builder = saved_model_builder.SavedModelBuilder(export_path)

sess = keras.backend.get_session()

# Add the meta_graph and the variables to the builder
builder.add_meta_graph_and_variables(
    sess, [tag_constants.SERVING],
    signature_def_map={
        'prediction': prediction_signature,
    })
# save the graph
builder.save()
