import cvzone
import cv2
from cvzone.FaceDetectionModule import FaceDetector
from time import time

offsetPercentageW = 10
offsetPercentageH = 20
confidence = 80
camWidth, camHeight = 640, 480
floatingPoint = 6
save = True
blurThreshold = 35
outputFolderPath = "DataSet/DataCollect"
classID = 0

videopath = 'fake2.mp4'
cap = cv2.VideoCapture(1)
cap.set(3, camWidth)
cap.set(4, camHeight)
# Initialize the FaceDetector object
# minDetectionCon: Minimum detection confidence threshold
# modelSelection: 0 for short-range detection (2 meters), 1 for long-range detection (5 meters)
detector = FaceDetector(minDetectionCon=0.5, modelSelection=0)

# Run the loop to continually get frames from the webcam
while True:
    # Read the current frame from the webcam
    # success: Boolean, whether the frame was successfully grabbed
    # img: the captured frame
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgOut = img.copy()
    # Detect faces in the image
    # img: Updated image
    # bboxs: List of bounding boxes around detected faces
    img, bboxs = detector.findFaces(img, draw=False)

    listBlur = []
    listInfo = []
    # Check if any face is detected
    if bboxs:
        # Loop through each bounding box
        for bbox in bboxs:
            # bbox contains 'id', 'bbox', 'score', 'center'

            # ---- Get Data  ---- #
            center = bbox["center"]
            x, y, w, h = bbox["bbox"]
            score = int(bbox["score"][0] * 100)

            # ---- Draw Data  ---- #
            cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)
            cvzone.putTextRect(img, f"{score}%", (x, y - 10))
            cvzone.cornerRect(img, (x, y, w, h))

            # Check the score
            if score > confidence:
                # Add offset of the face detected
                offsetW = (offsetPercentageW / 100) * w
                x = int(x - offsetW)
                w = int(w + offsetW * 2)

                offsetH = (offsetPercentageH / 100) * h
                y = int(y - offsetH * 3)
                h = int(h + offsetH * 3.5)

                # Avoid values below 0
                if x < 0: x = 0
                if y < 0: y = 0
                if w < 0:w = 0
                if h < 0: h = 0

                # Add blurriness
                imgFace = img[y : y + h, x : x + w]
                # cv2.imshow("face", imgFace)
                blurValue = int(cv2.Laplacian(imgFace, cv2.CV_64F).var())
                if blurValue>blurThreshold:listBlur.append(True)
                else : listBlur.append(False)

                # Normalize Values
                ih, iw, _ = img.shape
                xc, yc = x + w / 2, y + h / 2
                xcn, ycn = round(xc / iw, floatingPoint), round(yc / ih, floatingPoint)
                wn, hn = round(w / iw, floatingPoint), round(h / ih, floatingPoint)
                print(xcn, ycn, wn, hn)
                # Avoid values above 1
                if xcn > 1: xcn = 1
                if ycn > 1: ycn = 1
                if wn > 1: wn = 1
                if hn > 1:  hn = 1

                listInfo.append(f"{classID} {xcn} {ycn} {wn} {hn}\n ")
                
                # Draw
                cv2.rectangle(img, (x, y, w, h), (255, 0, 0), 3)
                cvzone.putTextRect(img, f"Score: {score}% Blur: {blurValue}", (x, y - 20), scale=1, thickness=2)
        
        # Save 
        if save:
            if all(listBlur) and listBlur!=[]:
                # Image 
                timeNow = str(time()).replace(".","")
                print(timeNow)
                cv2.imwrite(f"{outputFolderPath}/{timeNow}.jpg",imgOut)
                
                # Label text file
                for info in listInfo:
                    f = open(f"{outputFolderPath}/{timeNow}.txt", "a")
                    f.write(info)
                    f.close()

                
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    # Display the image in a window named 'Image'
    cv2.imshow("Image", img)
    # Wait for 1 millisecond, and keep the window open
    cv2.waitKey(1)
