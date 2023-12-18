import time
import requests


def login(username, password):
    url = "http://192.168.5.116:8080/login"  # Thay đổi URL login của ứng dụng của bạn

    # Dữ liệu gửi trong body của request
    data = {"username": username, "password": password}
    session = requests.Session() 
    response = session.post(url, data=data)

    if response.status_code == 200:
        print(session.cookies.get_dict()['JSESSIONID'])
    else:
        print("Yêu cầu thất bại! Mã lỗi:", response.status_code)


# Sử dụng hàm login để gửi request đăng nhập
username_input = "tencanh777@gmail.com"  # Thay đổi thành username của bạn
password_input = "123456"  # Thay đổi thành password của bạn


def log():
    url = "http://192.168.5.116:8080/user/1"  # Thay đổi URL login của ứng dụng của bạn

    response = requests.get(
        url,
    )

    if response.status_code == 200:
        print("Đăng nhập thành công!")
        # Xử lý response ở đây nếu cần thiết
        print("Response từ server:", response.text)
    else:
        print("Đăng nhập thất bại! Mã lỗi:", response.status_code)
        print("Lỗi chi tiết:", response.text)


login(username_input, password_input)
# log()
