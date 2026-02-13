import asyncio
import logging
import time
import json
import sys
import cv2
import os
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse

from app.core.config import settings
from app.services.detector import PeopleDetector
from app.services.stream_capture import StreamCapture
from app.services.image_processor import ImageProcessor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="People Detection Service")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/crops", StaticFiles(directory=settings.CROP_DIR), name="crops")

@app.get("/crops-list")
async def get_crops_list():
    try:
        # List all jpg files in crop dir, sorted by modification time (newest first)
        files = [f for f in os.listdir(settings.CROP_DIR) if f.endswith('.jpg')]
        files.sort(key=lambda x: os.path.getmtime(os.path.join(settings.CROP_DIR, x)), reverse=True)
        return {"crops": files}
    except Exception as e:
        logger.error(f"Error listing crops: {e}")
        return {"crops": []}

# Global services
detector = None
stream_capture = None
image_processor = None
latest_annotated_frame = None

@app.get("/")
async def get_dashboard():
    return FileResponse("index.html")

async def generate_frames():
    global latest_annotated_frame
    while True:
        if latest_annotated_frame is not None:
            ret, buffer = cv2.imencode('.jpg', latest_annotated_frame)
            if ret:
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        else:
            # If no frame yet, yield empty or wait
            pass
        await asyncio.sleep(0.05) # ~20 FPS stream

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.on_event("startup")
async def startup_event():
    global detector, stream_capture, image_processor
    logger.info("Initializing services...")
    
    # Initialize services
    try:
        detector = PeopleDetector()
        image_processor = ImageProcessor()
        stream_capture = StreamCapture()
        # Start capture immediately for the video feed to work even without websocket clients
        stream_capture.start()
    except Exception as e:
        logger.error(f"Startup failed: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down services...")
    if stream_capture:
        stream_capture.stop()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        async with self.lock:
            self.active_connections.append(websocket)
            # Stream capture is already started globally

    async def disconnect(self, websocket: WebSocket):
        async with self.lock:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        to_remove = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                to_remove.append(connection)
        
        if to_remove:
            async with self.lock:
                for conn in to_remove:
                    if conn in self.active_connections:
                        self.active_connections.remove(conn)

manager = ConnectionManager()

@app.websocket("/ws/people-detection")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text() 
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await manager.disconnect(websocket)

# Background detection task
async def detection_loop():
    global latest_annotated_frame
    logger.info("Starting detection loop")
    frame_interval = 1.0 / settings.MAX_FPS
    
    while True:
        start_time = time.time()
        
        if not stream_capture:
             await asyncio.sleep(1)
             continue

        # Get frame
        frame = stream_capture.get_frame()
        if frame is None:
            await asyncio.sleep(0.1)
            continue
            
        # Detect with drawing
        try:
            detections, annotated = detector.detect(frame, draw=True)
            
            # Update global frame for video feed
            latest_annotated_frame = annotated
            
            people_count = 0
            
            # Filter for person class
            person_detections = [d for d in detections if d['class'] == settings.TARGET_CLASS_ID]
            people_count = len(person_detections)
            
            # Process each detection
            for det in person_detections:
                bbox = det['bbox']
                is_unique, crop_path = image_processor.crop_and_save(frame, bbox) # Use original frame for crop
                
                payload = {
                    "id": int(time.time() * 1000),
                    "title": "Person Detected",
                    "createdAt": datetime.utcnow().isoformat() + "Z",
                    "location": "CCTV - Main Gate",
                    "type": "intrusion",
                    "isResolved": False,
                    "timeFormatted": datetime.now().strftime("%H:%M:%S"),
                    "icon": "person",
                    
                    "people_count": people_count,
                    "new_detection": is_unique,
                    "crop_path": crop_path if is_unique else "", 
                    "bbox": bbox
                }
                
                if is_unique:
                    await manager.broadcast(payload)
            
        except Exception as e:
            logger.error(f"Error in detection loop: {e}")
        
        # Maintain FPS
        elapsed = time.time() - start_time
        sleep_time = max(0, frame_interval - elapsed)
        await asyncio.sleep(sleep_time)

@app.on_event("startup")
async def start_background_task():
    asyncio.create_task(detection_loop())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
