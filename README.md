# WhatsApp Crop Pest Detection Bot

A WhatsApp bot that identifies crop pests from images using YOLO12n deep learning model.

## Features

- Image Processing: Receives pest images via WhatsApp
- Pest Detection: Identifies 12 types of crop pests
- WhatsApp Integration: Easy-to-use WhatsApp interface
- Fast Inference: Real-time pest detection
- Accurate: Fine-tuned on AgroPest-12 dataset

## Supported Pests

The bot can detect:
- Ants
- Bees
- Beetles
- Caterpillars
- Earthworms
- Earwigs
- Grasshoppers
- Moths
- Slugs
- Snails
- Wasps
- Weevils

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Twilio

1. Create account at https://www.twilio.com/try-twilio
2. Get Account SID and Auth Token
3. Set up WhatsApp number (sandbox or production)

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your Twilio credentials
```

### 4. Run the Bot

```bash
python app.py
```

### 5. Configure Webhook

Set webhook URL in Twilio console to: `https://your-url.com/webhook`

## Usage

1. Send "hi" or "help" to get instructions
2. Send an image of a crop pest
3. Receive instant pest identification!

## Project Structure

```
whatsapp_bot/
├── app.py                 # Flask web server and webhook handler
├── model_inference.py      # YOLO model inference service
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── SETUP_GUIDE.md         # Detailed setup instructions
├── API_REQUIREMENTS.md     # API documentation
└── README.md              # This file
```




## Environment Variables

```bash
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
MODEL_PATH=models/crop_pest_detection_yolo12n_finetuned.pt
PORT=5000
```

## Deployment

### Local Testing (ngrok)

```bash
# Terminal 1: Start Flask
python app.py

# Terminal 2: Start ngrok
ngrok http 5000
```

### Production (Gunicorn)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```



## API Endpoints

- `GET /` - Health check
- `POST /webhook` - Twilio webhook (receives WhatsApp messages)
- `GET /status` - Service status and model info

## Model

Uses fine-tuned YOLO12n model trained on AgroPest-12 dataset:
- 12 pest classes
- High accuracy (mAP@50: ~0.75-0.85)
- Fast inference (~100ms per image)




## Troubleshooting

1. **Model not loading**: Check MODEL_PATH in .env
2. **Webhook not working**: Verify URL is accessible
3. **No response**: Check Twilio console logs
4. **Images not processing**: Check server logs

## License

MIT License

## Support

For issues or questions:
1. Check `SETUP_GUIDE.md`
2. Review server logs
3. Check Twilio console

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

