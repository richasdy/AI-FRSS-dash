from ultralytics import YOLO
import cv2
import os

model_path = "yolo_models/People_yolov8s_trained.pt"
image_path = "debug_frame.jpg"

if not os.path.exists(image_path):
    print("Debug frame not found")
    exit(1)

print(f"Loading model: {model_path}")
model = YOLO(model_path)

print(f"Running detection on {image_path}")
# Run with low confidence and no class filter first to see what it detects
results = model(image_path, conf=0.1)

for result in results:
    print(f"Detected {len(result.boxes)} objects")
    for box in result.boxes:
        cls = int(box.cls[0].item())
        conf = box.conf[0].item()
        print(f"Class: {cls} ({model.names[cls]}), Conf: {conf:.4f}")

# Check image stats
img = cv2.imread(image_path)
print(f"Image shape: {img.shape}, Mean: {img.mean()}")
