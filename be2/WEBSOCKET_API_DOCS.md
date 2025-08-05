# 📡 WebSocket Surveillance API Documentation

## 🎯 Overview

The WebSocket Surveillance API provides real-time video detection and monitoring capabilities through a persistent WebSocket connection. This eliminates the overhead of HTTP requests and enables true real-time communication.

## 🔌 Connection

**WebSocket Endpoint:** `ws://localhost:8000/ws`

**Optional Parameters:**

- `client_id`: Custom client identifier (auto-generated if not provided)

**Example Connection:**

```javascript
const ws = new WebSocket("ws://localhost:8000/ws?client_id=my_client");
```

## 📨 Message Protocol

All messages follow this JSON structure:

```json
{
    "type": "message_type",
    "message_id": "unique_identifier",
    "data": {...},
    "timestamp": "2025-08-04T10:30:00.000Z"
}
```

## 🎛️ Available Message Types

### 1. **Connection Management**

#### Ping/Pong

```json
// Send
{"type": "ping"}

// Receive
{"type": "pong", "message_id": "msg_001", "timestamp": "..."}
```

#### Subscribe to Topics

```json
// Send
{"type": "subscribe", "topic": "detections"}

// Receive
{"type": "subscription_confirmed", "topic": "detections"}
```

**Available Topics:**

- `detections` - Real-time detection alerts
- `video_processing` - Video processing updates
- `cctv_feeds` - CCTV feed notifications
- `system_alerts` - System-wide alerts

### 2. **YOLO Object Detection**

#### Detection Request

```json
{
  "type": "detect",
  "model": "intrusion",
  "data": "base64_encoded_image_data",
  "confidence": 0.6,
  "iou_threshold": 0.45
}
```

**Available Models:**

- `intrusion` - Intrusion detection
- `people` - People detection
- `security_threats` - Security threats (weapons, etc.)
- `vehicle` - Vehicle detection

#### Detection Response

```json
{
  "type": "detection_result",
  "message_id": "det_001",
  "model_type": "intrusion",
  "result": {
    "success": true,
    "detections": [
      {
        "class_id": 0,
        "class_name": "person",
        "confidence": 0.85,
        "bbox": [100, 150, 200, 300]
      }
    ],
    "total_detections": 1,
    "processing_time": 0.152,
    "image_size": [640, 480]
  },
  "timestamp": "2025-08-04T10:30:00.000Z"
}
```

### 3. **System Information**

#### Get Statistics

```json
// Send
{"type": "get_stats"}

// Receive
{
    "type": "stats_response",
    "stats": {
        "connection_stats": {
            "total_connections": 3,
            "active_clients": ["client_001", "client_002"],
            "topic_subscriptions": {"detections": 2}
        },
        "client_stats": {
            "messages_sent": 45,
            "messages_received": 12,
            "detections_processed": 8
        }
    }
}
```

#### Get Available Models

```json
// Send
{"type": "get_models"}

// Receive
{
    "type": "models_response",
    "models": {
        "success": true,
        "models": [
            {
                "model_type": "intrusion",
                "model_file": "intrusion_yolov11.pt",
                "classes": ["person", "intrusion"],
                "loaded": true
            }
        ]
    }
}
```

## 🔄 Pub/Sub Pattern

The API supports a publish/subscribe pattern for real-time notifications:

1. **Subscribe** to topics of interest
2. **Receive automatic notifications** when events occur
3. **Process updates** without polling

### Example: Detection Alerts

```json
// Subscribe to detection alerts
{"type": "subscribe", "topic": "detections"}

// Automatically receive when any client detects objects
{
    "type": "detection_alert",
    "client_id": "mobile_app_001",
    "model_type": "intrusion",
    "detections_count": 3,
    "timestamp": "2025-08-04T10:30:00.000Z"
}
```

## 🛠️ Client Implementation Examples

### JavaScript/Web

```javascript
const ws = new WebSocket("ws://localhost:8000/ws");

ws.onopen = function () {
  console.log("Connected to surveillance API");

  // Subscribe to detection alerts
  ws.send(
    JSON.stringify({
      type: "subscribe",
      topic: "detections",
    })
  );
};

ws.onmessage = function (event) {
  const data = JSON.parse(event.data);

  switch (data.type) {
    case "detection_result":
      console.log("Detection:", data.result);
      break;
    case "detection_alert":
      console.log("Alert: Objects detected!");
      break;
  }
};

// Send image for detection
function detectObjects(base64Image) {
  ws.send(
    JSON.stringify({
      type: "detect",
      model: "intrusion",
      data: base64Image,
      confidence: 0.6,
    })
  );
}
```

### Python Client

```python
import asyncio
import websockets
import json
import base64

async def client():
    uri = "ws://localhost:8000/ws"

    async with websockets.connect(uri) as websocket:
        # Subscribe to detection alerts
        await websocket.send(json.dumps({
            "type": "subscribe",
            "topic": "detections"
        }))

        # Send image for detection
        with open("test_image.jpg", "rb") as f:
            image_data = base64.b64encode(f.read()).decode()

        await websocket.send(json.dumps({
            "type": "detect",
            "model": "people",
            "data": image_data,
            "confidence": 0.7
        }))

        # Listen for responses
        async for message in websocket:
            data = json.loads(message)
            print(f"Received: {data['type']}")

asyncio.run(client())
```

### Mobile App (React Native)

```javascript
import WebSocket from "ws";

class SurveillanceAPI {
  constructor() {
    this.ws = null;
    this.callbacks = {};
  }

  connect(clientId = null) {
    const url = `ws://localhost:8000/ws${
      clientId ? `?client_id=${clientId}` : ""
    }`;
    this.ws = new WebSocket(url);

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (this.callbacks[data.type]) {
        this.callbacks[data.type](data);
      }
    };
  }

  onDetectionResult(callback) {
    this.callbacks["detection_result"] = callback;
  }

  detectObjects(imageBase64, model = "intrusion") {
    this.ws.send(
      JSON.stringify({
        type: "detect",
        model: model,
        data: imageBase64,
        confidence: 0.6,
      })
    );
  }
}
```

## 🔧 HTTP API Compatibility

For backward compatibility, HTTP endpoints are still available at `/api/v1/*`:

- `POST /api/v1/intrusion/detect`
- `POST /api/v1/people/detect`
- `POST /api/v1/security_threats/detect`
- `POST /api/v1/vehicle/detect`

However, **WebSocket is recommended** for:

- ✅ Better performance
- ✅ Real-time notifications
- ✅ Lower bandwidth usage
- ✅ Persistent connections

## 📊 Management Endpoints

- `GET /ws/stats` - WebSocket connection statistics
- `GET /ws/clients` - List connected clients
- `DELETE /ws/clients/{client_id}` - Force disconnect client

## 🚀 Benefits of WebSocket Approach

| Feature            | HTTP REST               | WebSocket        |
| ------------------ | ----------------------- | ---------------- |
| **Latency**        | High (request/response) | Low (persistent) |
| **Real-time**      | Polling required        | Native support   |
| **Bandwidth**      | High overhead           | Low overhead     |
| **Notifications**  | Not supported           | Pub/Sub pattern  |
| **Mobile Battery** | High usage              | Optimized        |
| **Scalability**    | Limited                 | High             |

## 🔐 Security Considerations

- Authentication should be handled via HTTP endpoints first
- WebSocket connections inherit HTTP session security
- Consider rate limiting for detection requests
- Implement client identification and authorization

## 🧪 Testing

Use the provided `websocket_test_client.html` for interactive testing:

1. Open the HTML file in a browser
2. Connect to the WebSocket endpoint
3. Test detection, subscriptions, and statistics
4. Monitor real-time message flow

---

**🎯 The WebSocket Surveillance API provides a modern, efficient way to integrate real-time video detection into your applications!**
