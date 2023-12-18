import serial
import cv2
import time
from main2 import check_real_video

port = serial.Serial("COM4", 115200, timeout=1)

delay_seconds = 2
count = 0


def open_writer(count):
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    size = (640, 480)
    path = "Video/video_" + str(count) + ".avi"
    out = cv2.VideoWriter(path, fourcc, 20.0, size)
    return out, path


def read_ser(num_char=1):
    return port.read(num_char).decode()


def write_ser(data):
    port.write(data.encode())

try:  
    while True:
        ESP32_Data = read_ser(255)
        if len(ESP32_Data):
            if ESP32_Data == "1":
                ###############Video config
                cap = cv2.VideoCapture(0)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)
                size = (width, height)
                fourcc = cv2.VideoWriter_fourcc(*"XVID")
                ##############
                print("Mo camera")
                out, path = open_writer(count)
                start_time = time.time()  # Thời gian bắt đầu lưu video
                while int(time.time() - start_time) < 2:
                    ret, frame = cap.read()
                    out.write(frame)
                cap.release()
                out.release()
                print("Luu video thanh cong")
                video_path = path
                if check_real_video(video_path):
                    print("Nhan dien  khuon mat thanh cong")
                    write_ser("1")
                else:
                    print("Nhan dien khuon mat that bai")
                count += 1
                time.sleep(delay_seconds)
            # else:
            #     write_ser("0")
            else:
                print(ESP32_Data)
except : print("Dung chuong trinh")

