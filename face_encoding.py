# -*- coding: utf-8 -*-
"""
Created on Sun May 31 18:40:42 2020

@author: suchith
"""

from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

knownEncodings = []
knownNames = []

imgfolder=os.listdir('D:/facerecognition/sfr/dataset')
if(imgfolder==[]):
    print("error")
else:
    for i in imgfolder:
        path="D:/facerecognition/sfr/dataset/"+i
        print(i)
        images=os.listdir(path)
        for j in images:
            aaa="D:/facerecognition/sfr/dataset/"+i+'/'+j
            image = face_recognition.load_image_file(aaa)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(image)
            encodings = face_recognition.face_encodings(rgb, boxes)
            for encoding in encodings:
                print(encoding)
                knownEncodings.append(encoding)
                knownNames.append(i)
data = {"encodings": knownEncodings, "names": knownNames}
f = open("D:/facerecognition/sfr/encodings.pickle", "wb")
f.write(pickle.dumps(data))
f.close()