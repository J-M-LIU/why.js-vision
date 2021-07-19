import threading

import tensorflow as tf
from keras.models import load_model
facial_expression_model_path = 'models/face_expression.hdf5'
fall_model_path = 'models/fall_detection.hdf5'

class MyModel:
    def __init__(self,path):
        self.path=path
        self.model_graph=tf.Graph()
        self.model_sess=tf.Session(graph=self.model_graph)
        self.model=self.load()


    def load(self):
        with self.model_sess.as_default():
            with self.model_graph.as_default():
                return load_model(self.path)


    def model_predict(self,roi):
        with self.model_sess.as_default():
            with self.model_graph.as_default():
                return self.model.predict(roi)




