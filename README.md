# Holistic Health Agent - DOROST

An AI system that helps people figure out **which medical specialist to see** based on their symptoms, powered by multi-agent AI and Dr. Berg's health education methodology.

**Submission:** Google AI Agents Intensive Capstone - Healthcare Track

- **Kaggle Competition:** https://www.kaggle.com/competitions/agents-intensive-capstone-project
- **Program Info:** https://rsvp.withgoogle.com/events/google-ai-agents-intensive_2025

## The Problem

You're tired, have brain fog, and sugar cravings. Do you need an endocrinologist? Cardiologist? Just primary care?

Most people waste time seeing the wrong doctor first, or get generic advice that doesn't help.

## The Solution: Dorost

**Dorost** combines 6 AI agents to:
1. Ask intelligent health questions
2. Guide physical self-examination
3. Route to the right specialist (the core innovation)
4. Explain root causes in Dr. Berg's style
5. Give precise, actionable recommendations

## Example Conversation

```
You: "I'm constantly tired and crave sugar after meals"

Dorost: "That's a classic pattern of insulin resistance. Here's what's happening 
in your body:

When you eat high-carb foods, insulin spikes. Over time your cells stop responding.
Your pancreas makes MORE insulin. You can't burn fat for energy, but your cells are 
starving. That's the fatigue and cravings.

You should see an Endocrinologist - they specialize in metabolic issues.

They'll test: Fasting insulin, HbA1c, thyroid panel

What to do now: Try intermittent fasting + low carb to lower insulin naturally..."
```

## 9 Medical Specialties Covered

- Endocrinologist - Hormones, metabolism, diabetes, PCOS
- Gastroenterologist - Digestive system, IBS, IBD, gut health
- Cardiologist - Heart, blood pressure, palpitations
- Dermatologist - Skin, hair, nails, rashes
- Neurologist - Brain, nerves, headaches, numbness
- Rheumatologist - Autoimmune, arthritis, lupus
- Psychiatrist - Mental health, mood disorders
- Hematologist - Blood disorders, anemia
- Primary Care - General health, first contact

## How It Works - Multi-Agent Architecture

```
User Input
    ↓
┌─────────────────────────────────────┐
│ 1. INTAKE AGENT                     │
│ Asks: symptoms, diet, sleep, stress │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ 2. DIAGNOSTIC AGENT                 │
│ Guides: tongue, nails, skin checks  │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ 3. SPECIALTY ROUTER ⭐              │
│ Maps symptoms → right specialist    │
│ Uses medical knowledge base         │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ 4. KNOWLEDGE AGENT                  │
│ Explains biochemical mechanisms     │
│ Dr. Berg style teaching             │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ 5. ROOT CAUSE AGENT                 │
│ Shows systems thinking: cascades    │
│ Vicious cycles analysis             │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ 6. RECOMMENDER AGENT                │
│ Specific supplements, diet, lifestyle
│ Exact forms, dosages, timing        │
└─────────────────────────────────────┘
```

## Architecture Components

**Core Files:**
- `src/agents/` - 6 specialized AI agents
- `src/knowledge/medical_knowledge_base.py` - Medical specialties + red flags + routing
- `src/prompts/dr_berg_style.py` - 785 lines of system prompts
- `src/knowledge/context_engineering.py` - Session management + memory
- `src/evaluation.py` - Agent performance metrics & evaluation
- `src/logger.py` - Comprehensive logging & tracing
- `src/orchestrator.py` - Multi-agent coordination

**Key Features:**
- Multi-agent sequential pipeline with clean context flow
- Medical knowledge base (9 specialties, 16 red flags)
- Session management with clean context (no stale data)
- Specialty routing with pattern matching
- Safety checks (red flag detection, confidence scoring)
- Performance metrics & observability (evaluation tracking)
- Comprehensive logging (file + console output)

### System Architecture

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                        DOROST - Multi-Agent Health System                 ║
╚═══════════════════════════════════════════════════════════════════════════╝

                              User Input
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
            Session Management          Logging & Metrics
            (context_engineering.py)    (logger.py + evaluation.py)
                    │                           │
                    └─────────────┬─────────────┘
                                  │
        ┌─────────────────────────────────────────────────────────┐
        │          Sequential Agent Pipeline                      │
        │                                                         │
        │  ┌──────────────┐   ┌──────────────┐   ┌───────────┐  │
        │  │  1. INTAKE   │──▶│ 2. DIAGNOSTIC│──▶│ 3. ROUTER │  │
        │  │ Agent        │   │ Agent        │   │ Agent     │  │
        │  └──────────────┘   └──────────────┘   └─────┬─────┘  │
        │                                              │         │
        │                         ┌────────────────────┘         │
        │                         │                              │
        │                    ┌────▼──────────┐   ┌────────────┐ │
        │                    │ 4. KNOWLEDGE  │──▶│ 5. ROOT    │ │
        │                    │ Agent         │   │ CAUSE Ag.  │ │
        │                    └────────────────┘   └────┬───────┘ │
        │                                             │          │
        │                         ┌───────────────────┘          │
        │                         │                              │
        │                    ┌────▼──────────┐                  │
        │                    │ 6. RECOMMENDER│                  │
        │                    │ Agent         │                  │
        │                    └─────────────────┘                 │
        │                                                         │
        └─────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
            Output to User              Save Metrics
                                        (Evaluation Log)

CONTEXT FLOW:
User Input → Intake Profile → Diagnostic Findings → Specialty Recommendation
         → Medical Analysis → Root Cause Analysis → Final Recommendations

KNOWLEDGE INTEGRATION:
Every agent has access to:
• Medical knowledge base (9 specializations, 16 red flags)
• Dr. Berg-style prompts (785 lines of expertise)
• Clean session context (no stale data)
• Performance logging & metrics
```

### Data Flow Example

```
USER: "I have constant fatigue and sugar cravings"
  │
  ├─▶ INTAKE: "Tell me about your diet and sleep"
  │   │ Gathers health profile
  │   └─▶ OUTPUT: {symptoms, diet, sleep, stress, ...}
  │
  ├─▶ DIAGNOSTIC: "Check your tongue color and nails"
  │   │ Physical examination signs
  │   └─▶ OUTPUT: {tongue_findings, nail_condition, ...}
  │
  ├─▶ SPECIALTY ROUTER: Maps symptoms to specialist
  │   │ Pattern matching with medical KB
  │   └─▶ OUTPUT: "See ENDOCRINOLOGIST (confidence: 0.88)"
  │
  ├─▶ KNOWLEDGE: Explains the biochemistry
  │   │ Dr. Berg-style mechanism explanation
  │   └─▶ OUTPUT: "High insulin → cells resistant → fatigue..."
  │
  ├─▶ ROOT CAUSE: Shows cascade effects
  │   │ Systems thinking: diet → insulin → sleep → cortisol
  │   └─▶ OUTPUT: "Vicious cycle identified. Root cause: diet."
  │
  └─▶ RECOMMENDER: Precise action plan
      │ Specific supplements, dosages, timing
      └─▶ OUTPUT: "Magnesium Bisglycinate 400mg before bed..."
```

## Try It Locally

```bash
# 1. No API key needed - see what the system does
python3 quick_demo.py

# 2. See conversation branching
python3 branching_demo.py

# 3. With API key - live Dorost conversation
python3 chat.py
```

## Deploy Live (2 minutes)

```bash
# Get API key: https://aistudio.google.com/apikey
# Add to .env: GOOGLE_API_KEY=your-key

# Deploy to Google Cloud Run
gcloud run deploy dorost \
  --source . \
  --runtime python311 \
  --region us-central1 \
  --allow-unauthenticated

# Get your public URL
# Visit: https://dorost-xxxxx-uc.a.run.app
```

Full deployment guide: [DEPLOYMENT.md](DEPLOYMENT.md)

## What Makes This Different

**Generic health apps:**
> "You might be low on magnesium. Take a supplement."

**This agent:**
> "Your muscle cramps + poor sleep suggest magnesium deficiency.
> Take Magnesium Bisglycinate 400mg before bed (NOT Oxide - only 4% absorbed).
> Food sources: pumpkin seeds (150mg/oz), spinach (157mg/cup).
> Duration: 3 months. Safety: avoid if kidney disease."

It's **specific** - exact forms, dosages, timing, and explains *why* biochemically.

## Project Structure

```
src/
├── agents/
│   └── specialty_router_agent.py    # Core feature: symptom → specialist
├── knowledge/
│   └── medical_knowledge_base.py    # 9 specialists, red flags, routing logic
```

**Documentation:**
- [FAQ.md](FAQ.md) - Common questions
- [CONVERSATION_FLOW.md](CONVERSATION_FLOW.md) - How the conversation works

## Tech Stack

- Google ADK (multi-agent framework)
- Gemini 2.5-flash (medical knowledge)
- Python 3.11

## Quick Start

```bash
# 1. Set up environment
pip install -r requirements.txt

# 2. Add your API key
echo "GOOGLE_API_KEY=your-key-here" >> .env

# 3. Run tests
python -m pytest test_agents.py -v

# 4. Test the system
python -c "
from src.orchestrator import HealthAgentOrchestrator
orchestrator = HealthAgentOrchestrator()
result = orchestrator.run_consultation('I have fatigue and weight gain')
print('Status:', result['status'])
print('Confidence:', result['overall_confidence'])
"
```

## Project Info

- **Program:** Google AI Agents Intensive Capstone
- **Track:** Healthcare / Multi-Agent Systems
- **Submission:** Kaggle Agents Intensive Capstone Project
- **Links:**
  - Kaggle: https://www.kaggle.com/competitions/agents-intensive-capstone-project
  - Program: https://rsvp.withgoogle.com/events/google-ai-agents-intensive_2025
  - GitHub: https://github.com/Helialiaia01/Holistic-Health-Agent

Built November 2025
