import random
import websocket
import stomper

client_id = str(random.randint(0, 1000))


def parse_last_line(data):
    # Tách chuỗi thành danh sách các dòng và lấy dòng cuối cùng
    lines = data.splitlines()
    last_line = lines[-1] if lines else None
    if "True" in last_line:
        return True
    return False


def on_message(ws, message):
    parse_last_line(message)


def on_error(ws, error):
    print(f"Error: {error}")


def on_close(ws, close_status_code, close_msg):
    print("Connection closed")


def on_open(ws):
    def run():
        # Đăng ký để nhận thông điệp khi kết nối thành công
        print("Connected to WebSocket")

    # Gửi yêu cầu mở kết nối
    ws.send("CONNECT\naccept-version:1.0,1.1,2.0\n\n\x00\n")
    sub = stomper.subscribe("/topic/true", client_id, ack="auto")
    ws.send(sub)


if __name__ == "__main__":
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "ws://192.168.5.116:8080/ws",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open

    # Bắt đầu kết nối tới máy chủ WebSocket
    ws.run_forever()
