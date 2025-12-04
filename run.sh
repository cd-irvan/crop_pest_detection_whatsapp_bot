#!/bin/bash

# WhatsApp Bot Startup Script

echo "Starting WhatsApp Pest Detection Bot..."

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "Warning: .env file not found. Using defaults."
fi

# Check if model exists
if [ ! -f "$MODEL_PATH" ] && [ "$MODEL_PATH" != "models/crop_pest_detection_yolo12n_finetuned.pt" ]; then
    echo "Warning: Model file not found at $MODEL_PATH"
    echo "Bot will use pre-trained YOLO12n model"
fi

# Run the Flask app
if command -v gunicorn &> /dev/null; then
    echo "Starting with Gunicorn..."
    gunicorn -w 4 -b 0.0.0.0:${PORT:-5000} app:app
else
    echo "Starting with Flask development server..."
    python app.py
fi

