import tensorflow as tf
import logging

log = logging.getLogger('PredictAPI')

class PredictAPI(object):

    def __init__(self, modelPath: str):
        """
        Initalises API with Tensorflow model to load

        :param modelPath:   The file path to the TF model
        """
        self.modelPath = modelPath

        # Load the model file
        self.model = tf.keras.models.load_model(modelPath)

        log.info(f"Loaded model {modelPath}:\n{self.model.summary()}")

    def predict(self, img: str):
        """
        Make a skin diagnosis prediction from an image

        :param img:     The image to classify by the model
        :return:        The prediction
        """

        prediction =  self.model.predict(img)
        log.debug(f"Prediction: {prediction}")
        return prediction

    def getClass(self, prediction: int):

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