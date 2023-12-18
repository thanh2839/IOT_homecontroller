from ultralytics import YOLO
import cv2
import cvzone
import math
import time

confidence = 0.8

cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)
model = YOLO("models/best2.pt")
classNames = ["fake", "real"]
while True:
    new_frame_rate = time.time()
    success, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.flip(img, 1)
    results = model(img, stream=True, verbose=False)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            color = (0, 255, 0)
            if conf > confidence:
                if classNames[cls] == "real":
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)
                cvzone.cornerRect(img, (x1, y1, w, h), colorC=color, colorR=color)
                cvzone.putTextRect(
                    img,
                    f"{classNames[cls]} {conf}",
                    (max(0, x1), max(35, y1)),
                    scale=1,
                    thickness=1,
                    colorR=color,
                    colorB=color,
                )
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    cv2.imshow("Image", img)
    cv2.waitKey(1)
