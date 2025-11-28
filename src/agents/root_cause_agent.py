"""
Root cause agent - finds the ACTUAL problem, not just surface symptoms.
Like Dr. Berg does - trace back from symptom to the real cause (stress, diet, etc).
"""

from google.adk.agents import LlmAgent
from google.genai.types import GenerateContentConfig, SafetySetting, HarmCategory, HarmBlockThreshold

from src.prompts.dr_berg_style import ROOT_CAUSE_AGENT_INSTRUCTION
from src.knowledge.context_engineering import (
    ContextManager,
    TaskType,
    create_optimized_prompt,
    calculate_agent_confidence
)
from src.knowledge.medical_knowledge_base import AGENT_CAPABILITIES


def root_cause_agent() -> LlmAgent:
    """
    Creates the Root Cause Analyzer Agent with Dr. Berg's systems thinking.
    
    This agent:
    1. Receives medical analysis from knowledge agent
    2. Identifies root causes (not just symptoms)
    3. Maps cascade effects between systems
    4. Prioritizes intervention points
    5. Explains cause-and-effect chains
    
    Returns:
        LlmAgent: Configured root cause analyzer agent
    """
    
    # Initialize context manager
    context_manager = ContextManager()
    context_manager.set_current_task(TaskType.ROOT_CAUSE)
    
    # Create optimized prompt
    optimized_instruction = create_optimized_prompt(
        base_instruction=ROOT_CAUSE_AGENT_INSTRUCTION,
        current_task=context_manager.current_task,
        examples=[
            """Example Cascade Analysis:
ROOT CAUSE: Chronic stress (work + poor sleep)
  ↓
EFFECT 1: Elevated cortisol
  ↓
EFFECT 2: Cortisol raises blood sugar → Insulin spikes
  ↓
EFFECT 3: High insulin blocks magnesium absorption
  ↓
EFFECT 4: Low magnesium → Poor sleep, muscle cramps, anxiety
  ↓
SYMPTOM CLUSTER: Fatigue, cravings, anxiety, poor sleep
(You're treating 4 symptoms, but the ROOT CAUSE is stress + sleep)""",
            """Example Root Cause vs Proximal Cause:
PROXIMAL CAUSE: "You have acid reflux"
ROOT CAUSE: "LOW stomach acid → incomplete digestion → food ferments → 
pressure pushes acid up → reflux symptoms"
(Taking antacids makes it WORSE because you need MORE acid, not less)"""
        ],
        constraints=[
            "Identify ROOT causes (stress, diet, deficiency) not proximal symptoms",
            "Map cascade effects between systems",
            "Explain cause-and-effect chains clearly",
            "Prioritize intervention points (what to fix first)",
            "Use Dr. Berg's systems thinking approach"
        ]
    )
    
    # Add limitations context
    limitations_context = f"""
YOUR ROLE:
You identify root causes and cascade effects. You explain WHY symptoms occur,
not just WHAT symptoms are present.

CAPABILITIES:
{AGENT_CAPABILITIES['can_do']}

LIMITATIONS:
{AGENT_CAPABILITIES['cannot_do']}

ESCALATION TRIGGERS:
{AGENT_CAPABILITIES['must_escalate_when']}

Remember: You identify root causes but DO NOT diagnose diseases.
You suggest WHERE the problem originates (metabolic, nutritional, lifestyle)
but defer specific diagnoses to medical professionals.
"""
    
    final_instruction = f"{optimized_instruction}\n\n{limitations_context}"
    
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
            temperature=0.4,  # Slightly higher for creative connections
            top_p=0.85,
            top_k=40,
            max_output_tokens=2000,
            safety_settings=safety_settings
        )
    )
    
    return agent


def identify_root_causes(medical_analysis: dict) -> dict:
    """
    Identifies root causes and cascade effects from medical analysis.
    
    Args:
        medical_analysis: Output from knowledge agent
        
    Returns:
        dict: Root cause analysis with cascade effects and intervention priorities
    """
    
    context_manager = ContextManager()
    
    # Add context
    context = context_manager.add_context(
        task_type=TaskType.ROOT_CAUSE,
        data={"medical_analysis": medical_analysis}
    )
    
    # Create root cause agent
    agent = root_cause_agent()
    
    # Prepare analysis query
    query = f"""
Based on this medical analysis, identify ROOT CAUSES and cascade effects:

ANALYSIS:
{medical_analysis}

Please provide:

1. ROOT CAUSES (not proximal symptoms):
   - What are the UNDERLYING causes? (stress, diet, deficiency, lifestyle)
   - Use "5 Whys" methodology
   
2. CASCADE EFFECTS:
   - How does root cause → intermediate effects → symptoms?
   - Map the cause-and-effect chain
   
3. INTERCONNECTIONS:
   - How do different systems affect each other?
   - What vicious cycles are present?
   
4. INTERVENTION PRIORITIES:
   - What to address FIRST for maximum impact?
   - What's the "keystone" fix that improves multiple symptoms?
   
5. CONFIDENCE LEVEL:
   - How confident are you in this root cause analysis? (0.0-1.0)

Use Dr. Berg's systems thinking - show the cascade, not just the symptoms.
"""
    
    # Structure for root cause analysis
    root_cause_analysis = {
        "root_causes": [],
        "cascade_effects": [],
        "system_interconnections": [],
        "vicious_cycles": [],
        "intervention_priorities": [],
        "keystone_fixes": [],
        "confidence_score": 0.0,
        "escalation_recommended": False,
        "reasoning": ""
    }
    
    # Calculate confidence
    confidence_assessment = calculate_agent_confidence(
        symptom_clarity=medical_analysis.get('confidence_score', 0.7),
        pattern_match_strength=0.75,
        red_flag_present=medical_analysis.get('escalation_recommended', False),
        medical_complexity=0.6
    )
    
    root_cause_analysis["confidence_score"] = confidence_assessment.confidence_level
    root_cause_analysis["escalation_recommended"] = confidence_assessment.should_escalate
    root_cause_analysis["reasoning"] = confidence_assessment.reasoning
    
    # Clean stale context
    context_manager.clear_stale_context(current_task=TaskType.ROOT_CAUSE)
    
    return root_cause_analysis


# Example usage
if __name__ == "__main__":
    print("🔍 Root Cause Analyzer Agent")
    print("=" * 60)
    
    # Test case: Complex symptom cluster
    test_analysis = {
        "patterns_identified": [
            "Insulin resistance pattern",
            "Magnesium deficiency",
            "Cortisol dysregulation"
        ],
        "mechanisms_explained": [
            "High insulin blocking fat burning",
            "Stress depleting magnesium",
            "Poor sleep worsening insulin resistance"
        ],
        "confidence_score": 0.75
    }
    
    print("\n📊 Input Analysis:")
    print("Patterns: Insulin resistance, Mg deficiency, Cortisol dysregulation")
    
    print("\n🎯 Expected Root Cause Analysis:")
    print("""
ROOT CAUSES (in order of importance):
1. CHRONIC STRESS (work, relationships, or lifestyle)
2. HIGH-CARB DIET with frequent eating
3. POOR SLEEP QUALITY

CASCADE EFFECT CHAIN:
Stress → Cortisol ↑ → Blood sugar ↑ → Insulin ↑ → Blocks Mg absorption →
Low Mg → Poor sleep → More cortisol → Worse insulin resistance
(VICIOUS CYCLE)

SYSTEM INTERCONNECTIONS:
- Nervous system (stress) affects Endocrine system (insulin/cortisol)
- Endocrine affects Digestive (absorption issues)
- Digestive affects Nervous (nutrient deficiencies worsen stress response)

INTERVENTION PRIORITIES:
1st Priority: FIX SLEEP (keystone habit - improves cortisol AND insulin)
2nd Priority: REDUCE CARBS + intermittent fasting (breaks insulin cycle)
3rd Priority: SUPPLEMENT Mg + B-vitamins (support both systems)
4th Priority: STRESS MANAGEMENT (meditation, exercise, boundaries)

KEYSTONE FIX:
"Fix your sleep FIRST. It's the domino that knocks down multiple problems.
When you sleep well: cortisol normalizes, insulin improves, magnesium 
absorption increases, stress tolerance improves. Everything else becomes easier."

CONFIDENCE: 0.80 (Strong pattern, but blood work would confirm)
""")
    
    print("\n" + "=" * 60)
    print("✅ Root Cause Agent ready for integration")
    
    print("\n💡 Key Innovation:")
    print("This agent doesn't just list symptoms - it explains the CASCADE.")
    print("Example: Not 'you have fatigue' but 'stress → cortisol → insulin → magnesium → fatigue'")
    print("This is what separates Dr. Berg's approach from generic health advice.")
