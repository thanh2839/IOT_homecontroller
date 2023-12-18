import requests


def callDoor():
    url = "http://192.168.5.116:8080/api/door"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Response:", response.text)
            return response.text
        else:
            print("Failed to fetch data. Status code:", response.status_code)
            return response.status_code
    except requests.RequestException as e:
        print("Error:", e)


def uploadVid(path):
    url = "http://192.168.5.116:8080/api/uploadVid"
    # file_path = "Video/test.avi"  # Đường dẫn đến file video .avi
    with open(path, "rb") as file:
        files = {"file": file}
        response = requests.post(url, files=files)
        print("Response:", response.text)
        return response.text
