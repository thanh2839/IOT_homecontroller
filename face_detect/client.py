import math
import socket
import threading
import cv2
import time
import random
import serial
from ultralytics import YOLO
import websocket
import stomper
import requests
import face_recognition


##################         HTTP          ######################
def callOpenDoor():
    url = "http://192.168.86.11:8080/api/open-door"
    try:
        response = session.get(url)
        if response.status_code == 200:
            print("Open_Door_Response:", response.text)
            return response.text
        else:
            print("Failed to fetch data. Status code:", response.status_code)
            return response.status_code
    except requests.RequestException as e:
        print("Error:", e)


def callCloseDoor():
    url = "http://192.168.86.11:8080/api/close-door"
    try:
        response = session.get(url)
        if response.status_code == 200:
            print("Close_Door_Response:", response.text)
            return response.text
        else:
            print("Failed to fetch data. Status code:", response.status_code)
            return response.status_code
    except requests.RequestException as e:
        print("Error:", e)


def log_face(path, status):
    url = "http://192.168.86.11:8080/api/logFace"
    try:
        with open(path, "rb") as file:
            files = {"file": file}
            data = {"status": status}
            response = session.post(url, files=files, data=data)
            print("Check_Face_Response:", response.text)
            return response.text
    except requests.RequestException as e:
        print("Error:", e)


def sendStatus(status):
    try:
        url = "http://192.168.86.11:8080/api/status"
        data = {"status": status}
        response = session.post(url, data=data)
        print("Update_Status_Response:", response.text)
        return response.text
    except requests.RequestException as e:
        print("Error:", e)


#####################################################################
###########            SOCKET          #######################
client_id = str(random.randint(0, 1000))


def parse_last_line(data):
    lines = data.splitlines()
    last_line = lines[-1] if lines else None
    if "True" in last_line:
        return True
    if "False" in last_line:
        return False
    return None


def on_message(ws, message):
    if parse_last_line(message) == True:
        send_command("OPEN\n")
    if parse_last_line(message) == False:
        send_command("CLOSE\n")


def on_error(ws, error):
    print(f"Error: {error}")


def on_close(ws, close_status_code, close_msg):
    print("Connection closed")


def on_open(ws):
    def run():
        print("Connected to WebSocket")

    # Gửi yêu cầu mở kết nối
    ws.send("CONNECT\naccept-version:1.0,1.1,2.0\n\n\x00\n")
    sub = stomper.subscribe("/topic/true", client_id, ack="auto")
    ws.send(sub)


def handle_websocket():
    ws = websocket.WebSocketApp(
        "ws://192.168.86.11:8080/ws",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    ws.run_forever()


def login(username, password):
    url = "http://192.168.86.11:8080/login"  # Thay đổi URL login của ứng dụng của bạn

    # Dữ liệu gửi trong body của request
    data = {"username": username, "password": password}
    session = requests.Session()
    response = session.post(url, data=data)

    if response.status_code == 200:
        return session.cookies.get_dict()["JSESSIONID"]
    else:
        print("Yêu cầu thất bại! Mã lỗi:", response.status_code)


#######################################################
###################   SENSOR        #####################

ESP32_IP = "192.168.137.35"
ESP32_SERVER_PORT = 80


def send_command(command):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ESP32_IP, ESP32_SERVER_PORT))
        s.sendall(command.encode())


def check_face():
    try:
        start_time = time.time()
        print(start_time)
        detect = False
        img = None
        while (time.time() - start_time) < 5:
            ret, img = cap.read()
            faces = face_recognition.face_locations(img)
            if faces:
                detect = True
            print(f"faces {len(faces)}") 

            results = model(img, stream=True, verbose=False)
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    conf = math.ceil((box.conf[0] * 100)) / 100
                    cls = int(box.cls[0])
                    if conf > confidence:
                        if classNames[cls] == "real":
                            return True, True, img
                        elif classNames[cls] == "fake":
                            return True, False, img
        if detect == True:
            return True, None, img
        return False, None, None
    except Exception as e:
        print(e)
    return False, None, None


def handle_sensor():
    sleep_time = 0
    while True:
        try:
            ser = serial.Serial("COM4", 115200, timeout=1)
            if ser and ser.is_open:
                while True:
                    ESP32_Data = ser.readline().decode().strip()
                    if len(ESP32_Data):
                        print("ESP:" + ESP32_Data)
                        if "MOTION" in ESP32_Data:
                            try:
                                result = check_face()
                                detect, model, img = result
                                if detect == True:
                                    print("Detected!!!")
                                    path = f"Log/{time.time()}.jpg"
                                    cv2.imwrite(path, img)
                                    if model == None:
                                        send_command("CLOSE\n")
                                        log_face(path, "None")
                                        sleep_time = 2
                                    elif model == True:
                                        send_command("OPEN\n")
                                        log_face(path, "Real")
                                        sleep_time = 2
                                    elif model == False:
                                        send_command("CLOSE\n")
                                        log_face(path, "Fake")                          
                                        sleep_time = 2
                                else:
                                    print("No detect!!!")
                                    send_command("CLOSE\n")
                            except Exception as e:
                                print(e)
                                continue

                        if "CLOSE_DOOR" in ESP32_Data:
                            sendStatus(False)
                        if "OPEN_DOOR" in ESP32_Data:
                            sendStatus(True)
                    # time.sleep(sleep_time)
        except Exception as e:
            continue


####################################################

###############TACHLUONG###############

if __name__ == "__main__":
    # email = str(input("Nhập email: "))
    # password = str(input("Nhập password: "))
    confidence = 0.8
    cap = cv2.VideoCapture(1)
    cap.set(3, 640)
    cap.set(4, 480)
    model = YOLO("models/best2.pt")
    classNames = ["fake", "real"]
    print("Camera ready!!!")
    # jsession_id = login(email, password)
    jsession_id = login("giang41245@gmail.com", "123")
    global session
    session = requests.Session()
    session.cookies.set("JSESSIONID", jsession_id)
    websocket_thread = threading.Thread(target=handle_websocket)
    sensor_thread = threading.Thread(target=handle_sensor)
    websocket_thread.start()
    sensor_thread.start()
