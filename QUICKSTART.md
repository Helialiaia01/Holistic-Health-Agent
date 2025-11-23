# 🚀 Quick Start Guide

## See Your Agent Working in 3 Steps!

### Step 1: Install Dependencies
```bash
cd ~/holistic-health-agent
pip install -r requirements.txt
```

### Step 2: Setup Your API Key
1. Copy the template:
   ```bash
   cp .env.template .env
   ```

2. Edit `.env` and add your Google API key:
   ```bash
   nano .env
   ```
   
   Replace `your-api-key-here` with your actual key from: https://aistudio.google.com/apikey

3. Save and exit (Ctrl+X, then Y, then Enter)

### Step 3: Run the Demo!
```bash
python demo.py
```

You'll see a **simulated conversation** showing:
- ✅ The Intake Agent asking questions naturally
- ✅ Gemini powering the responses
- ✅ The agent remembering context from previous messages
- ✅ Conversational, empathetic tone

---

## Push to GitHub

### Option A: Using GitHub CLI (if you have it)
```bash
gh repo create holistic-health-agent --public --description "AI Multi-Agent Health Assistant using Google ADK" --source=. --remote=origin --push
```

### Option B: Manual (Web + Command Line)
1. Go to: https://github.com/new

2. Create repo:
   - Name: `holistic-health-agent`
   - Description: `AI Multi-Agent Health Assistant using Google ADK`
   - Public
   - Don't initialize with README (we already have one!)

3. Push your code:
   ```bash
   cd ~/holistic-health-agent
   git remote add origin https://github.com/YOUR_USERNAME/holistic-health-agent.git
   git push -u origin main
   ```

Replace `YOUR_USERNAME` with your actual GitHub username!

---

## What's Next?

After you see the demo working, we'll build:

1. **Analyzer Agent** (1 hour) - Identifies which of the 20 health patterns match
2. **Reasoning Agent** (1 hour) - Explains WHY you have these issues
3. **Recommender Agent** (1 hour) - Gives personalized supplement & lifestyle advice
4. **USDA Integration** (45 mins) - Real nutrient data for accurate recommendations

**Total time remaining:** ~4 hours of building

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'google.adk'"
→ Run: `pip install -r requirements.txt`

### "API key not valid"
→ Check your .env file has `GOOGLE_API_KEY=sk-...` (no quotes needed)

### "Permission denied"
→ Run: `chmod +x demo.py`

Need help? Just ask! 😊
