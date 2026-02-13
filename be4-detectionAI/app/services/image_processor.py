import cv2
import numpy as np
import os
import time
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self):
        self.seen_hashes = [] # List of (timestamp, hash)
        # Pruning config
        self.hash_retention_seconds = 60 * 5 # Keep hashes for 5 minutes

    def crop_and_save(self, frame, bbox):
        """
        Crops the image based on bbox, checks for duplicates, and saves if unique.
        Returns: (is_unique, file_path)
        """
        x1, y1, x2, y2 = bbox
        
        # Ensure coordinates are within frame bounds
        h, w = frame.shape[:2]
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)
        
        if x1 >= x2 or y1 >= y2:
            logger.warning(f"Invalid bbox: {bbox}")
            return False, None
            
        crop = frame[y1:y2, x1:x2]
        
        if crop.size == 0:
            logger.warning("Empty crop")
            return False, None

        # Check for duplicates
        if self._is_duplicate(crop):
            # logger.info("Duplicate detection skipped") 
            # Commented out to avoid spam, but useful for debug
            return False, None
            
        # Save crop
        timestamp = int(time.time() * 1000)
        filename = f"person_{timestamp}.jpg"
        filepath = os.path.join(settings.CROP_DIR, filename)
        
        try:
            success = cv2.imwrite(filepath, crop)
            if success:
                # Add to seen hashes
                self._add_hash(crop)
                logger.info(f"New unique person detected! Saved to {filepath}")
                return True, filepath
            else:
                logger.error(f"Failed to write image to {filepath}")
                return False, None
        except Exception as e:
            logger.error(f"Error saving crop: {e}")
            return False, None

    def _compute_hash(self, image):
        """
        Compute a perceptual hash (dHash) of the image.
        """
        try:
            # Resize to 9x8 for dHash
            resized = cv2.resize(image, (9, 8))
            # Convert to grayscale
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            
            # Compute differences between adjacent pixels
            diff = gray[:, 1:] > gray[:, :-1]
            
            # Convert to integer hash
            return sum([2**i for (i, v) in enumerate(diff.flatten()) if v])
        except Exception as e:
            logger.error(f"Hash computation error: {e}")
            return 0

    def _is_duplicate(self, image):
        """
        Check if the image is similar to recently seen images.
        """
        current_hash = self._compute_hash(image)
        current_time = time.time()
        
        # Prune old hashes
        self.seen_hashes = [(t, h) for t, h in self.seen_hashes 
                           if current_time - t < self.hash_retention_seconds]
        
        for _, saved_hash in self.seen_hashes:
            # Hamming distance
            distance = bin(current_hash ^ saved_hash).count('1')
            # Threshold: 0 means identical, < 5 is usually very similar for 64-bit hash
            if distance < 10: # Increased threshold to 10 for testing strictness (Wait, HIGHER means MORE tolerant to diffs)
                # If distance is small, images are similar.
                # Requirement: "If ... visually similar ... DO NOT save"
                # So we want to return True if distance < threshold.
                
                # If I want to see MORE alerts, I should DECREASE the threshold?
                # No.
                # Distance 0 = Identical.
                # Distance 64 = Completely different.
                
                # If distance < 5: return True (Duplicate)
                # If distance is 6: return False (Unique)
                
                # If I want FEWER duplicates (more uniques), I should LOWER the threshold.
                # e.g. Threshold 2 means only VERY similar images are duplicates.
                
                # If I want FEWER alerts (more strict deduplication), I RAISE the threshold.
                # e.g. Threshold 10 means somewhat similar images are duplicates.
                
                # Since the user says "Live Alerts still empty", it means everything is being treated as duplicate?
                # OR, nothing is being saved.
                
                # If I haven't saved ANYTHING yet, `seen_hashes` is empty. The first one SHOULD be unique.
                # So `_is_duplicate` returns False for the first one.
                
                return True
                
        return False

    def _add_hash(self, image):
        h = self._compute_hash(image)
        self.seen_hashes.append((time.time(), h))
