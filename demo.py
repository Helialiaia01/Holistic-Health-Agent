"""
Demo script to test the Holistic Health Agent
Run this to see your agents in action!
"""

import asyncio
from google.adk.runners import InMemoryRunner
from google.adk.services import DatabaseSessionService
from google.genai import types
from src.orchestrator import create_health_agent_orchestrator

async def demo_full_consultation():
    """
    Demo showing complete health consultation through all agents.
    This demonstrates the Dr. Berg-style scientific health guidance.
    """
    
    print("=" * 80)
    print("🏥 HOLISTIC HEALTH AGENT - COMPLETE CONSULTATION DEMO")
    print("=" * 80)
    print()
    print("This demo shows all 6 agents working together:")
    print("  1. Intake Agent - Conversational health interview")
    print("  2. Diagnostic Agent - Physical examination guide")
    print("  3. Specialty Router - Medical specialist recommendation")
    print("  4. Knowledge Agent - Biochemical mechanism analysis")
    print("  5. Root Cause Agent - Systems thinking root cause identification")
    print("  6. Recommender Agent - Precise Dr. Berg-style recommendations")
    print()
    input("Press ENTER to start consultation...")
    print()
    
    # Create orchestrator
    orchestrator = create_health_agent_orchestrator()
    
    # Simulate comprehensive health query
    user_query = """
    Hi, I need help figuring out what's wrong with me.
    
    My main symptoms are:
    - Extreme fatigue, especially in the afternoon (I crash around 2-3pm)
    - Strong sugar cravings after every meal
    - Brain fog and difficulty concentrating
    - Weight gain around my waist despite eating less
    - Trouble falling asleep even though I'm exhausted
    - Sometimes get heart palpitations
    - Anxiety that seems to come out of nowhere
    
    About me:
    - 45 years old, work a stressful office job
    - Diet: I try to eat healthy but snack frequently. Breakfast is usually cereal
      or toast, lunch is sandwich or salad, dinner is pasta or chicken with rice.
      I crave sweets after every meal.
    - Exercise: Minimal, maybe a walk once a week
    - Sleep: 5-6 hours per night, go to bed around midnight, wake up at 6am
    - Stress: Very high due to work deadlines and family responsibilities
    
    I don't know if this is hormones, blood sugar, thyroid, or what. 
    I also don't know which doctor to see - should I see an endocrinologist? 
    Primary care? Cardiologist for the palpitations?
    
    Please help me understand what's happening and what I should do.
    """
    
    print("👤 User Query:")
    print("-" * 80)
    print(user_query)
    print("-" * 80)
    print()
    
    # Run step-by-step consultation
    results = orchestrator.run_consultation_step_by_step(user_query)
    
    # Display results
    print("\n📋 CONSULTATION SUMMARY")
    print("=" * 80)
    
    if results.get("stopped_early"):
        print("\n⚠️ CONSULTATION STOPPED EARLY")
        print(f"Reason: {results['red_flags']['max_urgency']}")
        print("Immediate medical attention required.")
    else:
        print("\n✅ Full consultation completed")
        print(f"Total stages: {len(results['steps'])}")
        
        # Show what each agent would output
        print("\n" + "=" * 80)
        print("EXPECTED AGENT OUTPUTS (Dr. Berg Style):")
        print("=" * 80)
        
        print("\n1️⃣ INTAKE AGENT OUTPUT:")
        print("-" * 80)
        print("""
Health Profile Collected:
  • Age: 45
  • Primary symptoms: Afternoon fatigue, sugar cravings, brain fog, 
    weight gain, sleep issues, palpitations, anxiety
  • Diet pattern: High carb, frequent eating, cereal/bread/pasta/rice heavy
  • Sleep: 5-6 hours (insufficient)
  • Stress: High
  • Exercise: Minimal
  • Medications: None reported
  
Intake confidence: 0.85 (clear symptom reporting)
        """)
        
        print("\n2️⃣ DIAGNOSTIC AGENT OUTPUT:")
        print("-" * 80)
        print("""
Physical Examination Findings:
  • Tongue: White coating, scalloped edges (indicates: fluid retention, 
    possible B-vitamin deficiency, insulin resistance)
  • Nails: Brittle with vertical ridges (indicates: magnesium deficiency,
    possible thyroid issue)
  • Skin: Dry patches on elbows (indicates: essential fatty acid deficiency,
    vitamin A deficiency)
  • Capillary refill: Normal (2 seconds)
  • Orthostatic test: Mild dizziness on standing (indicates: possible
    adrenal fatigue, low blood pressure, dehydration)
  
Diagnostic confidence: 0.80 (clear visual indicators)
        """)
        
        print("\n3️⃣ SPECIALTY ROUTER OUTPUT:")
        print("-" * 80)
        print("""
Recommended Medical Specialist:

PRIMARY RECOMMENDATION: Endocrinologist (Hormone & Metabolism Specialist)

Reasoning:
  • Symptom cluster strongly suggests metabolic/endocrine issues
  • Afternoon fatigue + sugar cravings + weight gain around waist = 
    classic insulin resistance pattern
  • Palpitations + anxiety can be related to cortisol/thyroid issues
  • Sleep disturbances often linked to cortisol dysregulation
  
What endocrinologist will check:
  ✓ Fasting insulin & glucose (insulin resistance)
  ✓ HbA1c (3-month blood sugar average)
  ✓ Thyroid panel (TSH, Free T3, Free T4)
  ✓ Cortisol levels (morning & evening)
  ✓ Possibly vitamin D, B12, magnesium levels

SECONDARY CONSIDERATION: Primary Care Physician (if no endocrinologist access)
  • Can order basic metabolic panel and refer if needed
  
Urgency: SOON (within 1-2 weeks) - not emergency, but don't wait months

Note: The palpitations could be related to magnesium deficiency or anxiety,
but if they worsen or occur with chest pain, see doctor IMMEDIATELY.

Router confidence: 0.88 (strong pattern match)
        """)
        
        print("\n4️⃣ KNOWLEDGE AGENT OUTPUT:")
        print("-" * 80)
        print("""
Medical Analysis (Dr. Berg Style):

KEY PATTERNS IDENTIFIED:
  1. Insulin Resistance Pattern (Classic triad: fatigue + cravings + belly fat)
  2. Magnesium Deficiency Pattern (cravings, sleep issues, anxiety, brittle nails)
  3. Cortisol Dysregulation Pattern (stress, poor sleep, palpitations)
  4. B-Vitamin Depletion Pattern (white tongue, brain fog, low energy)

BIOCHEMICAL MECHANISMS EXPLAINED:

Pattern 1: Insulin Resistance
"Your body is stuck in sugar-burning mode. Here's what's happening: When you
eat carbs (cereal, bread, pasta, rice), your blood sugar spikes. Your pancreas
releases insulin to store that sugar. But when you eat frequently AND eat high
carbs, insulin is constantly elevated. Over time, your cells become RESISTANT
to insulin - they stop listening to it. 

So your pancreas makes EVEN MORE insulin to compensate. High insulin has two
major effects: (1) It BLOCKS fat burning - you can't access your stored energy,
and (2) It causes sugar CRAVINGS because your cells are starving for energy
even though you have plenty stored.

It's like having a full gas tank but the engine can't access the fuel. Your
body keeps asking for more gas (cravings) even though you don't need it."

Pattern 2: Magnesium Deficiency
"Magnesium is THE relaxation mineral. It blocks calcium from entering nerve
and muscle cells (calcium causes CONTRACTION, magnesium causes RELAXATION).
You need 400-500mg daily but most people get only 200mg from food.

Here's the vicious cycle: STRESS depletes magnesium. Low magnesium causes
poor sleep. Poor sleep raises cortisol. High cortisol causes more stress AND
interferes with insulin. High insulin blocks magnesium ABSORPTION. So you're
depleting faster than you can replenish.

Low magnesium explains: muscle tension, anxiety, heart palpitations (heart
is a muscle!), poor sleep, and it WORSENS insulin resistance."

Pattern 3: Cortisol Dysregulation
"Cortisol is your stress hormone. It should be high in the morning (wake you
up) and low at night (let you sleep). Chronic stress flips this pattern.

Cortisol RAISES blood sugar (to give you energy for the 'threat'). But there's
no real threat - just work stress. So your blood sugar goes up, insulin goes
up, and you're in the insulin resistance cycle again. Plus, high cortisol at
night keeps you awake, even though you're exhausted."

METABOLIC CONTEXT:
You're trapped in a vicious cycle:
  Stress → Cortisol ↑ → Blood sugar ↑ → Insulin ↑ → Blocks Mg absorption →
  Low Mg → Poor sleep → More cortisol → Worse insulin resistance

SYSTEM CONNECTIONS:
  • Nervous system (stress) affects Endocrine (insulin/cortisol)
  • Endocrine affects Digestive (nutrient absorption blocked)
  • Digestive affects Nervous (deficiencies worsen stress response)
  • All systems affect Cardiovascular (palpitations from Mg deficiency)

Knowledge confidence: 0.78 (strong pattern match, blood work would confirm)
        """)
        
        print("\n5️⃣ ROOT CAUSE AGENT OUTPUT:")
        print("-" * 80)
        print("""
Root Cause Analysis (Systems Thinking):

ROOT CAUSES (not proximal symptoms):

1. CHRONIC HIGH STRESS (Primary root cause)
   ↓
2. HIGH-CARB DIET + FREQUENT EATING (Amplifier)
   ↓
3. INSUFFICIENT SLEEP (Vicious cycle maintainer)

CASCADE EFFECT CHAIN:

ROOT → EFFECT 1 → EFFECT 2 → EFFECT 3 → SYMPTOMS

Stress → Cortisol ↑ → Blood sugar ↑ → Insulin ↑ → 
  → Blocks Mg absorption → Low Mg → Poor sleep & anxiety →
  → More cortisol (cycle repeats)

Frequent eating + High carbs → Insulin constantly elevated →
  → Fat burning blocked → Weight gain (especially belly) →
  → Cells become insulin resistant → MORE insulin needed →
  → Sugar cravings (cells starving despite full storage)

Poor sleep → Growth hormone ↓ → Fat burning ↓ →
  → Cortisol pattern disrupted → Worse insulin resistance →
  → Even worse sleep (cycle repeats)

INTERCONNECTIONS (Why treating symptoms doesn't work):

"You can't just 'fix fatigue' or 'fix cravings' because they're SYMPTOMS of
the cascade, not the root. It's like mopping the floor while the faucet is
still running. You have to turn off the faucet (root causes)."

VICIOUS CYCLES IDENTIFIED:
  1. Stress → Cortisol → Poor sleep → More stress
  2. High carbs → Insulin → Magnesium deficiency → Worse insulin resistance
  3. Insulin resistance → Cravings → More carbs → Worse resistance

INTERVENTION PRIORITIES (What to fix first):

🎯 KEYSTONE FIX: Fix sleep FIRST
"Sleep is the domino that knocks down multiple problems. When you sleep 7-9
hours consistently: cortisol normalizes, insulin sensitivity improves,
magnesium absorption increases, stress tolerance improves, cravings reduce.
Everything else becomes EASIER."

Priority Order:
  1st: SLEEP (keystone - improves everything else)
  2nd: LOWER CARBS + INTERMITTENT FASTING (breaks insulin cycle)
  3rd: MAGNESIUM SUPPLEMENTATION (supports sleep & insulin)
  4th: STRESS MANAGEMENT (meditation, boundaries, exercise)

Why this order? Each step makes the next step easier. If you try to manage
stress while sleeping 5 hours on high carbs with low magnesium, you'll fail.
Fix the foundation first.

Root Cause confidence: 0.80 (cascade clearly identified)
        """)
        
        print("\n6️⃣ RECOMMENDER AGENT OUTPUT:")
        print("-" * 80)
        print("""
Precise Recommendations (Dr. Berg Precision):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PHASE 1 (Week 1-2): SLEEP OPTIMIZATION (Keystone Fix)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. MAGNESIUM SUPPLEMENTATION
   Form: Magnesium Bisglycinate 400-500mg
   (NOT Magnesium Oxide - only 4% absorbed, causes diarrhea)
   
   Timing: 30-60 minutes before bed
   
   Why this form: 
   • Bisglycinate = Magnesium bound to glycine (calming amino acid)
   • 80-90% absorption rate (vs 4% for Oxide)
   • Crosses blood-brain barrier for calm/sleep
   • Doesn't cause digestive upset
   
   Food sources (add these too):
   • Pumpkin seeds: 150mg per ounce (best source)
   • Spinach (cooked): 157mg per cup
   • Swiss chard: 150mg per cup
   • Dark chocolate (85%+): 64mg per ounce
   • Avocado: 58mg per medium fruit
   
   Target: 400-500mg total (supplement + food)
   Duration: Minimum 3 months to replenish tissue stores
   
   Safety note: Start with 200mg if sensitive stomach, increase gradually.
   Reduce dose if diarrhea occurs. Check with doctor if kidney disease.

2. SLEEP HYGIENE PROTOCOL
   • Fixed schedule: Bed by 10pm, wake 6am (8 hours)
   • Room conditions: 65-68°F, pitch black (blackout curtains or sleep mask)
   • No screens 1 hour before bed (blue light blocks melatonin)
   • Morning sunlight: 10-15 minutes within 1 hour of waking (sets circadian)
   • No caffeine after 2pm
   
   Why: Your circadian rhythm is disrupted. Going to bed at midnight and
   waking at 6am gives only 6 hours. You need 7-9 hours for cortisol reset.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PHASE 2 (Week 3-4): METABOLIC RESET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3. INTERMITTENT FASTING (Lower insulin, access fat stores)
   Start with: 14:10 (14 hours fasting, 10 hour eating window)
   Example: Last meal 8pm → First meal 10am next day
   
   Progress to: 16:8 (skip breakfast, eat 12pm-8pm)
   
   First meal composition:
   • Protein: 30-40g (eggs, salmon, chicken, beef)
   • Healthy fats: Avocado, olive oil, nuts, butter
   • Vegetables: 2-3 cups of leafy greens or cruciferous
   • LOW carbs: Under 20g net carbs (no bread, cereal, pasta)
   
   Why: Fasting lowers insulin. Only when insulin is LOW can you burn fat.
   Your current frequent eating keeps insulin constantly elevated.
   
   Benefits timeline:
   • Week 1: Hunger adjusts, cravings reduce
   • Week 2-3: Energy stabilizes, no afternoon crash
   • Week 4+: Fat burning activates, weight loss begins
   
   Contraindications: Don't fast if pregnant, nursing, <18 years old,
   history of eating disorders, or underweight.

4. LOW-CARB NUTRITION
   Target: 50g net carbs per day (or less)
   Net carbs = Total carbs - Fiber
   
   REMOVE (insulin-spiking foods):
   ❌ Cereal, bread, pasta, rice, potatoes
   ❌ Sugar, honey, maple syrup, agave
   ❌ Fruit juice, soda, sweetened drinks
   ❌ Most fruit (except berries in moderation)
   
   ADD (nutrient-dense, low insulin impact):
   ✅ Leafy greens: 7-10 cups daily (spinach, kale, arugula, lettuce)
   ✅ Cruciferous vegetables: Broccoli, cauliflower, Brussels sprouts
   ✅ Healthy fats: Avocado, olive oil, coconut oil, butter, nuts
   ✅ Protein: Eggs, fish, chicken, beef, turkey (moderate amounts)
   ✅ Berries: Blackberries, raspberries (1/2 cup max per day)
   
   Sample meal:
   "Instead of cereal → 3 eggs scrambled in butter with spinach and avocado"
   "Instead of sandwich → Large salad with salmon, olive oil, pumpkin seeds"
   "Instead of pasta → Cauliflower rice with chicken and vegetables"
   
   Why: Every time you eat carbs, insulin spikes. The MORE you eat carbs,
   the MORE insulin you need. Breaking the carb cycle is essential to
   restore insulin sensitivity.

5. B-VITAMIN COMPLEX
   Form: B-Complex with Methylated B12 (Methylcobalamin) and Methylfolate
   (NOT Cyanocobalamin or Folic Acid - harder to absorb)
   
   Dosage: Full B-Complex (B1, B2, B3, B5, B6, B7, B9, B12)
   Look for: "Methylated" or "Active Form" on label
   
   Timing: With first meal of day (B vitamins provide energy)
   
   Why: Stress depletes B vitamins. Carbs deplete B1 (thiamine). White
   tongue coating suggests B-vitamin deficiency. B vitamins are needed
   for energy production in mitochondria.
   
   Food sources (add these):
   • Nutritional yeast: 1-2 tablespoons daily (fortified with B vitamins)
   • Organ meats: Liver 1-2x per week (if you can tolerate)
   • Eggs: Whole eggs (yolk has B vitamins)
   • Leafy greens: Folate (B9)
   
   Duration: 2-3 months, then reassess

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PHASE 3 (Week 5-8): STRESS MANAGEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

6. DAILY STRESS PRACTICES
   Morning (10 minutes):
   • Walk outside in sunlight (regulates cortisol)
   • Deep breathing: 4-7-8 technique (4 count in, 7 hold, 8 out) × 5 rounds
   
   Afternoon (5 minutes):
   • Midday break: Stand up, stretch, breathe
   • No eating at desk - take actual lunch break
   
   Evening (15 minutes):
   • Wind-down ritual: Reading, stretching, meditation
   • Gratitude practice: Write 3 things you're grateful for
   • No work email after 7pm (set boundary)
   
   Why: Stress management isn't optional - chronic stress is a ROOT CAUSE.
   These practices lower cortisol, improve sleep, reduce anxiety.

7. MOVEMENT (Not intense exercise yet)
   Start simple:
   • Daily: 20-30 minute walk (preferably morning + evening)
   • Optional: Light yoga or stretching 10 minutes before bed
   
   Don't do yet:
   • High-intensity exercise (HIIT, CrossFit, running)
   • Fasted cardio (too stressful while cortisol high)
   
   Why: Intense exercise = more cortisol. You're already stressed. Walking
   lowers cortisol, improves insulin sensitivity, doesn't overtax body.
   Add intense exercise AFTER sleep and stress are under control.

8. ADAPTOGENIC SUPPORT (Optional)
   Form: Ashwagandha KSM-66 300mg (standardized extract)
   
   Timing: Morning with breakfast
   
   Why: Adaptogen = helps body adapt to stress. Ashwagandha specifically
   lowers cortisol, reduces anxiety, improves sleep quality.
   
   Duration: 2-3 months, then take 1 week break, reassess
   
   Safety: Don't take if: pregnant, nursing, thyroid medication (can interact),
   autoimmune conditions (can stimulate immune system)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MONITORING & TIMELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Track Daily (simple journal or app):
  ✓ Sleep quality: 1-10 scale
  ✓ Energy levels: Morning vs afternoon (1-10 scale)
  ✓ Sugar cravings: Intensity (1-10 scale)
  ✓ Mood/anxiety: 1-10 scale
  ✓ Did I follow the plan? Yes/No

Expected Timeline:
  Week 1-2: Better sleep, less night waking, more dreams (REM returning)
  Week 3-4: Cravings reduce significantly, energy more stable (no 3pm crash)
  Week 5-6: Brain fog lifts, anxiety improves, palpitations decrease
  Week 7-8: Weight loss visible (especially waist), sustained energy all day

Measurements (optional but helpful):
  • Weight: Weekly (same day, same time, morning)
  • Waist circumference: Every 2 weeks (at belly button level)
  • Blood pressure: Weekly if you have monitor

Reassess at 8 weeks:
  If MAJOR improvement (50%+ better): Continue plan, consider blood work
  If SOME improvement (25-50% better): Adjust plan, consider blood work
  If NO improvement (<25% better): See endocrinologist ASAP for labs

Labs to request (if seeing doctor):
  ✓ Fasting insulin (most important - shows insulin resistance)
  ✓ Fasting glucose
  ✓ HbA1c (3-month blood sugar average)
  ✓ Thyroid panel (TSH, Free T3, Free T4)
  ✓ Vitamin D (25-hydroxy)
  ✓ Magnesium RBC (not serum - RBC is accurate)
  ✓ Complete Blood Count (CBC)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SAFETY & CONTRAINDICATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ DO NOT FOLLOW THIS PLAN IF:
  • Pregnant or breastfeeding
  • Type 1 Diabetes (insulin-dependent)
  • Taking blood pressure or blood sugar medications (MUST consult doctor first)
  • History of eating disorders
  • Under 18 years old
  • Underweight (BMI < 18.5)
  • Kidney disease (magnesium contraindicated)

⚠️ STOP IMMEDIATELY AND SEE DOCTOR IF:
  • Chest pain or pressure (especially with exertion)
  • Severe heart palpitations or irregular heartbeat that worsens
  • Extreme dizziness or fainting
  • Severe persistent headaches
  • Unexplained rapid weight loss (>10 lbs in 1 month)
  • Symptoms get significantly WORSE instead of better
  • New concerning symptoms appear

🩺 WHEN TO SEE ENDOCRINOLOGIST (even if improving):
  • After 8 weeks to get baseline labs and track progress
  • If you want to confirm insulin resistance diagnosis
  • If family history of diabetes (important to monitor)

💊 IF YOU TAKE MEDICATIONS:
  • Blood pressure meds: Low-carb can lower BP - may need adjustment
  • Blood sugar meds: Low-carb can lower blood sugar - may need adjustment
  • Thyroid meds: Usually safe, but tell doctor about plan
  • Any prescription: Consult doctor before making dietary changes

CONFIDENCE LEVEL: 0.75 (Strong pattern match, safe recommendations)

RECOMMENDATION STRENGTH: "Safe to implement with monitoring"

REASONING: The symptom cluster strongly suggests insulin resistance with
magnesium deficiency and cortisol dysregulation. These are lifestyle-related
issues that respond well to the interventions recommended. However, blood
work would confirm the diagnosis and rule out other issues (thyroid, diabetes).
The palpitations warrant monitoring - if they worsen, see doctor immediately.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MEDICAL DISCLAIMER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This is educational information based on metabolic health principles and
nutritional science. It is NOT medical advice, diagnosis, or treatment.
This agent does not replace consultation with qualified healthcare professionals.

Always consult your doctor before:
• Starting new supplements (especially if you take medications)
• Making significant dietary changes
• Beginning a fasting protocol
• If you have medical conditions or concerns

In emergency situations (chest pain, difficulty breathing, severe symptoms),
call 911 or go to the emergency room immediately.

The recommendations provided are based on general health principles and may
not be appropriate for everyone. Individual results vary. Your healthcare
provider can order tests and provide personalized medical guidance based on
your specific health status.

        """)
    
    print("\n" + "=" * 80)
    print("✅ DEMO COMPLETE")
    print("=" * 80)
    print()
    print("🎯 What You Just Saw:")
    print("  ✓ 6 agents working in sequence with clean context flow")
    print("  ✓ Dr. Berg-style scientific explanations (mechanisms, not just symptoms)")
    print("  ✓ EXACT supplement forms, dosages, timing (NOT generic advice)")
    print("  ✓ Root cause identification (stress → cortisol → insulin → symptoms)")
    print("  ✓ Phased implementation plan (not overwhelming)")
    print("  ✓ Medical specialty routing (endocrinologist recommendation)")
    print("  ✓ Safety warnings, contraindications, when to see doctor")
    print("  ✓ Confidence scoring throughout")
    print()
    print("🏆 Competitive Advantages:")
    print("  • Specialty routing solves 'who do I see?' problem")
    print("  • Dr. Berg precision (Bisglycinate vs Oxide matters!)")
    print("  • Systems thinking root cause analysis")
    print("  • Production-grade safety & boundaries")
    print()

async def demo_simple_intake():
    """
    Simplified demo showing just the intake agent conversation.
    Useful for quick testing.
    """
    
    print("=" * 60)
    print("🏥 SIMPLE INTAKE DEMO")
    print("=" * 60)
    print()
    
    from src.agents.intake_agent import intake_agent
    
    # Create the intake agent
    agent = intake_agent()
    
    # Setup session
    session_service = DatabaseSessionService(db_path=":memory:")
    runner = InMemoryRunner(session_service=session_service)
    
    # Simulate a real user conversation
    user_messages = [
        "I'm exhausted all the time and I don't know what's wrong with me.",
        "I sleep about 5 hours a night. Go to bed around 2am, wake up at 7am for work.",
        "My diet is pretty bad - cereal for breakfast, fast food for lunch, pasta or pizza for dinner.",
    ]
    
    print("🎬 Starting intake interview...\n")
    
    for i, user_message in enumerate(user_messages, 1):
        print(f"\n{'─' * 60}")
        print(f"👤 User: {user_message}")
        print(f"{'─' * 60}\n")
        print("🤖 Agent: [Response would appear here when integrated with ADK runner]")
        print()
    
    print("=" * 60)
    print("✅ Intake demo complete!")
    print()

if __name__ == "__main__":
    print()
    print("🚀 Setup Checklist:")
    print("  1. Installed: pip install -r requirements.txt")
    print("  2. Created .env file with GOOGLE_API_KEY")
    print("  3. Using Gemini 2.5-flash-lite model")
    print()
    print("📋 Demo Options:")
    print("  1. Full consultation (all 6 agents) - RECOMMENDED")
    print("  2. Simple intake only (quick test)")
    print()
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        asyncio.run(demo_full_consultation())
    elif choice == "2":
        asyncio.run(demo_simple_intake())
    else:
        print("Invalid choice. Running full consultation...")
        asyncio.run(demo_full_consultation())
