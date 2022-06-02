from copyreg import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

import tensorflow as tf


import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report

import os
os.chdir("D:\Git\HandGestNotebook\DJI_Tello-Hand-Gesture-Recognition")

class NeuralRecognition:

    def __init__(self):
        self.gestureNameList = ["forward", "backward", "left", "right", "up", "down", "rotate left", "rotate right", "stop", "land"]
        self.handData = {'0x':[],'0y':[], '1x':[], '1y':[], '2x':[], '2y':[], '3x':[],'3y':[], '4x':[], '4y':[], '5x':[ ], '5y':[], '6x':[ ], '6y':[], '7x':[ ], '7y':[], '8x':[ ], '8y':[], '9x':[ ],
                    '9y':[], '10x':[ ], '10y':[], '11x':[ ], '11y':[], '12x':[ ], '12y':[], '13x':[ ], '13y':[], '14x':[ ], '14y':[], '15x':[ ], '15y':[], '16x':[ ], '16y':[], 
                    '17x':[ ], '17y':[], '18x':[ ], '18y':[], '19x':[ ], '19y':[], '20x':[ ], '20y':[]}
        self.dataset = 'handsDataset/OtherDataset.csv'
        self.model_save_path = 'keypoint_classifier/keypoint_classifier.hdf5'
        self.tflite_save_path = 'keypoint_classifier/keypoint_classifier.tflite'
        self.NUM_CLASSES = 10

    def trainNetwork(self, save_model):

        handDataFrame = pd.read_pickle("handsDataset/OtherDataset.pickle")

        train,test = train_test_split(handDataFrame,test_size = 0.2)
        X_dataset = np.loadtxt(self.dataset, delimiter=',', dtype='float32', usecols=list(range(2, (21 * 2) + 2)))
        y_dataset = np.loadtxt(self.dataset, delimiter=',', dtype='int32', usecols=(1))

        X_trainNeural, X_testNeural, y_trainNeural, y_testNeural = train_test_split(X_dataset, y_dataset, train_size=0.8, random_state=42)

        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Input((21 * 2, )),
            tf.keras.layers.Dropout(0.0),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dropout(0.0),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dropout(0.0),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(self.NUM_CLASSES, activation='softmax')
        ])

        if save_model == True:
            # Model checkpoint callback
            cp_callback = tf.keras.callbacks.ModelCheckpoint(
                self.model_save_path, verbose=1, save_weights_only=False, save_best_only=True)
            # Callback for early stopping
            es_callback = tf.keras.callbacks.EarlyStopping(patience=50, verbose=1)

        self.model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        self.history = self.model.fit(
            X_trainNeural,
            y_trainNeural,
            epochs=11,
            batch_size=64,
            validation_data=(X_testNeural, y_testNeural),
            callbacks=[cp_callback, es_callback]
        )

        history_DF = pd.DataFrame(self.history.history)

        with open('keypoint_classifier/train_history.json', 'wb') as fileJSON:
            history_DF.to_json(fileJSON)


    def getGestureName(self, fingerLandmark, w, h):
            x0_point = int(fingerLandmark[0].x * w)
            y0_point = int(fingerLandmark[0].y * h)

            to_predict = []
            for i in range(0,21):
                cx = int(fingerLandmark[i].x * w) / x0_point
                cy = int(fingerLandmark[i].y * h) / y0_point
                to_predict.append(cx)
                to_predict.append(cy)
            
            gesture = self.model.predict(to_predict)[0]
            return self.gestureNameList[int(gesture)]

    def plot_model_acuracy(self):
        self.get_saved_history()
        history = self.history
        plt.plot(history['accuracy'])
        plt.plot(history['val_accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()

    def plot_model_loss(self):
        self.get_saved_history()
        history = self.history
        plt.plot(history['loss'])
        plt.plot(history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()

    def load_saved_model(self, model_path):
        self.model = tf.keras.models.load_model(model_path)

    def getGestureName(self, fingerLandmark, w, h):
        x0_point = int(fingerLandmark[0].x * w)
        y0_point = int(fingerLandmark[0].y * h)
        for i in range(0,21):
            cx = int(fingerLandmark[i].x * w) / x0_point
            cy = int(fingerLandmark[i].y * h) / y0_point
            self.handData[str(i) + 'x'] = cx
            self.handData[str(i) + 'y'] = cy
        dataFrame = pd.DataFrame([self.handData])
        gesture = self.model.predict(dataFrame)[0]
        maxval = max(gesture)
        index = np.where(gesture==maxval)
        gestureid = index[0][0]
        return self.gestureNameList[int(gestureid)]

    def get_saved_history(self):
        self.history = pd.read_json('keypoint_classifier/train_history.json')
        return self.history

