# WhatsApp Bot API Requirements

## Required APIs and Services

### 1. **Twilio API for WhatsApp** (Recommended)
- **Service**: Twilio WhatsApp API
- **Purpose**: Send and receive WhatsApp messages, handle media (images)
- **Cost**: Pay-as-you-go pricing (~$0.005 per message)
- **Setup**: 
  - Sign up at https://www.twilio.com/
  - Get a Twilio phone number with WhatsApp enabled
  - Get Account SID and Auth Token
- **Why Twilio**: 
  - Easy to set up
  - Excellent documentation
  - Supports media messages
  - Webhook-based architecture
  - Free trial available

### 2. **Alternative: WhatsApp Business API (Meta)**
- **Service**: Meta WhatsApp Business API
- **Purpose**: Official WhatsApp Business solution
- **Cost**: More complex pricing, requires business verification
- **Setup**: More complex, requires business verification
- **Why not recommended**: More complex setup, better for large-scale businesses

### 3. **Alternative: WhatsApp Cloud API**
- **Service**: Meta's Cloud API
- **Purpose**: WhatsApp messaging via Meta's infrastructure
- **Cost**: Free tier available, then pay-per-message
- **Setup**: Requires Meta Business Account
- **Why not recommended**: Newer service, less documentation

## Recommended Solution: Twilio

For this project, **Twilio is the best choice** because:
- ✅ Simple setup (5 minutes)
- ✅ Great Python SDK
- ✅ Handles image downloads automatically
- ✅ Webhook-based (perfect for Flask)
- ✅ Free trial with $15 credit
- ✅ Production-ready

## What You Need to Get Started

1. **Twilio Account** (free trial)
   - Sign up: https://www.twilio.com/try-twilio
   - Get Account SID
   - Get Auth Token
   - Request WhatsApp sandbox access (or get a WhatsApp-enabled number)

2. **Public URL for Webhooks**
   - Your Flask server needs to be accessible from the internet
   - Options:
     - **ngrok** (for testing): Free tunnel to localhost
     - **Heroku**: Free tier available
     - **Railway**: Easy deployment
     - **AWS/GCP/Azure**: Production hosting
     - **DigitalOcean**: Simple VPS

3. **Trained Model File**
   - Your fine-tuned YOLO12n model: `crop_pest_detection_yolo12n_finetuned.pt`
   - Or use the pre-trained model if fine-tuned model not available yet

## Cost Estimate

### Twilio WhatsApp Pricing (as of 2024):
- **Inbound messages**: $0.005 per message
- **Outbound messages**: $0.005 per message
- **Media messages**: $0.01 per message
- **Free trial**: $15 credit (good for ~1,500 messages)

### Example Monthly Cost:
- 1,000 users sending 1 image each = 1,000 messages
- Cost: ~$5-10/month (depending on media)

## Setup Steps Overview

1. Create Twilio account
2. Get WhatsApp-enabled number (or use sandbox)
3. Configure webhook URL in Twilio console
4. Deploy Flask server
5. Test with WhatsApp

## Next Steps

See `SETUP_GUIDE.md` for detailed setup instructions.

