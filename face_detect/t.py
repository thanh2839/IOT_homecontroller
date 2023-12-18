import sys
from ultralytics import YOLO
import cv2
import math
import os
import face_recognition


def check_face_recognition(image_path, faces_folder):
    check_image = face_recognition.load_image_file(image_path)
    check_face_encoding = face_recognition.face_encodings(check_image)[0]

    face_images = [f for f in os.listdir(faces_folder) if f.endswith(".jpg")]

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


def check_real_image(image_path):
    confidence = 0.8
    model = YOLO("models/best.pt")
    classNames = ["fake", "real"]

    img = cv2.imread(image_path)
    img = cv2.flip(img, 1)
    results = model(img, stream=True, verbose=False)

    for r in results.xyxy[0]:
        x1, y1, x2, y2, conf, cls = r
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        w, h = x2 - x1, y2 - y1
        conf = math.ceil((conf * 100)) / 100
        if conf > confidence:
            if classNames[int(cls)] == "real":
                return 1
            else:
                return -1
    return 0


imagePath = sys.argv[1]
listPath = sys.argv[2]


def check(model, face_detect):
    if model == 1:
        return "quoc"
    elif model == -1:
        return "False"
    elif model == 0:
        if face_detect == "False":
            return "False"
        else:
            return face_detect


check_model = check_real_image(imagePath)
check_face = check_face_recognition(imagePath, listPath)
print(check(check_model, check_face))
