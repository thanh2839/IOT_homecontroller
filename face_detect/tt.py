import cv2
import face_recognition

def find_best_quality_face(video_path, output_filename="best_quality_face.jpg"):
    video_capture = cv2.VideoCapture(video_path)
    best_face = None
    best_face_quality = 0
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        face_locations = face_recognition.face_locations(frame)
        
        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_image = frame[top:bottom, left:right]
            quality = (bottom - top) * (right - left)
            
            if quality > best_face_quality:
                best_face_quality = quality
                best_face = face_image
    
    video_capture.release()
    
    if best_face is not None:
        cv2.imwrite(output_filename, best_face)
        print(f"Frame chứa khuôn mặt có chất lượng tốt nhất đã được lưu thành '{output_filename}'")
    else:
        print("Không tìm thấy khuôn mặt trong video.")

# Sử dụng hàm để tìm và lưu frame có khuôn mặt chất lượng tốt nhất từ video
video_path = "test.mp4"
find_best_quality_face(video_path)
