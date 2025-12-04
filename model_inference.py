"""
Pest Detection Model Inference Service
Handles loading and running inference with the YOLO12n model
"""

import os
import cv2
import numpy as np
from ultralytics import YOLO
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PestDetectionModel:
    """Wrapper class for YOLO12n pest detection model"""
    
    def __init__(self, model_path):
        """
        Initialize the pest detection model
        
        Args:
            model_path: Path to the trained YOLO model (.pt file)
        """
        self.model_path = model_path
        self.model = None
        self.class_names = [
            "Ants", "Bees", "Beetles", "Caterpillars", "Earthworms", "Earwigs",
            "Grasshoppers", "Moths", "Slugs", "Snails", "Wasps", "Weevils"
        ]
        
        self._load_model()
    
    def _load_model(self):
        """Load the YOLO model"""
        try:
            # Check if model file exists
            if not os.path.exists(self.model_path):
                logger.warning(f"Model file not found at {self.model_path}")
                logger.info("Attempting to use pre-trained YOLO12n model...")
                # Fallback to pre-trained model
                self.model = YOLO("yolo12n.pt")
                logger.warning("Using pre-trained YOLO12n (not fine-tuned on AgroPest-12)")
            else:
                logger.info(f"Loading model from {self.model_path}")
                self.model = YOLO(self.model_path)
                logger.info("Model loaded successfully!")
            
            # Set model to evaluation mode
            self.model.model.eval()
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def detect(self, image, confidence_threshold=0.25):
        """
        Detect pests in an image
        
        Args:
            image: numpy array of image (BGR or RGB)
            confidence_threshold: Minimum confidence for detections (default: 0.25)
        
        Returns:
            List of detections, each with:
            - 'class': class name (string)
            - 'confidence': confidence score (float)
            - 'bbox': bounding box [x1, y1, x2, y2] (list)
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        try:
            # Ensure image is in correct format
            if isinstance(image, np.ndarray):
                # If image is RGB, convert to BGR for OpenCV
                if len(image.shape) == 3 and image.shape[2] == 3:
                    # Check if it's RGB (common from PIL)
                    image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                else:
                    image_bgr = image
            else:
                raise ValueError("Image must be a numpy array")
            
            # Run inference
            results = self.model.predict(
                image_bgr,
                conf=confidence_threshold,
                imgsz=640,
                verbose=False
            )
            
            # Parse results
            detections = []
            if len(results) > 0:
                result = results[0]
                
                # Get boxes, scores, and classes
                boxes = result.boxes
                
                for i in range(len(boxes)):
                    # Get box coordinates
                    box = boxes.xyxy[i].cpu().numpy()  # [x1, y1, x2, y2]
                    
                    # Get class and confidence
                    cls_id = int(boxes.cls[i].cpu().numpy())
                    confidence = float(boxes.conf[i].cpu().numpy())
                    
                    # Get class name
                    if cls_id < len(self.class_names):
                        class_name = self.class_names[cls_id]
                    else:
                        class_name = f"Class_{cls_id}"
                    
                    detections.append({
                        'class': class_name,
                        'confidence': confidence,
                        'bbox': box.tolist()
                    })
            
            # Sort by confidence (highest first)
            detections.sort(key=lambda x: x['confidence'], reverse=True)
            
            return detections
        
        except Exception as e:
            logger.error(f"Error during detection: {e}")
            raise
    
    def detect_from_path(self, image_path, confidence_threshold=0.25):
        """
        Detect pests from an image file path
        
        Args:
            image_path: Path to image file
            confidence_threshold: Minimum confidence for detections
        
        Returns:
            List of detections
        """
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image from {image_path}")
        
        return self.detect(image, confidence_threshold)
    
    def get_model_info(self):
        """Get information about the loaded model"""
        if self.model is None:
            return {"status": "not_loaded"}
        
        return {
            "status": "loaded",
            "model_path": self.model_path,
            "num_classes": len(self.class_names),
            "classes": self.class_names
        }

