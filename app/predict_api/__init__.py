# Remove Tensorflow FutureWarnings that were filling up logs
import warnings
warnings.filterwarnings('ignore',category=FutureWarning)

import tensorflow as tf
from werkzeug.datastructures import FileStorage

from app import app

class PredictAPI(object):

    def __top_2_accuracy(self, y_true, y_pred):
        tf.keras.metrics.top_k_categorical_accuracy(y_true, y_pred, k=2)

    def __top_3_accuracy(self, y_true, y_pred):
        tf.keras.metrics.top_k_categorical_accuracy(y_true, y_pred, k=3)

    def __init__(self, modelPath: str = './model/model.h5'):
        """
        Initalises API with Tensorflow model to load

        :param modelPath:   The file path to the TF model.
        """
        self.modelPath = modelPath

        # Load the model file - for some reason model requires custom metric functions
        #tf.keras.metrics.top_3_accuracy = self.__top_3_accuracy
        #tf.keras.metrics.top_2_accuracy = self.__top_2_accuracy

        self.model = tf.keras.models.load_model(modelPath,
                                custom_objects={'top_2_accuracy': self.__top_2_accuracy,
                                                'top_3_accuracy': self.__top_3_accuracy})
        print(self.model.summary())


        app.logger.info(f"Loaded model {modelPath}:\n{self.model.summary()}")

    def predict(self, img: FileStorage):
        """
        Make a skin diagnosis prediction from an image

        :param img:     The image to classify by the model
        :return:        The prediction
        """
        app.logger.debug(f"Predicting file {img.filename}")

        #prediction = self.model.predict(img)
        prediction = None

        # diagnosis = Diagnosis(
        #     time=int(time.time()),
        #     filename=img.filename,
        #     img=img.read(),
        #     prediction=1,
        #     certainty=0.953
        # )

        app.logger.debug(f"Prediction: {prediction}")
        return prediction

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
