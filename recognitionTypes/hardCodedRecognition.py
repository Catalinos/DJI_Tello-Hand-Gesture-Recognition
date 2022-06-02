
import math
import os
import random
import pandas as pd
directory = "D:\Git\HandGestNotebook"
os.chdir(directory)



hand_data = {'IdGesture': [], '0x':[],'0y':[], '1x':[], '1y':[], '2x':[], '2y':[], '3x':[],'3y':[], '4x':[], '4y':[], '5x':[ ], '5y':[], '6x':[ ], '6y':[], '7x':[ ], '7y':[], '8x':[ ], '8y':[], '9x':[ ],
                '9y':[], '10x':[ ], '10y':[], '11x':[ ], '11y':[], '12x':[ ], '12y':[], '13x':[ ], '13y':[], '14x':[ ], '14y':[], '15x':[ ], '15y':[], '16x':[ ], '16y':[], 
                '17x':[ ], '17y':[], '18x':[ ], '18y':[], '19x':[ ], '19y':[], '20x':[ ], '20y':[] }

gestureNameList = ["forward", "backward", "left", "right", "up", "down", "rotate left", "rotate right", "stop", "land"]


# Functions for saving the data
def appendDataToDict(fingerLandmarks, w, h, id):

    if(checkInRectangle(fingerLandmarks, w, h)):
        return " Not inserted";
    hand_data['IdGesture'].append(str(id))
    x0_point = int(fingerLandmarks[0].x * w)
    y0_point = int(fingerLandmarks[0].y * h)

    for i in range(0,21):
        y_point = int(fingerLandmarks[i].y * h) / y0_point
        x_point = int(fingerLandmarks[i].x * w) / x0_point
        hand_data[str(i)+'x'].append(x_point)
        hand_data[str(i)+'y'].append(y_point)

    return " Inserted"

def saveDataToPickle(filename):
    handDF = pd.DataFrame.from_dict(hand_data, orient='columns')
    handDF = handDF.dropna(axis='columns')
    handDF.isnull().sum().sum()
    handDF.to_pickle("filename")


# Functions for checking 
def getFingerPosition(fingerLandmark, w, h):
    print(int(fingerLandmark.x*w), int(fingerLandmark.y*h))

def checkContinousFingerPoints(fingerLandmark, startingPoint, h):
    index1 = int(fingerLandmark[startingPoint].y * h)
    index2 = int(fingerLandmark[startingPoint + 1].y * h)
    index3 = int(fingerLandmark[startingPoint + 2].y * h)

    if index1 > index2 > index3:
        return True
    return False

def checkNotContinousFinger(fingerLandmark, h):

    if (not checkContinousFingerPoints(fingerLandmark, 6, h) and not checkContinousFingerPoints(fingerLandmark, 10, h)
        and not checkContinousFingerPoints(fingerLandmark, 14, h) and not checkContinousFingerPoints(fingerLandmark, 18, h)):

        return False

    return True

def checkXDiscontinuityFingerPoints(fingerLandmark, startingPoint, w):
    index1 = int(fingerLandmark[startingPoint].x * w)
    index2 = int(fingerLandmark[startingPoint + 1].x * w)
    index3 = int(fingerLandmark[startingPoint+2].x * w)

    if index1 > index2 > index3 :
        return True
    return False

def checkInRectangle(handLandmarks, w, h):
    for landmarks in handLandmarks:
        cx, cy = int ( landmarks.x * w ), int ( landmarks.y * h )
        if cx not in range(20,300) or cy not in range(20,400):
            return True
    return False

def checkPointsRange(handLandmarks, w, h):
    for landmarks in handLandmarks:
        cx, cy = int ( landmarks.x * w ), int ( landmarks.y * h )
        if cx not in range(0,w) or cy not in range(0,h):
            return True
    return False



# Functions for recognising gestures
def recogniseOkGesture (fingerLandmarks,w,h):
    indexFingerX = int(fingerLandmarks[8].x * w)
    indexFingerY = int(fingerLandmarks[8].y * h)
    bigFingerX = int(fingerLandmarks[4].x * w)
    bigFingerY = int(fingerLandmarks[4].y * h)
    dist = math.hypot(indexFingerX - bigFingerX, indexFingerY - bigFingerY)
    if checkContinousFingerPoints(fingerLandmarks, 10, h) and checkContinousFingerPoints(fingerLandmarks, 14, h) and checkContinousFingerPoints(fingerLandmarks, 18, h):
        if dist < 20:
            return True
    return False

def recognisePeaceGesture (fingerLandmarks,w,h):
    ringFingerY = int(fingerLandmarks[14].y * h)
    pinkyFingerY = int(fingerLandmarks[18].y * h)
    middleFingerY = int(fingerLandmarks[10].y * h)
    if checkContinousFingerPoints(fingerLandmarks, 10, h) and checkContinousFingerPoints(fingerLandmarks, 6, h):
        if pinkyFingerY > ringFingerY > middleFingerY:
            if not checkContinousFingerPoints(fingerLandmarks, 14, h) and not checkContinousFingerPoints(fingerLandmarks, 18, h):
                return True
    return False

def recogniseLikeGesture(fingerLandmarks, w, h):
    ringFingerY = int( fingerLandmarks[13].y * h )
    pinkyFingerY = int( fingerLandmarks[17].y * h )
    middleFingerY = int( fingerLandmarks[9].y * h )
    indexFingerY = int( fingerLandmarks[5].y * h )
    if checkContinousFingerPoints(fingerLandmarks, 2, h):
        if indexFingerY < middleFingerY < ringFingerY < pinkyFingerY:
            if not checkContinousFingerPoints(fingerLandmarks, 10, h) and not checkContinousFingerPoints(fingerLandmarks, 14, h):
                if checkXDiscontinuityFingerPoints(fingerLandmarks,6,w) and checkXDiscontinuityFingerPoints(fingerLandmarks,10,w) and checkXDiscontinuityFingerPoints(fingerLandmarks,14,w) and checkXDiscontinuityFingerPoints(fingerLandmarks,18,w):
                    return True
    return False

def recogniseUpGesture(fingerLandmarks, w, h):

    dip_middleY = int (fingerLandmarks[10].y * h)
    dip_ringY = int(fingerLandmarks[14].y * h)
    dip_pinkyY = int(fingerLandmarks[18].y * h)

    if checkContinousFingerPoints(fingerLandmarks,6,h):
        if not checkContinousFingerPoints(fingerLandmarks,10,h) and not checkContinousFingerPoints(fingerLandmarks,14,h) and not checkContinousFingerPoints(fingerLandmarks,18,h):
            if(dip_middleY < dip_ringY < dip_pinkyY):
                return True
    return False

def recogniseDownGesture(fingerLandmarks, w, h):
    
    palmIndex = int(fingerLandmarks[5].y*h)
    palmMiddle = int(fingerLandmarks[9].y*h)
    palmRing = int(fingerLandmarks[13].y*h)
    palmPinky = int(fingerLandmarks[17].y*h)

    if palmPinky < palmRing < palmMiddle < palmIndex:
        index0 = int(fingerLandmarks[0].y * h)
        index1 = int(fingerLandmarks[1].y * h)
        index2 = int(fingerLandmarks[2].y * h)
        index3 = int(fingerLandmarks[3].y * h)
        index4 = int(fingerLandmarks[4].y * h)

        if checkNotContinousFinger(fingerLandmarks, h):
            return False

        if index0 < index1 < index2 < index3 < index4:
            return True

    return False

def checkBigFingerPosition(fingerLandmarks, w):
    big2 = int(fingerLandmarks[2].x * w)
    big3 = int(fingerLandmarks[3].x * w)
    big4 = int(fingerLandmarks[4].x * w)

    for i in range(5,21):
        checkedFinger = int(fingerLandmarks[i].x *w)
        if big2 > checkedFinger or big3 > checkedFinger or big4 > checkedFinger:
            return "right"
    return "left"            

def recogniseLeftGesture(fingerLandmarks, w, h):

    index0 = int(fingerLandmarks[0].x * w)
    index1 = int(fingerLandmarks[1].x * w)
    index2 = int(fingerLandmarks[2].x * w)
    index3 = int(fingerLandmarks[3].x * w)
    index4 = int(fingerLandmarks[4].x * w)

    if index0 > index1 > index2 > index3 > index4:
        index0 = int(fingerLandmarks[0].y * h)
        index1 = int(fingerLandmarks[1].y * h)
        index2 = int(fingerLandmarks[2].y * h)
        index3 = int(fingerLandmarks[3].y * h)
        index4 = int(fingerLandmarks[4].y * h)

        if checkNotContinousFinger(fingerLandmarks, h):
            return False

        if checkBigFingerPosition(fingerLandmarks, w) == "right":
            return False


        if index2 > index3 > index4:
          return True

    return False

def recogniseRightGesture(fingerLandmarks, w, h):

    index0 = int(fingerLandmarks[0].x * w)
    index1 = int(fingerLandmarks[1].x * w)
    index2 = int(fingerLandmarks[2].x * w)
    index3 = int(fingerLandmarks[3].x * w)
    index4 = int(fingerLandmarks[4].x * w)

    if index0 < index1 < index2 < index3 < index4:
        index0 = int(fingerLandmarks[0].y * h)
        index1 = int(fingerLandmarks[1].y * h)
        index2 = int(fingerLandmarks[2].y * h)
        index3 = int(fingerLandmarks[3].y * h)
        index4 = int(fingerLandmarks[4].y * h)

        if checkNotContinousFinger(fingerLandmarks, h):
            return False


        if checkBigFingerPosition(fingerLandmarks, w) == "left":
            return False

        if index2 > index3 > index4:
          return True


    return False

def recognisePalmGesture(fingerLandmarks, w, h):

    for val in range(6,18,4):
        if not checkContinousFingerPoints(fingerLandmarks, val, h):
            return False

    if checkContinousFingerPoints(fingerLandmarks, 2, h):
        return True

    return False

def recogniseCounterClockwiseGesture(fingerLandmarks, w, h):

    if checkBigFingerPosition(fingerLandmarks, w) == "right":
        return False

    if checkContinousFingerPoints(fingerLandmarks, 6, h) or checkContinousFingerPoints(fingerLandmarks, 10, h) or checkContinousFingerPoints(fingerLandmarks, 14, h):
        return False

    if checkContinousFingerPoints(fingerLandmarks, 2, h):
        if checkContinousFingerPoints(fingerLandmarks, 18, h):
            return True
    return False

def recogniseClockwiseGesture(fingerLandmarks, w, h):

    if checkBigFingerPosition(fingerLandmarks, w) == "left":
        return False

    if checkContinousFingerPoints(fingerLandmarks, 6, h) or checkContinousFingerPoints(fingerLandmarks, 10, h) or checkContinousFingerPoints(fingerLandmarks, 14, h):
        return False

    if checkContinousFingerPoints(fingerLandmarks, 2, h):
        if checkContinousFingerPoints(fingerLandmarks, 18, h):
            return True

    return False

def recogniseLandGesture(fingerLandmarks, w, h):

    if not (checkContinousFingerPoints(fingerLandmarks, 10, h) or checkContinousFingerPoints(fingerLandmarks, 14, h) or checkContinousFingerPoints(fingerLandmarks, 18, h)):
        return False
    if checkContinousFingerPoints(fingerLandmarks, 6, h):
        return False
    if checkContinousFingerPoints(fingerLandmarks, 2, h):
        return False

    return True



# All recognising functions in one
def getGestureName(fingerLandmarks, w, h):

# 0 - forward, 1 - backward, 2 - left, 3 - right, 4 - up, 5 - down, 6 - rotate left, 7 - rotate right, 8 - stop, 9 - land

    if checkPointsRange(fingerLandmarks, w, h):
        return "Gesture: NOT IN RANGE"

    if recognisePalmGesture(fingerLandmarks, w, h):
        return "Gesture: Stop" + appendDataToDict(fingerLandmarks, w, h, 8)
    if recogniseLandGesture(fingerLandmarks, w, h):
        return "Gesture: Land" + appendDataToDict(fingerLandmarks, w, h, 9)


    if recogniseOkGesture(fingerLandmarks, w, h):
        return "Gesture: Forward" + appendDataToDict(fingerLandmarks, w, h, 0)
    if recognisePeaceGesture(fingerLandmarks, w, h):
        return "Gesture: Backward" + appendDataToDict(fingerLandmarks, w, h, 1)
    if recogniseLeftGesture(fingerLandmarks, w, h):
        return "Gesture: Left" + appendDataToDict(fingerLandmarks, w, h, 2)
    if recogniseRightGesture(fingerLandmarks, w, h):
        return "Gesture: Right" + appendDataToDict(fingerLandmarks, w, h, 3)
    if recogniseUpGesture(fingerLandmarks, w, h):
        return "Gesture: Up" + appendDataToDict(fingerLandmarks, w, h, 4)
    if recogniseDownGesture(fingerLandmarks, w, h):
        return "Gesture: Down" + appendDataToDict(fingerLandmarks, w, h, 5)


    if recogniseCounterClockwiseGesture(fingerLandmarks, w, h):
        return "Gesture: Rotate LEFT" + appendDataToDict(fingerLandmarks, w, h, 6)
    if recogniseClockwiseGesture(fingerLandmarks, w, h):
        return "Gesture: Rotate RIGHT" + appendDataToDict(fingerLandmarks, w, h, 7)

    return "Gesture: None"
