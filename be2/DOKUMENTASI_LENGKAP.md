# DOKUMENTASI LENGKAP: AI-FRSS MULTI-MODEL YOLO DETECTION SYSTEM

## RINGKASAN PERUBAHAN

Sistem telah direfactor untuk mendukung deteksi simultan menggunakan 4 model YOLO secara bersamaan dengan arsitektur modular yang terstruktur.

---

## STRUKTUR DIREKTORI BARU

```
be2/
├── app/
│   ├── main.py                          # Entry point aplikasi FastAPI
│   ├── config/
│   │   ├── settings.py                  # Konfigurasi aplikasi
│   │   └── db_helper.py                 # Helper database (existing)
│   ├── services/                        # Layer business logic
│   │   ├── __init__.py                  # Modul init
│   │   ├── yolo_service.py             # Manager YOLO models
│   │   ├── image_service.py            # Utilities pemrosesan gambar
│   │   └── database_service.py         # Service PostgreSQL
│   ├── controller/                      # Layer API endpoints
│   │   ├── detection_controller.py     # REST API untuk deteksi
│   │   ├── websocket_controller.py     # WebSocket real-time
│   │   ├── auth_controller.py          # Authentication (existing)
│   │   └── faces_controller.py         # Face recognition (existing)
│   ├── models/                         # Database models
│   │   ├── database_models.py          # SQLAlchemy models PostgreSQL
│   │   ├── auth.py                     # Auth models (existing)
│   │   └── faces.py                    # Face models (existing)
│   └── yolo_models/                    # File model YOLO
│       ├── intrusion_yolov11.pt        # Model deteksi intrusi
│       ├── People_yolov8s_trained.pt   # Model deteksi orang
│       ├── SecurityThreats_best_gun.pt # Model deteksi senjata
│       └── vehicle_model_v11.pt        # Model deteksi kendaraan
├── requirements.txt                     # Dependencies Python
├── .env.example                        # Template environment
├── alembic.ini                         # Konfigurasi migrasi database
├── setup_postgresql.py                 # Script setup database
└── README_YOLO.md                      # Dokumentasi implementasi
```

---

## ANALISIS FILE PER FILE

### 1. main.py (Entry Point Aplikasi)

**Fungsi Utama:**

- Entry point untuk aplikasi FastAPI
- Konfigurasi middleware CORS
- Setup lifecycle management (startup/shutdown)
- Pre-loading semua model YOLO
- Health check endpoint dengan status database dan model

**Perubahan Signifikan:**

**Baris 1-12: Import Dependencies**

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
from contextlib import asynccontextmanager

from controller.detection_controller import router as detection_router
from controller.websocket_controller import router as websocket_router
from controller.auth_controller import router as auth_router
from controller.faces_controller import router as faces_router
from services.yolo_service import yolo_manager
from services.database_service import db_service
```

- Import semua router untuk modularitas
- Import service layer untuk YOLO dan database
- Menggunakan asynccontextmanager untuk lifecycle management

**Baris 20-45: Lifecycle Management**

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting AI-FRSS YOLO Detection Service...")

    try:
        logger.info("Checking PostgreSQL connection...")
        db_connected = await db_service.check_connection()
        if db_connected:
            logger.info("✅ PostgreSQL connected successfully")
            await db_service.create_tables()
        else:
            logger.error("❌ PostgreSQL connection failed")
    except Exception as e:
        logger.error(f"❌ Database initialization error: {e}")

    try:
        logger.info("Loading default YOLO models...")
        models_to_load = ["intrusion", "people", "security_threats", "vehicle"]
        for model_name in models_to_load:
            try:
                yolo_manager.load_model(model_name)
                logger.info(f"✅ Model {model_name} loaded successfully")
            except Exception as e:
                logger.error(f"❌ Failed to load model {model_name}: {e}")

        loaded_count = len(yolo_manager.loaded_models)
        logger.info(f"✅ {loaded_count}/{len(models_to_load)} models loaded successfully")
    except Exception as e:
        logger.error(f"❌ Error loading default models: {e}")

    yield

    logger.info("🛑 Shutting down AI-FRSS service...")
    await db_service.close()
```

- Mengecek koneksi database pada startup
- Membuat tabel database jika belum ada
- Pre-loading semua 4 model YOLO untuk performa optimal
- Graceful shutdown dengan menutup koneksi database

**Baris 79-103: Enhanced Health Check**

```python
@app.get("/health", tags=["Health"])
async def health_check():
    try:
        available_models = yolo_manager.get_available_models()
        loaded_models = list(yolo_manager.loaded_models.keys())

        db_status = await db_service.check_connection()

        return {
            "status": "healthy" if db_status else "degraded",
            "timestamp": "2025-07-18",
            "database": {
                "status": "connected" if db_status else "disconnected",
                "type": "PostgreSQL"
            },
            "models": {
                "available": len(available_models),
                "loaded": len(loaded_models),
                "available_models": list(available_models.keys()),
                "loaded_models": loaded_models
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Service unhealthy: {str(e)}")
```

- Health check yang comprehensive meliputi database dan model status
- Menampilkan informasi detail tentang model yang tersedia dan dimuat
- Status database connection untuk monitoring

---

### 2. services/yolo_service.py (YOLO Model Manager)

**Fungsi Utama:**

- Centralized management untuk semua model YOLO
- Loading dan unloading model dengan lazy loading
- Single model dan multi-model prediction
- Kombinasi hasil dari multiple model

**Komponen Utama:**

**Baris 10-32: Model Configuration**

```python
class YOLOModelManager:
    def __init__(self, models_path: str = "yolo_models"):
        self.models_path = models_path
        self.loaded_models: Dict[str, YOLO] = {}
        self.model_configs = {
            "intrusion": {
                "file": "intrusion_yolov11.pt",
                "description": "Deteksi intrusi/penyusupan",
                "classes": ["person", "intruder"]
            },
            "people": {
                "file": "People_yolov8s_trained.pt",
                "description": "Deteksi dan counting orang",
                "classes": ["person"]
            },
            "security_threats": {
                "file": "SecurityThreats_best_gun.pt",
                "description": "Deteksi ancaman keamanan (senjata)",
                "classes": ["gun", "knife", "weapon"]
            },
            "vehicle": {
                "file": "vehicle_model_v11.pt",
                "description": "Deteksi kendaraan",
                "classes": ["car", "truck", "motorcycle", "bus"]
            }
        }
```

- Konfigurasi semua 4 model YOLO dengan metadata lengkap
- Lazy loading pattern untuk efisiensi memory
- Path konfigurasi yang fleksibel

**Baris 34-52: Model Loading Logic**

```python
def load_model(self, model_name: str) -> YOLO:
    if model_name in self.loaded_models:
        return self.loaded_models[model_name]

    if model_name not in self.model_configs:
        raise ValueError(f"Model {model_name} tidak tersedia. Available: {list(self.model_configs.keys())}")

    model_file = self.model_configs[model_name]["file"]
    model_path = os.path.join(self.models_path, model_file)

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file tidak ditemukan: {model_path}")

    try:
        model = YOLO(model_path)
        self.loaded_models[model_name] = model
        logger.info(f"Model {model_name} berhasil dimuat dari {model_path}")
        return model
    except Exception as e:
        logger.error(f"Error loading model {model_name}: {e}")
        raise
```

- Lazy loading: model dimuat hanya saat dibutuhkan
- Validasi file existence sebelum loading
- Error handling yang comprehensive
- Caching model yang sudah dimuat untuk efisiensi

**Baris 65-87: Single Model Prediction**

```python
def predict(self, model_name: str, image, **kwargs) -> List[Dict[str, Any]]:
    model = self.load_model(model_name)

    default_params = {
        "conf": 0.5,
        "iou": 0.45,
        "max_det": 100,
        "classes": None
    }
    default_params.update(kwargs)

    try:
        results = model(image, **default_params)

        detections = []
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for i in range(len(boxes)):
                    detection = {
                        "bbox": boxes.xyxy[i].cpu().numpy().tolist(),
                        "confidence": float(boxes.conf[i].cpu().numpy()),
                        "class_id": int(boxes.cls[i].cpu().numpy()),
                        "class_name": model.names[int(boxes.cls[i].cpu().numpy())]
                    }
                    detections.append(detection)

        return detections
    except Exception as e:
        logger.error(f"Error during prediction with {model_name}: {e}")
        raise
```

- Standardized inference parameters dengan override capability
- Konversi hasil YOLO ke format JSON yang konsisten
- Error handling untuk robustness
- Normalisasi output dari berbagai versi YOLO

**Baris 89-110: Multi-Model Prediction (FITUR UTAMA)**

```python
def predict_multi_model(self, image, models: List[str] = None, **kwargs) -> Dict[str, List[Dict[str, Any]]]:
    if models is None:
        models = list(self.model_configs.keys())

    default_params = {
        "conf": 0.5,
        "iou": 0.45,
        "max_det": 100,
        "classes": None
    }
    default_params.update(kwargs)

    results = {}

    for model_name in models:
        try:
            detections = self.predict(model_name, image, **default_params)
            results[model_name] = detections
            logger.info(f"Model {model_name}: {len(detections)} detections")
        except Exception as e:
            logger.error(f"Error with model {model_name}: {e}")
            results[model_name] = []

    return results
```

- **INTI SISTEM**: Menjalankan semua 4 model secara bersamaan
- Graceful failure: jika satu model error, model lain tetap berjalan
- Logging untuk monitoring performance setiap model
- Fleksibilitas untuk memilih subset model

**Baris 112-124: Result Combination**

```python
def get_combined_detections(self, multi_results: Dict[str, List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    combined = []

    for model_name, detections in multi_results.items():
        for detection in detections:
            detection["source_model"] = model_name
            detection["model_description"] = self.model_configs[model_name]["description"]
            combined.append(detection)

    return combined
```

- Menggabungkan hasil dari semua model dengan metadata source
- Tracking asal deteksi untuk analisis lebih lanjut
- Mempertahankan traceability hasil deteksi

---

### 3. services/image_service.py (Image Processing Utilities)

**Fungsi Utama:**

- Utilities untuk pemrosesan gambar
- Konversi format (base64, PIL Image)
- Drawing bounding boxes dengan multiple colors
- Image resizing untuk optimasi

**Komponen Utama:**

**Baris 1-20: Class Initialization**

```python
class ImageProcessor:
    def __init__(self):
        self.colors = [
            (255, 0, 0),    # Red
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (255, 255, 0),  # Yellow
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
            (128, 0, 128),  # Purple
            (255, 165, 0),  # Orange
        ]
```

- Predefined color palette untuk visualisasi multiple model
- Setiap model akan mendapat warna yang berbeda

**Baris 22-37: Format Conversion Methods**

```python
def base64_to_image(self, base64_string: str) -> Image.Image:
    try:
        img_bytes = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        return image
    except Exception as e:
        raise ValueError(f"Error converting base64 to image: {e}")

def image_to_base64(self, image: Image.Image, format: str = "PNG") -> str:
    try:
        buf = io.BytesIO()
        image.save(buf, format=format)
        buf.seek(0)
        img_b64 = base64.b64encode(buf.read()).decode("utf-8")
        return img_b64
    except Exception as e:
        raise ValueError(f"Error converting image to base64: {e}")
```

- Robust conversion antara base64 dan PIL Image
- Error handling untuk data corruption
- Support untuk WebSocket dan REST API communication

**Baris 39-85: Advanced Drawing Function**

```python
def draw_detections(self, image: Image.Image, detections: List[Dict[str, Any]],
                   draw_labels: bool = True, line_width: int = 3) -> Image.Image:
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()

    for i, detection in enumerate(detections):
        bbox = detection["bbox"]
        confidence = detection["confidence"]
        class_name = detection["class_name"]

        color = self.colors[i % len(self.colors)]

        # Draw bounding box
        draw.rectangle(bbox, outline=color, width=line_width)

        if draw_labels:
            label = f"{class_name}: {confidence:.2f}"

            bbox_text = draw.textbbox((0, 0), label, font=font)
            text_width = bbox_text[2] - bbox_text[0]
            text_height = bbox_text[3] - bbox_text[1]

            # Draw label background
            label_bg = [
                bbox[0],
                bbox[1] - text_height - 4,
                bbox[0] + text_width + 4,
                bbox[1]
            ]
            draw.rectangle(label_bg, fill=color)

            # Draw label text
            draw.text(
                (bbox[0] + 2, bbox[1] - text_height - 2),
                label,
                fill="white",
                font=font
            )

    return image
```

- Advanced bounding box drawing dengan automatic color assignment
- Label dengan background untuk readability
- Font fallback untuk compatibility
- Support untuk multiple detection sources

---

### 4. controller/detection_controller.py (REST API Endpoints)

**Fungsi Utama:**

- REST API endpoints untuk deteksi YOLO
- Single model dan multi-model detection
- Batch processing dan comparison utilities

**Endpoint Baru untuk Multi-Model:**

**Baris 120-200: Multi-Model Detection Endpoint**

```python
@router.post("/predict-all")
async def detect_all_models(
    file: UploadFile = File(...),
    confidence: float = 0.5,
    draw_boxes: bool = True,
    return_image: bool = True,
    combine_results: bool = False
):
    # Validasi file
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File harus berupa gambar")

    try:
        # Load dan process image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image_processor.resize_image(image)

        # Predict menggunakan semua model YOLO
        multi_results = yolo_manager.predict_multi_model(
            image=image,
            conf=confidence
        )

        total_detections = sum(len(detections) for detections in multi_results.values())

        response_data = {
            "total_models_used": len(multi_results),
            "image_size": {"width": image.width, "height": image.height},
            "total_detections": total_detections,
            "results_by_model": multi_results
        }

        if combine_results:
            combined_detections = yolo_manager.get_combined_detections(multi_results)
            response_data["combined_detections"] = combined_detections
```

- **ENDPOINT UTAMA**: Menjalankan semua 4 model sekaligus
- Parameter fleksibel untuk customization
- Option untuk menggabungkan hasil atau memisahkan per model
- Comprehensive response dengan metadata lengkap

**Baris 230-290: Model Comparison Endpoint**

```python
@router.post("/compare-models")
async def compare_models(
    file: UploadFile = File(...),
    confidence: float = 0.5
):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image_processor.resize_image(image)

        multi_results = yolo_manager.predict_multi_model(
            image=image,
            conf=confidence
        )

        comparison = {
            "image_info": {
                "size": {"width": image.width, "height": image.height},
                "confidence_threshold": confidence
            },
            "model_comparison": []
        }

        for model_name, detections in multi_results.items():
            model_info = yolo_manager.model_configs[model_name]

            if detections:
                confidences = [d["confidence"] for d in detections]
                avg_confidence = sum(confidences) / len(confidences)
                max_confidence = max(confidences)
                min_confidence = min(confidences)
            else:
                avg_confidence = max_confidence = min_confidence = 0.0

            comparison["model_comparison"].append({
                "model_name": model_name,
                "description": model_info["description"],
                "detection_count": len(detections),
                "confidence_stats": {
                    "average": round(avg_confidence, 3),
                    "maximum": round(max_confidence, 3),
                    "minimum": round(min_confidence, 3)
                },
                "detections": detections
            })

        return comparison
```

- Analisis performa comparative antar model
- Statistik confidence untuk setiap model
- Useful untuk model evaluation dan tuning

---

### 5. controller/websocket_controller.py (Real-time Communication)

**Fungsi Utama:**

- WebSocket endpoints untuk real-time detection
- Multi-model detection via WebSocket
- Connection management dan broadcasting

**Multi-Model WebSocket Endpoint:**

**Baris 180-280: Multi-Model WebSocket**

```python
@router.websocket("/detection-all")
async def websocket_multi_detection(websocket: WebSocket):
    await manager.connect(websocket, "multi-model")

    try:
        await manager.send_personal_message({
            "type": "connection_established",
            "model": "all-models",
            "message": "Connected to multi-model detection service",
            "available_models": list(yolo_manager.model_configs.keys())
        }, websocket)

        while True:
            data = await websocket.receive_text()

            try:
                message = json.loads(data)

                if message.get("type") == "image":
                    base64_image = message.get("data")
                    confidence = message.get("confidence", 0.5)
                    combine_results = message.get("combine_results", False)

                    if not base64_image:
                        await manager.send_personal_message({
                            "type": "error",
                            "message": "No image data provided"
                        }, websocket)
                        continue

                    image = image_processor.base64_to_image(base64_image)
                    image = image_processor.resize_image(image)

                    # Predict menggunakan semua model YOLO
                    multi_results = yolo_manager.predict_multi_model(
                        image=image,
                        conf=confidence
                    )

                    total_detections = sum(len(detections) for detections in multi_results.values())

                    response = {
                        "type": "multi_detection_result",
                        "models_used": list(multi_results.keys()),
                        "image_size": {"width": image.width, "height": image.height},
                        "total_detections": total_detections,
                        "results_by_model": multi_results,
                        "timestamp": message.get("timestamp")
                    }

                    if combine_results:
                        combined_detections = yolo_manager.get_combined_detections(multi_results)
                        response["combined_detections"] = combined_detections
```

- **REAL-TIME MULTI-MODEL**: WebSocket untuk deteksi simultan
- Async processing untuk responsiveness
- Flexible result format (per-model atau combined)
- Error handling yang robust untuk production use

---

### 6. services/database_service.py (PostgreSQL Integration)

**Fungsi Utama:**

- Async PostgreSQL connection management
- Session factory dengan proper cleanup
- Health check untuk database monitoring

**Key Components:**

**Baris 10-25: Database Configuration**

```python
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://username:password@localhost:5432/ai_frss"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600
)

async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)
```

- Async engine dengan connection pooling
- Environment-based configuration
- Production-ready connection parameters

**Baris 35-50: Session Management**

```python
async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
    async with self.session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

- Proper transaction management
- Automatic rollback pada error
- Resource cleanup yang guaranteed

---

### 7. models/database_models.py (Database Schema)

**Fungsi Utama:**

- SQLAlchemy models untuk PostgreSQL
- Schema untuk logging detection results
- User management dan system configuration

**Key Models:**

**Baris 15-25: Detection Log Model**

```python
class DetectionLog(Base):
    __tablename__ = "detection_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    model_name = Column(String(50), nullable=False, index=True)
    image_path = Column(String(500), nullable=True)
    detections = Column(JSON, nullable=False)
    confidence_threshold = Column(Float, default=0.5)
    detection_count = Column(Integer, default=0)
    processing_time = Column(Float, nullable=True)
    camera_id = Column(String(100), nullable=True, index=True)
    location = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

- Comprehensive logging untuk analisis performance
- JSON storage untuk detection results
- Indexing untuk query performance
- Timestamp tracking untuk audit trail

---

## FLOW DETEKSI MULTI-MODEL

### 1. Startup Process

1. FastAPI app starts dengan lifespan manager
2. Database connection check dan table creation
3. Pre-loading semua 4 model YOLO ke memory
4. Health check endpoint ready

### 2. Multi-Model Detection Flow

1. Client upload image via REST atau WebSocket
2. Image divalidasi dan di-resize untuk optimasi
3. YOLOModelManager.predict_multi_model() dipanggil
4. Semua 4 model dijalankan secara sequential
5. Hasil dikombinasi dengan source model tracking
6. Response dikirim dengan metadata lengkap

### 3. Real-time WebSocket Flow

1. Client connect ke /ws/detection-all
2. Send base64 image dengan parameters
3. Server process dengan semua model
4. Send back results dengan optional image overlay
5. Connection maintained untuk continuous detection

---

## KEUNGGULAN IMPLEMENTASI

### 1. Modularitas

- Separation of concerns yang jelas
- Service layer terpisah dari controller
- Reusable components untuk maintainability

### 2. Performance

- Lazy loading untuk efisiensi memory
- Connection pooling untuk database
- Async processing untuk scalability

### 3. Robustness

- Comprehensive error handling
- Graceful degradation jika model error
- Health monitoring untuk system status

### 4. Flexibility

- Parameter customization untuk setiap endpoint
- Multiple output format (per-model atau combined)
- WebSocket dan REST support

### 5. Production-Ready

- Proper logging untuk debugging
- Database integration untuk audit
- Environment-based configuration

---

## TESTING DAN MONITORING

### 1. Health Check Endpoints

- GET /health: Status sistem, database, dan model
- Monitor loaded models dan connection status

### 2. Model Performance

- Detection count per model
- Confidence statistics
- Processing time tracking

### 3. Database Logging

- Semua detection results disimpan
- Audit trail untuk compliance
- Performance analysis data

---

## DEPLOYMENT CONSIDERATIONS

### 1. Hardware Requirements

- GPU support untuk inference speed
- Memory untuk 4 model simultaneous
- Storage untuk image dan log data

### 2. Environment Setup

- PostgreSQL database setup
- Environment variables configuration
- Model files placement

### 3. Monitoring

- Application performance monitoring
- Database connection monitoring
- Model accuracy tracking

---

DOKUMENTASI INI MENJELASKAN SEMUA PERUBAHAN YANG DILAKUKAN UNTUK MENDUKUNG DETEKSI SIMULTAN MENGGUNAKAN 4 MODEL YOLO DALAM SISTEM SURVEILLANCE AI-FRSS.
