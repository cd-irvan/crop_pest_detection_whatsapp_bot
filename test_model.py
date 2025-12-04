"""
Test script for the pest detection model
Run this to verify the model is working correctly
"""

import os
import sys
from model_inference import PestDetectionModel
import cv2
import numpy as np

def test_model():
    """Test the pest detection model"""
    
    # Get model path
    model_path = os.getenv('MODEL_PATH', 'models/crop_pest_detection_yolo12n_finetuned.pt')
    
    print("=" * 60)
    print("Testing Pest Detection Model")
    print("=" * 60)
    
    # Load model
    print(f"\n1. Loading model from: {model_path}")
    try:
        model = PestDetectionModel(model_path)
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False
    
    # Get model info
    print("\n2. Model Information:")
    info = model.get_model_info()
    for key, value in info.items():
        print(f"   {key}: {value}")
    
    # Test with a sample image (if provided)
    if len(sys.argv) > 1:
        test_image_path = sys.argv[1]
        print(f"\n3. Testing with image: {test_image_path}")
        
        if not os.path.exists(test_image_path):
            print(f"❌ Image not found: {test_image_path}")
            return False
        
        try:
            # Run detection
            detections = model.detect_from_path(test_image_path)
            
            print(f"\n✅ Detection complete!")
            print(f"   Found {len(detections)} pest(s):\n")
            
            for i, detection in enumerate(detections, 1):
                print(f"   {i}. {detection['class']}")
                print(f"      Confidence: {detection['confidence']*100:.1f}%")
                print(f"      Bounding box: {detection['bbox']}")
                print()
            
            return True
            
        except Exception as e:
            print(f"❌ Error during detection: {e}")
            import traceback
            traceback.print_exc()
            return False
    else:
        print("\n3. No test image provided.")
        print("   Usage: python test_model.py <path_to_image>")
        print("   Example: python test_model.py test_image.jpg")
        return True

if __name__ == '__main__':
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    success = test_model()
    sys.exit(0 if success else 1)

