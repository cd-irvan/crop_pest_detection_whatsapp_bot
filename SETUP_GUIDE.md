# WhatsApp Bot Setup Guide

Complete guide to set up and deploy the Crop Pest Detection WhatsApp Bot.

## Prerequisites

1. **Python 3.8+** installed
2. **Trained YOLO12n model** (or use pre-trained)
3. **Twilio account** (free trial available)
4. **Public URL** for webhooks (ngrok for testing, or cloud hosting)

## Step 1: Install Dependencies

```bash
cd whatsapp_bot
pip install -r requirements.txt
```

## Step 2: Set Up Twilio

### 2.1 Create Twilio Account

1. Go to https://www.twilio.com/try-twilio
2. Sign up for a free account
3. Verify your phone number
4. You'll get $15 free credit

### 2.2 Get WhatsApp Access

**Option A: Use WhatsApp Sandbox (Free, for testing)**
1. Go to Twilio Console → Messaging → Try it out → Send a WhatsApp message
2. Follow instructions to join the sandbox
3. Send "join [code]" to the sandbox number
4. Use sandbox number: `whatsapp:+14155238886`

**Option B: Get WhatsApp-Enabled Number (Production)**
1. Go to Twilio Console → Phone Numbers → Buy a Number
2. Search for numbers with WhatsApp capability
3. Purchase a number (costs ~$1/month)

### 2.3 Get Your Credentials

1. Go to Twilio Console → Account → API Keys & Tokens
2. Copy your:
   - **Account SID**
   - **Auth Token**

## Step 3: Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your credentials:
```bash
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
MODEL_PATH=models/crop_pest_detection_yolo12n_finetuned.pt
PORT=5000
```

## Step 4: Prepare Model

### Option A: Use Fine-Tuned Model (Recommended)

1. Copy your trained model to the models directory:
```bash
mkdir -p models
cp /path/to/crop_pest_detection_yolo12n_finetuned.pt models/
```

2. Update `MODEL_PATH` in `.env`:
```bash
MODEL_PATH=models/crop_pest_detection_yolo12n_finetuned.pt
```

### Option B: Use Pre-Trained Model

If you don't have a fine-tuned model yet, the bot will automatically use the pre-trained YOLO12n model (less accurate for pests, but works).

## Step 5: Set Up Public URL (for Webhooks)

### Option A: Using ngrok (For Testing)

1. Install ngrok: https://ngrok.com/download
2. Start your Flask server:
```bash
python app.py
```

3. In another terminal, start ngrok:
```bash
ngrok http 5000
```

4. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### Option B: Deploy to Cloud (For Production)

**Heroku:**
```bash
heroku create your-app-name
heroku config:set TWILIO_ACCOUNT_SID=your_sid
heroku config:set TWILIO_AUTH_TOKEN=your_token
git push heroku main
```

**Railway:**
1. Connect your GitHub repo
2. Add environment variables in Railway dashboard
3. Deploy automatically

**DigitalOcean:**
1. Create a Droplet
2. Install dependencies
3. Use systemd to run as a service

## Step 6: Configure Twilio Webhook

1. Go to Twilio Console → Messaging → Settings → WhatsApp Sandbox (or your number)
2. Set **Webhook URL** to: `https://your-url.com/webhook`
3. Set **HTTP Method** to: `POST`
4. Save configuration

## Step 7: Test the Bot

1. Start the Flask server:
```bash
python app.py
```

2. Send a WhatsApp message to your Twilio number:
   - Text: "hi" or "help"
   - Or send an image of a pest

3. You should receive a response!

## Step 8: Production Deployment

### Using Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using systemd (Linux)

Create `/etc/systemd/system/pest-bot.service`:
```ini
[Unit]
Description=WhatsApp Pest Detection Bot
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/whatsapp_bot
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable pest-bot
sudo systemctl start pest-bot
```

## Troubleshooting

### Model Not Loading
- Check that MODEL_PATH is correct
- Ensure model file exists
- Check file permissions

### Webhook Not Receiving Messages
- Verify webhook URL is accessible (test with curl)
- Check Twilio webhook configuration
- Check server logs for errors

### Images Not Processing
- Check image format (JPG, PNG supported)
- Verify model is loaded (check /status endpoint)
- Check server logs for errors

### Twilio Errors
- Verify Account SID and Auth Token
- Check Twilio console for error messages
- Ensure WhatsApp number is properly configured

## Monitoring

### Health Check
```bash
curl http://localhost:5000/status
```

### Check Logs
```bash
tail -f logs/app.log  # if using file logging
```

## Cost Management

- Monitor usage in Twilio Console
- Set up usage alerts
- Consider rate limiting for production

## Security

1. **Never commit `.env` file** to git
2. Use environment variables in production
3. Add rate limiting for production
4. Validate incoming requests
5. Use HTTPS (required by Twilio)

## Next Steps

- Add image caching
- Add user analytics
- Add multi-language support
- Add pest information/details
- Add treatment recommendations

## Support

For issues:
1. Check server logs
2. Check Twilio console logs
3. Test model separately
4. Verify webhook URL is accessible

