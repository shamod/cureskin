# Remove Tensorflow FutureWarnings that were filling up logs
import warnings
warnings.filterwarnings('ignore',category=FutureWarning)

import numpy as np
import keras
import os

dir = os.path.realpath(__file__).replace("predict_test.py", "")

# Define Top2 and Top3 Accuracy
from keras.metrics import categorical_accuracy, top_k_categorical_accuracy

def top_3_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=3)


def top_2_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=2)


keras.metrics.top_3_accuracy = top_3_accuracy
keras.metrics.top_2_accuracy = top_2_accuracy

model = keras.models.load_model(dir + 'model.h5')

model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics=[categorical_accuracy, top_2_accuracy, top_3_accuracy])

from keras.preprocessing import image

test_image = image.load_img(dir + 'test_imgs/ISIC_0024702_Mel.jpg', target_size = (224, 224))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)

#predict the result
prediction = model.predict(test_image)

CANCER_CLASSES = {
 0: 'Melanoma',
 1: 'Melanocytic Nevi',
 2: 'Actinic Keratoses (Solar Keratoses) or Intraepithelial Carcinoma',
 3: 'Benign Keratosis',
 4: 'Basal Cell Carcinoma',
 5: 'Dermatofibroma',
 6: 'Vascular Skin Lesion'
}

i = 0
for result in np.nditer(prediction):
    print(f"{i}. {CANCER_CLASSES[i]}: {round(result * 100, 2)}%")
    i += 1
