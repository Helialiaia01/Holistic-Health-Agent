#!/usr/bin/env python3
"""
Quick Demo - Shows the system's expected output and key features
No complex imports or function calls - just demonstrates what the agents produce
"""

def show_system_overview():
    """Show what the system does"""
    print("\n" + "=" * 80)
    print("🏥 HOLISTIC HEALTH AGENT - SYSTEM OVERVIEW")
    print("=" * 80)
    
    print("""
This system helps users with TWO key problems:

1. ❓ "I don't know WHAT's wrong with me"
   → 6 AI agents analyze symptoms using Dr. Berg's scientific approach
   
2. ❓ "I don't know WHICH SPECIALIST to see" ⭐ (Our Unique Feature)
   → Specialty Router maps symptoms → medical specialization
   
Example: "I'm fatigued with sugar cravings"
→ System recommends: "See an ENDOCRINOLOGIST (not Primary Care)"
→ Why: "Insulin resistance pattern - they specialize in metabolic disorders"
→ Tests: "Fasting insulin, HbA1c, thyroid panel"
    """)

def show_specializations():
    """Show the 9 medical specializations"""
    print("\n" + "=" * 80)
    print("🏥 MEDICAL SPECIALIZATIONS COVERED (9 total)")
    print("=" * 80)
    
    specializations = [
        ("Endocrinologist", "Hormones & metabolism", "Diabetes, thyroid, PCOS, hormone imbalances"),
        ("Gastroenterologist", "Digestive system", "IBS, IBD, acid reflux, gut health"),
        ("Cardiologist", "Heart & circulation", "High blood pressure, palpitations, chest pain"),
        ("Dermatologist", "Skin, hair, nails", "Rashes, acne, hair loss, skin conditions"),
        ("Neurologist", "Brain & nervous system", "Headaches, numbness, nerve pain"),
        ("Rheumatologist", "Joints & autoimmune", "Arthritis, lupus, autoimmune diseases"),
        ("Psychiatrist", "Mental health (MD)", "Depression, anxiety, mood disorders"),
        ("Hematologist", "Blood disorders", "Anemia, clotting issues, blood diseases"),
        ("Primary Care", "General health", "First point of contact, unclear symptoms")
    ]
    
    for i, (name, specialty, treats) in enumerate(specializations, 1):
        print(f"\n{i}. {name}")
        print(f"   Specialty: {specialty}")
        print(f"   Treats: {treats}")

def show_example_consultation():
    """Show complete consultation output"""
    print("\n" + "=" * 80)
    print("🎬 EXAMPLE: COMPLETE CONSULTATION")
    print("=" * 80)
    
    print("""
USER QUERY:
"I'm constantly fatigued with strong sugar cravings. I don't know if I 
should see an endocrinologist or primary care doctor."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ INTAKE AGENT:
Collects health profile through conversational interview
→ Output: Age, symptoms, diet, sleep, stress, medications

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2️⃣ DIAGNOSTIC AGENT:
Guides physical self-examination
→ Output: Tongue (white coating), Nails (brittle), Skin (dry patches)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3️⃣ SPECIALTY ROUTER ⭐ (OUR INNOVATION):

Recommended Medical Specialization: ENDOCRINOLOGIST

Reasoning:
• Fatigue + sugar cravings = insulin resistance pattern
• Endocrinology specializes in metabolic & hormone disorders
• Primary Care would just refer you anyway - save time!

What to expect:
✓ Fasting insulin & glucose (insulin resistance test)
✓ HbA1c (3-month blood sugar average)
✓ Thyroid panel (TSH, Free T3, Free T4)
✓ Possibly vitamin D, B12, magnesium levels

Urgency: SOON (1-2 weeks)
Confidence: 0.88

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4️⃣ KNOWLEDGE AGENT (Dr. Berg Style):

Biochemical Mechanism:
"When you eat carbs frequently, insulin stays elevated. Over time, cells 
become RESISTANT - they stop listening. Your pancreas makes MORE insulin 
to compensate.

High insulin:
1. BLOCKS fat burning → You can't access stored energy
2. CAUSES sugar cravings → Cells starving despite full stores

It's like having a full gas tank but the engine can't use the fuel."

Confidence: 0.78

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5️⃣ ROOT CAUSE AGENT (Systems Thinking):

Root Cause Cascade:
  High-carb diet + Frequent eating
    ↓
  Insulin constantly elevated
    ↓
  Insulin resistance develops
    ↓
  SYMPTOMS: Fatigue, cravings, weight gain

Vicious Cycle:
High insulin → Blocks magnesium → Poor sleep → Stress → 
More cortisol → Higher insulin (repeats)

Keystone Fix: Intermittent fasting + low-carb
(Breaks the insulin cycle at its source)

Confidence: 0.80

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

6️⃣ RECOMMENDER AGENT (Dr. Berg Precision):

MAGNESIUM SUPPLEMENTATION:
• Form: Magnesium Bisglycinate 400mg
  (NOT Oxide - only 4% absorbed, causes diarrhea)
• Timing: 30-60 minutes before bed
• Why: Stress depletes magnesium. Insulin blocks absorption.
  Magnesium is THE relaxation mineral.
• Food sources:
  - Pumpkin seeds: 150mg per ounce (best)
  - Spinach (cooked): 157mg per cup
  - Dark chocolate (85%): 64mg per ounce
• Duration: 3 months minimum to replenish tissues
• Safety: Start 200mg if sensitive. Avoid if kidney disease.

INTERMITTENT FASTING:
• Start: 14:10 (14 hours fasting, 10 hour eating)
• Progress to: 16:8 (skip breakfast, eat 12pm-8pm)
• Why: ONLY way to lower insulin. Low insulin = fat burning.

LOW-CARB:
• Target: 50g net carbs per day
• Remove: Cereal, bread, pasta, rice
• Add: Leafy greens (7-10 cups), healthy fats, protein

Expected Timeline:
Week 1-2: Better sleep, reduced cravings
Week 3-4: Stable energy, no afternoon crashes
Week 5-8: Significant energy improvement

Confidence: 0.75

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MEDICAL DISCLAIMER:
Educational information, NOT medical advice. Consult your doctor before 
making significant health changes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)

def show_key_features():
    """Show what makes this system special"""
    print("\n" + "=" * 80)
    print("🎯 KEY INNOVATIONS")
    print("=" * 80)
    
    print("""
1. SPECIALTY ROUTING ⭐ (Our Unique Feature)
   Problem: "I don't know which specialist to see"
   Solution: AI maps symptoms → correct medical specialization
   Value: Saves time, money, prevents wrong specialist visits

2. DR. BERG PRECISION (Not Generic Advice)
   ❌ Generic: "Take magnesium"
   ✅ Our System: "Magnesium Bisglycinate 400mg before bed (NOT Oxide - 4% absorbed)"
   
   Every recommendation includes:
   • Exact form (Bisglycinate vs Oxide matters!)
   • Precise dosage (400mg, not "some")
   • Timing (before bed, with food, etc.)
   • Food sources (pumpkin seeds 150mg/oz)
   • Duration (3 months)
   • Safety warnings (kidney disease contraindication)

3. SYSTEMS THINKING (Root Causes, Not Symptoms)
   ❌ Symptom treatment: "You have fatigue"
   ✅ Root cause: "Stress → Cortisol → Insulin → Mg deficiency → Fatigue"
   
   Shows cascade effects and vicious cycles

4. PRODUCTION SAFETY
   • 16 red flags with urgency levels (EMERGENCY_911, URGENT_24HR, SOON, MONITOR)
   • Confidence scoring (0.0-1.0) with escalation at <0.60
   • Agent self-awareness of limitations
   • Medical disclaimer always included

5. CLEAN ARCHITECTURE
   • Single source of truth (medical_knowledge_base.py)
   • No stale context between tasks
   • Clear agent boundaries
   • 9 medical specializations fully mapped
    """)

def show_how_it_works():
    """Explain the technology"""
    print("\n" + "=" * 80)
    print("🔧 HOW IT WORKS (No Training Required!)")
    print("=" * 80)
    
    print("""
We DON'T train the AI - we use Google's Gemini 2.5-flash-lite
(already trained on medical literature: PubMed, textbooks, research)

Our Approach:
┌─────────────────────────────────────────────────────────┐
│ Gemini 2.5-flash-lite (Pre-trained on medical data)    │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Our Prompt Engineering (Dr. Berg Style)                 │
│ "Explain like Dr. Berg: exact forms, dosages, timing"  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Our Knowledge Base (Single Source of Truth)             │
│ • 9 medical specializations                             │
│ • 16 red flags with urgency levels                      │
│ • Routing logic (symptom → specialist)                  │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ 6 Specialized Agents                                    │
│ Each = Gemini + Custom prompt + Tools                   │
└─────────────────────────────────────────────────────────┘

Key Insight: Prompt engineering DIRECTS pre-trained intelligence.
We're not training - we're INSTRUCTING with precision.
    """)

def show_testing_instructions():
    """Show how to test"""
    print("\n" + "=" * 80)
    print("🧪 HOW TO TEST")
    print("=" * 80)
    
    print("""
OPTION 1: See This Demo (No API Key Needed)
────────────────────────────────────────────
python quick_demo.py

Shows: Expected output quality, all features


OPTION 2: Test with Live API (Full Experience)
───────────────────────────────────────────────
1. Get API key: https://aistudio.google.com/apikey
2. Create .env file: cp .env.template .env
3. Add key to .env: GOOGLE_API_KEY=your-key-here
4. Run: python demo.py

Shows: Live Gemini responses with Dr. Berg style


OPTION 3: Validate Components
──────────────────────────────
python test_agents.py

Checks: Knowledge base, prompts, context engineering


WHERE TO FIND AGENTS:
────────────────────
/src/agents/
├── intake_agent.py          ← Health interview
├── diagnostic_agent.py      ← Physical examination guide
├── specialty_router_agent.py ← Specialization routing ⭐
├── knowledge_agent.py       ← Dr. Berg explanations
├── root_cause_agent.py      ← Systems thinking cascade
└── recommender_agent.py     ← Precise recommendations

/src/orchestrator.py         ← Coordinates all 6 agents
    """)

def main():
    """Run the quick demo"""
    print("\n")
    show_system_overview()
    input("\n▶️  Press ENTER to see specializations...")
    
    show_specializations()
    input("\n▶️  Press ENTER to see example consultation...")
    
    show_example_consultation()
    input("\n▶️  Press ENTER to see key features...")
    
    show_key_features()
    input("\n▶️  Press ENTER to see how it works...")
    
    show_how_it_works()
    input("\n▶️  Press ENTER to see testing instructions...")
    
    show_testing_instructions()
    
    print("\n" + "=" * 80)
    print("✅ DEMO COMPLETE!")
    print("=" * 80)
    print("""
🎯 Key Takeaways:
   1. Specialty routing solves "who do I see?" problem ⭐
   2. Dr. Berg precision (exact forms, dosages, timing)
   3. Systems thinking (root causes, not symptoms)
   4. Production-ready safety systems
   5. No ML training needed - prompt engineering!

📝 Next Steps:
   • Add GOOGLE_API_KEY to .env
   • Run: python demo.py
   • Experience live AI consultations!
    """)

if __name__ == "__main__":
    main()
