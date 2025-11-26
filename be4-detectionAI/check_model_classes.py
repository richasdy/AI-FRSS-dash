from ultralytics import YOLO
import sys
import os

# Adjust path if needed
model_path = "yolo_models/People_yolov8s_trained.pt"

if not os.path.exists(model_path):
    print(f"Error: Model not found at {model_path}")
    sys.exit(1)

try:
    print(f"Loading model: {model_path}")
    model = YOLO(model_path)
    print("Model loaded successfully.")
    print("Class names mapping:")
    print(model.names)
except Exception as e:
    print(f"Failed to load model: {e}")
