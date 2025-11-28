"""
Specialty Router - maps symptoms to the right medical specialist.

The main problem I'm solving: people don't know which doctor to see.
Is it hormones? Skin? Digestive? This figures it out based on symptom patterns.
"""

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import FunctionTool
from google.genai import types
from src.config import config
from src.knowledge.medical_knowledge_base import (
    MEDICAL_SPECIALTIES,
    route_to_specialist,
    RED_FLAGS,
    UrgencyLevel
)
from typing import Dict, List

def create_specialty_router_tool() -> FunctionTool:
    """
    Creates the specialty routing tool - the core of intelligent specialist matching.
    
    This tool solves a critical healthcare problem: patients often don't know which doctor
    to see. Rather than guessing (endocrinologist? dermatologist? GI doctor?), this tool
    uses symptom pattern matching and medical knowledge to recommend the RIGHT specialist.
    
    ARCHITECTURE:
    1. Red Flag Check: Immediate safety assessment (emergency symptoms? escalate to ER)
    2. Body System Mapping: Convert user description to medical system (e.g., "always tired" → "hormonal")
    3. Symptom Overlap Analysis: Match symptoms to specialist expertise
    4. Recommendation Ranking: Prioritize by match score (most relevant first)
    5. Summary Generation: Explain why each specialist and what to expect
    """
    
    def recommend_specialist(
        symptoms: List[str],
        body_system_affected: str,
        duration: str,
        severity: str
    ) -> Dict:
        """
        Recommend which medical specialist to consult based on symptoms.
        
        LOGIC FLOW:
        1. Check for red flags (safety first - if found, stop and escalate)
        2. Map body system to likely specialist categories
        3. Score each specialist based on symptom overlap
        4. Return ranked recommendations with reasoning
        
        Args:
            symptoms: List of main symptoms (e.g., ["fatigue", "weight_gain", "cold_hands"])
                     Used for pattern matching against specialist expertise areas
            body_system_affected: Which system (e.g., "hormonal", "digestive", "skin", "heart")
                                 Provides context for prioritizing specialists
            duration: How long symptoms present (e.g., "2 weeks", "6 months")
                     Used to determine urgency (acute vs chronic)
            severity: How severe (e.g., "mild", "moderate", "severe")
                     Helps determine if primary care or specialist needed
        
        Returns:
            Dictionary with specialist recommendations and reasoning:
            - status: "RED_FLAG_DETECTED" or "SUCCESS"
            - recommendations: List of specialists ranked by match score
            - routing_summary: Human-readable explanation
        
        EXAMPLE:
        Input: symptoms=["fatigue", "weight_gain"], body_system="hormonal"
        → Returns: [{specialist: "Endocrinologist", match_score: 0.85, ...},
                     {specialist: "Primary Care", match_score: 0.60, ...}]
        """
        
        # ====================================================================
        # STEP 1: RED FLAG DETECTION (Safety Check)
        # ====================================================================
        # RED FLAGS are symptoms that indicate medical emergencies or serious
        # conditions requiring immediate specialist attention (ER, urgent care, etc.)
        # These take priority over routine routing logic.
        # If ANY red flag is found → stop normal processing and alert user
        red_flag_matches = []
        for flag in RED_FLAGS:
            # Match flag symptoms with user symptoms
            # We use substring matching to catch variations (e.g., "chest pain" matches "chest pains" or "sharp chest pain")
            if any(keyword in ' '.join(symptoms).lower() for keyword in flag.symptom.lower().split()):
                red_flag_matches.append({
                    "symptom": flag.symptom,
                    "urgency": flag.urgency.value if hasattr(flag.urgency, 'value') else str(flag.urgency),
                    "reason": flag.reason,
                    "action": flag.action,
                    "specialist": flag.specialist
                })
        
        # If red flags found → STOP and return emergency info (don't continue routing)
        if red_flag_matches:
            return {
                "status": "RED_FLAG_DETECTED",
                "red_flags": red_flag_matches,
                "message": "⚠️ RED FLAGS DETECTED - Immediate medical attention may be required. See details below."
            }
        
        # ====================================================================
        # STEP 2: BODY SYSTEM → SPECIALIST MAPPING
        # ====================================================================
        # This maps the body system the user thinks is affected to likely specialists.
        # For example: "hormonal" issues → Endocrinologist is primary, Primary Care is secondary
        # This creates a priority order for the ranking step.
        # Map body system to likely specialists
        system_to_specialists = {
            "hormonal": ["endocrinologist", "primary_care"],
            "digestive": ["gastroenterologist", "primary_care"],
            "skin": ["dermatologist"],
            "heart": ["cardiologist"],
            "brain": ["neurologist"],
            "joints": ["rheumatologist", "primary_care"],
            "mental": ["psychiatrist", "primary_care"],
            "blood": ["hematologist", "primary_care"],
            "general": ["primary_care"]
        }
        
        # Get the specialists for this body system (default to primary_care if unknown)
        likely_specialists = system_to_specialists.get(body_system_affected.lower(), ["primary_care"])
        
        # ====================================================================
        # STEP 3: SYMPTOM OVERLAP SCORING
        # ====================================================================
        # For each specialist, we calculate how well their expertise matches the user's symptoms.
        # Match score = (number of symptom overlaps) / (total number of symptoms)
        # Higher score = better specialist match
        # Example: If user has fatigue + weight_gain + cold_hands, and Endocrinologist treats
        # fatigue, weight_gain, cold_intolerance → overlap=3/3=1.0 (perfect match)
        # Build recommendations
        recommendations = []
        for spec_key in likely_specialists:
            if spec_key in MEDICAL_SPECIALTIES:
                spec = MEDICAL_SPECIALTIES[spec_key]
                
                # Check if symptoms match this specialty
                # We create sets of symptoms and find the intersection (common items)
                symptom_overlap = len(set(symptoms) & set(spec.common_symptoms))
                
                recommendations.append({
                    "specialist": spec.name,
                    "description": spec.description,
                    "why_this_specialist": spec.when_to_see,
                    "treats_conditions": spec.treats_conditions,
                    "typical_tests": spec.typical_tests,
                    "match_score": symptom_overlap / len(symptoms) if symptoms else 0.5,
                    "priority": "primary" if spec_key == likely_specialists[0] else "secondary"
                })
        
        # ====================================================================
        # STEP 4: RANKING
        # ====================================================================
        # Sort by match score (highest first) so best matches appear first
        # Sort by match score
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        
        return {
            "status": "SUCCESS",
            "recommendations": recommendations,
            "routing_summary": _generate_routing_summary(recommendations, symptoms, duration, severity)
        }
    
    return FunctionTool(
        name="recommend_medical_specialist",
        description="Recommends which medical specialist to consult based on symptoms and affected body system",
        func=recommend_specialist
    )


def _generate_routing_summary(recommendations: List[Dict], symptoms: List[str], duration: str, severity: str) -> str:
    """Generate human-readable routing summary"""
    
    if not recommendations:
        return "Unable to determine specialist. Please consult Primary Care for evaluation."
    
    primary = recommendations[0]
    
    summary = f"""
Based on your symptoms ({', '.join(symptoms)}) and their {severity} severity over {duration}, 
I recommend consulting a **{primary['specialist']}**.

WHY THIS SPECIALIST:
{primary['why_this_specialist']}

WHAT THEY TREAT:
{', '.join(primary['treats_conditions'][:5])}...

TESTS YOU MIGHT EXPECT:
{', '.join(primary['typical_tests'][:3])}

"""
    
    if len(recommendations) > 1:
        secondary = recommendations[1]
        summary += f"""
ALTERNATIVE/ADDITIONAL SPECIALIST:
You may also consider seeing a **{secondary['specialist']}** if the primary specialist doesn't resolve the issue.
"""
    
    return summary.strip()


# ============================================================================
# MEDICAL SPECIALTY ROUTER AGENT
# ============================================================================

SPECIALTY_ROUTER_INSTRUCTION = """
You are a medical specialty routing expert. Your job is to help patients understand 
which type of doctor they should see for their symptoms.

THE PROBLEM YOU'RE SOLVING:
Many people struggle with: "I have these symptoms - which doctor do I see?"
- Ask 5 people with fatigue where to go: you'll get 5 different answers
- People waste time seeing wrong specialists (wrong treatment, costs money, delays care)
- Many patients delay care because they don't know which doctor is right
- This confusion contributes to worse health outcomes

YOUR MISSION:
Help patients find the RIGHT specialist FASTER. This saves time, money, and potentially lives.

YOUR APPROACH:

1. LISTEN carefully to their symptoms and concerns
   - What are the main symptoms?
   - When did it start?
   - Is it getting worse, stable, or improving?
   - How severe is it affecting their life?

2. ASK smart clarifying questions to narrow down the body system affected:
   - "Does this seem related to hormones, digestion, skin, joints, heart, or brain?"
   - "How long have symptoms lasted?" (acute = <2 weeks, chronic = >3 months)
   - "How severe?" (mild = annoying, moderate = affecting daily life, severe = can't function)
   - "Any red flag symptoms?" (chest pain, bloody vomit, severe headache, etc.)
   
   WHY? Because symptoms often overlap between specialties. A patient with brain fog
   might think it's neurological, but it could be thyroid (endocrinology). Your questions
   help disambiguate.

3. USE the recommend_medical_specialist tool to get recommendations
   - This tool has access to all 9+ medical specialties
   - It knows which specialists treat which conditions
   - It performs symptom pattern matching
   - It detects red flags automatically
   
   Example: symptoms=["fatigue", "weight_gain", "cold_hands"], body_system="hormonal"
   → Returns: Endocrinologist (0.88 match), Primary Care (0.60 match)

4. EXPLAIN CLEARLY why each specialist is recommended:
   - What specialist to see (primary recommendation)
   - Why this specialist (show them the symptom overlap)
   - What the specialist treats (show it matches their symptoms)
   - What tests they might do (set expectations)
   - Alternative specialists if needed (give options)
   - How to access (go directly or through primary care?)

5. CRITICAL SAFETY RULES:
   - IF RED FLAGS DETECTED → Emphasize urgency (ER, 911, 24hr, 1-week, or routine)
   - Always mention: "You can also start with Primary Care if unsure"
   - Clarify: "This is guidance for specialist matching, not a medical diagnosis"
   - Encourage: "Don't delay if symptoms severe, worsening, or affecting quality of life"
   - If multiple red flags → Stop routing and tell them to go to ER
   - If high uncertainty → Recommend Primary Care first (they can refer to specialist)

EXAMPLE INTERACTION:

User: "I'm exhausted all the time, I've gained 20 lbs despite dieting, my hands are cold, 
       and my eyebrows are falling out. I don't know which doctor to see."

STEP 1 - LISTEN:
✓ Main symptoms: fatigue, weight gain, cold hands, hair loss
✓ Pattern: All consistent with THYROID DYSFUNCTION

STEP 2 - ASK CLARIFYING QUESTIONS:
"How long have these symptoms been going on? And did they start suddenly or gradually?"
[User: "About 6 months, started gradually after high stress"]
→ Temporal pattern consistent with chronic thyroid issue

STEP 3 - USE TOOL:
You call: recommend_medical_specialist(
    symptoms=["fatigue", "weight gain", "cold hands", "hair loss"],
    body_system="hormonal",
    duration="6 months",
    severity="moderate"
)
Tool returns: Endocrinologist (match: 0.88), Primary Care (match: 0.60)
Red flags: None detected (not emergent)

STEP 4 - EXPLAIN:
"Based on your symptoms - fatigue, weight gain, cold intolerance, and hair loss - 
I strongly recommend seeing an ENDOCRINOLOGIST.

Here's why:
These symptoms are classic for hypothyroidism (underactive thyroid), which is exactly 
what endocrinologists specialize in. They treat thyroid disorders, and your symptom 
pattern matches perfectly.

What they'll do:
• Blood test: TSH, Free T4, Free T3, thyroid antibodies
• Physical exam: Feel your thyroid, check reflexes
• If needed: Thyroid ultrasound
• Treatment: Usually thyroid hormone replacement (levothyroxine)

How to get an appointment:
Option 1: Ask your PCP for a referral to endocrinologist (insurance often requires this)
Option 2: Call endocrinology clinics directly (many accept self-referrals)
Option 3: Search online: '[your city] endocrinologist accepting patients'

Timeline: Schedule within 2-3 weeks. This isn't emergency, but don't delay.

Important: I'm not diagnosing you - only an endocrinologist can diagnose. But your 
symptoms fit their expertise perfectly."

STEP 5 - SAFETY CHECK:
✓ No red flags detected
✓ Not emergency (so specialist appointment, not ER)
✓ Clear recommendation given
✓ Explained reasoning
✓ Set expectations for tests
✓ Clarified I'm not diagnosing
✓ Encouraged them not to delay

KEY DESIGN PRINCIPLES:

1. BE EMPATHETIC - People are often frustrated navigating healthcare system
2. BE SPECIFIC - Give actionable recommendations, not vague guidance
3. BE CLEAR - Explain in plain English, no medical jargon
4. BE SAFE - Red flags first, always defer to real doctors
5. BE HELPFUL - Save them time by matching them to RIGHT specialist FIRST
6. BE HUMBLE - I'm a router, not a doctor. I help navigate healthcare.

COMMON ROUTING SCENARIOS:

Scenario 1: Fatigue + Weight Gain + Cold Hands
→ Endocrinologist (thyroid dysfunction is #1 cause of this triad)

Scenario 2: Joint Pain + Morning Stiffness + Swelling
→ Rheumatologist (classic autoimmune pattern)

Scenario 3: Abdominal Bloating + Diarrhea + Constipation
→ Gastroenterologist (IBS pattern) or Primary Care first

Scenario 4: Chest Pain + Shortness of Breath
→ RED FLAG! ER immediately. NOT specialist routing.

Scenario 5: Brain Fog + Can't Find Words + Forgetfulness
→ Neurologist OR could be thyroid/B-vitamin/blood sugar
→ Start with Primary Care for blood work first

Remember:
- When in doubt, recommend Primary Care (they're the hub)
- Multiple specialists may be needed (they communicate with each other)
- Your job is to save patients time by matching them to the RIGHT doctor FIRST
- You prevent: wrong specialist visits, delayed diagnosis, frustrated patients
- You enable: faster diagnosis, correct treatment, better health outcomes
"""


def medical_specialty_router_agent() -> LlmAgent:
    """
    Create the Medical Specialty Router Agent.
    
    This agent solves the "who do I see?" problem by analyzing symptoms
    and recommending the appropriate medical specialist.
    """
    
    specialty_tool = create_specialty_router_tool()
    
    agent = LlmAgent(
        name="specialty_router",
        model=Gemini(
            model=config.MODEL_NAME,
            api_key=config.GOOGLE_API_KEY
        ),
        description="Medical specialty routing agent. Recommends which type of doctor to consult based on symptoms.",
        instruction=SPECIALTY_ROUTER_INSTRUCTION,
        tools=[specialty_tool],
        output_key="specialist_recommendation"
    )
    
    return agent


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def demo_specialty_router():
    """Demo the specialty router agent"""
    from google.adk.runners import InMemoryRunner
    
    agent = medical_specialty_router_agent()
    runner = InMemoryRunner(agent=agent)
    
    test_cases = [
        "I'm exhausted all the time, gained 20 lbs without changing diet, and I'm always cold. Which doctor should I see?",
        "I have joint pain in multiple joints, morning stiffness for over an hour, and my hands are swollen. Who do I see?",
        "My stomach is constantly bloated, I have diarrhea and constipation alternating, and abdominal cramps. Which specialist?",
        "I have chest pain that comes and goes, shortness of breath when climbing stairs, and my heart races sometimes. Who should I see?"
    ]
    
    print("=" * 70)
    print("MEDICAL SPECIALTY ROUTER AGENT - DEMO")
    print("=" * 70)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 70}")
        print(f"TEST CASE {i}")
        print(f"{'=' * 70}")
        print(f"\nPatient: {test_case}\n")
        print("Router Agent:")
        
        user_content = types.Content(parts=[types.Part(text=test_case)])
        
        async for event in runner.run_async(new_message=user_content):
            if event.is_final_response() and event.content:
                for part in event.content.parts:
                    if hasattr(part, "text"):
                        print(part.text)
        
        print()


if __name__ == "__main__":
    import asyncio
    asyncio.run(demo_specialty_router())
