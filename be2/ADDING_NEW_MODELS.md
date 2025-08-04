# 🚀 Tutorial: Menambahkan Model YOLO Baru

Panduan lengkap untuk menambahkan model YOLO baru ke sistem AI-FRSS-DASH dengan mudah menggunakan copy-paste template.

## 📋 Prerequisites

- Model YOLO yang sudah di-train (format `.pt`)
- Mengetahui class names yang bisa dideteksi oleh model
- Akses ke folder `be2/app/`

## 🎯 Langkah-langkah (5 Menit Setup)

### **Step 1: Siapkan Model File**

1. **Copy model file** ke folder `yolo_models/`:

   ```bash
   # Contoh untuk model fire detection
   cp your_fire_model.pt be2/app/yolo_models/fire_detection_v1.pt
   ```

2. **Verifikasi model** sudah ada:
   ```bash
   ls be2/app/yolo_models/
   # Output harus menampilkan file baru:
   # fire_detection_v1.pt
   ```

### **Step 2: Update Model Configuration**

Edit file `be2/app/services/models_service.py`:

```python
# Line 34-50: Tambahkan config baru
self.model_configs = {
    "intrusion": {
        "file": "intrusion_yolov11.pt",
        "classes": ["person", "intrusion"]
    },
    "people": {
        "file": "People_yolov8s_trained.pt",
        "classes": ["person"]
    },
    "security_threats": {
        "file": "SecurityThreats_best_gun.pt",
        "classes": ["gun", "knife", "weapon"]
    },
    "vehicle": {
        "file": "vehicle_model_v11.pt",
        "classes": ["car", "truck", "bus", "motorcycle"]
    },
    # 🔧 TAMBAHKAN MODEL BARU DI SINI
    "fire_detection": {                          # Model type (snake_case)
        "file": "fire_detection_v1.pt",         # File name di yolo_models/
        "classes": ["fire", "smoke", "flame"]   # Expected classes (optional)
    }
}
```

### **Step 3: Copy Template API**

1. **Copy template** dari model existing:

   ```bash
   cd be2/app/api/mobile_v1/
   cp intrusion_api.py fire_api.py
   ```

2. **Edit file baru** `fire_api.py` - **hanya 4 tempat yang perlu diubah:**

#### **🔧 Change 1: Header & MODEL_TYPE**

```python
"""
Universal YOLO API Template - FIRE DETECTION MODEL    # ← Ubah ini
Copy-paste this file and change MODEL_TYPE for new models

For new models:
1. Copy this file
2. Rename to [model_name]_api.py
3. Change MODEL_TYPE = "your_model_name"
4. Import in main.py
"""

# 🔧 CHANGE THIS FOR NEW MODELS
MODEL_TYPE = "fire_detection"  # ← Ubah ini (harus sama dengan config key)
```

#### **🔧 Change 2: Function Names (4 functions)**

```python
# Ganti semua function names:
@router.post("/detect", response_model=DetectionResponse)
async def detect_fire(request: DetectionRequest):  # ← Ubah dari detect_intrusion

@router.get("/info")
async def get_fire_model_info():  # ← Ubah dari get_intrusion_model_info

@router.get("/history")
async def get_fire_history(limit: int = 100):  # ← Ubah dari get_intrusion_history

@router.post("/load")
async def load_fire_model():  # ← Ubah dari load_intrusion_model
```

#### **🔧 Change 3: Docstrings**

```python
"""
Detect fire in image    # ← Ubah dari "Detect intrusion in image"

Copy-paste template - only MODEL_TYPE changes for different models
"""
```

```python
"""
Get fire model information    # ← Ubah dari "Get intrusion model information"

Copy-paste template - only MODEL_TYPE changes
"""
```

```python
"""
Get fire detection history    # ← Ubah dari "Get intrusion detection history"

Copy-paste template - only MODEL_TYPE changes
"""
```

```python
"""
Load fire model into memory    # ← Ubah dari "Load intrusion model into memory"

Copy-paste template - only MODEL_TYPE changes
"""
```

#### **🔧 Change 4: Error Messages**

```python
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Fire detection failed: {str(e)}")
    # ← Ubah dari "Intrusion detection failed"
```

### **Step 4: Register di Main Application**

Edit file `be2/app/main.py`:

```python
# Import router baru
try:
    from controller.auth_controller import router as auth_router
    app.include_router(auth_router, prefix="/mobile/v1/auth", tags=["authentication"])
    logger.info("Authentication routes loaded successfully")
except ImportError as e:
    logger.warning(f"Auth routes could not be loaded: {str(e)}")

# 🔧 TAMBAHKAN IMPORT & ROUTER BARU
try:
    from api.mobile_v1.fire_api import router as fire_router
    app.include_router(fire_router, prefix="/mobile/v1/fire", tags=["fire-detection"])
    logger.info("Fire detection routes loaded successfully")
except ImportError as e:
    logger.warning(f"Fire routes could not be loaded: {str(e)}")
```

### **Step 5: Test API**

1. **Restart server**:

   ```bash
   cd be2/app
   python main.py
   ```

2. **Test endpoints**:

   ```bash
   # Health check
   curl http://localhost:8000/mobile/v1/fire/info

   # Load model
   curl -X POST http://localhost:8000/mobile/v1/fire/load

   # Test detection (dengan base64 image)
   curl -X POST http://localhost:8000/mobile/v1/fire/detect \
     -H "Content-Type: application/json" \
     -d '{"image_data": "base64_image_here", "model_type": "fire_detection"}'
   ```

## 📂 File Structure Result

Setelah menambahkan model baru:

```
be2/app/
├── yolo_models/
│   ├── intrusion_yolov11.pt
│   ├── People_yolov8s_trained.pt
│   ├── SecurityThreats_best_gun.pt
│   ├── vehicle_model_v11.pt
│   └── fire_detection_v1.pt          # ✅ Model baru
├── services/
│   └── models_service.py              # ✅ Updated config
├── api/mobile_v1/
│   ├── intrusion_api.py
│   ├── people_api.py
│   ├── security_api.py
│   ├── vehicle_api.py
│   └── fire_api.py                    # ✅ API baru
└── main.py                            # ✅ Updated imports
```

## 🎯 API Endpoints Baru

Model baru akan tersedia di:

```
POST /mobile/v1/fire/detect     # Object detection
GET  /mobile/v1/fire/info       # Model information
GET  /mobile/v1/fire/history    # Detection history
POST /mobile/v1/fire/load       # Load model to memory
```

## 📝 Naming Convention

| Component                   | Format      | Example                |
| --------------------------- | ----------- | ---------------------- |
| **Model Type (config key)** | snake_case  | `fire_detection`       |
| **MODEL_TYPE Variable**     | snake_case  | `fire_detection`       |
| **API Filename**            | readable    | `fire_api.py`          |
| **Function Names**          | descriptive | `detect_fire()`        |
| **URL Prefix**              | clean       | `/mobile/v1/fire/`     |
| **Model File**              | descriptive | `fire_detection_v1.pt` |

## ⚡ Quick Reference

**Untuk model baru, ubah hanya:**

1. ✅ **models_service.py** → Tambah 1 config block
2. ✅ **[model]\_api.py** → Copy-paste & ubah 4 tempat
3. ✅ **main.py** → Tambah 1 import & 1 router
4. ✅ **yolo_models/** → Copy 1 file model

**Total waktu: 5 menit!** 🚀

## 🔧 Troubleshooting

### **Model tidak bisa di-load**

```python
# Check file path
ls be2/app/yolo_models/your_model.pt

# Check config di models_service.py
"your_model": {
    "file": "your_model.pt",  # Pastikan nama file benar
    "classes": [...]
}
```

### **Import error**

```python
# Check import di main.py
from api.mobile_v1.your_model_api import router as your_model_router

# Check MODEL_TYPE di API file
MODEL_TYPE = "your_model"  # Harus sama dengan config key
```

### **Endpoint 404**

```python
# Check router registration di main.py
app.include_router(your_model_router, prefix="/mobile/v1/your_model")
```

## 🎉 Selesai!

Model YOLO baru sudah siap digunakan dengan endpoints yang konsisten dan maintainable!

**Copy-paste template membuat penambahan model menjadi super mudah dan cepat.** 🚀
