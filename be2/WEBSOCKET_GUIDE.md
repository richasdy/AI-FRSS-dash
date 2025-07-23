# 🚀 AI-FRSS WebSocket API Guide

## 📋 Overview

WebSocket API untuk real-time object detection menggunakan YOLO models. Mendukung 4 model detection: intrusion, people, security_threats, dan vehicle.

## 🔗 WebSocket Endpoints

### 1. Single Model Detection

```
ws://localhost:8000/ws/detection/{model_name}
```

**Available Models:**

- `intrusion` - Deteksi intrusi/penyusupan
- `people` - Deteksi orang
- `security_threats` - Deteksi ancaman keamanan (senjata, dll)
- `vehicle` - Deteksi kendaraan

### 2. Multi-Model Detection

```
ws://localhost:8000/ws/detection-all
```

## 📡 Message Format

### Request Messages

#### 1. Image Detection

```json
{
  "type": "image",
  "data": "base64_encoded_image_string",
  "confidence": 0.5,
  "draw_boxes": true,
  "timestamp": "2025-07-21T10:30:00Z"
}
```

#### 2. Change Model (Single Model Endpoint Only)

```json
{
  "type": "change_model",
  "model": "people"
}
```

#### 3. Health Check

```json
{
  "type": "ping",
  "timestamp": "2025-07-21T10:30:00Z"
}
```

### Response Messages

#### 1. Connection Established

```json
{
  "type": "connection_established",
  "model": "intrusion",
  "message": "Connected to intrusion detection service"
}
```

#### 2. Detection Result (Single Model)

```json
{
  "type": "detection_result",
  "model_used": "intrusion",
  "image_size": {
    "width": 640,
    "height": 480
  },
  "detections_count": 2,
  "detections": [
    {
      "class": "person",
      "confidence": 0.87,
      "bbox": [100, 150, 200, 300],
      "center": [150, 225]
    }
  ],
  "image_with_boxes": "base64_image_with_bounding_boxes",
  "timestamp": "2025-07-21T10:30:00Z"
}
```

#### 3. Multi-Model Detection Result

```json
{
  "type": "multi_detection_result",
  "models_used": ["intrusion", "people", "security_threats", "vehicle"],
  "combined_results": {
    "intrusion": [
      {
        "class": "person",
        "confidence": 0.87,
        "bbox": [100, 150, 200, 300]
      }
    ],
    "people": [
      {
        "class": "person",
        "confidence": 0.92,
        "bbox": [105, 148, 198, 305]
      }
    ],
    "security_threats": [],
    "vehicle": []
  },
  "total_detections": 2,
  "image_with_boxes": "base64_image_with_all_detections"
}
```

#### 4. Error Response

```json
{
  "type": "error",
  "message": "No image data provided"
}
```

#### 5. Pong Response

```json
{
  "type": "pong",
  "timestamp": "2025-07-21T10:30:00Z",
  "loaded_models": ["intrusion", "people", "security_threats", "vehicle"]
}
```

## 💻 Client Examples

### JavaScript/Browser Example

```javascript
// Connect to single model detection
const ws = new WebSocket("ws://localhost:8000/ws/detection/intrusion");

ws.onopen = function (event) {
  console.log("Connected to WebSocket");
};

ws.onmessage = function (event) {
  const response = JSON.parse(event.data);
  console.log("Received:", response);

  if (response.type === "detection_result") {
    // Handle detection results
    console.log(`Found ${response.detections_count} objects`);

    // Display image with bounding boxes if available
    if (response.image_with_boxes) {
      const img = document.getElementById("result-image");
      img.src = "data:image/jpeg;base64," + response.image_with_boxes;
    }
  }
};

// Send image for detection
function sendImage(base64Image) {
  const message = {
    type: "image",
    data: base64Image,
    confidence: 0.5,
    draw_boxes: true,
    timestamp: new Date().toISOString(),
  };

  ws.send(JSON.stringify(message));
}

// Convert file input to base64
function handleFileSelect(event) {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      const base64 = e.target.result.split(",")[1]; // Remove data:image/...;base64,
      sendImage(base64);
    };
    reader.readAsDataURL(file);
  }
}
```

### Python Client Example

```python
import asyncio
import websockets
import json
import base64
from PIL import Image
import io

async def detection_client():
    uri = "ws://localhost:8000/ws/detection/people"

    async with websockets.connect(uri) as websocket:
        # Wait for connection message
        response = await websocket.recv()
        print("Connected:", json.loads(response))

        # Send image for detection
        with open("test_image.jpg", "rb") as f:
            image_data = base64.b64encode(f.read()).decode()

        message = {
            "type": "image",
            "data": image_data,
            "confidence": 0.6,
            "draw_boxes": True
        }

        await websocket.send(json.dumps(message))

        # Receive result
        result = await websocket.recv()
        detection_result = json.loads(result)

        print(f"Detections: {detection_result['detections_count']}")
        for detection in detection_result['detections']:
            print(f"- {detection['class']}: {detection['confidence']:.2f}")

# Run the client
asyncio.run(detection_client())
```

### React.js Hook Example

```javascript
import { useState, useEffect, useRef } from "react";

export const useWebSocketDetection = (modelName = "intrusion") => {
  const [isConnected, setIsConnected] = useState(false);
  const [lastResult, setLastResult] = useState(null);
  const [error, setError] = useState(null);
  const ws = useRef(null);

  useEffect(() => {
    const connectWebSocket = () => {
      ws.current = new WebSocket(
        `ws://localhost:8000/ws/detection/${modelName}`
      );

      ws.current.onopen = () => {
        setIsConnected(true);
        setError(null);
      };

      ws.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === "detection_result") {
          setLastResult(data);
        } else if (data.type === "error") {
          setError(data.message);
        }
      };

      ws.current.onclose = () => {
        setIsConnected(false);
      };

      ws.current.onerror = (error) => {
        setError("WebSocket error occurred");
        setIsConnected(false);
      };
    };

    connectWebSocket();

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, [modelName]);

  const sendImage = (base64Image, options = {}) => {
    if (ws.current && isConnected) {
      const message = {
        type: "image",
        data: base64Image,
        confidence: options.confidence || 0.5,
        draw_boxes: options.drawBoxes !== false,
        timestamp: new Date().toISOString(),
      };

      ws.current.send(JSON.stringify(message));
    }
  };

  const changeModel = (newModel) => {
    if (ws.current && isConnected) {
      const message = {
        type: "change_model",
        model: newModel,
      };

      ws.current.send(JSON.stringify(message));
    }
  };

  return {
    isConnected,
    lastResult,
    error,
    sendImage,
    changeModel,
  };
};
```

## 🔧 Configuration

### Environment Variables

Pastikan file `.env` sudah dikonfigurasi:

```bash
# WebSocket Configuration
PORT=8000
DEBUG=true

# YOLO Models
YOLO_MODELS_PATH=yolo_models
DEFAULT_CONFIDENCE=0.5
```

### Available Models Status

Cek status models yang tersedia:

```bash
curl http://localhost:8000/health
```

## 🚨 Error Handling

### Common Errors

1. **"No image data provided"** - Base64 image data kosong
2. **"Invalid JSON format"** - Message format tidak valid
3. **"Model {name} not available"** - Model tidak tersedia
4. **"Processing error"** - Error saat memproses image

### Connection Issues

- Pastikan server berjalan di port 8000
- Cek firewall settings
- Verifikasi WebSocket URL format

## 📊 Performance Tips

1. **Resize Images**: Resize image ke 640x640 untuk performa optimal
2. **Batch Processing**: Untuk multiple images, gunakan interval minimal 100ms
3. **Confidence Threshold**: Sesuaikan confidence (0.3-0.8) sesuai kebutuhan
4. **Connection Pooling**: Gunakan connection manager untuk multiple clients

## 🔐 Security Notes

1. **Rate Limiting**: Implement rate limiting di production
2. **Authentication**: Tambahkan authentication jika diperlukan
3. **Input Validation**: Validasi ukuran dan format image
4. **CORS**: Configure CORS untuk cross-origin requests

## 📱 Mobile Integration

### React Native Example

```javascript
// Install: npm install react-native-websocket
import WebSocket from "react-native-websocket";

<WebSocket
  url="ws://localhost:8000/ws/detection/people"
  onOpen={() => console.log("Connected")}
  onMessage={(event) => {
    const data = JSON.parse(event.data);
    handleDetectionResult(data);
  }}
  onError={(error) => console.error("WebSocket error:", error)}
  reconnect={true}
/>;
```

## ✅ Testing

### Test WebSocket Connection

```bash
# Install wscat for testing
npm install -g wscat

# Test connection
wscat -c ws://localhost:8000/ws/detection/intrusion

# Send test message
{"type": "ping", "timestamp": "2025-07-21T10:30:00Z"}
```

Panduan ini memberikan semua informasi yang diperlukan untuk mengintegrasikan WebSocket detection API dengan aplikasi frontend Anda! 🚀
