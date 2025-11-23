# 🏥 Holistic Health Agent

> **AI Multi-Agent System with Dr. Berg-Style Scientific Health Guidance**  
> Kaggle Agents Intensive - Capstone Project (Healthcare Track)  
> November 2025

[![Gemini](https://img.shields.io/badge/Gemini-2.5--flash--lite-blue)](https://ai.google.dev)
[![Google ADK](https://img.shields.io/badge/Google-ADK-green)](https://google.adk.dev)
[![Python](https://img.shields.io/badge/Python-3.11-yellow)](https://python.org)

---

## 🎯 The Problem We Solve

**"I have symptoms but don't know which medical professional to consult."**

> *"Is it hormones? My skin? Digestive system? Do I need an endocrinologist, dermatologist, or gastroenterologist?"*

Most health apps give generic advice: "Take magnesium" or "Eat healthier."  
But they don't:
- Explain **WHY** (biochemical mechanisms)
- Specify **WHAT** (Magnesium Bisglycinate vs Oxide - forms matter!)
- Tell you **WHEN** (400mg before bed, not morning)
- Help you find **WHO** (which medical specialist to see)

---

## 💡 Our Solution

A **6-agent AI system** inspired by **Dr. Eric Berg's teaching style**:

1. 🗣️ **Intake Agent** - Conversational metabolic health interview
2. 🔬 **Diagnostic Agent** - Physical examination guide (tongue, nails, skin)
3. 🏥 **Specialty Router** - Maps symptoms → medical specialist recommendation
4. 🧠 **Knowledge Agent** - Explains biochemical mechanisms (simple language)
5. 🔍 **Root Cause Agent** - Identifies cascade effects (not just symptoms)
6. 💊 **Recommender Agent** - Precise recommendations (exact forms, dosages, timing)

### What Makes This Different?

**Generic health apps:**
> "You might have low magnesium. Take a supplement."

**Our agent (Dr. Berg style):**
> "Your muscle cramps + anxiety + sleep issues point to magnesium deficiency. Magnesium is THE relaxation mineral - it blocks calcium from entering nerve cells (calcium = contraction, magnesium = relaxation). You need 400-500mg daily but most people get 200mg.
> 
> **Recommendation:**  
> - Form: Magnesium Bisglycinate 400mg (NOT Oxide - only 4% absorbed)
> - Timing: Before bed (enhances sleep)
> - Food sources: Pumpkin seeds (150mg/oz), Spinach (157mg/cup cooked)
> - Duration: 3 months to replenish tissues
> - Safety: Reduce if diarrhea. Avoid if kidney disease.
>
> **Why:** Stress depletes magnesium. High insulin blocks absorption. It's a vicious cycle."

---

## 🏗️ System Architecture

```
User: "Constant fatigue, sugar cravings, can't sleep. Which doctor should I see?"

┌─────────────────────────────────────────────────────────────┐
│                   ORCHESTRATOR                               │
│  (Sequential Agent Flow with Clean Context Management)      │
└─────────────────────────────────────────────────────────────┘
   │
   ├──▶ 1️⃣ INTAKE AGENT
   │      "Tell me about your diet, sleep, stress..."
   │      → health_profile
   │
   ├──▶ 2️⃣ DIAGNOSTIC AGENT  
   │      "Let's check your tongue, nails, skin..."
   │      → diagnostic_findings
   │
   ├──▶ 3️⃣ SPECIALTY ROUTER ⭐ (Unique Feature)
   │      "Based on symptoms: See Endocrinologist"
   │      "Why: Insulin resistance + metabolic issues"
   │      "Tests: Fasting insulin, HbA1c, thyroid panel"
   │      → specialist_recommendation
   │
   ├──▶ 4️⃣ KNOWLEDGE AGENT
   │      "Here's what's happening biochemically..."
   │      "Insulin resistance → blocks fat burning → cravings"
   │      → medical_analysis
   │
   ├──▶ 5️⃣ ROOT CAUSE AGENT
   │      "Root: Stress → Cortisol ↑ → Insulin ↑ → Mg deficiency"
   │      "Vicious cycle identified"
   │      → root_cause_analysis
   │
   └──▶ 6️⃣ RECOMMENDER AGENT
         "Phase 1: Mg Bisglycinate 400mg before bed"
         "Phase 2: Low-carb + intermittent fasting 16:8"
         "Phase 3: Stress management protocols"
         → precise_recommendations

┌─────────────────────────────────────────────────────────────┐
│            SINGLE SOURCE OF TRUTH                           │
│  • Medical Knowledge Base (symptoms → conditions → specialists)│
│  • Context Engineering (clean context, no stale logs)       │
│  • Red Flag Detection (emergency, urgent, soon, routine)    │
│  • Confidence Scoring (agent knows when to escalate)        │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Key Innovations

### 1. **Medical Specialty Routing** ⭐
Solves the "Who do I see?" problem by mapping symptoms to 9 medical specialists:
- Endocrinologist (hormones, metabolism)
- Gastroenterologist (digestive)
- Cardiologist (heart, circulation)
- Dermatologist (skin)
- Neurologist (neurological)
- Rheumatologist (autoimmune, joints)
- Psychiatrist (mental health)
- Hematologist (blood disorders)
- Primary Care (general/unclear)

### 2. **Dr. Berg-Style Scientific Precision**
Not "take magnesium" but:
- **Exact form:** Magnesium Bisglycinate (NOT Oxide - 4% absorbed)
- **Dosage:** 400mg elemental magnesium
- **Timing:** Before bed
- **Food sources:** Pumpkin seeds 150mg/oz, Spinach 157mg/cup
- **Duration:** 3 months
- **Mechanism:** "Blocks calcium entry → relaxation"

### 3. **Root Cause Analysis (Systems Thinking)**
Identifies cascades, not just symptoms:
```
ROOT: Stress
  ↓
Cortisol ↑
  ↓
Blood sugar ↑
  ↓
Insulin ↑
  ↓
Blocks Mg absorption
  ↓
Low Mg → Poor sleep
  ↓
More stress (vicious cycle)
```

### 4. **Production-Grade Safety**
- **Red flag detection:** 15+ emergency/urgent conditions
- **Confidence scoring:** 0.0-1.0 with escalation at <0.60
- **Agent self-awareness:** Knows limitations, when to escalate
- **Clean context:** Removes stale logs between tasks
- **Medical disclaimer:** Always included

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | Google ADK | Multi-agent orchestration |
| **Model** | Gemini 2.5-flash-lite | Fast, medical training (PubMed) |
| **Language** | Python 3.11 | Core implementation |
| **Architecture** | Clean Architecture | Single source of truth, clear boundaries |
| **Context** | Context Engineering | Clean context flow, task decomposition |
| **Safety** | Red Flags + Confidence | Emergency detection, escalation logic |
| **Deployment** | Google Cloud Run (planned) | Serverless deployment |

---

## 📦 Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/Holistic-Health-Agent.git
cd Holistic-Health-Agent

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.template .env
# Add your GOOGLE_API_KEY to .env

# Run demo
python demo.py
```

---

## 🚀 Quick Start

```python
from src.orchestrator import create_health_agent_orchestrator

# Create orchestrator
orchestrator = create_health_agent_orchestrator()

# Run consultation
query = """
I'm constantly fatigued, have strong sugar cravings, 
and don't know if I should see an endocrinologist or 
primary care doctor.
"""

results = orchestrator.run_consultation_step_by_step(query)

# Results include:
# - health_profile
# - diagnostic_findings  
# - specialist_recommendation ⭐
# - medical_analysis
# - root_cause_analysis
# - recommendations (with exact forms, dosages, timing)
```

---

## 📊 Example Output

```
🏥 SPECIALTY ROUTER OUTPUT:

Recommended Medical Specialist: Endocrinologist (Hormone & Metabolism)

Reasoning:
• Symptom cluster suggests metabolic/endocrine issues
• Afternoon fatigue + sugar cravings + belly fat = insulin resistance pattern
• Palpitations + anxiety can be cortisol/thyroid related

What endocrinologist will check:
✓ Fasting insulin & glucose (insulin resistance)
✓ HbA1c (3-month blood sugar average)
✓ Thyroid panel (TSH, Free T3, Free T4)
✓ Cortisol levels (morning & evening)

Confidence: 0.88

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💊 RECOMMENDER OUTPUT (Dr. Berg Precision):

PHASE 1 (Week 1-2): SLEEP OPTIMIZATION

1. MAGNESIUM SUPPLEMENTATION
   Form: Magnesium Bisglycinate 400mg
   (NOT Oxide - only 4% absorbed, causes diarrhea)
   
   Timing: 30-60 minutes before bed
   
   Why this form:
   • Bisglycinate = Mg + glycine (calming amino acid)
   • 80-90% absorption vs 4% for Oxide
   • Crosses blood-brain barrier for sleep
   
   Food sources:
   • Pumpkin seeds: 150mg per ounce
   • Spinach (cooked): 157mg per cup
   • Dark chocolate (85%): 64mg per ounce
   
   Duration: 3 months to replenish tissues
   
   Safety: Start 200mg if sensitive stomach. Reduce if diarrhea.
   Check with doctor if kidney disease.

2. SLEEP HYGIENE
   • Fixed schedule: Bed 10pm, wake 6am (8 hours)
   • Room: 65-68°F, pitch black
   • No screens 1 hour before bed
   • Morning sunlight: 10-15 minutes within 1 hour of waking

PHASE 2 (Week 3-4): METABOLIC RESET

3. INTERMITTENT FASTING
   Start: 14:10 (14 hours fasting, 10 hour eating)
   Progress to: 16:8 (skip breakfast, eat 12pm-8pm)
   
   First meal:
   • Protein: 30-40g (eggs, salmon, chicken)
   • Healthy fats: Avocado, olive oil, nuts
   • Vegetables: 2-3 cups leafy greens
   • LOW carbs: Under 20g net carbs
   
   Why: Fasting lowers insulin. Only when insulin is LOW
   can you burn fat.

Confidence: 0.75 (Strong pattern, safe recommendations)
```

---

## 🗂️ Project Structure

```
Holistic-Health-Agent/
├── src/
│   ├── agents/
│   │   ├── intake_agent.py           # Metabolic health interview
│   │   ├── diagnostic_agent.py       # Physical examination guide
│   │   ├── specialty_router_agent.py # Medical specialist routing ⭐
│   │   ├── knowledge_agent.py        # Biochemical mechanism analysis
│   │   ├── root_cause_agent.py       # Systems thinking root cause
│   │   └── recommender_agent.py      # Dr. Berg precision recommendations
│   ├── knowledge/
│   │   ├── medical_knowledge_base.py # Single source of truth
│   │   └── context_engineering.py    # Clean context management
│   ├── prompts/
│   │   └── dr_berg_style.py          # Dr. Berg communication style
│   ├── tools/
│   │   ├── health_patterns.py        # Pattern database
│   │   └── pattern_matcher.py        # Pattern matching logic
│   ├── orchestrator.py               # Multi-agent coordination
│   └── config.py                     # Configuration
├── tests/
│   └── test_agents.py                # Agent tests
├── docs/
│   ├── CLEAN_ARCHITECTURE.md         # Production design principles
│   ├── DR_BERG_AGENT.md              # Dr. Berg style guide
│   └── ENHANCED_ARCHITECTURE.md      # Technical specifications
├── demo.py                           # Interactive demo
├── requirements.txt                  # Dependencies
├── .env.template                     # Environment template
└── README.md                         # This file
```

---

## 🎯 Kaggle Competition Requirements

| Category | Requirement | Implementation | Status |
|----------|-------------|----------------|--------|
| **1. Multi-Agent** | 2+ agents | 6 specialized agents | ✅ |
| **2. Tools** | FunctionTool | Specialty router, pattern matcher | ✅ |
| **3. Prompts** | Quality prompts | Dr. Berg style, optimized | ✅ |
| **4. Context** | Context management | Context engineering system | ✅ |
| **5. Safety** | Red flags, escalation | 15+ red flags, confidence scoring | ✅ |
| **6. Architecture** | Clean design | Single source of truth, clear boundaries | ✅ |
| **7. Innovation** | Novel features | Specialty routing, systems thinking | ✅ |

**Bonus Points:**
- ✅ **+5** Using Gemini throughout
- 📅 **+5** Cloud Run deployment (planned)
- 📅 **+10** YouTube demo video (planned)

**Projected Score:** 93-102/100 (capped at 100)

---

## 🏆 Competitive Advantages

1. **Specialty Routing** - Solves real problem: "Who do I see?"
2. **Dr. Berg Precision** - Exact forms, dosages, timing (NOT generic)
3. **Systems Thinking** - Root causes, not symptoms
4. **Production Safety** - Red flags, confidence scoring, agent self-awareness
5. **Clean Architecture** - Single source of truth, no stale context
6. **Scientific Depth** - Explains biochemical mechanisms simply

---

## 🧪 Testing

### Quick Demos (No API Key Required)

```bash
# See full system overview and expected output
python quick_demo.py

# See conversation branching demonstration  
python branching_demo.py
```

### Live Testing (Requires API Key)

```bash
# Get API key: https://aistudio.google.com/apikey
# Add to .env: GOOGLE_API_KEY=your-key-here
python demo.py
```

### Component Validation

```bash
# Run all tests
python test_agents.py

# Or run pytest suite
python -m pytest tests/
```

**See [TESTING_GUIDE.md](TESTING_GUIDE.md) for comprehensive testing instructions.**

---

## 📚 Documentation

- **[CLEAN_ARCHITECTURE.md](docs/CLEAN_ARCHITECTURE.md)** - Production design principles
- **[DR_BERG_AGENT.md](docs/DR_BERG_AGENT.md)** - Dr. Berg style implementation
- **[ENHANCED_ARCHITECTURE.md](docs/ENHANCED_ARCHITECTURE.md)** - Technical specifications
- **[CONVERSATION_FLOW.md](CONVERSATION_FLOW.md)** - How conversation branching works
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Comprehensive testing instructions
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide

---

## 🚀 Deployment (Planned)

```bash
# Build Docker image
docker build -t health-agent .

# Run locally
docker run -p 8080:8080 --env-file .env health-agent

# Deploy to Cloud Run
gcloud run deploy health-agent \
  --image gcr.io/PROJECT_ID/health-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 🛣️ Roadmap

**✅ Completed (60% of project)**
- Clean architecture design
- Single source of truth knowledge base
- Context engineering system
- Specialty routing agent
- Dr. Berg style prompts
- All 6 core agents
- Orchestrator
- Comprehensive documentation

**🔄 In Progress (30% of project)**
- Integration testing
- End-to-end conversation flows
- Bug fixes and refinement
- Demo video creation

**📅 Planned (10% of project)**
- Cloud Run deployment
- Performance optimization
- Additional test coverage

**Deadline:** December 1, 2025 (8 days remaining)

---

## 🤝 Contributing

This is a capstone project submission. After the competition, contributions welcome!

---

## 📜 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- **Dr. Eric Berg** - Teaching style inspiration (scientific depth + simple explanations)
- **Google ADK Team** - Agent Development Kit framework
- **Kaggle Agents Intensive** - Course and competition
- **Gemini API** - Powering the medical intelligence

---

## 👤 Author

**Kaggle Agents Intensive - Capstone Project**  
Healthcare Track | November 2025

Built to demonstrate:
- Production-grade multi-agent systems
- Clean architecture principles
- AI safety in healthcare
- Novel problem-solving (specialty routing)
- Scientific depth (Dr. Berg style)

---

## 📞 Support

For questions or issues:
- Open a GitHub issue
- Check documentation in `/docs`
- Run `python demo.py` for interactive examples

---

⭐ **If you find this project helpful, please star it!** ⭐

---

## 🎬 Demo Video

Coming soon: 3-minute video showing:
1. The problem (who do I see?)
2. Why multi-agent AI?
3. System architecture
4. Live demonstration
5. Build process insights

**YouTube link:** [Coming December 1, 2025]

---

**End of README** 🏥
