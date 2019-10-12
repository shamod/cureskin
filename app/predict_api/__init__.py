# Remove Tensorflow FutureWarnings that were filling up logs
import warnings
warnings.filterwarnings('ignore',category=FutureWarning)

import tensorflow as tf
from keras.preprocessing import image
import numpy as np
from werkzeug.datastructures import FileStorage

from app import app

class PredictAPI(object):

    def __top_2_accuracy(self, y_true, y_pred):
        return tf.keras.metrics.top_k_categorical_accuracy(y_true, y_pred, k=2)

    def __top_3_accuracy(self, y_true, y_pred):
        return tf.keras.metrics.top_k_categorical_accuracy(y_true, y_pred, k=3)

    def __init__(self, modelPath: str = './model/model.h5'):
        """
        Initalises API with Tensorflow model to load

        :param modelPath:   The file path to the TF model.
        """
        self.modelPath = modelPath

        # Load the model file - requires custom metric functions
        self.model = tf.keras.models.load_model(modelPath,
                                custom_objects={'categorical_accuracy': tf.keras.metrics.categorical_accuracy,
                                                'top_2_accuracy': self.__top_2_accuracy,
                                                'top_3_accuracy': self.__top_3_accuracy})

        # We grab a reference to the graph to ensure no threading issues
        # While running the prediction
        self.graph = tf.compat.v1.get_default_graph()

        app.logger.info(f"Loaded model {modelPath}")

    def predict(self, img: FileStorage):
        """
        Make a skin diagnosis prediction from an image

        :param img:     The image to classify by the model
        :return:        The highest prediction class and certainty
        """
        app.logger.debug(f"Predicting file {img.filename}")

        # Pre-process image
        input_image = image.load_img(img, target_size=(224, 224))
        input_image = image.img_to_array(input_image)
        input_image = np.expand_dims(input_image, axis=0)


        # Make sure we run prediction thread safe
        with self.graph.as_default():
            prediction = self.model.predict(input_image)

        # Get index of predicted class and Record prediction results in logs
        i = 0
        predicted_class = 0
        predicted_certainty = 0.0
        results = ""
        for result in np.nditer(prediction):

            certainty = round(result * 100, 2)

            if certainty > predicted_certainty:
                predicted_certainty = certainty
                predicted_class = i

            results += f"{i}. {PredictAPI.getClass(i)['name']}: {certainty}%\n"
            i += 1
        results += f"\nDiagnosis: {PredictAPI.getClass(predicted_class)['name']} - {round(predicted_certainty, 2)}"
        app.logger.debug(f"Prediction for {img.filename}:\n\n {results}")

        # Return prediction tuple
        return predicted_class, predicted_certainty

    @staticmethod
    def getClass(prediction: int):

        classes = [
            {
                'name': 'Melanoma',
                'url':  'https://www.mayoclinic.org/diseases-conditions/melanoma/diagnosis-treatment/drc-20374888'
            },
            {
                'name': 'Melanocytic Nevi',
                'url': 'https://emedicine.medscape.com/article/1058445-overview'
            },
            {
                'name': 'Actinic Keratoses (Solar Keratoses) or Intraepithelial Carcinoma',
                'url': 'https://www.mayoclinic.org/diseases-conditions/squamous-cell-carcinoma/symptoms-causes/syc-20352480'
            },
            {
                'name': 'Benign Keratosis',
                'url': 'https://www.mayoclinic.org/diseases-conditions/seborrheic-keratosis/symptoms-causes/syc-20353878'
            },
            {
                'name': 'Basal Cell Carcinoma',
                'url': 'https://www.mayoclinic.org/diseases-conditions/basal-cell-carcinoma/symptoms-causes/syc-20354187'
            },
            {
                'name': 'Dermatofibroma',
                'url': 'https://www.dermnetnz.org/topics/dermatofibroma/'
            },
            {
                'name': 'Vascular Skin Lesion',
                'url': 'https://www.ssmhealth.com/cardinal-glennon/pediatric-plastic-reconstructive-surgery/hemangiomas'
            }
        ]

        return classes[prediction]
