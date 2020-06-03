# raspberrypifacerecognition

My code is based on https://www.pyimagesearch.com/2018/06/25/raspberry-pi-face-recognition/ where i learned the face_recognition and understood the code architecture</br>


 Requirement :-</br>
                 pip install dlib</br>
                pip install face_detection</br>
                pip install imutils</br>
                pip install opencv-python</br>
               
               
               
Architecture :- </br>
picamera ------> frame/image -------->Detect face --------> compute 128-d face embedded---------> compare 128-d vector to known database ------> Recognize face
