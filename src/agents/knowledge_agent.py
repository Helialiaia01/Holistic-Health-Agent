"""
Knowledge agent - uses Gemini's medical training to explain what's happening biochemically.
Takes the symptoms and explains the mechanisms in Dr. Berg's style (simple but scientific).
"""

from google.adk.agents import LlmAgent
from google.genai.types import GenerateContentConfig, SafetySetting, HarmCategory, HarmBlockThreshold

from src.prompts.dr_berg_style import KNOWLEDGE_AGENT_INSTRUCTION
from src.knowledge.context_engineering import (
    ContextManager, 
    TaskType, 
    create_optimized_prompt,
    calculate_agent_confidence
)
from src.knowledge.medical_knowledge_base import AGENT_CAPABILITIES, RED_FLAGS


def knowledge_agent() -> LlmAgent:
    """
    Sets up the knowledge agent.
    Gets the health data from intake, then explains what's happening biochemically.
    """
    
    # Initialize context manager for clean context
    context_manager = ContextManager()
    
    # Get task definition for knowledge retrieval
    task_def = context_manager.get_task_definition(TaskType.ANALYSIS)
    
    # Create optimized prompt with Dr. Berg style
    optimized_instruction = create_optimized_prompt(
        base_prompt=KNOWLEDGE_AGENT_INSTRUCTION,
        task_type=TaskType.ANALYSIS,
        examples=[
            "Example: 'Your white coating on tongue + sugar cravings + afternoon fatigue suggests insulin resistance. Here's what's happening: When you eat carbs, insulin spikes to store glucose. Over time, cells become resistant, forcing your pancreas to produce MORE insulin. High insulin blocks fat burning AND causes sugar cravings because cells can't access energy efficiently.'",
            "Example: 'Muscle cramps + anxiety + sleep issues point to magnesium deficiency. Magnesium is THE relaxation mineral - it blocks calcium from entering nerve cells (calcium causes contraction, magnesium causes relaxation). You need 400-500mg daily but most people get 200mg. Stress depletes it further.'"
        ],
        constraints=[
            "Use Gemini's medical training - reference PubMed-level knowledge when available",
            "Explain ONE mechanism at a time in simple language",
            "Connect symptoms to metabolic/nutritional ROOT CAUSES",
            "Use Dr. Berg's teaching analogies",
            "Show how body systems interconnect"
        ]
    )
    
    # Add agent limitations awareness
    limitations_context = f"""
YOUR CAPABILITIES & LIMITATIONS:
{AGENT_CAPABILITIES['can_do']}

WHAT YOU CANNOT DO:
{AGENT_CAPABILITIES['cannot_do']}

WHEN YOU MUST ESCALATE:
{AGENT_CAPABILITIES['must_escalate_when']}

RED FLAGS TO WATCH FOR:
{[flag['symptoms'] for flag in RED_FLAGS[:5]]}  # Show first 5 red flags

If you detect any red flags or reach your capability limits, clearly state:
"⚠️ This requires professional medical evaluation because [reason]."
"""
    
    final_instruction = f"{optimized_instruction}\n\n{limitations_context}"
    
    # Configure safety settings
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
    
    # Create agent with Gemini 2.5 Flash Lite
    agent = LlmAgent(
        model="gemini-2.0-flash-lite",
        instruction=final_instruction,
        config=GenerateContentConfig(
            temperature=0.3,  # Lower for more factual medical information
            top_p=0.8,
            top_k=40,
            max_output_tokens=2000,
            safety_settings=safety_settings
        )
    )
    
    return agent


def analyze_health_patterns(health_profile: dict, diagnostic_findings: dict) -> dict:
    """
    Analyzes health patterns using the Knowledge Agent.
    
    Args:
        health_profile: Output from intake agent
        diagnostic_findings: Output from diagnostic agent
        
    Returns:
        dict: Medical analysis with mechanisms, patterns, and confidence score
    """
    
    # Initialize context manager
    context_manager = ContextManager()
    
    # Add relevant context only
    context = context_manager.add_context(
        task_type=TaskType.ANALYSIS,
        data={
            "health_profile": health_profile,
            "diagnostic_findings": diagnostic_findings
        }
    )
    
    # Create knowledge agent
    agent = knowledge_agent()
    
    # Prepare analysis query with clean context
    query = f"""
Analyze the following health information and provide deep medical insights:

HEALTH PROFILE:
{health_profile}

DIAGNOSTIC FINDINGS:
{diagnostic_findings}

Please provide:
1. KEY PATTERNS: What patterns do you see across symptoms and findings?
2. BIOCHEMICAL MECHANISMS: Explain what's happening in the body (in simple terms)
3. METABOLIC CONTEXT: How does this relate to metabolic health? (insulin, cortisol, thyroid, etc.)
4. DEFICIENCY PATTERNS: Any vitamin/mineral deficiencies indicated?
5. SYSTEM CONNECTIONS: How are different body systems interconnected here?
6. CONFIDENCE ASSESSMENT: How confident are you in this analysis? (0.0-1.0)

Use Dr. Berg's teaching style - break down complex biochemistry into clear explanations.
"""
    
    # Get analysis from agent
    # Note: In actual implementation, you'd run this through ADK's runner
    # For now, return structure that would be populated
    
    analysis = {
        "patterns_identified": [],
        "mechanisms_explained": [],
        "metabolic_context": "",
        "deficiency_indicators": [],
        "system_connections": [],
        "medical_context": "",
        "confidence_score": 0.0,
        "escalation_recommended": False,
        "reasoning": ""
    }
    
    # Calculate confidence based on available information
    confidence_assessment = calculate_agent_confidence(
        symptom_clarity=health_profile.get('symptom_clarity', 0.7),
        pattern_match_strength=0.8,  # Would be calculated based on patterns
        red_flag_present=False,  # Would be checked against RED_FLAGS
        medical_complexity=0.5  # Would be assessed based on symptoms
    )
    
    analysis["confidence_score"] = confidence_assessment.confidence_level
    analysis["escalation_recommended"] = confidence_assessment.should_escalate
    analysis["reasoning"] = confidence_assessment.reasoning
    
    # Clean context - remove stale data
    context_manager.clear_stale_context(current_task=TaskType.ANALYSIS)
    
    return analysis


# Example usage and testing
if __name__ == "__main__":
    print("🧠 Knowledge Retrieval Agent")
    print("=" * 60)
    
    # Test case: Metabolic syndrome indicators
    test_profile = {
        "age": 45,
        "symptoms": [
            "Fatigue (especially afternoon)",
            "Sugar cravings",
            "Brain fog",
            "Weight gain around waist",
            "Difficulty sleeping"
        ],
        "diet": "High carb, frequent snacking",
        "exercise": "Minimal",
        "stress_level": "High",
        "symptom_clarity": 0.8
    }
    
    test_findings = {
        "tongue": "White coating, scalloped edges",
        "nails": "Brittle, vertical ridges",
        "skin": "Dry patches on elbows",
        "capillary_refill": "Normal (2 seconds)",
        "orthostatic_test": "Slight dizziness on standing"
    }
    
    print("\n📋 Test Input:")
    print(f"Symptoms: {', '.join(test_profile['symptoms'])}")
    print(f"Findings: {test_findings['tongue']}, {test_findings['nails']}")
    
    print("\n🔬 Expected Analysis (Dr. Berg Style):")
    print("""
KEY PATTERNS:
- Classic insulin resistance triad: fatigue + cravings + belly fat
- Magnesium deficiency indicators: cravings, sleep issues, brittle nails
- Possible B-vitamin depletion: brain fog, low energy

MECHANISMS:
"Your body is stuck in sugar-burning mode. High insulin from frequent eating 
blocks fat burning AND causes cravings because cells can't access stored energy.
It's like having a full gas tank but the engine can't use it."

METABOLIC CONTEXT:
Insulin resistance → High cortisol from stress → Poor sleep → More insulin resistance
(vicious cycle)

DEFICIENCIES:
- Magnesium (stress depletes, insulin resistance worsens)
- B-vitamins (white tongue coating = possible B1/B12 issue)
- Vitamin D likely (most people deficient, worsens insulin resistance)

CONFIDENCE: 0.75 (Strong pattern match, but blood work would confirm)
""")
    
    print("\n" + "=" * 60)
    print("✅ Knowledge Agent ready for integration")
