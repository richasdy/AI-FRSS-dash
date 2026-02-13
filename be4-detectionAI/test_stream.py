import cv2
import time

url = "http://200.46.196.243/mjpg/video.mjpg"

print(f"Connecting to {url}...")
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Failed to open stream")
    exit(1)

print("Stream opened. Reading frames...")
for i in range(10):
    start = time.time()
    ret, frame = cap.read()
    if ret:
        print(f"Frame {i} read successfully in {time.time()-start:.4f}s")
    else:
        print(f"Failed to read frame {i}")
        break

cap.release()
