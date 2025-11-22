# 🏥 Holistic Health Agent

> **AI Multi-Agent System for Personalized Health Guidance**  
> Kaggle Agents Intensive - Capstone Project  
> November 2025

---

## 🎯 Project Overview

A conversational AI health coach powered by **4 specialized agents** working together to provide personalized health recommendations. The system learns from each conversation, remembers user health history, and gets smarter over time.

### **The Problem**
- Generic health advice doesn't work for everyone
- People don't understand WHY they feel bad (root causes)
- No accessible personalized health guidance
- No system that learns and improves with each conversation

### **The Solution**
Multi-agent AI system that:
1. 🗣️ **Listens** to your health concerns (Intake Agent)
2. 🔍 **Analyzes** patterns in your lifestyle (Analyzer Agent)
3. 💡 **Explains** root causes and mechanisms (Reasoning Agent)
4. 💊 **Recommends** personalized supplements + lifestyle changes (Recommender Agent)
5. 🧠 **Remembers** your health history across sessions (Memory System)

---

## 🏗️ Multi-Agent Architecture

```
User: "I'm exhausted all the time, sleep only 5 hours"

┌─────────────────────────────────────────────────┐
│           ORCHESTRATOR AGENT                     │
│      (Sequential: Intake→Analyze→Reason→Recommend)│
└─────────────────────────────────────────────────┘
         │          │            │          │
         ▼          ▼            ▼          ▼
    ┌────────┐ ┌────────┐ ┌─────────┐ ┌──────────┐
    │INTAKE  │ │ANALYZER│ │REASONING│ │RECOMMEND │
    │        │ │        │ │         │ │          │
    │Asks    │ │Finds   │ │Explains │ │Suggests  │
    │questions│ │patterns│ │causes   │ │solutions │
    └────────┘ └────────┘ └─────────┘ └──────────┘
                   │           │           │
              ┌────┴────┐  ┌───┴───┐  ┌───┴────┐
              │20 Health│  │Root    │  │USDA    │
              │Patterns │  │Cause   │  │Nutrient│
              │Database │  │Logic   │  │Database│
              └─────────┘  └────────┘  └────────┘
```

---

## ✨ Key Features

- **4 Specialized Agents** - Each agent is an expert in its domain
- **Conversational Interface** - Natural dialogue, not survey-like
- **Pattern Matching** - 20 health patterns with 40+ indicators
- **Root Cause Analysis** - Explains WHY issues are happening
- **Personalized Recommendations** - Tailored to your specific situation
- **Session Memory** - Remembers your health history
- **Learning System** - Gets smarter with each conversation
- **Real Data Integration** - USDA Nutrient Database for accuracy

---

## 🛠️ Technology Stack

- **Framework:** Google ADK (Agent Development Kit)
- **Model:** Gemini 2.5-flash-lite
- **Language:** Python 3.11
- **Session Management:** DatabaseSessionService (SQLite)
- **Memory:** Auto-save callbacks + persistent storage
- **Data:** USDA FoodData Central API
- **Deployment:** Google Cloud Run
- **Observability:** LoggingPlugin

---

## 📊 7 Competition Requirements

| Requirement | Implementation | Status |
|-------------|-----------------|--------|
| Multi-agent system | 4 sequential agents (Intake→Analyzer→Reasoning→Recommender) | ✅ |
| Basic tools | Pattern matching, health scoring | ✅ |
| Advanced tools | USDA API integration, preload_memory | 🔄 In Progress |
| Sessions | DatabaseSessionService (SQLite) | 🔄 In Progress |
| Memory | Auto-save callbacks + long-term storage | 🔄 In Progress |
| Observability | LoggingPlugin + custom callbacks | 🔄 In Progress |
| Deployment | Google Cloud Run | 📅 Planned |

**Bonus Points:**
- ✅ +5: Using Gemini API throughout
- 📅 +5: Cloud Run deployment
- 📅 +10: YouTube demo video

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Google Gemini API key
- (Optional) Google Cloud account for deployment

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/holistic-health-agent.git
cd holistic-health-agent

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.template .env
# Edit .env and add your GOOGLE_API_KEY
```

### Run the Agent

```bash
# Test the agents (coming soon)
python src/main.py
```

---

## 📖 Example Conversation

```
User: "I'm exhausted all the time, sleep only 5 hours, eat mostly processed food"

Intake Agent:
"That sounds tough. Tell me more about your sleep - what time do you go to bed? 
And your diet - what does a typical day look like?"

User: "I go to bed around 2am, wake at 7am. Breakfast is cereal, lunch is fast food, 
dinner is pasta or pizza. I work at a desk all day, no exercise."

Analyzer Agent:
"Based on your profile, I'm identifying 3 key patterns:
• Vitamin D deficiency (indoor lifestyle, no sun exposure)
• Magnesium deficiency (poor sleep, high stress, processed diet)
• Blood sugar dysregulation (high carbs, no protein, sedentary)"

Reasoning Agent:
"Here's WHY this is happening:
1. Vitamin D: You're indoors all day. Without sun, your body can't make Vitamin D. 
   Low Vitamin D → fatigue, low mood, weak immunity
2. Magnesium: Processed foods are stripped of magnesium. Poor sleep depletes it further.
   Low magnesium → anxiety, poor sleep quality, muscle tension
3. Blood Sugar: High carb meals without protein cause sugar spikes and crashes.
   This creates the afternoon energy crash you're feeling."

Recommender Agent:
"Based on your specific situation, I recommend:
1. Vitamin D3 2000 IU daily (take with breakfast)
2. Magnesium Glycinate 300mg at bedtime
3. Walk outdoors 20 minutes daily (morning for Vitamin D + energy)
4. Add protein to every meal (eggs, chicken, fish, beans)
5. Set bedtime 30 minutes earlier

Timeline: 2-3 weeks to feel energy improvement
Follow-up: Check in 1 week about caffeine intake and stress levels"
```

---

## 🗂️ Project Structure

```
holistic-health-agent/
├── src/
│   ├── agents/
│   │   ├── intake_agent.py        # Conversational health intake
│   │   ├── analyzer_agent.py      # Pattern matching & analysis
│   │   ├── reasoning_agent.py     # Root cause explanations
│   │   └── recommender_agent.py   # Personalized recommendations
│   ├── tools/
│   │   ├── health_patterns.py     # 20 health patterns database
│   │   ├── pattern_matcher.py     # Matching algorithm
│   │   ├── usda_integration.py    # USDA Nutrient Database
│   │   └── callbacks.py           # Auto-save memory
│   ├── config.py                  # Configuration management
│   ├── orchestrator.py            # Sequential agent coordination
│   └── main.py                    # Entry point
├── tests/
│   └── test_agents.py
├── deployment/
│   ├── Dockerfile
│   └── .agent_engine_config.json
├── requirements.txt
├── .env.template
└── README.md
```

---

## 🧪 Health Patterns Database

The system recognizes 20 common health patterns:

1. Vitamin D Deficiency
2. Magnesium Deficiency
3. B Vitamin Deficiency
4. Iron Deficiency
5. Zinc Deficiency
6. Caffeine Sensitivity
7. Blood Sugar Dysregulation
8. Sleep Deprivation
9. Omega-3 Deficiency
10. Chronic Stress
11. Sedentary Lifestyle
12. Processed Food Diet
13. Protein Deficiency
14. Dehydration
15. Gut Health Issues
16. Calcium Deficiency
17. Thyroid Issues
18. Inflammation
19. Hormonal Imbalance
20. Mental Health Challenges

Each pattern includes:
- Indicators (symptoms/signs)
- Severity factors (lifestyle factors that worsen it)
- Root cause explanation
- Specific supplement recommendations with dosages
- Lifestyle interventions
- Expected timeline for improvement

---

## 🎓 Learning & Evaluation

The system is evaluated on:
- Response quality (matching expected recommendations)
- Tool usage (correct pattern matching)
- Reasoning depth (explanation quality)
- Personalization (memory usage)
- User experience (conversational flow)

---

## 🚧 Future Improvements

If we had more time/resources:
- Real-time fitness tracker integration (Fitbit, Google Fit)
- Blood test lab data API integration
- Barcode scanner for nutrition tracking
- Shopping agent for supplement price comparison
- Dr. Eric Berg video knowledge integration via MCP
- A2A protocol to expose recommender as service
- Mobile app for daily health tracking
- Advanced memory with semantic search

---

## 📜 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- Google ADK Team for the Agent Development Kit
- Kaggle Agents Intensive Course instructors
- USDA for the FoodData Central API
- Gemini API for powering the intelligence

---

## 👤 Author

Built as part of Kaggle Agents Intensive - Capstone Project  
November 2025

**Submission Track:** Healthcare  
**Goal:** Demonstrate practical multi-agent AI system for personalized health guidance

---

## 📞 Contact

For questions or feedback, please open an issue on GitHub.

---

⭐ **Star this repo if you find it helpful!** ⭐
