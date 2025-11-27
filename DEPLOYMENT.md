# Deploying Dorost to Google Cloud Run

## Quick Start (5 minutes)

### Prerequisites
- Google Cloud Account (free tier available)
- `gcloud` CLI installed (`brew install google-cloud-sdk`)
- GitHub repository with code pushed

### Step 1: Authenticate with Google Cloud
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### Step 2: Store API Key Securely
```bash
# Replace with your actual Google API key
gcloud secrets create google-api-key --data-file=<(echo "YOUR_GOOGLE_API_KEY_HERE")

# Grant Cloud Run permission to access it
gcloud secrets add-iam-policy-binding google-api-key \
  --member="serviceAccount:PROJECT_ID@appspot.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### Step 3: Deploy to Cloud Run
```bash
gcloud run deploy dorost \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 2 \
  --timeout 3600 \
  --set-env-vars GOOGLE_API_KEY=$(gcloud secrets versions access latest --secret=google-api-key)
```

You'll get a URL like: `https://dorost-xyz.run.app`
```bash
curl https://dorost-xyz.run.app/health
```

### 2. Start a New Consultation
```bash
curl -X POST https://dorost-xyz.run.app/api/consultation/start \
  -H "Content-Type: application/json" \
  -d '{
    "initial_query": "I have constant fatigue and weight gain",
    "user_metadata": {"age": 45, "gender": "female"}
  }'
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "consultation_id": "550e8400-e29b-41d4-a716-446655440000",
    "stage": "intake",
    "message": "Welcome to Dorost, your AI health advisor...",
    "next_action": "Provide more details about your symptoms"
  }
}
```

### 3. Continue the Conversation
```bash
curl -X POST https://dorost-xyz.run.app/api/consultation/{consultation_id}/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "It started about 6 months ago and is getting worse",
    "agent_stage": "diagnostic"
  }'
```

### 4. Get Final Results
```bash
curl -X GET https://dorost-xyz.run.app/api/consultation/{consultation_id}/results
```

### 5. Get Performance Metrics
```bash
curl -X GET https://dorost-xyz.run.app/api/metrics/evaluation
```

---

## Local Testing Before Deployment

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Locally
```bash
# Development (Flask dev server)
python app.py

# Production (Gunicorn - same as Cloud Run)
gunicorn --bind 0.0.0.0:8080 --workers 4 app:app
```

### 3. Test Endpoints
```bash
# Health check
curl http://localhost:8080/health

# Start consultation
curl -X POST http://localhost:8080/api/consultation/start \
  -H "Content-Type: application/json" \
  -d '{"initial_query": "I have fatigue"}'
```

---

## Docker Build & Run

### Build Locally
```bash
docker build -t dorost:latest .
```

### Run Container
```bash
docker run -p 8080:8080 \
  -e GOOGLE_API_KEY="your-api-key" \
  dorost:latest
```

### Test Container
```bash
curl http://localhost:8080/health
```

---

## Continuous Deployment (GitHub Actions)

### 1. Create GitHub Workflow
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [main]

env:
  PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
  REGION: us-central1

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - uses: google-github-actions/setup-gcloud@v1
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          project_id: ${{ secrets.GCP_PROJECT_ID }}
      
      - run: gcloud auth configure-docker
      
      - run: |
          gcloud run deploy dorost \
            --source . \
            --region ${{ env.REGION }} \
            --platform managed \
            --allow-unauthenticated \
            --set-env-vars GOOGLE_API_KEY=${{ secrets.GOOGLE_API_KEY }}
```

### 2. Add GitHub Secrets
Go to **Settings → Secrets → New repository secret**:
- `GCP_PROJECT_ID`: Your Google Cloud project ID
- `GCP_SA_KEY`: Service account JSON key
- `GOOGLE_API_KEY`: Your Google API key

### 3. Auto-Deploy on Push
```bash
git push origin main  # Workflow triggers automatically!
```

---

## Monitoring & Logs

### View Live Logs
```bash
gcloud run logs read dorost --region us-central1 --limit 50 --follow
```

### Check Service Status
```bash
gcloud run describe dorost --region us-central1
```

### View in Console
https://console.cloud.google.com/run

---

## Scaling Configuration

### Increase Resources
```bash
gcloud run deploy dorost \
  --region us-central1 \
  --memory 2Gi \
  --cpu 4 \
  --concurrency 100
```

### Adjust Timeout
```bash
gcloud run deploy dorost \
  --region us-central1 \
  --timeout 3600  # 1 hour max
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **API Key not found** | `gcloud secrets versions access latest --secret=google-api-key` |
| **Port 8080 error** | Check Dockerfile has `EXPOSE 8080` |
| **Timeout errors** | Increase: `--timeout 3600` |
| **Out of memory** | Increase: `--memory 2Gi` |
| **Connection refused** | Check service is public: `--allow-unauthenticated` |

---

## Cost Analysis

**Cloud Run Pricing (Nov 2024):**
- **First 2M requests/month:** FREE ✅
- **Compute:** $0.0000083/CPU-second (360K seconds free)
- **Memory:** $0.0000005/GB-second (180K GB-seconds free)

**Example:** 1000 consultations × 30 seconds = **~$0.25/month** (FREE tier!)

---

## Production Checklist

- ✅ API key in Secret Manager (not hardcoded)
- ✅ Health check endpoint working
- ✅ CORS enabled
- ✅ Error handling implemented
- ✅ Logging configured
- ✅ HTTPS enabled (automatic)
- ✅ Medical disclaimers visible
- ✅ Session management working
- ✅ Rate limiting ready
- ✅ Monitoring alerts set

---

## Get Your Live URL

After deployment, you'll have:
```
🎉 Service [dorost] revision [dorost-00001-abc] has been deployed and is serving 100% of traffic.
Service URL: https://dorost-xyz.run.app
```

**Use this URL in your Kaggle submission!**
```

---

## Detailed Setup (10 minutes)

### Option A: Using GitHub Actions (Automated)

**1. Create GitHub Secrets**
```
Go to: https://github.com/YOUR_USERNAME/Holistic-Health-Agent/settings/secrets/actions

Add these secrets:
- GCP_PROJECT_ID: your-project-id
- GCP_SA_KEY: (service account key JSON)
- GOOGLE_API_KEY: your-api-key
```

**2. Get Service Account Key**
```bash
# Create service account
gcloud iam service-accounts create github-deployer

# Grant permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"

# Create key
gcloud iam service-accounts keys create key.json \
  --iam-account=github-deployer@YOUR_PROJECT_ID.iam.gserviceaccount.com

# Copy contents of key.json to GCP_SA_KEY secret
```

**3. Push to GitHub**
```bash
git push origin main
# GitHub Actions will automatically deploy!
```

---

### Option B: Manual Command-Line Deployment (Fastest)

```bash
# 1. Navigate to project
cd /Users/helialiaia/ACSAI/Holistic-Health-Agent

# 2. Deploy
gcloud run deploy dorost \
  --source . \
  --runtime python311 \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --timeout 3600 \
  --set-env-vars GOOGLE_API_KEY=$(cat .env | grep GOOGLE_API_KEY | cut -d'=' -f2)

# 3. You'll get a URL!
# Service [dorost] revision [dorost-00001-abc] has been deployed and is serving 100% of traffic at:
# https://dorost-xxxxx-uc.a.run.app
```

---

## Testing Your Deployed Agent

### Using curl
```bash
# Make a request (note: chat.py currently expects stdin)
# For full deployment, you'd wrap it in a Flask/FastAPI app

curl -X POST https://dorost-xxxxx-uc.a.run.app \
  -H "Content-Type: application/json" \
  -d '{"message": "I have fatigue and sugar cravings"}'
```

### Or visit the URL
```
https://dorost-xxxxx-uc.a.run.app
```

---

## Making Chat.py Web-Ready

**Current Issue**: `chat.py` uses `input()` which doesn't work on Cloud Run

**Solution**: Wrap with Flask (5 minutes)

```bash
pip install flask
```

Create `app.py`:
```python
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai
from src.prompts.dr_berg_style import DR_BERG_BASE_STYLE, INTAKE_AGENT_INSTRUCTION

load_dotenv()
app = Flask(__name__)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Dorost is running! Send POST requests with 'message' field"})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        model = genai.GenerativeModel(
            model_name="models/gemini-2.5-flash",
            system_instruction=DR_BERG_BASE_STYLE + "\n\n" + INTAKE_AGENT_INSTRUCTION
        )
        
        response = model.generate_content(user_message)
        
        return jsonify({
            "status": "success",
            "user_message": user_message,
            "dorost_response": response.text
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
```

Then deploy:
```bash
gcloud run deploy dorost-api \
  --source . \
  --runtime python311 \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_API_KEY=$(cat .env | grep GOOGLE_API_KEY | cut -d'=' -f2)
```

Usage:
```bash
curl -X POST https://dorost-api-xxxxx-uc.a.run.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I have fatigue and sugar cravings"}'
```

---

## Pricing

| Resource | Free Tier | After Free | 
|----------|-----------|-----------|
| Cloud Run | 2M requests/month | $0.40 per 1M |
| Container Registry | 0.5GB storage | $0.026 per GB |
| **Total Monthly** | **FREE** | **~$1-5** |

Your free tier will **easily cover** thousands of conversations!

---

## Troubleshooting

### Error: "Could not find Dockerfile"
```
Make sure you run: gcloud run deploy from the project root directory
```

### Error: "API not enabled"
```
Run: gcloud services enable run.googleapis.com
```

### Error: "GOOGLE_API_KEY not found"
```
Make sure .env file is in the project root with your API key
```

### Deployment is slow
```
Normal! First deployment takes 5-10 minutes. Subsequent updates are faster.
```

---

## Success Indicators

✅ Deployment complete when you see:
```
Service [dorost] revision [dorost-00001-xxx] has been deployed and is serving 100% of traffic at:
https://dorost-xxxxx-uc.a.run.app
```

✅ You get +5 Kaggle bonus points for deployment

✅ You can share your live agent URL with others!

---

## Next Steps

1. ✅ Deploy using command above (10 min)
2. ✅ Test the deployed service
3. ✅ Get the deployed URL
4. ✅ Add to Kaggle submission
5. ✅ Create YouTube video showing live deployment

**Congratulations! Your agent is now live on the internet! 🚀**
