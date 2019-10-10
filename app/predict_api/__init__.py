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