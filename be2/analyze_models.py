#!/usr/bin/env python3
"""
Script untuk menganalisis setiap model YOLO secara detail
Mengetahui class names, input size, architecture, dll
"""

import os
import sys
from pathlib import Path
import torch

# Add app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

try:
    from ultralytics import YOLO
except ImportError:
    print("❌ ultralytics tidak terinstall. Install dengan: pip install ultralytics")
    sys.exit(1)

def analyze_yolo_model(model_path: str, model_name: str):
    """Analisis detail sebuah model YOLO"""
    print(f"\n{'='*60}")
    print(f"📊 ANALISIS MODEL: {model_name}")
    print(f"📁 File: {model_path}")
    print(f"{'='*60}")
    
    if not os.path.exists(model_path):
        print(f"❌ File tidak ditemukan: {model_path}")
        return None
    
    try:
        # Load model
        print("🔄 Loading model...")
        model = YOLO(model_path)
        
        # Basic info
        print(f"✅ Model berhasil dimuat")
        print(f"📋 Model Type: {type(model.model).__name__}")
        
        # Model metadata
        if hasattr(model, 'info'):
            try:
                model.info()
            except:
                pass
        
        # Class information
        if hasattr(model, 'names') and model.names:
            print(f"\n🏷️  CLASS INFORMATION:")
            print(f"   Total Classes: {len(model.names)}")
            print(f"   Class Names: {list(model.names.values())}")
            
            # Print detailed class mapping
            print(f"\n   Class ID → Name Mapping:")
            for class_id, class_name in model.names.items():
                print(f"   {class_id:2d} → {class_name}")
        else:
            print("⚠️  Class information tidak tersedia")
        
        # Model architecture info
        if hasattr(model.model, 'yaml'):
            yaml_info = model.model.yaml
            print(f"\n🏗️  ARCHITECTURE INFO:")
            if 'nc' in yaml_info:
                print(f"   Number of Classes: {yaml_info['nc']}")
            if 'depth_multiple' in yaml_info:
                print(f"   Depth Multiple: {yaml_info['depth_multiple']}")
            if 'width_multiple' in yaml_info:
                print(f"   Width Multiple: {yaml_info['width_multiple']}")
        
        # Input size info
        if hasattr(model.model, 'stride'):
            print(f"\n📐 INPUT INFO:")
            print(f"   Model Stride: {model.model.stride}")
            
        # Try to get more model info
        if hasattr(model.model, 'model') and hasattr(model.model.model, '__len__'):
            print(f"   Model Layers: {len(model.model.model)}")
        
        # Task info
        if hasattr(model, 'task'):
            print(f"   Task: {model.task}")
            
        # File size
        file_size = os.path.getsize(model_path) / (1024 * 1024)  # MB
        print(f"\n💾 FILE INFO:")
        print(f"   File Size: {file_size:.2f} MB")
        
        # Try prediction on dummy data to understand input/output
        print(f"\n🧪 DUMMY PREDICTION TEST:")
        try:
            import numpy as np
            from PIL import Image
            
            # Create dummy image
            dummy_img = Image.fromarray(np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8))
            
            # Run prediction
            results = model(dummy_img, conf=0.1, verbose=False)
            
            if results and len(results) > 0:
                result = results[0]
                print(f"   ✅ Prediction successful")
                print(f"   Input Shape: {dummy_img.size}")
                
                if hasattr(result, 'boxes') and result.boxes is not None:
                    print(f"   Output: Detection boxes available")
                    print(f"   Box format: xyxy coordinates")
                else:
                    print(f"   Output: No detection boxes")
                    
                if hasattr(result, 'names'):
                    print(f"   Available classes: {len(result.names)}")
            else:
                print(f"   ⚠️  No results from prediction")
                
        except Exception as e:
            print(f"   ❌ Dummy prediction failed: {e}")
        
        return {
            'model_name': model_name,
            'classes': model.names if hasattr(model, 'names') else {},
            'file_size_mb': file_size,
            'loaded_successfully': True
        }
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return {
            'model_name': model_name,
            'error': str(e),
            'loaded_successfully': False
        }

def main():
    """Main analysis function"""
    print("🔍 AI-FRSS YOLO MODEL ANALYZER")
    print("="*60)
    
    # Define models to analyze
    models_dir = Path("app/yolo_models")
    
    if not models_dir.exists():
        print(f"❌ Directory tidak ditemukan: {models_dir}")
        return
    
    models_to_analyze = [
        ("intrusion_yolov11.pt", "Intrusion Detection"),
        ("People_yolov8s_trained.pt", "People Detection"),
        ("SecurityThreats_best_gun.pt", "Security Threats"),
        ("vehicle_model_v11.pt", "Vehicle Detection")
    ]
    
    results = []
    
    for model_file, model_desc in models_to_analyze:
        model_path = models_dir / model_file
        result = analyze_yolo_model(str(model_path), f"{model_desc} ({model_file})")
        if result:
            results.append(result)
    
    # Summary
    print(f"\n\n{'='*60}")
    print("📋 SUMMARY ANALYSIS")
    print(f"{'='*60}")
    
    successful_models = [r for r in results if r.get('loaded_successfully', False)]
    failed_models = [r for r in results if not r.get('loaded_successfully', False)]
    
    print(f"✅ Successfully loaded: {len(successful_models)}/{len(results)} models")
    
    if successful_models:
        print(f"\n🏷️  CLASS SUMMARY:")
        for result in successful_models:
            classes = result.get('classes', {})
            print(f"   {result['model_name']}: {len(classes)} classes")
            if classes:
                class_names = list(classes.values())
                print(f"      → {', '.join(class_names)}")
    
    if failed_models:
        print(f"\n❌ FAILED MODELS:")
        for result in failed_models:
            print(f"   {result['model_name']}: {result.get('error', 'Unknown error')}")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    print("1. Verify all models are compatible with current ultralytics version")
    print("2. Test each model with actual images from your use case")
    print("3. Consider model performance vs accuracy trade-offs")
    print("4. Validate class names match your application requirements")
    
    return results

if __name__ == "__main__":
    try:
        results = main()
        print(f"\n🎉 Analysis completed!")
    except KeyboardInterrupt:
        print(f"\n⏹️  Analysis cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
