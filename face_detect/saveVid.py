import cv2
import time

count = 0
# Khởi tạo camera



def record_video(cap, output_filename, fourcc, size):
    out = cv2.VideoWriter(output_filename, fourcc, 20.0, size)
    start_time = time.time()  # Thời gian bắt đầu lưu video
    while int(time.time() - start_time) < 5:
        ret, frame = cap.read()
        out.write(frame)
    cap.release()
    out.release()


# while True:
#     ret, frame = cap.read()

#     cv2.imshow("Camera", frame)
#     out.write(frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Giải phóng tài nguyên
# cap.release()
# out.release()
cv2.destroyAllWindows()
