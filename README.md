# DJI Tello Hand Gesture Recognition and Control
## This is a work in progress!!

/

Main purpose of this project is to remote control the DJI Tello drone just with hand gestures.

## Content Table
1. [Introduction](#Introduction)
2. [Packages needed](#Packages)
3. [Making your own Dataset](#Custom_Dataset)


## Introduction

This project needs 3 main components:
1. A Laptop
2. Web camera
3. A DJI Tello drone

Using a Machine Learning module named MediaPipe we can keep track of all finger joints and get their (x,y) coordinates.

After creating a simple neural network based on some gesture's joints coordinates, we can recognise them as a labeled gest.

This application will recognise the following gestures:


This will send specific instructions for the drone to perform.

## Packages
!! NOTE: This project was realised with the python 3.8.8 kernel

```sh
djitellopy
numpy
pandas
opencv2
tensorflow
mediapipe
```



## Custom_Dataset

`hardCodedRecognition.py` is a custom module made with the purpose of creating and saving our custom Dataset for the neural network.

The dataset is saved in the _handsDataset_ directory