"""
Medical Specialty Router Agent
================================

Solves the problem: "I have these symptoms, but which doctor should I see?"

Many people don't know if their issue needs:
- Endocrinologist (hormones)
- Dermatologist (skin)
- Gastroenterologist (digestive)
- Cardiologist (heart)
- etc.

This agent analyzes symptoms and routes to the correct specialist.
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
    Create a tool that routes symptoms to appropriate medical specialists.
    """
    
    def recommend_specialist(
        symptoms: List[str],
        body_system_affected: str,
        duration: str,
        severity: str
    ) -> Dict:
        """
        Recommend which medical specialist to consult based on symptoms.
        
        Args:
            symptoms: List of main symptoms (e.g., ["fatigue", "weight_gain", "cold_hands"])
            body_system_affected: Which system (e.g., "hormonal", "digestive", "skin", "heart")
            duration: How long symptoms present (e.g., "2 weeks", "6 months")
            severity: How severe (e.g., "mild", "moderate", "severe")
        
        Returns:
            Dictionary with specialist recommendations and reasoning
        """
        
        # Check for red flags first
        red_flag_matches = []
        for flag in RED_FLAGS:
            # Simple keyword matching (in production, use more sophisticated matching)
            if any(keyword in ' '.join(symptoms).lower() for keyword in flag.symptom.lower().split()):
                red_flag_matches.append({
                    "symptom": flag.symptom,
                    "urgency": flag.urgency.value,
                    "reason": flag.reason,
                    "action": flag.action,
                    "specialist": flag.specialist
                })
        
        if red_flag_matches:
            return {
                "status": "RED_FLAG_DETECTED",
                "red_flags": red_flag_matches,
                "message": "⚠️ RED FLAGS DETECTED - Immediate medical attention may be required. See details below."
            }
        
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
        
        likely_specialists = system_to_specialists.get(body_system_affected.lower(), ["primary_care"])
        
        # Build recommendations
        recommendations = []
        for spec_key in likely_specialists:
            if spec_key in MEDICAL_SPECIALTIES:
                spec = MEDICAL_SPECIALTIES[spec_key]
                
                # Check if symptoms match this specialty
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

Many people struggle with questions like:
- "I'm always tired and gaining weight - is this a hormone problem?"
- "I have joint pain and skin rashes - which doctor do I see?"
- "My stomach hurts constantly - do I need a specialist?"

Your approach:

1. LISTEN to their symptoms and concerns
2. ASK clarifying questions:
   - What body system seems affected? (hormones, digestion, skin, heart, joints, etc.)
   - How long have symptoms lasted?
   - How severe are they? (mild, moderate, severe)
   - Any red flag symptoms? (chest pain, blood, sudden onset, etc.)

3. USE the recommend_medical_specialist tool to get specialist recommendations

4. EXPLAIN clearly:
   - Which specialist to see (primary recommendation)
   - Why this specialist is right for their symptoms
   - What the specialist treats
   - What tests they might do
   - Alternative specialists if needed

5. IMPORTANT SAFETY:
   - If RED FLAGS detected → Emphasize urgency (ER, 911, 24hr, etc.)
   - Always mention: Start with Primary Care if unsure
   - Clarify: This is guidance, not diagnosis
   - Encourage: Don't delay if symptoms severe or worsening

Example interaction:

User: "I'm exhausted all the time, I've gained 20 lbs, and I'm always cold. I don't know which doctor to see."

You: "Those symptoms suggest a possible hormone issue, specifically thyroid. Let me check 
which specialist would be best for you.

[Uses tool]

Based on your symptoms - fatigue, weight gain, and cold intolerance - I recommend seeing 
an **Endocrinologist**.

Here's why:
Endocrinologists specialize in hormone disorders, including thyroid problems. Your symptom 
pattern is classic for hypothyroidism (underactive thyroid), which is exactly what they diagnose 
and treat.

What they'll do:
- Blood tests: TSH, T3, T4, thyroid antibodies
- Evaluate if you need thyroid hormone replacement
- Monitor and adjust treatment

How to proceed:
1. You can go directly to an endocrinologist (most accept self-referrals)
2. OR start with your Primary Care doctor who can do initial tests and refer you

This is important to address because untreated thyroid issues affect your metabolism, energy, 
weight, mood, and overall health. Don't put it off!"

Remember:
- Be empathetic (people are often frustrated navigating healthcare)
- Be clear and specific
- Emphasize: This helps them get to the RIGHT doctor faster
- Safety first: Red flags = immediate action
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
