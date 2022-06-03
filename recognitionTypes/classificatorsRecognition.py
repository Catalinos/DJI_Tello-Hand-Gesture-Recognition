from traceback import clear_frames
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import os
os.chdir("D:\Git\HandGestNotebook\DJI_Tello-Hand-Gesture-Recognition")

class ClassificatorRecognition:

    def __init__(self):
        self.gestureNameList = ["forward", "backward", "left", "right", "up", "down", "rotate left", "rotate right", "stop", "land"]
        self.handData = {'0x':[],'0y':[], '1x':[], '1y':[], '2x':[], '2y':[], '3x':[],'3y':[], '4x':[], '4y':[], '5x':[ ], '5y':[], '6x':[ ], '6y':[], '7x':[ ], '7y':[], '8x':[ ], '8y':[], '9x':[ ],
                '9y':[], '10x':[ ], '10y':[], '11x':[ ], '11y':[], '12x':[ ], '12y':[], '13x':[ ], '13y':[], '14x':[ ], '14y':[], '15x':[ ], '15y':[], '16x':[ ], '16y':[], 
                '17x':[ ], '17y':[], '18x':[ ], '18y':[], '19x':[ ], '19y':[], '20x':[ ], '20y':[]}

        self.clf = DecisionTreeClassifier(random_state=0)
        self.handDF = pd.read_pickle("handsDataset/OtherDataset.pickle")
        self.X_test = pd.DataFrame()
        self.y_test = []

    def startClassificator(self):
        
        handDF = self.handDF.dropna(axis='columns')
        handDF.isnull().sum().sum()

        train,test = train_test_split(handDF,test_size = 0.2)

        X_train = pd.DataFrame()
        y_train = train["IdGesture"]
        self.y_test = test["IdGesture"]
        for i in range (21):
            X_train[str(i)+"x"] = train[str(i)+"x"]
            X_train[str(i)+"y"] = train[str(i)+"y"]
            self.X_test[str(i)+"x"] = test[str(i)+"x"]
            self.X_test[str(i)+"y"] = test[str(i)+"y"]

        self.clf.fit(X_train,y_train)

    def printAccuracy(self):
        yhat_test = self.clf.predict(self.X_test)

        acc = accuracy_score(self.y_test, yhat_test)

        print(acc)

    def doRandomTest(self):
        fortest = self.X_test.sample(1)
        toValidate = self.y_test[fortest.index[0]]

        topredict = self.clf.predict(fortest)[0]
        print(topredict)
        print(toValidate)


        values = fortest.values[0]
        x_vals = values[0::2] / values[0]
        y_vals = values[1::2] / values[1]

        print(x_vals, y_vals)

        fig = plt.figure(figsize=(10,4))

        ax1 = fig.add_subplot(121)
        ax1.invert_yaxis()
        ax1.scatter(y_vals,x_vals)
        ax1.set_title(f"Gestul pentru {self.gestureNameList[int(topredict)]}")

    def getGestureName(self, fingerLandmark, w, h):
            x0_point = int(fingerLandmark[0].x * w)
            y0_point = int(fingerLandmark[0].y * h)
            for i in range(0,21):
                cx = int(fingerLandmark[i].x * w) / x0_point
                cy = int(fingerLandmark[i].y * h) / y0_point
                self.handData[str(i) + 'x'] = cx
                self.handData[str(i) + 'y'] = cy
            dataFrame = self.X_test.sample(1)
            dataFrame = pd.DataFrame([self.handData])
            
            gesture = self.clf.predict(dataFrame)[0]
            return self.gestureNameList[int(gesture)], int(gesture)

    def getDataFrame(self):
        return self.handDF
    
    def showDataFrame(self):
        print(self.handDF)