import serial

# Mở cổng COM4 với baudrate 115200
ser = serial.Serial('COM4', 115200)

while True:
    # Đọc dữ liệu từ cổng serial
    data = ser.readline().decode('utf-8').strip()
    if data:
        print(data)
