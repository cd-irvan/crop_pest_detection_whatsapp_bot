"""
WhatsApp Bot for Crop Pest Detection
Handles incoming WhatsApp messages, processes images, and returns pest detection results
"""

from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
import requests
import cv2
import numpy as np
from PIL import Image
import io
import logging
from pathlib import Path
import time

# Import model inference
from model_inference import PestDetectionModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Load environment variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')  # Sandbox number
MODEL_PATH = os.getenv('MODEL_PATH', 'models/crop_pest_detection_yolo12n_finetuned.pt')

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Initialize pest detection model
logger.info("Loading pest detection model...")
try:
    pest_model = PestDetectionModel(MODEL_PATH)
    logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    pest_model = None

# Class names for AgroPest-12
CLASS_NAMES = [
    "Ants", "Bees", "Beetles", "Caterpillars", "Earthworms", "Earwigs",
    "Grasshoppers", "Moths", "Slugs", "Snails", "Wasps", "Weevils"
]


def download_image_from_url(url):
    """Download image from Twilio media URL and return as numpy array.

    Twilio-hosted media requires HTTP Basic Auth using the Account SID and Auth Token,
    so we include those credentials in the request.
    """
    try:
        # Use Twilio credentials for authenticated media download
        auth = None
        if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
            auth = (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        response = requests.get(url, timeout=10, auth=auth)
        response.raise_for_status()
        
        # Convert to PIL Image
        image = Image.open(io.BytesIO(response.content))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to numpy array
        img_array = np.array(image)
        return img_array
    except Exception as e:
        logger.error(f"Error downloading image: {e}")
        return None


def format_detection_results(results):
    """Format detection results into a readable message"""
    if not results or len(results) == 0:
        return "❌ No pests detected in the image. Please try another photo."
    
    message = "🐛 *Pest Detection Results:*\n\n"
    
    # Group detections by class
    detections_by_class = {}
    for detection in results:
        class_name = detection['class']
        confidence = detection['confidence']
        
        if class_name not in detections_by_class:
            detections_by_class[class_name] = []
        detections_by_class[class_name].append(confidence)
    
    # Format message
    for class_name, confidences in detections_by_class.items():
        count = len(confidences)
        avg_confidence = sum(confidences) / len(confidences)
        confidence_pct = avg_confidence * 100
        
        message += f"• *{class_name}*: {count} detected"
        message += f" ({confidence_pct:.1f}% confidence)\n"
    
    message += "\n📸 Send another image to detect more pests!"
    return message


@app.route('/')
def home():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "WhatsApp Pest Detection Bot",
        "model_loaded": pest_model is not None
    }, 200


@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming WhatsApp messages"""
    try:
        # Get incoming message data
        incoming_msg = request.values.get('Body', '').strip()
        incoming_num = request.values.get('From', '')
        num_media = int(request.values.get('NumMedia', 0))
        
        logger.info(f"Received message from {incoming_num}: {incoming_msg}")
        logger.info(f"Number of media files: {num_media}")
        
        # Create response
        resp = MessagingResponse()
        
        # Check if message contains media (image)
        if num_media > 0:
            # Get image URL
            media_url = request.values.get('MediaUrl0', '')
            media_content_type = request.values.get('MediaContentType0', '')
            
            logger.info(f"Received image: {media_url}")
            logger.info(f"Content type: {media_content_type}")
            
            # Check if it's an image
            if media_content_type and media_content_type.startswith('image/'):
                # Download and process image
                if pest_model is None:
                    resp.message("❌ Model not loaded. Please check server configuration.")
                    return str(resp)
                
                # Download image
                logger.info("Downloading image...")
                image = download_image_from_url(media_url)
                
                if image is None:
                    resp.message("❌ Could not download image. Please try again.")
                    return str(resp)
                
                # Run inference
                logger.info("Running pest detection...")
                results = pest_model.detect(image)
                
                # Format and send response
                response_message = format_detection_results(results)
                resp.message(response_message)
                
                logger.info(f"Detection complete. Found {len(results)} pests.")
            else:
                resp.message("❌ Please send an image file (JPG, PNG, etc.)")
        else:
            # Text message - provide instructions
            if incoming_msg.lower() in ['hi', 'hello', 'start', 'help']:
                welcome_msg = (
                    "👋 *Welcome to Crop Pest Detection Bot!*\n\n"
                    "📸 *How to use:*\n"
                    "1. Take a photo of a crop pest or insect\n"
                    "2. Send the image to this number\n"
                    "3. Get instant pest identification!\n\n"
                    "🔍 *Supported pests:*\n"
                    "Ants, Bees, Beetles, Caterpillars, Earthworms, Earwigs, "
                    "Grasshoppers, Moths, Slugs, Snails, Wasps, Weevils\n\n"
                    "Send an image to get started! 🐛"
                )
                resp.message(welcome_msg)
            else:
                resp.message(
                    "📸 Please send an image of a crop pest for identification.\n\n"
                    "Type 'help' for instructions."
                )
        
        return str(resp)
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        resp = MessagingResponse()
        resp.message("❌ An error occurred. Please try again later.")
        return str(resp)


@app.route('/status', methods=['GET'])
def status():
    """Status endpoint for monitoring"""
    return {
        "status": "online",
        "model_loaded": pest_model is not None,
        "model_path": MODEL_PATH if pest_model else None,
        "timestamp": time.time()
    }, 200


if __name__ == '__main__':
    # Check required environment variables
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        logger.error("Missing Twilio credentials. Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN")
        exit(1)
    
    # Run Flask app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

