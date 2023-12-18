from ultralytics import YOLO


if __name__ == "__main__":
    model = YOLO("yolov8n.pt")
    model.train(data="DataSet/SplitData/data.yaml", epochs=50, batch=-1)
