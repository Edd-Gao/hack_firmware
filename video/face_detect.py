import numpy as np
import cv2
import time
import requests
import json
import threading
import time


#IP = "127.0.0.1"
IP = "121.201.24.49"

cap = cv2.VideoCapture(1)
classfier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
color = (0, 0, 0)


def main():
    i = 0
    success, frame = cap.read()
    size=frame.shape[:2]
    divisor=16
    h, w = size
    minSize=(w/divisor, h/divisor)
    while True:
        success, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.equalizeHist(gray, gray)
        faceRects = classfier.detectMultiScale(gray, 1.3, 5,cv2.CASCADE_SCALE_IMAGE, minSize)
        if len(faceRects) > 0 & i == 0:
            cv2.imwrite("face.jpg", frame)
            file = {'image': open("face.jpg", "rb")}
            threading.Thread(target=check_image, args=(file,)).start()

            for faceRect in faceRects:
                x, y, w, h = faceRect
                #cv2.rectangle(frame, (x, y), (x+w, y+h), color)
                cv2.circle(frame, (x+w/2, y+h/2), w/2, color, 2, 8, 0)

        cv2.imshow("face", frame)
        key = cv2.waitKey(10)
        c = chr(key & 255)
        if c in ['q', 'Q', chr(27)]:
            break
        i = (i + 1) % 80
    cv2.destroyAllWindows()


def check_image(file):
    resp = requests.post(
        "http://" + IP + ":5000/upload_image",
        files=file
    )
    json_resp = json.loads(resp.content)
    emotion = json_resp['emotion']
    handler_emotion(emotion)


def handler_emotion(emotion):
    pass


if __name__ == '__main__':
    main()

