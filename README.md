# Holistic Health Agent

An AI system that helps people figure out **which medical specialist to see** based on their symptoms.

## The Problem

You're tired, have brain fog, and sugar cravings. Do you need an endocrinologist? Cardiologist? Just primary care?

Most people waste time seeing the wrong doctor first, or get generic advice that doesn't help.

## What This Does

This agent analyzes your symptoms and tells you which specialist you actually need:

```
You: "I'm constantly tired and crave sugar after meals"

Agent: "See an Endocrinologist
       
       Why: Your symptoms (fatigue + cravings + crashes) 
       match insulin resistance - a metabolic issue.
       
       They'll test: Fasting insulin, HbA1c, thyroid panel
       
       Primary care usually misses this - they only check 
       glucose, which looks normal in early stages."
```

### 9 Specialties Covered

- Endocrinologist (hormones, metabolism)
- Gastroenterologist (digestive)
- Cardiologist (heart)
- Dermatologist (skin)
- Neurologist (brain/nerves)
- Rheumatologist (autoimmune, joints)
- Psychiatrist (mental health)
- Hematologist (blood)
- Primary Care (general)

## How It Works

Uses **Gemini 2.5-flash-lite** with custom prompts to:
1. Ask intelligent follow-up questions about your symptoms
2. Match symptom patterns to medical specializations
3. Explain the biochemical mechanism in simple terms
4. Give precise recommendations (not generic advice)

Built with Google's Agent Development Kit (ADK).

## Try It

```bash
# No API key needed - see what it does
python quick_demo.py

# See how conversation branching works
python branching_demo.py
```

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
- Gemini 2.5-flash-lite (medical knowledge)
- Python 3.11

## Live Testing

```bash
# Get API key from: https://aistudio.google.com/apikey
# Add to .env: GOOGLE_API_KEY=your-key-here
python demo.py
```

---

Built for Kaggle Agents Intensive - Healthcare Track, November 2025
