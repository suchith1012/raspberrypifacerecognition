# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 20:22:48 2020

@author: suchith
"""
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import yagmail
import os 
import requests
import datetime

def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False
    
listintruder=[]
receiver = "suchith.ponnuru@gmail.com"
body = "Hello there is a intruder please check the attachment and call 100"

yag = yagmail.SMTP('hia87599@gmail.com', 'suchithpnvs')

print("[INFO] loading encodings + face detector...")
data = pickle.loads(open("/home/pi/Documents/sfr/encodings.pickle", "rb").read())
detector = cv2.CascadeClassifier("/home/pi/Documents/sfr/haarcascade_frontalface_default.xml")
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()
#intrudercount=0
while True:
    frame=vs.read()
    frame=imutils.resize(frame,width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rects = detector.detectMultiScale(gray, scaleFactor=1.1,minNeighbors=5, minSize=(30, 30),
    flags=cv2.CASCADE_SCALE_IMAGE)
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
    encodings = face_recognition.face_encodings(rgb, boxes)
    #names = []
    for encode in encodings:
        matches=face_recognition.compare_faces(data["encodings"],encode)
        #name="unknown"
        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)
            #names.append(name)
            date = datetime.datetime.now()
            f=open("/home/pi/Documents/sfr/knownlogs", "a+")
            f.write(name+"----"+"Entered"+"----"+str(date))
            f.close()

            #print("known face"+name)
        else:
            #intrudercount=intrudercount+1
            intrudate = datetime.datetime.now()
            path='/home/pi/Documents/sfr/interuderphoto'
            #cv2.imwrite('intruder'+str(intrudercount)+'.jpg',frame)
            cv2.imwrite(os.path.join(path , 'intruder'+str(intrudate)+'.jpg'), frame)
            filename='/home/pi/Documents/sfr/interuderphoto/'+'intruder'+str(intrudate)+'.jpg'
            f=open("/home/pi/Documents/sfr/intruderlog", "a+")
            f.write("Intruder Entered"+"----"+str(date)+"----"+filename)
            f.close()
            netcheck=check_internet()
            if(netcheck==True):
                if(listintruder==[]):
                    yag.send(
                        to=receiver,
                        subject="Intruder alert",
                        contents=body,
                        attachments=filename,
                        )
                else:
                    for list in listintruder:
                        yag.send(
                        to=receiver,
                        subject="Intruder alert",
                        contents=body,
                        attachments=list,
                        )
                        
            else:
                listintruder.append(filename)
            
            #print("intruder")

    cv2.imshow("Frame",frame)
    key=cv2.waitKey(1)&0xFF
    if key == ord("q"):
        break
    fps.update()
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

cv2.destroyAllWindows()
vs.stop()

