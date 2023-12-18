import socket
import requests
import asyncio
import websockets

hostname=socket.gethostname()
SERVER_IP = socket.gethostbyname(hostname) 

async def handle_connection(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        if message == "{'sensor': true}":
            url = "http://192.168.5.11696/led"
            data = {"plain": "led:on"}  
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print("LED đã được bật thành công.")
            else:
                print("Không thể kết nối tới ESP32.")

start_server = websockets.serve(handle_connection, "192.168.5.11696", "80")

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

