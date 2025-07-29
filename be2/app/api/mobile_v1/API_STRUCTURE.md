"""
API Structure Overview
Mobile API v1 Organized Structure

📁 api/mobile_v1/
├── 🤖 models/           # YOLO Model Detection APIs
│   ├── intrusion_api.py    # Intrusion detection model
│   ├── people_api.py       # People detection model  
│   ├── security_api.py     # Security threats detection model
│   ├── vehicle_api.py      # Vehicle detection model
│   └── faces_api.py        # Face recognition model (legacy)
│
├── 🚀 features/         # Implementation Feature APIs
│   ├── video_upload_api.py # Video upload & batch processing
│   ├── realtime_api.py     # WebSocket real-time detection
│   └── cctv_api.py         # CCTV/IP camera monitoring
│
└── 🔐 auth/             # Authentication APIs
    └── auth_api.py         # Login, register, JWT management

=== API ENDPOINTS MAPPING ===

🤖 MODELS APIs:
/mobile/v1/intrusion/*          - Intrusion detection
/mobile/v1/people/*             - People detection
/mobile/v1/security_threats/*   - Security threats detection
/mobile/v1/vehicle/*            - Vehicle detection

🚀 FEATURES APIs:
/mobile/v1/video/*              - Video upload & processing
/mobile/v1/realtime/*           - Real-time detection via WebSocket
/mobile/v1/cctv/*               - CCTV monitoring & management

🔐 AUTH APIs:
/mobile/v1/auth/*               - Authentication & authorization

=== USAGE PATTERNS ===

📱 Mobile App Usage:
1. Authentication: /mobile/v1/auth/login
2. Image Detection: /mobile/v1/{model}/detect
3. Video Processing: /mobile/v1/video/upload
4. Real-time: /mobile/v1/realtime/ws

🏢 Enterprise Usage:
1. CCTV Setup: /mobile/v1/cctv/cameras
2. Monitoring: /mobile/v1/cctv/monitoring/start
3. Alerts: /mobile/v1/cctv/detections/history

=== SCALABILITY ===

Adding New Models:
1. Copy any model API template from models/
2. Change MODEL_TYPE variable
3. Add import in main.py
4. Model automatically integrated

Adding New Features:
1. Create new API file in features/
2. Implement feature-specific endpoints
3. Add import in main.py
4. Feature available across all models

This structure provides:
✅ Clear separation of concerns
✅ Easy model scaling
✅ Feature reusability
✅ Clean mobile app integration
✅ Enterprise-ready architecture
"""
