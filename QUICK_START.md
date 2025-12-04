# Quick Start Guide

Get your WhatsApp bot running in 5 minutes!

## Prerequisites

- Python 3.8+
- Twilio account (free trial: https://www.twilio.com/try-twilio)

## Step 1: Install Dependencies

```bash
cd whatsapp_bot
pip install -r requirements.txt
```

## Step 2: Get Twilio Credentials

1. Sign up at https://www.twilio.com/try-twilio
2. Go to Console → Account → API Keys
3. Copy:
   - Account SID
   - Auth Token

## Step 3: Configure Environment

```bash
cp .env.example .env
# Edit .env and add your Twilio credentials
```

Edit `.env`:
```bash
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

## Step 4: Set Up WhatsApp Sandbox

1. Go to Twilio Console → Messaging → Try it out → Send a WhatsApp message
2. Follow instructions to join sandbox
3. Send "join [code]" to `+1 415 523 8886`

## Step 5: Start Server (Local Testing)

### Option A: Using ngrok

```bash
# Terminal 1: Start Flask
python app.py

# Terminal 2: Start ngrok
ngrok http 5000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### Option B: Direct (if you have public IP)

```bash
python app.py
```

## Step 6: Configure Twilio Webhook

1. Go to Twilio Console → Messaging → Settings → WhatsApp Sandbox
2. Set **Webhook URL**: `https://your-ngrok-url.ngrok.io/webhook`
3. Set **HTTP Method**: `POST`
4. Save

## Step 7: Test!

1. Send a WhatsApp message to your Twilio number:
   - Text: "hi" or "help"
   - Or send an image of a pest

2. You should receive a response! 🎉

## Troubleshooting

**No response?**
- Check server logs
- Verify webhook URL is accessible
- Check Twilio console for errors

**Model not loading?**
- Check MODEL_PATH in .env
- Model will auto-download if not found (uses pre-trained YOLO12n)

**Webhook not working?**
- Ensure URL is HTTPS (required by Twilio)
- Test URL with: `curl https://your-url.com/status`

## Next Steps

- Deploy to production (Heroku, Railway, etc.)
- Add your fine-tuned model
- Customize responses
- Add analytics

See `SETUP_GUIDE.md` for detailed instructions!

