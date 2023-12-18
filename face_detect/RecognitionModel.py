import time
from ultralytics import YOLO
import cv2
import math
import os
import face_recognition
import cvzone

def check_face_recognition(image_path, faces_folder):
    check_image = face_recognition.load_image_file(image_path)
    check_face_encoding = face_recognition.face_encodings(check_image)[0]

    face_images = [f for f in os.listdir(faces_folder) if f.endswith(".jpg")]

    if len(face_images) == 0:
        return "False"
    for face_image in face_images:
        face_path = os.path.join(faces_folder, face_image)
        face_to_compare = face_recognition.load_image_file(face_path)
        face_to_compare_encoding = face_recognition.face_encodings(face_to_compare)[0]

        matches = face_recognition.compare_faces(
            [check_face_encoding], face_to_compare_encoding
        )

        if matches[0]:
            return os.path.splitext(face_image)[0]
    return "False"


def detect_objects_with_confidence():
    cap = cv2.VideoCapture(0)
    confidence=0.8
    cap.set(3, 640)
    cap.set(4, 480)

    model = YOLO("models/best.pt")
    classNames = ["fake", "real"]
    prev_frame_rate = 0
    new_frame_rate = 0
    
    while True:
        new_frame_rate = time.time()
        success, img = cap.read()
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
                        # color = (0, 255, 0)
                        return "Real"
                    else:
                        return "Fake"
                        # color = (0, 0, 255)
                    # cvzone.cornerRect(img, (x1, y1, w, h), colorC=color, colorR=color)
                    # cvzone.putTextRect(
                    #     img,
                    #     f"{classNames[cls]} {conf}",
                    #     (max(0, x1), max(35, y1)),
                    #     scale=1,
                    #     thickness=1,
                    #     colorR=color,
                    #     colorB=color,
                    # )
        
        
        # if cv2.waitKey(1) & 0xFF == ord("q"):
        #     break
       
        # cv2.imshow("Image", img)
        # cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()


# check_model = check_real_image(imagePath)

# def check():
#     check_model = check_real_image(imagePath)
#     if check_model == 1:
#         return "quoc"
#     elif check_model == -1:
#         return "Fake"
#     elif check_model == 0:
#         return check_face_recognition(imagePath, listPath)
# print(check())
