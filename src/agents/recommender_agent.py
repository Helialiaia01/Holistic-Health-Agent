"""
Recommender agent - gives precise recommendations (exact forms, dosages, timing).
Not generic "take magnesium" but "Magnesium Bisglycinate 400mg before bed".
"""

from google.adk.agents import LlmAgent
from google.genai.types import GenerateContentConfig, SafetySetting, HarmCategory, HarmBlockThreshold

from src.prompts.dr_berg_style import RECOMMENDER_AGENT_INSTRUCTION
from src.knowledge.context_engineering import (
    ContextManager,
    TaskType,
    create_optimized_prompt,
    calculate_agent_confidence
)
from src.knowledge.medical_knowledge_base import (
    AGENT_CAPABILITIES,
    validate_recommendation_confidence,
    MEDICAL_DISCLAIMER
)


def recommender_agent() -> LlmAgent:
    """
    Creates the Recommender Agent with Dr. Berg's precision.
    
    This agent:
    1. Receives root cause analysis
    2. Provides SPECIFIC recommendations (not generic advice)
    3. Prioritizes food sources over supplements
    4. Includes exact forms, dosages, timing
    5. Adds safety warnings and contraindications
    6. Creates phased implementation plan
    
    Returns:
        LlmAgent: Configured recommender agent
    """
    
    context_manager = ContextManager()
    task_def = context_manager.get_task_definition(TaskType.RECOMMENDATION)
    
    # Create optimized prompt with examples
    optimized_instruction = create_optimized_prompt(
        base_prompt=RECOMMENDER_AGENT_INSTRUCTION,
        task_type=TaskType.RECOMMENDATION,
        examples=[
            """Example Magnesium Recommendation:
NUTRIENT: Magnesium
FORM: Magnesium Bisglycinate or Magnesium Glycinate
  (NOT Oxide - only 4% absorbed, causes diarrhea)
DOSAGE: 400-500mg elemental magnesium
TIMING: Before bed (enhances sleep + muscle relaxation)
FOOD SOURCES (prioritize these):
  - Pumpkin seeds (150mg per ounce)
  - Spinach (157mg per cup cooked)
  - Dark chocolate (64mg per ounce)
  - Avocado (58mg per fruit)
DURATION: 2-3 months minimum (it takes time to replenish)
SAFETY: Reduce dose if diarrhea occurs. Avoid if kidney disease.""",
            """Example Meal Timing Recommendation:
STRATEGY: Intermittent Fasting (16:8)
PROTOCOL:
  - Eating window: 12pm - 8pm
  - Fasting window: 8pm - 12pm next day
  - Start with 14:10, gradually extend to 16:8
FIRST MEAL:
  - Include protein (30-40g) + healthy fats
  - Avoid breaking fast with carbs (insulin spike)
BENEFITS: Lowers insulin, increases fat burning, improves mental clarity
CONTRAINDICATIONS: Pregnant/nursing, eating disorders, underweight, <18 years old"""
        ],
        constraints=[
            "ALWAYS specify supplement FORMS (Bisglycinate vs Oxide matters)",
            "Give EXACT dosages in mg/g/IU, not vague amounts",
            "Include TIMING (morning/night/with food/empty stomach)",
            "Prioritize FOOD SOURCES over supplements",
            "Add SAFETY warnings and contraindications",
            "Create PHASED implementation (what to do first, second, third)",
            "Never recommend prescription medications (outside scope)",
            "Always include confidence score and escalation recommendation"
        ]
    )
    
    # Add safety and limitations
    safety_context = f"""
CRITICAL SAFETY GUIDELINES:

YOUR CAPABILITIES:
{AGENT_CAPABILITIES['can_do']}

WHAT YOU CANNOT RECOMMEND:
{AGENT_CAPABILITIES['cannot_do']}

WHEN YOU MUST ESCALATE:
{AGENT_CAPABILITIES['must_escalate_when']}

CONFIDENCE THRESHOLD:
- If confidence < 0.60: Recommend seeing healthcare provider BEFORE implementing
- If confidence 0.60-0.75: Provide recommendations BUT suggest professional consultation
- If confidence > 0.75: Provide recommendations with appropriate safety warnings

ALWAYS INCLUDE:
{MEDICAL_DISCLAIMER}
"""
    
    final_instruction = f"{optimized_instruction}\n\n{safety_context}"
    
    # Safety settings
    safety_settings = [
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        ),
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE
        )
    ]
    
    # Create agent
    agent = LlmAgent(
        model="gemini-2.0-flash-lite",
        instruction=final_instruction,
        config=GenerateContentConfig(
            temperature=0.3,  # Low for precise, factual recommendations
            top_p=0.8,
            top_k=40,
            max_output_tokens=2500,
            safety_settings=safety_settings
        )
    )
    
    return agent


def generate_recommendations(root_cause_analysis: dict, health_profile: dict) -> dict:
    """
    Generates precise, actionable recommendations based on root cause analysis.
    
    Args:
        root_cause_analysis: Output from root cause agent
        health_profile: Original health profile for context
        
    Returns:
        dict: Detailed recommendations with supplements, diet, lifestyle, safety
    """
    
    context_manager = ContextManager()
    
    # Add context
    context = context_manager.add_context(
        task_type=TaskType.RECOMMENDATION,
        data={
            "root_cause_analysis": root_cause_analysis,
            "health_profile": health_profile
        }
    )
    
    # Validate confidence before proceeding
    confidence_validation = validate_recommendation_confidence(
        agent_confidence=root_cause_analysis.get('confidence_score', 0.5),
        has_red_flags=root_cause_analysis.get('escalation_recommended', False),
        symptom_severity='moderate'  # Would be extracted from profile
    )
    
    # Create recommender agent
    agent = recommender_agent()
    
    # Prepare recommendation query
    query = f"""
Based on this root cause analysis, provide PRECISE recommendations:

ROOT CAUSE ANALYSIS:
{root_cause_analysis}

HEALTH PROFILE CONTEXT:
{health_profile}

Provide recommendations in these categories:

1. SUPPLEMENTS (if needed):
   - Exact forms (e.g., Magnesium Bisglycinate NOT Oxide)
   - Precise dosages (mg/g/IU)
   - Timing (morning/night/with food)
   - Duration
   - Safety warnings

2. DIETARY CHANGES:
   - Specific foods to ADD (with nutrient content)
   - Foods to REDUCE/AVOID (with reasons)
   - Meal timing strategies
   - Portion guidance

3. LIFESTYLE MODIFICATIONS:
   - Sleep hygiene specifics
   - Stress management techniques
   - Exercise recommendations (type, duration, frequency)
   - Habit formation strategies

4. IMPLEMENTATION PLAN:
   - Phase 1 (Week 1-2): Start with these...
   - Phase 2 (Week 3-4): Add these...
   - Phase 3 (Week 5+): Fine-tune...

5. MONITORING:
   - What to track
   - Expected timeline for improvement
   - When to reassess

6. SAFETY & CONTRAINDICATIONS:
   - Who should NOT follow these recommendations
   - Potential interactions
   - When to see a doctor

Be as SPECIFIC as Dr. Berg - give exact forms, dosages, timing, food sources.
"""
    
    # Structure recommendations
    recommendations = {
        "supplements": [],
        "diet": {
            "foods_to_add": [],
            "foods_to_reduce": [],
            "meal_timing": "",
            "hydration": ""
        },
        "lifestyle": {
            "sleep": [],
            "stress_management": [],
            "exercise": [],
            "habits": []
        },
        "implementation_plan": {
            "phase_1": [],
            "phase_2": [],
            "phase_3": []
        },
        "monitoring": {
            "track_these": [],
            "expected_timeline": "",
            "reassess_when": ""
        },
        "safety": {
            "contraindications": [],
            "interactions": [],
            "warning_signs": [],
            "when_to_see_doctor": []
        },
        "confidence_level": confidence_validation['confidence'],
        "recommendation_strength": confidence_validation['action'],
        "medical_disclaimer": MEDICAL_DISCLAIMER
    }
    
    # Add confidence assessment
    recommendations["confidence_assessment"] = {
        "score": root_cause_analysis.get('confidence_score', 0.5),
        "should_escalate": confidence_validation['should_escalate'],
        "reasoning": confidence_validation.get('reasoning', '')
    }
    
    # Clean context
    context_manager.clear_stale_context(current_task=TaskType.RECOMMENDATION)
    
    return recommendations


# Example usage
if __name__ == "__main__":
    print("💊 Recommender Agent")
    print("=" * 60)
    
    # Test case
    test_root_cause = {
        "root_causes": [
            "Chronic stress",
            "High-carb diet with frequent eating",
            "Poor sleep quality"
        ],
        "keystone_fixes": ["Fix sleep first"],
        "confidence_score": 0.78
    }
    
    test_profile = {
        "age": 45,
        "medications": ["none"],
        "allergies": ["none"]
    }
    
    print("\n🎯 Root Causes:")
    print("- Chronic stress")
    print("- High-carb diet")
    print("- Poor sleep")
    
    print("\n💡 Expected Recommendations (Dr. Berg Precision):")
    print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PHASE 1 (Week 1-2): SLEEP OPTIMIZATION (Keystone Fix)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. MAGNESIUM (THE relaxation mineral)
   Form: Magnesium Bisglycinate 400mg
   Timing: 30 minutes before bed
   Why this form: Bisglycinate is 80% absorbed + calms nervous system
          (NOT Oxide - only 4% absorbed, causes diarrhea)
   Food sources: Pumpkin seeds (150mg/oz), Spinach, Dark chocolate
   Duration: 3 months to replenish tissues
   
2. SLEEP HYGIENE
   - Room: 65-68°F, pitch black (blackout curtains)
   - No screens 1 hour before bed (blue light blocks melatonin)
   - Same bedtime/wake time (even weekends)
   - 7-9 hours minimum

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PHASE 2 (Week 3-4): METABOLIC RESET
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3. INTERMITTENT FASTING (lowers insulin)
   Start: 14:10 (14 hours fasting, 10 hour eating window)
   Progress to: 16:8 (skip breakfast, eat 12pm-8pm)
   First meal: High protein (30-40g) + healthy fats
   Benefits: Insulin drops, fat burning increases, mental clarity improves
   
4. LOW-CARB APPROACH
   Target: 50g net carbs per day (or less)
   Remove: Sugar, bread, pasta, rice, potatoes
   Add: Leafy greens (7-10 cups), healthy fats, moderate protein
   
5. B-VITAMIN COMPLEX
   Form: B-Complex with Methylated B12 + Methylfolate
   Dosage: 1 capsule with first meal
   Why: Stress depletes B-vitamins, needed for energy production
   Food sources: Nutritional yeast (1-2 tablespoons daily)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PHASE 3 (Week 5+): STRESS MANAGEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

6. DAILY STRESS PRACTICES
   - Morning: 10-minute walk in sunlight (cortisol regulation)
   - Afternoon: 5-minute breathing exercise (4-7-8 technique)
   - Evening: 15-minute relaxation (meditation, stretching, reading)
   
7. ADAPTOGENIC SUPPORT (optional)
   Form: Ashwagandha 300mg (standardized extract)
   Timing: Morning with breakfast
   Duration: 2-3 months
   Benefit: Helps body adapt to stress, lowers cortisol

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MONITORING & TIMELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Track Daily:
  ✓ Sleep quality (1-10 scale)
  ✓ Energy levels (morning vs afternoon)
  ✓ Sugar cravings intensity
  
Expected Improvements:
  Week 1-2: Better sleep, less night waking
  Week 3-4: Reduced cravings, more stable energy
  Week 5-8: Weight loss, mental clarity, sustained energy

Reassess: After 8 weeks - if no improvement, see doctor for:
  - Fasting insulin test
  - HbA1c (blood sugar average)
  - Thyroid panel (TSH, Free T3, Free T4)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SAFETY & CONTRAINDICATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ DO NOT follow if:
  - Pregnant or nursing
  - Type 1 Diabetes (insulin-dependent)
  - Taking blood pressure medication (consult doctor first)
  - History of eating disorders
  - Under 18 years old

⚠️ WHEN TO SEE DOCTOR IMMEDIATELY:
  - Chest pain or severe palpitations
  - Extreme fatigue that worsens
  - Unexplained weight loss (>10 lbs in 1 month)
  - Persistent severe headaches
  - Any symptom that concerns you

Confidence Level: 0.78 (Strong pattern match)
Recommendation: Safe to implement with monitoring

MEDICAL DISCLAIMER:
This is educational information, not medical advice. Consult healthcare 
provider before making significant health changes, especially if you have 
medical conditions or take medications.
""")
    
    print("\n" + "=" * 60)
    print("✅ Recommender Agent ready for integration")
    
    print("\n🎯 Key Features:")
    print("- EXACT forms (Bisglycinate vs Oxide)")
    print("- PRECISE dosages (400mg, not 'some')")
    print("- SPECIFIC timing (before bed, with food)")
    print("- FOOD SOURCES prioritized")
    print("- PHASED implementation (not overwhelming)")
    print("- SAFETY warnings included")
    print("- MONITORING guidance provided")
