from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image
import io
from typing import List, Dict, Any

from services.yolo_service import yolo_manager
from services.image_service import image_processor

router = APIRouter(prefix="/detection", tags=["Object Detection"])

@router.get("/models")
async def get_available_models():
    """Dapatkan daftar model YOLO yang tersedia"""
    return {
        "models": yolo_manager.get_available_models(),
        "loaded_models": list(yolo_manager.loaded_models.keys())
    }

@router.post("/predict/{model_name}")
async def detect_objects(
    model_name: str,
    file: UploadFile = File(...),
    confidence: float = 0.5,
    draw_boxes: bool = True,
    return_image: bool = True
):
    """
    Deteksi objek menggunakan model YOLO tertentu
    
    - **model_name**: intrusion, people, security_threats, vehicle
    - **confidence**: threshold confidence (0.0-1.0)
    - **draw_boxes**: apakah menggambar bounding boxes
    - **return_image**: apakah mengembalikan gambar dengan boxes
    """
    
    # Validasi file
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File harus berupa gambar")
    
    try:
        # Load dan process image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Resize jika terlalu besar
        image = image_processor.resize_image(image)
        
        # Predict menggunakan YOLO
        detections = yolo_manager.predict(
            model_name=model_name,
            image=image,
            conf=confidence
        )
        
        response_data = {
            "model_used": model_name,
            "image_size": {"width": image.width, "height": image.height},
            "detections_count": len(detections),
            "detections": detections
        }
        
        if return_image and draw_boxes:
            # Draw bounding boxes
            image_with_boxes = image_processor.draw_detections(image, detections)
            
            # Convert ke bytes untuk response
            buf = io.BytesIO()
            image_with_boxes.save(buf, format="PNG")
            buf.seek(0)
            
            return StreamingResponse(
                buf, 
                media_type="image/png",
                headers={"X-Detection-Data": str(response_data)}
            )
        else:
            return response_data
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during detection: {str(e)}")

@router.post("/batch-predict/{model_name}")
async def batch_detect_objects(
    model_name: str,
    files: List[UploadFile] = File(...),
    confidence: float = 0.5
):
    """Deteksi objek pada multiple gambar sekaligus"""
    
    if len(files) > 10:  # Limit untuk mencegah overload
        raise HTTPException(status_code=400, detail="Maksimal 10 gambar per request")
    
    results = []
    
    for i, file in enumerate(files):
        if not file.content_type.startswith("image/"):
            results.append({
                "file_index": i,
                "filename": file.filename,
                "error": "File bukan gambar"
            })
            continue
        
        try:
            # Process image
            image_bytes = await file.read()
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            image = image_processor.resize_image(image)
            
            # Predict
            detections = yolo_manager.predict(
                model_name=model_name,
                image=image,
                conf=confidence
            )
            
            results.append({
                "file_index": i,
                "filename": file.filename,
                "image_size": {"width": image.width, "height": image.height},
                "detections_count": len(detections),
                "detections": detections
            })
            
        except Exception as e:
            results.append({
                "file_index": i,
                "filename": file.filename,
                "error": str(e)
            })
    
    return {
        "model_used": model_name,
        "total_files": len(files),
        "results": results
    }

@router.post("/crop-detections/{model_name}")
async def crop_detected_objects(
    model_name: str,
    file: UploadFile = File(...),
    confidence: float = 0.5
):
    """Crop objek yang terdeteksi dan kembalikan sebagai gambar terpisah"""
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File harus berupa gambar")
    
    try:
        # Process image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image_processor.resize_image(image)
        
        # Predict
        detections = yolo_manager.predict(
            model_name=model_name,
            image=image,
            conf=confidence
        )
        
        if not detections:
            return {"message": "Tidak ada objek yang terdeteksi", "crops": []}
        
        # Crop detected objects
        crops = image_processor.crop_detections(image, detections)
        
        # Convert crops ke base64
        crop_data = []
        for i, (crop, detection) in enumerate(zip(crops, detections)):
            crop_b64 = image_processor.image_to_base64(crop)
            crop_data.append({
                "index": i,
                "class_name": detection["class_name"],
                "confidence": detection["confidence"],
                "image_base64": crop_b64
            })
        
        return {
            "model_used": model_name,
            "total_crops": len(crop_data),
            "crops": crop_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during cropping: {str(e)}")

@router.post("/predict-all")
async def detect_all_models(
    file: UploadFile = File(...),
    confidence: float = 0.5,
    draw_boxes: bool = True,
    return_image: bool = True,
    combine_results: bool = False
):
    """
    Deteksi objek menggunakan SEMUA model YOLO sekaligus
    
    - **confidence**: threshold confidence (0.0-1.0)
    - **draw_boxes**: apakah menggambar bounding boxes
    - **return_image**: apakah mengembalikan gambar dengan boxes
    - **combine_results**: apakah menggabungkan hasil semua model
    """
    
    # Validasi file
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File harus berupa gambar")
    
    try:
        # Load dan process image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Resize jika terlalu besar
        image = image_processor.resize_image(image)
        
        # Predict menggunakan semua model YOLO
        multi_results = yolo_manager.predict_multi_model(
            image=image,
            conf=confidence
        )
        
        # Hitung total deteksi
        total_detections = sum(len(detections) for detections in multi_results.values())
        
        response_data = {
            "total_models_used": len(multi_results),
            "image_size": {"width": image.width, "height": image.height},
            "total_detections": total_detections,
            "results_by_model": multi_results
        }
        
        # Jika diminta, gabungkan hasil
        if combine_results:
            combined_detections = yolo_manager.get_combined_detections(multi_results)
            response_data["combined_detections"] = combined_detections
        
        if return_image and draw_boxes and total_detections > 0:
            # Draw bounding boxes dari semua model
            if combine_results:
                detections_to_draw = yolo_manager.get_combined_detections(multi_results)
            else:
                # Draw semua deteksi dengan warna berbeda per model
                detections_to_draw = []
                colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
                color_map = {}
                for i, (model_name, detections) in enumerate(multi_results.items()):
                    color_map[model_name] = colors[i % len(colors)]
                    for detection in detections:
                        detection["color"] = color_map[model_name]
                        detection["source_model"] = model_name
                        detections_to_draw.append(detection)
            
            # Draw bounding boxes
            image_with_boxes = image_processor.draw_detections(image, detections_to_draw)
            
            # Convert ke bytes untuk response
            buf = io.BytesIO()
            image_with_boxes.save(buf, format="PNG")
            buf.seek(0)
            
            return StreamingResponse(
                buf, 
                media_type="image/png",
                headers={"X-Detection-Data": str(response_data)}
            )
        else:
            return response_data
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during multi-model detection: {str(e)}")

@router.post("/compare-models")
async def compare_models(
    file: UploadFile = File(...),
    confidence: float = 0.5
):
    """
    Bandingkan performa semua model pada gambar yang sama
    """
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File harus berupa gambar")
    
    try:
        # Process image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image_processor.resize_image(image)
        
        # Get results from all models
        multi_results = yolo_manager.predict_multi_model(
            image=image,
            conf=confidence
        )
        
        # Create comparison summary
        comparison = {
            "image_info": {
                "size": {"width": image.width, "height": image.height},
                "confidence_threshold": confidence
            },
            "model_comparison": []
        }
        
        for model_name, detections in multi_results.items():
            model_info = yolo_manager.model_configs[model_name]
            
            # Calculate statistics
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
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during model comparison: {str(e)}")
