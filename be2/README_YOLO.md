# AI-FRSS Multi-Model YOLO Detection System

## Overview

Sistem deteksi surveillance berbasis FastAPI yang mendukung 4 model YOLO secara simultan untuk deteksi intrusi, orang, ancaman keamanan, dan kendaraan.

## Quick Start

### 1. Environment Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env

# Edit .env file dengan konfigurasi database
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/ai_frss
```

### 2. Database Setup

```bash
# Run PostgreSQL setup
python setup_postgresql.py

# Atau manual setup database
createdb ai_frss
```

### 3. Model Files

Pastikan file model YOLO berada di folder `yolo_models/`:

- `intrusion_yolov11.pt`
- `People_yolov8s_trained.pt`
- `SecurityThreats_best_gun.pt`
- `vehicle_model_v11.pt`

### 4. Run Application

```bash
cd app
python main.py
```

## API Endpoints

### Health Check

```
GET /health
```

### Single Model Detection

```
POST /api/v1/predict/{model_name}
```

### Multi-Model Detection (UTAMA)

```
POST /api/v1/predict-all
```

### Model Comparison

```
POST /api/v1/compare-models
```

### WebSocket Real-time

#### Single Model

```
WS /ws/detection/{model_name}
```

#### Multi-Model (UTAMA)

```
WS /ws/detection-all
```

## Key Features

### 1. Concurrent Multi-Model Detection

- Menjalankan 4 model YOLO bersamaan
- Hasil terpisah per model atau dikombinasi
- Real-time processing via WebSocket

### 2. Modular Architecture

```
services/         # Business logic
├── yolo_service.py
├── image_service.py
└── database_service.py

controller/       # API endpoints
├── detection_controller.py
└── websocket_controller.py

models/          # Database models
└── database_models.py
```

### 3. Production Ready

- PostgreSQL integration dengan async support
- Comprehensive error handling
- Health monitoring
- Request/response logging
- ✅ **Health Checks**: System monitoring endpoints

---

## 🚀 **API Endpoints Baru**

### 📊 **Detection Endpoints**

```bash
GET  /detection/models           # List available models
POST /detection/predict/{model}  # Single image detection
POST /detection/batch-predict/{model}  # Multiple images
POST /detection/crop-detections/{model} # Extract detected objects
```

### 🔌 **WebSocket Endpoints**

```bash
WS /ws/detection/{model_name}    # Real-time detection
WS /ws/broadcast                 # Alert broadcasting
```

### 🏥 **System Endpoints**

```bash
GET  /                          # Root health check
GET  /health                    # Detailed system status
```

---

## 🔧 **Cara Menjalankan Service Baru**

### 1️⃣ **Install Dependencies**

```bash
cd be2
pip install -r requirements.txt
```

### 2️⃣ **Setup Environment**

```bash
cp .env.example .env
# Edit .env sesuai kebutuhan
```

### 3️⃣ **Run Application**

```bash
cd app
python main.py
```

### 4️⃣ **Access Documentation**

- **API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 🎮 **Contoh Penggunaan**

### 📷 **Upload & Detect (REST API)**

```bash
curl -X POST "http://localhost:8000/detection/predict/intrusion" \
     -H "accept: image/png" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@image.jpg" \
     -F "confidence=0.7"
```

### ⚡ **Real-time Detection (WebSocket)**

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/detection/intrusion");

// Send image for detection
ws.send(
  JSON.stringify({
    type: "image",
    data: base64ImageString,
    confidence: 0.6,
  })
);

// Receive detection results
ws.onmessage = (event) => {
  const result = JSON.parse(event.data);
  console.log("Detections:", result.detections);
};
```

---

## 🎯 **Model YOLO yang Tersedia**

| Model Name         | File                        | Use Case             |
| ------------------ | --------------------------- | -------------------- |
| `intrusion`        | intrusion_yolov11.pt        | Deteksi penyusupan   |
| `people`           | People_yolov8s_trained.pt   | Counting orang       |
| `security_threats` | SecurityThreats_best_gun.pt | Deteksi senjata      |
| `vehicle`          | vehicle_model_v11.pt        | Monitoring kendaraan |

---

## 🏗️ **Keunggulan Arsitektur Baru**

### 🎯 **Modularitas**

- **Services Layer**: Business logic terpisah
- **Controllers**: API endpoints yang focused
- **Configuration**: Environment-based settings

### ⚡ **Performance**

- **Model Caching**: Models dimuat sekali, digunakan berkali-kali
- **Async Processing**: Non-blocking operations
- **Optimized Image Processing**: Resize otomatis, batch processing

### 🔒 **Reliability**

- **Error Handling**: Proper exception management
- **Health Monitoring**: System status tracking
- **Graceful Shutdown**: Clean resource management

### 🔌 **Flexibility**

- **Multi-Model Support**: Switch models on-the-fly
- **REST + WebSocket**: Multiple interaction patterns
- **Configurable**: Easy customization via environment

---

## 🎪 **Migration dari main.py Lama**

Jika Anda ingin migrate dari implementasi lama:

1. **Backup** file lama: `mv main.py main_old.py`
2. **Copy** file baru yang sudah dibuat
3. **Install** dependencies: `pip install -r requirements.txt`
4. **Test** dengan: `python main.py`

---

## 📝 **Next Steps**

1. **✅ Test semua endpoints** di `/docs`
2. **✅ Upload model YOLO** ke folder `yolo_models/`
3. **✅ Configure environment** di `.env`
4. **✅ Integrate dengan frontend** menggunakan WebSocket
5. **✅ Add monitoring & logging** untuk production

---

_Happy coding! 🚀_
