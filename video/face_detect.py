import numpy as np
import cv2

cap = cv2.VideoCapture(0)
classfier=cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
color = (0,0,0)

while(True):
    success, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.equalizeHist(frame, frame)
    faceRects = classfier.detectMultiScale(frame, 1.3, 5)
    if len(faceRects)>0:#如果检测到人脸，则将人脸进行标记
        for faceRect in faceRects: #对每一个人脸画圆形标记
                x, y, w, h = faceRect
                #cv2.rectangle(frame, (x, y), (x+w, y+h), color)
                cv2.circle(frame,(x+w/2,y+h/2),w/2,color,2,8,0)
    cv2.imshow("face", frame)
    key=cv2.waitKey(10)
    c = chr(key & 255)
    if c in ['q', 'Q', chr(27)]:
        break
cv2.destroyAllWindows