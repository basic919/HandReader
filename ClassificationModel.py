import tensorflow as tf
import numpy as np
from PIL import Image


class ClassificationModel:

    MODEL_PATH = r'ModelFiles/hand_reader_model_autosave.h5'

    def __init__(self):
        self.model = tf.keras.models.load_model(self.MODEL_PATH)

    def predict(self, inp=r'ModelFiles/input_examples/ex0_0.jpg'):  # TODO: Remove default test value
        """inp: path to the image to be classified"""

        img = np.array([np.array(Image.open(inp))])  # noqa
        img = img.reshape(1, 28, 28, 1)  # noqa
        img = img.astype('float32')
        img /= 255

        return str(np.argmax(self.model.predict(img)))


# def get_model():
#     MODEL_PATH = r'ModelFiles/hand_reader_model_autosave.h5'
#     print('Loading model...')
#     return tf.keras.models.load_model(MODEL_PATH)
#
#
# def predict(model, inp=r'ModelFiles/input_examples/ex0_0.jpg'):  # TODO: Remove default test value
#     img = np.array([np.array(Image.open(inp))])  # noqa
#     img = img.reshape(1, 28, 28, 1)  # noqa
#     img = img.astype('float32')
#     img /= 255
#
#     return str(np.argmax(model.predict(img)))


if __name__ == '__main__':

    IMAGE_PATH = r'ModelFiles/input_examples/ex0_0.jpg'

    model = ClassificationModel()

    print(model.predict(IMAGE_PATH))


