from PIL import Image, ImageDraw, ImageFont
import io
import base64
from typing import List, Dict, Any, Tuple
import numpy as np

class ImageProcessor:
    """Utility untuk processing gambar dan visualisasi"""
    
    def __init__(self):
        self.colors = [
            (255, 0, 0), # Red
            (0, 255, 0), # Green 
            (0, 0, 255), # Blue
            (255, 255, 0), # Yellow
            (255, 0, 255), # Magenta
            (0, 255, 255), # Cyan
            (128, 0, 128), # Purple
            (255, 165, 0), # Orange
        ]
    
    def base64_to_image(self, base64_string: str) -> Image.Image:
        """Convert base64 string ke PIL Image"""
        try:
            img_bytes = base64.b64decode(base64_string)
            image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
            return image
        except Exception as e:
            raise ValueError(f"Error converting base64 to image: {e}")
    
    def image_to_base64(self, image: Image.Image, format: str = "PNG") -> str:
        """Convert PIL Image ke base64 string"""
        try:
            buf = io.BytesIO()
            image.save(buf, format=format)
            buf.seek(0)
            img_b64 = base64.b64encode(buf.read()).decode("utf-8")
            return img_b64
        except Exception as e:
            raise ValueError(f"Error converting image to base64: {e}")
    
    def draw_detections(self, image: Image.Image, detections: List[Dict[str, Any]], 
                       draw_labels: bool = True, line_width: int = 3) -> Image.Image:
        """Draw bounding boxes dan labels pada gambar"""
        draw = ImageDraw.Draw(image)
        
        try:
            # Try to load a font, fallback to default if not available
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        for i, detection in enumerate(detections):
            bbox = detection["bbox"] # [x1, y1, x2, y2]
            confidence = detection["confidence"]
            class_name = detection["class_name"]
            
            # Get color for this class
            color = self.colors[i % len(self.colors)]
            
            # Draw bounding box
            draw.rectangle(bbox, outline=color, width=line_width)
            
            if draw_labels:
                # Prepare label text
                label = f"{class_name}: {confidence:.2f}"
                
                # Get text size
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
    
    def resize_image(self, image: Image.Image, max_width: int = 1280, max_height: int = 720) -> Image.Image:
        """Resize gambar dengan mempertahankan aspect ratio"""
        width, height = image.size
        
        # Calculate scaling factor
        scale_w = max_width / width
        scale_h = max_height / height
        scale = min(scale_w, scale_h, 1.0) # Don't upscale
        
        if scale < 1.0:
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        return image
    
    def crop_detections(self, image: Image.Image, detections: List[Dict[str, Any]]) -> List[Image.Image]:
        """Crop deteksi objek dari gambar"""
        crops = []
        
        for detection in detections:
            bbox = detection["bbox"] # [x1, y1, x2, y2]
            
            # Add some padding
            padding = 10
            x1 = max(0, int(bbox[0]) - padding)
            y1 = max(0, int(bbox[1]) - padding)
            x2 = min(image.width, int(bbox[2]) + padding)
            y2 = min(image.height, int(bbox[3]) + padding)
            
            crop = image.crop((x1, y1, x2, y2))
            crops.append(crop)
        
        return crops

# Global instance
image_processor = ImageProcessor()
