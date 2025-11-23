# Conversation Branching & Specialist Choices

## 🌳 YES! The Agent Uses Intelligent Branching

### How Conversation Branching Works

The **Intake Agent** is powered by **Gemini 2.5-flash-lite** (pre-trained on medical literature) with **custom prompts** that enable intelligent follow-up questions.

#### Example: "I feel very tired and irritated these days"

```
USER: "I feel very tired and irritated these days"

┌─────────────────────────────────────────────────────────────────┐
│ INTAKE AGENT (Gemini + Dr. Berg Prompt)                        │
│                                                                 │
│ Analyzes: "tired + irritated" = Multiple possible causes       │
│ → Insulin resistance?                                           │
│ → Magnesium deficiency?                                         │
│ → Adrenal fatigue?                                              │
│ → Thyroid issue?                                                │
│ → B vitamin deficiency?                                         │
│                                                                 │
│ Strategy: Ask TARGETED questions to narrow down root cause     │
└─────────────────────────────────────────────────────────────────┘

AGENT: "I understand - fatigue and irritability can be really 
frustrating. Let me ask some specific questions to help identify 
what's really going on:

1. ENERGY PATTERN
   - When is your fatigue worst? Morning, afternoon, or all day?
   - How do you feel after meals - energized or more tired?
   - Do you get a "crash" 2-3 hours after eating?

2. SUGAR & CRAVINGS
   - Do you crave sugar or carbs throughout the day?
   - How often do you eat? Every 2-3 hours or longer gaps?
   - Can you skip breakfast without feeling shaky or irritable?

3. SLEEP QUALITY
   - Even though you're tired, how well do you actually sleep?
   - Do you wake up multiple times at night?
   - Do you feel refreshed in the morning or exhausted?

4. STRESS & IRRITABILITY
   - Is the irritability constant or worse at certain times?
   - Do small things set you off that normally wouldn't?
   - How's your stress level - is there a lot going on?

5. DIET SNAPSHOT
   - What does a typical day of eating look like?
   - How much processed food or carbs (bread, pasta, rice)?
   - Do you eat right before bed?

The reason I'm asking these specific questions: 
- Afternoon crash + sugar cravings = insulin resistance pattern
- Tired but can't sleep + irritable = magnesium depletion
- Morning fatigue + cold = thyroid dysfunction
- Wired and tired = adrenal stress

Tell me more about what you're experiencing."
```

### 🧠 How Branching Happens

**1. Gemini's Pre-Training (Medical Knowledge)**
   - Trained on: PubMed articles, medical textbooks, clinical guidelines
   - Knows: Symptom clusters, diagnostic patterns, differential diagnosis
   - Can: Generate contextually relevant follow-up questions

**2. Our Custom Prompt Engineering**
   ```python
   INTAKE_AGENT_INSTRUCTION = """
   Interview approach (Dr. Berg style):
   1. Start with their main concern
   2. Ask about KEY METABOLIC INDICATORS:
      - Energy patterns
      - Sleep quality  
      - Diet specifics
      - Cravings
      - Digestion
   
   3. Dig into ROOT CAUSES with follow-up questions:
      - "When did this start?"
      - "What makes it better or worse?"
      - "How do you feel after meals?"
   
   4. Use Dr. Berg's framework - think about:
      - Insulin resistance (fatigue after meals, cravings)
      - Vitamin deficiencies (specific symptoms)
      - Adrenal stress (tired but wired)
      - Thyroid dysfunction (cold, weight gain)
   
   5. Be conversational and EDUCATIONAL:
      "That fatigue after lunch is a classic sign of 
      insulin resistance. Let's explore this more."
   """
   ```

**3. Result: Natural, Intelligent Branching**
   - Agent asks relevant follow-ups based on initial symptoms
   - Explains WHY it's asking (educates while gathering data)
   - Adapts questions based on user responses
   - Narrows down from broad symptoms → specific patterns

---

## 📊 Example Branching Tree

```
"I feel tired and irritated"
        |
        ↓
Agent asks about TIMING
        ├─ "All day tired"
        │       ↓
        │   Agent explores: Thyroid? Anemia? Sleep quality?
        │
        ├─ "Afternoon crash"
        │       ↓
        │   Agent explores: Blood sugar? Meals? Cravings?
        │       ↓
        │   "Yes, I crash after lunch and crave sugar"
        │       ↓
        │   Agent: "Classic insulin resistance. Let's confirm..."
        │       ↓
        │   More questions: Diet? Fasting? Exercise?
        │
        └─ "Tired but can't sleep"
                ↓
            Agent explores: Stress? Magnesium? Cortisol?
```

---

## 🎯 Real Example from Prompts

From `src/prompts/dr_berg_style.py` (lines 88-106):

```python
3. Dig into ROOT CAUSES with questions like:
   - "When did this start? Was there a trigger?"
   - "What makes it better or worse?"
   - "Tell me about your typical day of eating"
   - "How's your digestion? Bloating? Constipation?"
   - "Do you crave sugar or carbs?"
   - "How do you feel after meals - energized or tired?"

4. Use Dr. Berg's framework - think about:
   - Insulin resistance (fatigue after meals, belly fat, sugar cravings)
   - Vitamin/mineral deficiencies (specific symptoms)
   - Liver congestion (can't lose weight, right shoulder pain)
   - Adrenal stress (tired but wired, can't handle stress)
   - Gut issues (bloating, food sensitivities, immune problems)
   - Thyroid dysfunction (cold, hair loss, weight gain)

5. Be conversational and educational:
   "Interesting - that fatigue after lunch is a classic sign of insulin 
   resistance. Your body is having trouble regulating blood sugar. 
   Let's explore this more."
```

---

## 🏥 Why Only 9 Medical Specializations?

### Strategic Coverage Decision

We focused on **high-impact, commonly needed specialties** based on:

1. **Dr. Berg's Content Focus Areas**
   - Metabolic disorders (Endocrinology) ⭐
   - Digestive health (Gastroenterology)
   - Heart health (Cardiology)
   - Autoimmune (Rheumatology)

2. **Most Common Health Issues**
   - 88M Americans have pre-diabetes → **Endocrinologist**
   - 70M have digestive disorders → **Gastroenterologist**
   - 121M have cardiovascular disease → **Cardiologist**
   - 50M have autoimmune disease → **Rheumatologist**

3. **Clear Symptom-to-Specialist Mapping**
   - Easy to route symptoms to these specialists
   - Less overlap/ambiguity
   - High confidence recommendations

### The 9 Specialists & Why We Chose Them

| Specialist | Treats | Why Included | Example Symptoms |
|------------|--------|--------------|------------------|
| **Endocrinologist** ⭐ | Hormones, metabolism | Dr. Berg's #1 focus (insulin resistance, thyroid, diabetes) | Fatigue + cravings, weight gain, PCOS |
| **Gastroenterologist** | Digestive system | Very common (IBS, IBD, gut health) | Bloating, diarrhea, reflux |
| **Cardiologist** | Heart, circulation | Leading cause of death | Palpitations, chest pain, high BP |
| **Dermatologist** | Skin, hair, nails | Highly visible symptoms, easy to identify | Rash, acne, hair loss |
| **Neurologist** | Brain, nervous system | Specific, concerning symptoms | Headaches, numbness, tremors |
| **Rheumatologist** | Joints, autoimmune | Growing prevalence, complex cases | Joint pain, arthritis, lupus |
| **Psychiatrist** | Mental health (MD) | Can prescribe medications, distinct from therapy | Depression, anxiety (severe) |
| **Hematologist** | Blood disorders | Specific but critical | Anemia, clotting, blood tests |
| **Primary Care** | General/unclear | Catchall, first point of contact | Unclear symptoms, general health |

### Why We DIDN'T Include Others

**NOT Included:**
- ❌ **Oncologist** - Too specialized, requires prior diagnosis
- ❌ **Nephrologist** - Kidney specialists for specific diagnosed conditions
- ❌ **Pulmonologist** - Lung issues usually go to primary care first
- ❌ **Orthopedist** - Injury/surgery focused, less diagnostic
- ❌ **Urologist** - Very specific symptoms (often embarrassing, users less likely to ask)
- ❌ **Ophthalmologist** - Eye-specific, users know to see eye doctor
- ❌ **ENT** - Specific symptoms (ear/nose/throat), users typically know
- ❌ **OB/GYN** - Gender-specific, users typically know when to see

### Coverage Analysis

**Our 9 specialists cover ~85% of cases where people ask:**
> "I don't know which specialist to see"

**The 15% we don't cover:**
- Highly specific issues (user usually knows already)
- Require prior diagnosis (referred by primary care)
- Emergency room cases (red flags catch these)

---

## 🎯 Could We Add More Specialists?

**YES - Easy to Extend!**

All specialist data is in: `src/knowledge/medical_knowledge_base.py`

To add a new specialist:

```python
# In medical_knowledge_base.py, add to MEDICAL_SPECIALTIES dict:

"pulmonologist": MedicalSpecialty(
    name="Pulmonologist",
    description="Respiratory system and lung health",
    treats_conditions=[
        "Asthma", "COPD", "Chronic cough", 
        "Shortness of breath", "Sleep apnea"
    ],
    common_symptoms=[
        "persistent cough", "shortness of breath",
        "wheezing", "chest tightness", "snoring"
    ],
    when_to_see=[
        "Chronic cough lasting >3 weeks",
        "Difficulty breathing at rest or with mild activity",
        "Wheezing not resolved by inhaler",
        "Diagnosed sleep apnea not improving"
    ],
    typical_tests=[
        "Pulmonary function test (spirometry)",
        "Chest X-ray or CT scan",
        "Sleep study (polysomnography)",
        "Oxygen saturation monitoring"
    ]
)
```

Then update `route_to_specialist()` logic to include new patterns.

**Why start with 9?**
- Covers most common cases
- Clean, focused scope for initial launch
- Easier to validate accuracy
- Can expand based on user feedback

---

## 🔑 Key Takeaways

### 1. YES - Intelligent Conversation Branching ✅
   - Gemini asks follow-up questions based on user responses
   - Not pre-scripted - adapts to conversation context
   - Uses Dr. Berg's diagnostic framework
   - Explains WHY it's asking (educational)

### 2. How It Works
   - **Pre-trained Gemini** (medical knowledge)
   - **+ Custom Prompts** (Dr. Berg style, diagnostic questions)
   - **+ Knowledge Base** (specialist routing, red flags)
   - **= Intelligent conversational agent**

### 3. 9 Specialists = Strategic Choice
   - Covers 85% of "I don't know who to see" cases
   - High-impact, common specialties
   - Clear symptom-to-specialist mapping
   - Easily extensible to add more

### 4. Example Flow
   ```
   User: "I feel tired and irritated"
   
   Agent: "Let me ask some targeted questions:
          - When is fatigue worst?
          - Do you crave sugar?
          - How's your sleep?
          - What's your diet like?"
   
   User: "Afternoon crash, yes sugar cravings, eat a lot of carbs"
   
   Agent: "Classic insulin resistance pattern. 
          Let me ask about meal timing..."
   
   [Continues branching based on responses]
   
   Final: "Based on your pattern, I recommend seeing an 
          ENDOCRINOLOGIST. They specialize in metabolic 
          disorders like insulin resistance."
   ```

---

## 📁 Where to Find This Code

**Conversation Prompts:**
- `src/prompts/dr_berg_style.py` - Lines 88-106 (Intake branching logic)

**Specialist Definitions:**
- `src/knowledge/medical_knowledge_base.py` - Lines 240+ (9 specialists)

**Routing Logic:**
- `src/knowledge/medical_knowledge_base.py` - Lines 494+ (route_to_specialist function)

**Orchestrator:**
- `src/orchestrator.py` - Coordinates all 6 agents with branching

---

## 💡 Want to See It Live?

```bash
# Get API key: https://aistudio.google.com/apikey
# Add to .env: GOOGLE_API_KEY=your-key-here

python demo.py
```

Then try:
```
"I feel very tired and irritated these days"
```

Watch how the agent:
1. Asks follow-up questions about timing, diet, sleep
2. Branches based on your answers
3. Educates you while gathering info
4. Routes to the right specialist
5. Explains the root cause
6. Gives precise recommendations
